# LoL RAG Chatbot — UNAB 2026

Chatbot sobre League of Legends que combina dos piezas:

1. **Retrieval (notebook)** — `sentence-transformers` (`paraphrase-multilingual-MiniLM-L12-v2`)
   genera embeddings 384d y elige la entrada del Knowledge Base más cercana por
   *cosine similarity* (esto es `Q·Kᵀ` a nivel de oraciones, ver
   `lol_chatbot.ipynb`).
2. **Generation** — el contexto recuperado se inyecta como *system + user prompt*
   a un modelo Ollama tiny (`qwen2.5:0.5b`, ~400 MB) que reformula la respuesta
   en español coloquial gamer.

```
backend/    FastAPI + RAG + Ollama
frontend/   Astro + Tailwind (dark glass UI)
lol_chatbot.ipynb   notebook original (intacto)
```

## Requisitos

- Python ≥ 3.14, [`uv`](https://docs.astral.sh/uv/)
- Node ≥ 20, npm
- [Ollama](https://ollama.com) corriendo local (`ollama serve`) con `qwen2.5:0.5b`:
  ```sh
  curl -fsSL https://ollama.com/install.sh | sh
  ollama pull qwen2.5:0.5b
  ```

## Arrancar

**Backend** (puerto 8000):
```sh
uv sync
uv run python main.py
# o: uv run uvicorn backend.app:app --reload
```

**Frontend** (puerto 4321):
```sh
cd frontend
npm install
npm run dev
```

Abre <http://127.0.0.1:4321>.

## Configuración

Variables de entorno:

| Var | Default | Descripción |
|---|---|---|
| `OLLAMA_HOST` | `http://127.0.0.1:11434` | Endpoint de Ollama |
| `OLLAMA_MODEL` | `qwen2.5:0.5b` | Modelo de generación |
| `PUBLIC_BACKEND_URL` (frontend) | `http://127.0.0.1:8000` | URL del backend |

## Endpoints

- `GET  /health` → `{ ok, model }`
- `POST /chat`   → `{ message }` → `{ reply, matched_question, matched_answer, score, below_threshold }`
