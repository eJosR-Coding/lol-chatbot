"""Knowledge-base ingestion: validate ``data/kb.jsonl`` and build the embedding index.

    uv run python -m backend.ingest            # validate, build and persist the index
    uv run python -m backend.ingest --check    # validate only (no model needed)

The index (``data/index/``) is derived data: an ``.npz`` with the embeddings and a
manifest recording the model, entry count and a hash of the data that produced it.
The API loads it at startup and rebuilds it when the manifest no longer matches.
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from .encoder import Encoder
from .kb import DATA_PATH, Entry, KBValidationError, content_hash, load_entries

INDEX_DIR = DATA_PATH.parent / "index"
# Bump when the passage text or the index layout changes.
INDEX_FORMAT = 2
NEAR_DUPLICATE_SIMILARITY = 0.85


@dataclass
class KBIndex:
    entries: list[Entry]
    passage_emb: np.ndarray  # (n_entries, dim): "names: answer" per entry
    variant_emb: np.ndarray  # (n_variants, dim): one row per headword or alias
    variant_owner: np.ndarray  # (n_variants,): entry position of each variant
    manifest: dict


def passage_text(entry: Entry) -> str:
    return f"{', '.join(entry.names)}: {entry.answer}"


def near_duplicates(
    entries: list[Entry], passage_emb: np.ndarray, threshold: float = NEAR_DUPLICATE_SIMILARITY
) -> list[dict]:
    """Pairs of entries whose passages are almost identical. Reported, never removed."""
    sims = passage_emb @ passage_emb.T
    pairs = []
    for i, j in zip(*np.where(np.triu(sims, k=1) >= threshold)):
        pairs.append(
            {
                "a": entries[i].id,
                "b": entries[j].id,
                "similarity": round(float(sims[i, j]), 3),
                "questions": [entries[i].question, entries[j].question],
            }
        )
    return sorted(pairs, key=lambda p: -p["similarity"])


def build_index(entries: list[Entry], encoder: Encoder) -> KBIndex:
    passages = [passage_text(e) for e in entries]
    variants, owner = [], []
    for pos, entry in enumerate(entries):
        for name in entry.names:
            variants.append(name)
            owner.append(pos)
    passage_emb = encoder.encode(passages)
    variant_emb = encoder.encode(variants)
    manifest = {
        "format": INDEX_FORMAT,
        "model": encoder.name,
        "entries": len(entries),
        "variants": len(variants),
        "dim": int(passage_emb.shape[1]),
        "content_hash": content_hash(entries),
        "built_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "near_duplicates": near_duplicates(entries, passage_emb),
    }
    return KBIndex(entries, passage_emb, variant_emb, np.asarray(owner), manifest)


def save_index(index: KBIndex, directory: Path = INDEX_DIR) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        directory / "index.npz",
        passage_emb=index.passage_emb.astype(np.float16),
        variant_emb=index.variant_emb.astype(np.float16),
        variant_owner=index.variant_owner,
    )
    (directory / "manifest.json").write_text(
        json.dumps(index.manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def manifest_matches(manifest: dict, entries: list[Entry], model_name: str) -> str | None:
    """None when the manifest describes this data and model, else the reason it does not."""
    if manifest.get("format") != INDEX_FORMAT:
        return f"index format {manifest.get('format')} != {INDEX_FORMAT}"
    if manifest.get("model") != model_name:
        return f"model {manifest.get('model')} != {model_name}"
    if manifest.get("entries") != len(entries):
        return f"{manifest.get('entries')} indexed entries != {len(entries)} in the data"
    if manifest.get("content_hash") != content_hash(entries):
        return "data changed since the index was built (content hash mismatch)"
    return None


def load_index(entries: list[Entry], model_name: str, directory: Path = INDEX_DIR) -> KBIndex:
    """Load a prebuilt index; raises FileNotFoundError or ValueError when unusable."""
    manifest_path = directory / "manifest.json"
    npz_path = directory / "index.npz"
    if not manifest_path.exists() or not npz_path.exists():
        raise FileNotFoundError(f"no index in {directory}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    reason = manifest_matches(manifest, entries, model_name)
    if reason:
        raise ValueError(f"stale index: {reason}")
    with np.load(npz_path) as z:
        return KBIndex(
            entries,
            z["passage_emb"].astype(np.float32),
            z["variant_emb"].astype(np.float32),
            z["variant_owner"],
            manifest,
        )


def ensure_index(
    entries: list[Entry],
    encoder: Encoder,
    directory: Path = INDEX_DIR,
    strict: bool = False,
    log=print,
) -> KBIndex:
    """Use the prebuilt index when it matches the data, otherwise rebuild it.

    With ``strict`` a missing or stale index is an error that names the command to run.
    """
    try:
        return load_index(entries, encoder.name, directory)
    except (FileNotFoundError, ValueError, KeyError) as e:
        if strict:
            raise RuntimeError(
                f"{e}. Run `uv run python -m backend.ingest` to rebuild the index."
            ) from e
        log(f"[index] {e}; rebuilding")
    index = build_index(entries, encoder)
    try:
        save_index(index, directory)
    except OSError as e:  # read-only checkout: keep the in-memory index
        log(f"[index] could not persist index: {e}")
    return index


def report(index: KBIndex) -> str:
    m = index.manifest
    lines = [
        f"entries: {m['entries']}  variants: {m['variants']}  dim: {m['dim']}  model: {m['model']}",
        f"content hash: {m['content_hash'][:16]}",
    ]
    dups = m["near_duplicates"]
    if dups:
        lines.append(f"near-duplicates (passage cosine >= {NEAR_DUPLICATE_SIMILARITY}, not removed):")
        lines += [f"  #{d['a']} ~ #{d['b']}  {d['similarity']}  {d['questions']}" for d in dups]
    else:
        lines.append(f"near-duplicates (passage cosine >= {NEAR_DUPLICATE_SIMILARITY}): none")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--data", type=Path, default=DATA_PATH, help="path to kb.jsonl")
    ap.add_argument("--out", type=Path, default=INDEX_DIR, help="index output directory")
    ap.add_argument("--check", action="store_true", help="validate the data only")
    args = ap.parse_args(argv)
    try:
        entries = load_entries(args.data)
    except KBValidationError as e:
        print(e, file=sys.stderr)
        return 1
    print(f"{args.data}: {len(entries)} entries, schema OK")
    if args.check:
        return 0
    from .encoder import SentenceEncoder

    index = build_index(entries, SentenceEncoder())
    save_index(index, args.out)
    print(report(index))
    print(f"index written to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
