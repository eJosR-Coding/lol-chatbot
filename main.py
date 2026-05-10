"""Atajo para arrancar el backend FastAPI: `uv run python main.py`."""
import uvicorn


def main() -> None:
    uvicorn.run("backend.app:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
