"""FastAPI app — RAG (notebook) + Ollama (qwen2.5:0.5b) generation, con historia."""
from __future__ import annotations

import os
import re
from contextlib import asynccontextmanager
from typing import Literal

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .kb import KNOWLEDGE_BASE
from .rag import LolRetriever

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5:0.5b")

# Si el match RAG queda debajo de este score, el modelo NO recibe contexto KB
# y se apoya solo en la conversación previa.
WEAK_MATCH_THRESHOLD = 0.45
HISTORY_TURNS_FOR_LLM = 6
HISTORY_TURNS_FOR_RETRIEVAL = 2

state: dict = {}


@asynccontextmanager
async def lifespan(_app: FastAPI):
    state["retriever"] = LolRetriever()
    state["http"] = httpx.AsyncClient(base_url=OLLAMA_HOST, timeout=60.0)
    yield
    await state["http"].aclose()


app = FastAPI(title="LoL RAG Chatbot", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    message: str
    history: list[Message] = Field(default_factory=list)


class ChatResponse(BaseModel):
    reply: str
    matched_question: str
    matched_answer: str
    score: float
    below_threshold: bool
    used_context: bool


SYSTEM_PROMPT = (
    "Eres un asistente experto en League of Legends que habla español coloquial gamer. "
    "Responde SIEMPRE en español, en 1 a 3 oraciones, natural y amistoso. "
    "Cuando recibas una nota '[CONTEXTO]', tómala como información autoritativa "
    "y reformula con tus propias palabras. "
    "NUNCA copies literalmente etiquetas como 'P:', 'R:', '[CONTEXTO]', 'Pregunta:' o similares. "
    "Si la pregunta es un follow-up (pide ejemplos, aclaraciones, etc.), "
    "responde manteniendo el tema de los turnos previos."
)


def build_retrieval_query(message: str, history: list[Message]) -> str:
    """Combina el último mensaje de usuario con el actual para mejorar follow-ups."""
    prev_user = [m.content for m in history if m.role == "user"][
        -HISTORY_TURNS_FOR_RETRIEVAL:
    ]
    if not prev_user:
        return message
    combined = " ".join([*prev_user, message])
    return combined[:300]


def best_retrieval(retriever: LolRetriever, message: str, history: list[Message]) -> dict:
    """Recupera con la query sola y combinada; se queda con la de mayor score.

    Esto resuelve dos casos:
    - Follow-up sin tema explícito ('explícamelo'): la combinada gana.
    - Cambio de tema con palabra clave clara ('y qué onda con flash'): la sola gana.
    """
    direct = retriever.retrieve(message)
    if not history:
        return direct
    combined_query = build_retrieval_query(message, history)
    combined = retriever.retrieve(combined_query)
    return direct if direct["score"] >= combined["score"] else combined


def build_user_prompt(user_msg: str, retrieval: dict | None) -> str:
    if retrieval is None:
        return user_msg
    return (
        f"[CONTEXTO autoritativo del Knowledge Base, similitud {retrieval['score']:.2f}]\n"
        f"{retrieval['matched_answer']}\n"
        f"[FIN CONTEXTO]\n\n"
        f"{user_msg}"
    )


_LEAK_PATTERNS = [
    re.compile(r"^\s*P\s*:\s*¿[^?]+\?\s*", re.MULTILINE),
    re.compile(r"^\s*R\s*:\s*", re.MULTILINE),
    re.compile(r"^\s*Pregunta\s+del\s+usuario\s*:\s*", re.IGNORECASE | re.MULTILINE),
    re.compile(r"\[/?CONTEXTO[^\]]*\]\s*", re.IGNORECASE),
    re.compile(r"^\s*\[FIN[^\]]*\]\s*$", re.IGNORECASE | re.MULTILINE),
]


def clean_reply(text: str) -> str:
    for pat in _LEAK_PATTERNS:
        text = pat.sub("", text)
    return text.strip()


@app.get("/health")
async def health() -> dict:
    return {"ok": True, "model": OLLAMA_MODEL}


@app.get("/kb")
async def get_kb() -> dict:
    return {"count": len(KNOWLEDGE_BASE), "entries": KNOWLEDGE_BASE}


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    msg = req.message.strip()
    if not msg:
        raise HTTPException(status_code=400, detail="empty message")

    retriever: LolRetriever = state["retriever"]
    retrieval = best_retrieval(retriever, msg, req.history)

    # Si no hay historial Y el match es flojo → fallback estilo notebook
    if retrieval["below_threshold"] and not req.history:
        return ChatResponse(
            reply="No entendí esa. Pregunta algo sobre LoL bro.",
            used_context=False,
            **retrieval,
        )

    # Inyectamos contexto KB solo si el match es razonable
    use_context = retrieval["score"] >= WEAK_MATCH_THRESHOLD
    user_prompt = build_user_prompt(msg, retrieval if use_context else None)

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for m in req.history[-HISTORY_TURNS_FOR_LLM:]:
        messages.append({"role": m.role, "content": m.content})
    messages.append({"role": "user", "content": user_prompt})

    payload = {
        "model": OLLAMA_MODEL,
        "stream": False,
        "messages": messages,
        "options": {"temperature": 0.3, "num_predict": 200, "repeat_penalty": 1.15},
    }

    http: httpx.AsyncClient = state["http"]
    try:
        r = await http.post("/api/chat", json=payload)
        r.raise_for_status()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"ollama error: {e}") from e

    data = r.json()
    raw_reply = (data.get("message") or {}).get("content", "").strip()
    reply = clean_reply(raw_reply)
    if not reply:
        reply = retrieval["matched_answer"] if use_context else (
            "No te seguí del todo. ¿Puedes reformular tu pregunta?"
        )

    return ChatResponse(reply=reply, used_context=use_context, **retrieval)
