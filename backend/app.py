"""FastAPI app — RAG (notebook) + Ollama (qwen2.5:0.5b) generation."""
from __future__ import annotations

import os
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .kb import KNOWLEDGE_BASE
from .rag import LolRetriever

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5:0.5b")

state: dict = {}


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Cargar el retriever una sola vez al arrancar (descarga el modelo de embeddings la primera vez)
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


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str
    matched_question: str
    matched_answer: str
    score: float
    below_threshold: bool


SYSTEM_PROMPT = (
    "Eres un asistente experto en League of Legends que habla español coloquial gamer. "
    "Responde SIEMPRE en español, breve (máximo 3 oraciones). "
    "Te paso un fragmento del Knowledge Base relevante a la pregunta del usuario. "
    "Úsalo como base de tu respuesta y reformúlalo de forma natural y amistosa. "
    "Si el fragmento no es relevante, dilo claramente."
)


def build_user_prompt(user_msg: str, retrieval: dict) -> str:
    return (
        f"Pregunta del usuario: {user_msg}\n\n"
        f"Knowledge Base más cercana (similitud {retrieval['score']:.2f}):\n"
        f"  P: {retrieval['matched_question']}\n"
        f"  R: {retrieval['matched_answer']}\n\n"
        "Responde al usuario en español usando esa información."
    )


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
    retrieval = retriever.retrieve(msg)

    if retrieval["below_threshold"]:
        return ChatResponse(
            reply="No entendí esa. Pregunta algo sobre LoL bro.",
            **retrieval,
        )

    payload = {
        "model": OLLAMA_MODEL,
        "stream": False,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(msg, retrieval)},
        ],
        "options": {"temperature": 0.4, "num_predict": 180},
    }

    http: httpx.AsyncClient = state["http"]
    try:
        r = await http.post("/api/chat", json=payload)
        r.raise_for_status()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"ollama error: {e}") from e

    data = r.json()
    reply = (data.get("message") or {}).get("content", "").strip()
    if not reply:
        # fallback: serve the KB answer directly
        reply = retrieval["matched_answer"]

    return ChatResponse(reply=reply, **retrieval)
