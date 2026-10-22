"""Hybrid retrieval over the glossary knowledge base.

Each entry is represented three ways:

* a passage embedding of "headwords, aliases: answer" (what the entry is about,
  not the shape of its question),
* one embedding per term (headwords and English/Spanish aliases),
* the terms themselves for an exact / prefix / fuzzy lexical match.

The query is embedded as written and, with the question frame removed, against
the term embeddings. The final score is the best dense similarity plus a bonus
when a glossary term appears in the query; ties between entries are broken by
the dense score. Only the standard library is used for the lexical part.
"""
from __future__ import annotations

import re
from collections import Counter
from difflib import SequenceMatcher

import numpy as np

from .encoder import MODEL_NAME, Encoder, SentenceEncoder  # noqa: F401  (re-exported)
from .ingest import KBIndex, ensure_index
from .kb import Entry, load_entries
from .text import normalize, strip_frame, tokens

# Retrieval gate: below this fused score the chatbot refuses and never calls the LLM.
GATE_THRESHOLD = 0.70
# Weight of a lexical (glossary term) hit on top of the dense similarity.
LEXICAL_BONUS = 0.35
# A lexical hit is a signal, not a verdict: dense similarity is trusted at this fraction
# when no term of the entry appears in the query.
TERM_DENSE_WEIGHT = 0.9
# Terms shorter than this must match a whole token; longer ones may match by shared stem.
STEM_MIN = 5
FUZZY_RATIO = 0.88
# Words used by at least this many glossary questions ("campeón", "habilidad") are too
# generic to identify an entry on their own.
GENERIC_TERM_DF = 4
# A single word of a multi-word term is weak evidence.
PARTIAL_STRENGTH = 0.2
# A capitalised word the glossary has never seen ("Ahri", "Francia") means the question is
# probably about something the glossary does not cover: its dense score is reduced by this.
UNKNOWN_ENTITY_PENALTY = 0.15
_GAME_NAMES = {"league", "legends", "lol", "riot", "games"}
_CAPITALISED = re.compile(r"\b[A-ZÁÉÍÓÚÑ][\wáéíóúñ'\u2019]+")
# Hubness correction (CSLS-style): entries that sit close to many unrelated short texts
# get their dense score reduced by this fraction of their excess hubness.
HUB_ALPHA = 1.0
HUB_K = 10


class Lexicon:
    """Exact / prefix / fuzzy matching of glossary terms against a query."""

    def __init__(self, entries: list[Entry]) -> None:
        self.terms: list[list[tuple[str, ...]]] = []  # per entry: full terms as token tuples
        self.partial: list[list[str]] = []  # per entry: single non-generic tokens of multi-token terms
        df: Counter[str] = Counter()
        full: list[set[tuple[str, ...]]] = []
        for entry in entries:
            entry_full = {tuple(tokens(n)) for n in entry.names if tokens(n)}
            full.append(entry_full)
            df.update({t for term in entry_full for t in term})
        generic = {t for t, n in df.items() if n >= GENERIC_TERM_DF}
        self.term_df: Counter[tuple[str, ...]] = Counter(t for e in full for t in e)
        for entry_full in full:
            self.terms.append(sorted(entry_full))
            partial = {
                t
                for term in entry_full
                if len(term) > 1
                for t in term
                if t not in generic and len(t) >= STEM_MIN
            }
            self.partial.append(sorted(partial))

    @staticmethod
    def _token_match(term: str, query_tokens: list[str]) -> float:
        """Strength 0..1 of one single-token term against the query tokens."""
        best = 0.0
        for tok in query_tokens:
            if tok == term:
                return 1.0
            if len(term) < STEM_MIN or len(tok) < STEM_MIN:
                continue
            # Shared stem: "wardeos" ~ "wardear", "trolleando" ~ "trollear", "tanquear" ~ "tanque".
            stem = 0
            for a, b in zip(term, tok):
                if a != b:
                    break
                stem += 1
            if stem >= max(STEM_MIN, 0.75 * min(len(term), len(tok))):
                best = max(best, 0.5)
            elif SequenceMatcher(None, term, tok).ratio() >= FUZZY_RATIO:
                best = max(best, 0.4)
        return best

    @staticmethod
    def _phrase_in(term: tuple[str, ...], query_tokens: list[str]) -> bool:
        n = len(term)
        return any(tuple(query_tokens[i : i + n]) == term for i in range(len(query_tokens) - n + 1))

    def scores(self, query: str) -> np.ndarray:
        q = tokens(query)
        out = np.zeros(len(self.terms))
        for i, (terms, partial) in enumerate(zip(self.terms, self.partial)):
            best = 0.0
            for term in terms:
                if len(term) == 1:
                    strength = self._token_match(term[0], q)
                else:
                    strength = len(term) ** 0.5 if self._phrase_in(term, q) else 0.0  # longer phrase, stronger hit
                # A term claimed by several entries identifies none of them well.
                best = max(best, strength / self.term_df[term] ** 0.5)
            for tok in partial:
                best = max(best, PARTIAL_STRENGTH * self._token_match(tok, q))
            out[i] = best
        return out


