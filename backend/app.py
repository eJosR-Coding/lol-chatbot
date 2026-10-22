"""FastAPI app: hybrid retrieval over the glossary, a retrieval gate, and an LLM
rewrite that is kept only when it stays faithful to the knowledge-base answer."""
from __future__ import annotations

import os
from contextlib import asynccontextmanager
from typing import Literal

import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from . import grounding
from .rag import GATE_THRESHOLD, LolRetriever, load_retriever

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5:0.5b")
# Comma-separated list of allowed browser origins.
CORS_ORIGINS = os.environ.get(
    "CORS_ORIGINS", "http://127.0.0.1:4410,http://localhost:4410,http://127.0.0.1:4321,http://localhost:4321"
).split(",")
# Fail at startup (instead of rebuilding) when the index is missing or stale.
STRICT_INDEX = os.environ.get("LOL_INDEX_STRICT") == "1"

# A short follow-up ("¿y un ejemplo?") may borrow the topic of the previous user turns.
FOLLOWUP_MAX_WORDS = 5
HISTORY_TURNS_FOR_RETRIEVAL = 2
SUGGESTION_MIN_SCORE = 0.5


class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    message: str
    history: list[Message] = Field(default_factory=list)


class Suggestion(BaseModel):
    id: int
    term: str


class ChatResponse(BaseModel):
    reply: str
    # refusal: below the gate, the LLM was not called. verbatim: KB answer as written.
    # rewrite: the LLM paraphrase passed the drift check.
    mode: Literal["refusal", "verbatim", "rewrite"]
    reason: str = ""  # why a verbatim/refusal answer was chosen (empty for rewrite)
    source_id: int | None  # 1-based KB entry id of the answer, None on refusal
    source_term: str | None
    matched_question: str  # closest entry even on refusal (for transparency)
    matched_answer: str
    score: float
    gate: float
    below_threshold: bool
    used_context: bool
    suggestions: list[Suggestion] = []


def best_retrieval(retriever: LolRetriever, message: str, history: list[Message]) -> dict:
    """Retrieve for the message; a short follow-up that misses the gate may reuse the topic."""
    direct = retriever.retrieve(message)
    prev_user = [m.content for m in history if m.role == "user"][-HISTORY_TURNS_FOR_RETRIEVAL:]
    if not direct["below_threshold"] or not prev_user or len(message.split()) > FOLLOWUP_MAX_WORDS:
        return direct
    combined = retriever.retrieve(" ".join([*prev_user, message])[:300])
    return combined if combined["score"] > direct["score"] else direct


def create_app(
    retriever: LolRetriever | None = None, http: httpx.AsyncClient | None = None
) -> FastAPI:
    """Build the app. Tests inject a fake retriever and HTTP client."""

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.state.retriever = retriever or load_retriever(strict=STRICT_INDEX)
        app.state.http = http or httpx.AsyncClient(base_url=OLLAMA_HOST, timeout=60.0)
        yield
        if http is None:
            await app.state.http.aclose()

    app = FastAPI(title="LoL RAG Chatbot", lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware, allow_origins=CORS_ORIGINS, allow_methods=["GET", "POST"], allow_headers=["*"]
    )

    @app.get("/health")
    async def health(request: Request) -> dict:
        try:
            r = await request.app.state.http.get("/api/tags", timeout=1.5)
            llm = r.status_code == 200
        except httpx.HTTPError:
            llm = False
        return {
            "ok": True,
            "model": OLLAMA_MODEL,
            "llm": llm,
            "entries": len(request.app.state.retriever.entries),
            "gate": GATE_THRESHOLD,
        }

    @app.get("/kb")
    async def get_kb(request: Request) -> dict:
        entries = [e.model_dump() for e in request.app.state.retriever.entries]
        return {"count": len(entries), "entries": entries}

    @app.post("/chat", response_model=ChatResponse)
    async def chat(req: ChatRequest, request: Request) -> ChatResponse:
        msg = req.message.strip()
        if not msg:
            raise HTTPException(status_code=400, detail="empty message")
        r: LolRetriever = request.app.state.retriever
        retrieval = best_retrieval(r, msg, req.history)
        entry = next(e for e in r.entries if e.id == retrieval["id"])
        common = {
            "matched_question": retrieval["matched_question"],
            "matched_answer": retrieval["matched_answer"],
            "score": retrieval["score"],
            "gate": r.threshold,
            "below_threshold": retrieval["below_threshold"],
        }

        if retrieval["below_threshold"]:  # never ask the model about something we cannot ground
            close = [
                Suggestion(id=c["id"], term=c["term"])
                for c in retrieval["candidates"]
                if c["score"] >= SUGGESTION_MIN_SCORE
            ]
            by_id = {e.id: e for e in r.entries}
            return ChatResponse(
                reply=grounding.refusal([by_id[s.id] for s in close]),
                mode="refusal",
                reason="below_gate",
                source_id=None,
                source_term=None,
                used_context=False,
                suggestions=close,
                **common,
            )

        verbatim = dict(source_id=entry.id, source_term=entry.term, used_context=True, **common)
        payload = {
            "model": OLLAMA_MODEL,
            "stream": False,
            "messages": [
                {"role": "system", "content": grounding.SYSTEM_PROMPT},
                {"role": "user", "content": grounding.build_user_prompt(msg, entry.answer)},
            ],
            "options": grounding.LLM_OPTIONS,
        }
        try:
            resp = await request.app.state.http.post("/api/chat", json=payload)
            resp.raise_for_status()
        except httpx.HTTPError:
            return ChatResponse(reply=entry.answer, mode="verbatim", reason="llm_unavailable", **verbatim)

        raw = (resp.json().get("message") or {}).get("content", "")
        rewrite = grounding.clean_reply(raw)
        ok, why = grounding.check_rewrite(rewrite, entry, msg)
        if not ok:
            return ChatResponse(reply=entry.answer, mode="verbatim", reason=f"drift: {why}", **verbatim)
        return ChatResponse(reply=rewrite, mode="rewrite", **verbatim)

    return app


app = create_app()
