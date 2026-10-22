"""Knowledge base: schema, validation and loader for ``data/kb.jsonl``.

The JSONL file is the source of truth (one entry per line). ``backend.ingest``
validates it and builds the embedding index; the API only reads it through
``load_entries``.
"""
from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, ValidationError, field_validator

from .text import headwords, normalize

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "kb.jsonl"

Category = Literal[
    "game_mode", "role", "crowd_control", "stat", "map", "chat", "tactic", "mechanics"
]


def clean(text: str) -> str:
    """NFC-normalise and collapse whitespace."""
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", text)).strip()


class Entry(BaseModel):
    """One glossary entry. ``question`` and ``answer`` are what the chatbot shows."""

    model_config = ConfigDict(extra="forbid")

    id: int
    term: str
    question: str
    answer: str
    aliases: list[str] = []
    category: Category
    source: str

    @field_validator("term", "question", "answer", "source", mode="before")
    @classmethod
    def _clean_text(cls, v: object) -> object:
        return clean(v) if isinstance(v, str) else v

    @field_validator("aliases", mode="before")
    @classmethod
    def _clean_aliases(cls, v: object) -> object:
        if not isinstance(v, list):
            return v
        seen: set[str] = set()
        out = []
        for alias in v:
            if not isinstance(alias, str):
                return v
            alias = clean(alias)
            if alias and normalize(alias) not in seen:
                seen.add(normalize(alias))
                out.append(alias)
        return out

    @field_validator("id")
    @classmethod
    def _positive_id(cls, v: int) -> int:
        if v < 1:
            raise ValueError("id must be >= 1")
        return v

    @field_validator("term", "question", "answer", "source")
    @classmethod
    def _non_empty(cls, v: str) -> str:
        if not v:
            raise ValueError("must not be empty")
        return v

    @field_validator("question")
    @classmethod
    def _is_question(cls, v: str) -> str:
        if not v.endswith("?"):
            raise ValueError("question must end with '?'")
        return v

    @property
    def names(self) -> list[str]:
        """Headwords of the question plus aliases: every way to call this concept."""
        return [*headwords(self.question), *self.aliases]


class KBValidationError(ValueError):
    """Raised with one human-readable line per problem found in the data file."""

    def __init__(self, problems: list[str]) -> None:
        self.problems = problems
        super().__init__("invalid knowledge base:\n  " + "\n  ".join(problems))


def parse_entries(lines: list[str]) -> list[Entry]:
    """Validate JSONL lines; exact duplicate ids or questions are errors."""
    problems: list[str] = []
    entries: list[Entry] = []
    for n, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            entries.append(Entry.model_validate(json.loads(line)))
        except json.JSONDecodeError as e:
            problems.append(f"line {n}: not valid JSON ({e.msg})")
        except ValidationError as e:
            for err in e.errors():
                where = ".".join(str(p) for p in err["loc"]) or "entry"
                problems.append(f"line {n}: {where}: {err['msg']}")
    ids: dict[int, int] = {}
    questions: dict[str, int] = {}
    for n, entry in enumerate(entries, 1):
        if entry.id in ids:
            problems.append(f"entry #{entry.id}: duplicate id (also entry {ids[entry.id]})")
        ids.setdefault(entry.id, n)
        key = normalize(entry.question)
        if key in questions:
            problems.append(
                f"entry #{entry.id}: duplicate question {entry.question!r} "
                f"(also entry {questions[key]})"
            )
        questions.setdefault(key, n)
    if problems:
        raise KBValidationError(problems)
    return entries


def load_entries(path: Path = DATA_PATH) -> list[Entry]:
    return parse_entries(path.read_text(encoding="utf-8").splitlines())


def content_hash(entries: list[Entry]) -> str:
    """Stable hash of everything that feeds the index."""
    payload = json.dumps(
        [e.model_dump() for e in entries], ensure_ascii=False, sort_keys=True
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
