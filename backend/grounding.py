"""Grounding of the LLM rewrite: prompts, refusal text and the drift check.

The knowledge-base answer is the only source of truth. The model may rephrase it,
and the rephrasing is kept only if it stays close to the source; otherwise the
chatbot returns the KB answer verbatim.
"""
from __future__ import annotations

import re
from collections import Counter

from .kb import Entry
from .text import normalize, shares_stem, tokens

SYSTEM_PROMPT = (
    "Eres un asistente de League of Legends que habla español coloquial gamer. "
    "Recibirás un TEXTO DE REFERENCIA y una pregunta. "
    "Responde reformulando SOLO lo que dice el texto de referencia, en 1 o 2 oraciones. "
    "No agregues datos, nombres, números, ejemplos ni explicaciones que no estén en el texto. "
    "Si el texto no responde la pregunta, repite el texto tal cual. "
    "Responde siempre en español y no menciones el 'texto de referencia'."
)

LLM_OPTIONS = {"temperature": 0.1, "top_p": 0.8, "num_predict": 120, "repeat_penalty": 1.1}

# A 0.5B model paraphrases loosely and invents details, so a rewrite is only kept when at least
# this share of its content words (compared by 5-letter stem) comes from the source, the question
# or the entry aliases. Everything else falls back to the KB text.
MIN_OVERLAP = 0.8
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
# Names of the game itself are not inventions.
_GAME_NAMES = {"league", "legends", "riot", "lol"}
_NON_SPANISH = re.compile(r"[぀-ヿ㐀-鿿가-힯Ѐ-ӿ]")
_NUMBER = re.compile(r"\d+(?:[.,]\d+)?")
_CAPITALISED = re.compile(r"(?<![.!?¿¡\n]\s)(?<!^)\b[A-ZÁÉÍÓÚÑ][a-záéíóúñ]{2,}")


def _stem(word: str) -> str:
    return word[:5]


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


def same_text(a: str, b: str) -> bool:
    return normalize(" ".join(tokens(a))) == normalize(" ".join(tokens(b)))


def _content_words(text: str) -> list[str]:
    return [t for t in tokens(text) if len(t) >= 4 and t not in _STOPWORDS and t not in _GAME_NAMES and not t.isdigit()]


# One group of names per glossary entry: "AFK" and "away from keyboard" are the same concept.
DomainTerms = list[frozenset[tuple[str, ...]]]


def domain_terms(entries: list[Entry]) -> DomainTerms:
    """Every glossary term and alias of the knowledge base, grouped by entry, as token tuples."""
    return [
        frozenset(tuple(tokens(name)) for name in e.names if tokens(name)) for e in entries
    ]


def _contains(term: tuple[str, ...], toks: list[str]) -> bool:
    """Phrase match; single words also match by shared stem (like the lexical scorer)."""
    if len(term) == 1:
        return any(shares_stem(term[0], t) for t in toks)
    n = len(term)
    return any(tuple(toks[i : i + n]) == term for i in range(len(toks) - n + 1))


def dropped_term(rewrite: str, source: str, terms: DomainTerms) -> str | None:
    """A glossary concept the source answer uses that the rewrite no longer mentions.

    For every entry with a term or alias in the source, at least one of that entry's names
    must still appear in the rewrite (so "AFK" may become "away from keyboard", but a
    "junglero" cannot silently turn into an "enemigo")."""
    src, new = tokens(source), tokens(rewrite)
    for names in terms:
        in_source = sorted((t for t in names if _contains(t, src)), key=lambda t: (-len(t), t))
        if in_source and not any(_contains(t, new) for t in names):
            return " ".join(in_source[0])
    return None


def duplicated_word(rewrite: str, source: str) -> str | None:
    """A content word of the source that the rewrite uses more often than the source does: the
    signature of a substitution ("junglero" replaced by a second "enemigo"). Words the source
    never uses are left to the overlap check."""
    seen = Counter(_stem(w) for w in _content_words(source))
    used = Counter(_stem(w) for w in _content_words(rewrite))
    for word in _content_words(rewrite):
        if seen[_stem(word)] and used[_stem(word)] > seen[_stem(word)]:
            return word
    return None


def check_rewrite(
    rewrite: str, entry: Entry, message: str, terms: DomainTerms | None = None
) -> tuple[bool, str]:
    """Return (ok, reason). ``reason`` explains a rejection and is empty when ok.

    ``terms`` is the glossary vocabulary of the whole KB (see ``domain_terms``); without it
    only the names of ``entry`` itself are protected."""
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
    known = {t for t in tokens(allowed_text) if len(t) >= 4} | _GAME_NAMES
    new_names = [
        n
        for n in _CAPITALISED.findall(rewrite)
        if normalize(n) not in allowed_norm
        and not any(t.startswith(normalize(n)[:4]) or normalize(n).startswith(t) for t in known)
    ]
    if new_names:
        return False, f"new names: {new_names}"
    words = _content_words(rewrite)
    if words:
        known = {_stem(w) for w in _content_words(allowed_text)}
        overlap = sum(_stem(w) in known for w in words) / len(words)
        if overlap < MIN_OVERLAP:
            return False, f"low overlap with the source ({overlap:.2f})"
    missing = dropped_term(rewrite, entry.answer, terms if terms is not None else domain_terms([entry]))
    if missing:
        return False, f"dropped_term: {missing!r}"
    repeated = duplicated_word(rewrite, entry.answer)
    if repeated:
        return False, f"duplicated_word: {repeated!r}"
    return True, ""
