"""Small text helpers shared by retrieval and grounding (standard library only)."""
from __future__ import annotations

import re
import unicodedata

_WORD = re.compile(r"[a-z0-9]+")

# Tokens that only make up the question frame ("¿Qué es un ...?", "What is a ...?").
_LEADING_FRAME = {
    "que", "cual", "cuales", "como", "quien", "para", "es", "son", "significa",
    "significan", "quiere", "decir", "hace", "hacen", "sirve", "funciona", "se",
    "llama", "el", "la", "los", "las", "un", "una", "unos", "unas", "what", "who",
    "how", "is", "are", "does", "do", "the", "a", "an", "mean", "means", "to",
}
_TRAILING_FRAME = {
    "mean", "means", "en", "in", "league", "of", "legends", "lol", "juego", "el",
    "al", "jugar", "de",
}


def normalize(text: str) -> str:
    """Lowercase, strip accents and apostrophes ("3's" -> "3s")."""
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    return text.lower().replace("'", "").replace("’", "")


def tokens(text: str) -> list[str]:
    return _WORD.findall(normalize(text))


def strip_frame(toks: list[str]) -> list[str]:
    """Drop the shared question scaffolding and keep the subject of the question."""
    start, end = 0, len(toks)
    while start < end - 1 and toks[start] in _LEADING_FRAME:
        start += 1
    while end - 1 > start and toks[end - 1] in _TRAILING_FRAME:
        end -= 1
    return toks[start:end]


def subject(text: str) -> str:
    """The question without its frame, e.g. '¿Qué es un campeón tanque?' -> 'campeon tanque'."""
    return " ".join(strip_frame(tokens(text)))


def headwords(question: str) -> list[str]:
    """Terms a glossary question is about: '¿Qué es AA o autoataque?' -> ['aa', 'autoataque']."""
    parts = re.split(r"\s+o\s+|/", subject(question))
    return [p.strip() for p in parts if p.strip()]
