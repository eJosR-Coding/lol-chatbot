import httpx
import pytest
from fastapi.testclient import TestClient

from backend.app import create_app
from tests.conftest import ENTRIES, LLMStub

GOOD_REWRITE = "Un tank es un campeón resistente que aguanta daño en las peleas de equipo."
CHAT_KEYS = {
    "reply", "mode", "reason", "source_id", "source_term", "matched_question",
    "matched_answer", "score", "gate", "below_threshold", "used_context", "suggestions",
}


def client_for(retriever, llm: LLMStub):
    return TestClient(create_app(retriever=retriever, http=llm.client()))


def chat(client, message, history=None):
    return client.post("/chat", json={"message": message, "history": history or []})


def test_below_the_gate_the_llm_is_never_called(retriever):
    llm = LLMStub(reply="no debería usarse")
    with client_for(retriever, llm) as c:
        body = chat(c, "¿Cuál es la capital de Francia?").json()
    assert llm.chat_calls == 0
    assert body["mode"] == "refusal" and body["reason"] == "below_gate"
    assert body["source_id"] is None and body["used_context"] is False and body["below_threshold"] is True
    assert "glosario" in body["reply"]
    assert body["score"] < body["gate"]


def test_above_the_gate_a_faithful_rewrite_is_returned(retriever):
    llm = LLMStub(reply=GOOD_REWRITE)
    with client_for(retriever, llm) as c:
        body = chat(c, "¿Qué es un tank?").json()
    assert llm.chat_calls == 1
    assert body["mode"] == "rewrite" and body["reply"] == GOOD_REWRITE
    assert body["source_id"] == 1 and body["source_term"] == "un tank" and body["reason"] == ""


@pytest.mark.parametrize(
    "drifted, reason",
    [
        ("Un tank es un campeón resistente que absorbe 900 de daño por segundo.", "numbers"),
        ("Es un personaje inventado por la empresa en el año pasado para animar torneos.", "overlap"),
        ("Un tank 是 un campeón resistente.", "script"),
        ("", "empty"),
    ],
)
def test_drifting_rewrite_falls_back_to_the_kb_answer(retriever, drifted, reason):
    llm = LLMStub(reply=drifted)
    with client_for(retriever, llm) as c:
        body = chat(c, "¿Qué es un tank?").json()
    assert llm.chat_calls == 1
    assert body["mode"] == "verbatim" and body["reply"] == ENTRIES[0].answer
    assert body["reason"].startswith("drift") and reason in body["reason"]
    assert body["source_id"] == 1


def test_unavailable_llm_returns_the_kb_answer(retriever):
    with client_for(retriever, LLMStub(fail=True)) as c:
        body = chat(c, "¿Qué es un tank?").json()
    assert body["mode"] == "verbatim" and body["reason"] == "llm_unavailable"
    assert body["reply"] == ENTRIES[0].answer


def test_chat_response_shape(retriever):
    with client_for(retriever, LLMStub(reply=GOOD_REWRITE)) as c:
        for message in ("¿Qué es un tank?", "¿Cuál es la capital de Francia?"):
            body = chat(c, message).json()
            assert set(body) == CHAT_KEYS
            assert isinstance(body["score"], float) and isinstance(body["suggestions"], list)


def test_empty_message_is_rejected(retriever):
    with client_for(retriever, LLMStub()) as c:
        assert chat(c, "   ").status_code == 400


def test_short_follow_up_reuses_the_previous_topic(retriever):
    history = [{"role": "user", "content": "¿Qué es un tank?"}, {"role": "assistant", "content": "..."}]
    with client_for(retriever, LLMStub(reply=GOOD_REWRITE)) as c:
        assert chat(c, "¿y un ejemplo?").json()["mode"] == "refusal"
        assert chat(c, "¿y un ejemplo?", history).json()["source_id"] == 1
        assert chat(c, "¿Cuál es la capital de Francia hoy en día?", history).json()["mode"] == "refusal"


def test_health_and_kb_endpoints(retriever):
    with client_for(retriever, LLMStub()) as c:
        health = c.get("/health").json()
        kb = c.get("/kb").json()
    assert health["ok"] is True and health["llm"] is True and health["entries"] == 6
    assert set(health) == {"ok", "model", "llm", "entries", "gate"}
    assert kb["count"] == 6 and kb["entries"][0]["term"] == "un tank"
    assert {"id", "term", "question", "answer", "aliases", "category", "source"} <= set(kb["entries"][0])


def test_health_reports_unavailable_llm(retriever):
    down = httpx.AsyncClient(
        base_url="http://llm.test", transport=httpx.MockTransport(lambda _r: httpx.Response(503))
    )
    with TestClient(create_app(retriever=retriever, http=down)) as c:
        assert c.get("/health").json()["llm"] is False
