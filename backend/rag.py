"""Retrieval module — replica de la sección de retrieval del notebook.

Usa sentence-transformers + cosine similarity para encontrar la entrada del
Knowledge Base más cercana a la pregunta del usuario. Es el mismo mecanismo
descrito en el notebook (Q·Kᵀ / √dk a nivel de oraciones).
"""
from __future__ import annotations

import numpy as np
from sentence_transformers import SentenceTransformer

from .kb import KNOWLEDGE_BASE

MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"


class LolRetriever:
    def __init__(self, threshold: float = 0.3) -> None:
        self.threshold = threshold
        self.model = SentenceTransformer(MODEL_NAME)
        self.kb_preguntas = [qa["pregunta"] for qa in KNOWLEDGE_BASE]
        self.kb_respuestas = [qa["respuesta"] for qa in KNOWLEDGE_BASE]
        self.kb_embeddings = self.model.encode(
            self.kb_preguntas, normalize_embeddings=True
        )

    def retrieve(self, query: str) -> dict:
        query_emb = self.model.encode([query], normalize_embeddings=True)[0]
        scores = self.kb_embeddings @ query_emb  # already normalized → dot = cosine
        best_idx = int(np.argmax(scores))
        best_score = float(scores[best_idx])
        return {
            "matched_question": self.kb_preguntas[best_idx],
            "matched_answer": self.kb_respuestas[best_idx],
            "score": best_score,
            "below_threshold": best_score < self.threshold,
        }
