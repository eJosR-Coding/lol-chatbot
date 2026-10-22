"""Test fixtures: a tiny knowledge base and a deterministic encoder, so no model
download and no Ollama are needed."""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import httpx
import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.ingest import build_index  # noqa: E402
from backend.kb import Entry  # noqa: E402
from backend.rag import LolRetriever  # noqa: E402
from backend.text import tokens  # noqa: E402

DIM = 128


class FakeEncoder:
    """Hashed bag of words: texts sharing words get a high cosine, others about zero."""

    name = "fake-bow"

    def encode(self, texts: list[str]) -> np.ndarray:
        out = np.zeros((len(texts), DIM), dtype=np.float32)
        for row, text in enumerate(texts):
            for tok in tokens(text):
                out[row, int(hashlib.md5(tok.encode()).hexdigest(), 16) % DIM] += 1.0
        norms = np.linalg.norm(out, axis=1, keepdims=True)
        return out / np.maximum(norms, 1e-9)


def make_entry(id: int, term: str, answer: str, aliases: list[str] | None = None, category: str = "mechanics") -> Entry:
    return Entry(
        id=id,
        term=term,
        question=f"¿Qué es {term}?",
        answer=answer,
        aliases=aliases or [],
        category=category,
        source="test",
    )


ENTRIES = [
    make_entry(1, "un tank", "Un tank es un campeón resistente que absorbe daño en las peleas de equipo.", ["tanque", "frontline"], "role"),
    make_entry(2, "un gank", "Un gank es una emboscada del jungler a un carril para conseguir una kill.", ["emboscada"], "tactic"),
    make_entry(3, "Stun", "Stun es un control de masas que aturde al enemigo 2 segundos.", ["aturdimiento"], "crowd_control"),
    make_entry(4, "un ward", "Un ward es un objeto que da visión de un área del mapa.", ["centinela"], "map"),
    make_entry(5, "Flash o Destello", "Flash es un hechizo de invocador que teletransporta una corta distancia.", ["blink"], "mechanics"),
    make_entry(6, "AFK", "AFK significa away from keyboard: un jugador que no está jugando.", ["ausente"], "chat"),
]


@pytest.fixture(scope="session")
def encoder() -> FakeEncoder:
    return FakeEncoder()


@pytest.fixture(scope="session")
def retriever(encoder: FakeEncoder) -> LolRetriever:
    return LolRetriever(build_index(ENTRIES, encoder), encoder, threshold=0.5)


class LLMStub:
    """Records /api/chat calls; reply is what the 'model' answers."""

    def __init__(self, reply: str = "", fail: bool = False) -> None:
        self.reply = reply
        self.fail = fail
        self.chat_calls = 0

    def client(self) -> httpx.AsyncClient:
        def handler(request: httpx.Request) -> httpx.Response:
            if request.url.path == "/api/chat":
                self.chat_calls += 1
                if self.fail:
                    return httpx.Response(500)
                return httpx.Response(200, json={"message": {"content": self.reply}})
            return httpx.Response(200, json={"models": []})

        return httpx.AsyncClient(base_url="http://llm.test", transport=httpx.MockTransport(handler))