class LolRetriever:
    def __init__(
        self, index: KBIndex, encoder: Encoder, threshold: float = GATE_THRESHOLD
    ) -> None:
        self.index = index
        self.entries = index.entries
        self.encoder = encoder
        self.threshold = threshold
        self.lexicon = Lexicon(self.entries)
        self.vocab = {
            t
            for e in self.entries
            for text in (e.term, e.question, e.answer, *e.aliases)
            for t in tokens(text)
        } | _GAME_NAMES
        self.hub = self._hubness()

    def _hubness(self) -> np.ndarray:
        """Mean similarity of each passage to its closest short texts from *other* entries."""
        ix = self.index
        sims = ix.passage_emb @ ix.variant_emb.T
        sims[np.arange(len(self.entries))[:, None] == ix.variant_owner[None, :]] = -1.0
        hub = np.sort(sims, axis=1)[:, -HUB_K:].mean(axis=1)
        return hub - hub.mean()

    def unknown_entities(self, query: str) -> list[str]:
        """Capitalised words (not the first of the sentence) that appear nowhere in the KB."""
        words = [(m.start(), m.group()) for m in _CAPITALISED.finditer(query)]
        first = re.search(r"[A-Za-zÁÉÍÓÚÑáéíóúñ]", query)
        start = first.start() if first else 0
        return [w for pos, w in words if pos != start and normalize(w).replace("'", "") not in self.vocab
                and not all(t in self.vocab for t in tokens(w))]

    def score_all(self, query: str) -> dict[str, np.ndarray]:
        ix = self.index
        subject_text = " ".join(strip_frame(tokens(query))) or normalize(query)
        q_raw, q_subj = self.encoder.encode([query, subject_text])
        passage = ix.passage_emb @ q_raw
        term = np.full(len(self.entries), -1.0)
        np.maximum.at(term, ix.variant_owner, ix.variant_emb @ q_subj)
        dense = np.maximum(passage - HUB_ALPHA * self.hub, TERM_DENSE_WEIGHT * term)
        if self.unknown_entities(query):
            dense = dense - UNKNOWN_ENTITY_PENALTY
        lexical = self.lexicon.scores(query)
        fused = dense + LEXICAL_BONUS * lexical  # unclipped so phrase hits still rank above single words
        return {"dense": dense, "lexical": lexical, "score": fused}

    def retrieve(self, query: str, k: int = 3) -> dict:
        s = self.score_all(query)
        order = np.argsort(-s["score"], kind="stable")[:k]
        candidates = [self._candidate(int(i), s) for i in order]
        best = candidates[0]
        return {
            "id": best["id"],
            "term": best["term"],
            "matched_question": best["question"],
            "matched_answer": best["answer"],
            "score": best["score"],
            "below_threshold": best["score"] < self.threshold,
            "candidates": candidates,
        }

    def _candidate(self, idx: int, s: dict[str, np.ndarray]) -> dict:
        entry = self.entries[idx]
        return {
            "id": entry.id,
            "term": entry.term,
            "question": entry.question,
            "answer": entry.answer,
            "category": entry.category,
            "score": min(float(s["score"][idx]), 1.0),
            "dense": float(s["dense"][idx]),
            "lexical": float(s["lexical"][idx]),
        }


def load_retriever(strict: bool = False, log=print) -> LolRetriever:
    """Load the data, the prebuilt index (rebuilt if stale) and the sentence encoder."""
    entries = load_entries()
    encoder = SentenceEncoder()
    return LolRetriever(ensure_index(entries, encoder, strict=strict, log=log), encoder)
