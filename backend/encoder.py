"""Sentence encoder interface. sentence-transformers is imported lazily so that
tests (and ``ingest --check``) run without downloading or loading the model."""
from __future__ import annotations

from typing import Protocol

import numpy as np

MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"


class Encoder(Protocol):
    name: str

    def encode(self, texts: list[str]) -> np.ndarray:
        """Return L2-normalised float32 embeddings, one row per text."""


class SentenceEncoder:
    def __init__(self, model_name: str = MODEL_NAME) -> None:
        from sentence_transformers import SentenceTransformer

        self.name = model_name
        self.model = SentenceTransformer(model_name)

    def encode(self, texts: list[str]) -> np.ndarray:
        return np.asarray(
            self.model.encode(texts, normalize_embeddings=True), dtype=np.float32
        )
