"""Grounding of the LLM rewrite: prompts, refusal text and the drift check.

The knowledge-base answer is the only source of truth. The model may rephrase it,
and the rephrasing is kept only if it stays close to the source; otherwise the
chatbot returns the KB answer verbatim.
"""
from __future__ import annotations

import re

from .kb import Entry
from .text import normalize, tokens

SYSTEM_PROMPT = (
    "Eres un asistente de League of Legends que habla español coloquial gamer. "
    "Recibirás un TEXTO DE REFERENCIA y una pregunta. "
    "Responde reformulando SOLO lo que dice el texto de referencia, en 1 o 2 oraciones. "
    "No agregues datos, nombres, números, ejemplos ni explicaciones que no estén en el texto. "
    "Si el texto no responde la pregunta, repite el texto tal cual. "
    "Responde siempre en español y no menciones el 'texto de referencia'."
)

LLM_OPTIONS = {"temperature": 0.1, "top_p": 0.8, "num_predict": 120, "repeat_penalty": 1.1}

# Rewrites must keep at least this share of their content words from the source.
MIN_OVERLAP = 0.6
MAX_LENGTH_RATIO = 2.5

_STOPWORDS = {
    "para", "como", "pero", "porque", "cuando", "donde", "este", "esta", "estos",
    "estas", "esto", "ese", "esa", "eso", "con", "sin", "sobre", "entre", "desde",
    "hasta", "hacia", "tambien", "algo", "cada", "otro", "otra", "otros", "otras",
    "muy", "mas", "menos", "solo", "pues", "puede", "pueden", "tiene", "tienen",
    "hace", "hacen", "sera", "son", "una", "unos", "unas", "del", "los", "las",
    "que", "por", "ser", "esta", "hay", "asi", "aqui", "bien", "mismo", "misma",
    "cual", "quien", "tipo", "vez", "veces", "algun", "alguna", "ellos", "ellas",
    "siempre", "normalmente", "decir", "dice", "llama", "llaman", "significa",
    "refiere", "usa", "usan", "usar", "sirve", "sirven", "forma", "manera",
}
_NON_SPANISH = re.compile(r"[぀-ヿ㐀-鿿가-힯Ѐ-ӿ]")
_NUMBER = re.compile(r"\d+(?:[.,]\d+)?")
_CAPITALISED = re.compile(r"(?<![.!?¿¡\n]\s)(?<!^)\b[A-ZÁÉÍÓÚÑ][a-záéíóúñ]{2,}")


def refusal(suggestions: list[Entry]) -> str:
    if suggestions:
        terms = ", ".join(f"«{s.term}»" for s in suggestions)
        return (
            "Esa no la tengo en mi glosario de LoL, bro. "
            f"¿Quizás buscabas algo como {terms}?"
        )
    return (
        "Esa no la tengo en mi glosario de LoL, bro. Solo sé términos y jerga del juego, "
        "por ejemplo qué es un gank, un ward o el CS."
    )


def build_user_prompt(message: str, source_answer: str) -> str:
    return f"TEXTO DE REFERENCIA:\n{source_answer}\n\nPREGUNTA: {message}\n\nRESPUESTA:"


_LEAK_PATTERNS = [
    re.compile(r"^\s*P\s*:\s*¿[^?]+\?\s*", re.MULTILINE),
    re.compile(r"^\s*R\s*:\s*", re.MULTILINE),
    re.compile(r"^\s*(?:RESPUESTA|PREGUNTA|Pregunta del usuario)\s*:\s*", re.IGNORECASE | re.MULTILINE),
    re.compile(r"\[/?(?:CONTEXTO|FIN)[^\]]*\]\s*", re.IGNORECASE),
    re.compile(r"TEXTO DE REFERENCIA\s*:?\s*", re.IGNORECASE),
]


def clean_reply(text: str) -> str:
    for pat in _LEAK_PATTERNS:
        text = pat.sub("", text)
    return text.strip()


def _content_words(text: str) -> list[str]:
    return [t for t in tokens(text) if len(t) >= 4 and t not in _STOPWORDS and not t.isdigit()]


def _stem(word: str) -> str:
    return word[:5]


def check_rewrite(rewrite: str, entry: Entry, message: str) -> tuple[bool, str]:
    """Return (ok, reason). ``reason`` explains a rejection and is empty when ok."""
    if not rewrite.strip():
        return False, "empty"
    if _NON_SPANISH.search(rewrite):
        return False, "non-spanish script"
    allowed_text = " ".join([entry.answer, entry.question, entry.term, " ".join(entry.aliases), message])
    if len(rewrite) > MAX_LENGTH_RATIO * len(entry.answer) + 80:
        return False, "too long"
    allowed_numbers = {n.replace(",", ".") for n in _NUMBER.findall(allowed_text)}
    extra = {n.replace(",", ".") for n in _NUMBER.findall(rewrite)} - allowed_numbers
    if extra:
        return False, f"new numbers: {sorted(extra)}"
    allowed_norm = normalize(allowed_text)
    new_names = [
        n for n in _CAPITALISED.findall(rewrite) if normalize(n) not in allowed_norm
    ]
    if new_names:
        return False, f"new names: {new_names}"
    words = _content_words(rewrite)
    if words:
        known = {_stem(w) for w in _content_words(allowed_text)}
        overlap = sum(_stem(w) in known for w in words) / len(words)
        if overlap < MIN_OVERLAP:
            return False, f"low overlap with the source ({overlap:.2f})"
    return True, ""
