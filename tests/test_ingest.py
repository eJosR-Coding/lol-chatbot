import json

import pytest

from backend import ingest
from backend.ingest import build_index, ensure_index, load_index, near_duplicates, save_index
from backend.kb import Entry
from tests.conftest import ENTRIES, FakeEncoder, make_entry


def test_build_index_shapes_and_manifest(encoder):
    ix = build_index(ENTRIES, encoder)
    m = ix.manifest
    assert ix.passage_emb.shape == (len(ENTRIES), 128)
    assert len(ix.variant_emb) == len(ix.variant_owner) == m["variants"]
    assert m["entries"] == len(ENTRIES) and m["model"] == "fake-bow" and len(m["content_hash"]) == 64
    assert set(ix.variant_owner) == set(range(len(ENTRIES)))


def test_near_duplicates_are_reported_not_removed(encoder):
    twin = make_entry(7, "un tank (otra vez)", ENTRIES[0].answer, ["tanque", "frontline"])
    entries = [*ENTRIES, twin]
    ix = build_index(entries, encoder)
    pairs = ix.manifest["near_duplicates"]
    assert [(p["a"], p["b"]) for p in pairs] == [(1, 7)]
    assert pairs[0]["similarity"] >= ingest.NEAR_DUPLICATE_SIMILARITY
    assert len(ix.entries) == len(entries)  # nothing is deleted
    assert near_duplicates(ENTRIES, build_index(ENTRIES, encoder).passage_emb) == []


def test_save_and_load_roundtrip(tmp_path, encoder):
    ix = build_index(ENTRIES, encoder)
    save_index(ix, tmp_path)
    loaded = load_index(ENTRIES, encoder.name, tmp_path)
    assert loaded.manifest == ix.manifest
    assert loaded.passage_emb == pytest.approx(ix.passage_emb, abs=1e-2)  # stored as float16
    assert (loaded.variant_owner == ix.variant_owner).all()


def test_changed_data_makes_the_index_stale(tmp_path, encoder):
    save_index(build_index(ENTRIES, encoder), tmp_path)
    edited = [*ENTRIES[:-1], make_entry(6, "AFK", "Otra respuesta distinta.", ["ausente"])]
    with pytest.raises(ValueError, match="content hash"):
        load_index(edited, encoder.name, tmp_path)


def test_other_model_or_entry_count_makes_the_index_stale(tmp_path, encoder):
    save_index(build_index(ENTRIES, encoder), tmp_path)
    with pytest.raises(ValueError, match="model"):
        load_index(ENTRIES, "another-model", tmp_path)
    with pytest.raises(ValueError, match="entries"):
        load_index(ENTRIES[:-1], encoder.name, tmp_path)


def test_ensure_index_rebuilds_on_hash_mismatch_and_persists(tmp_path, encoder):
    save_index(build_index(ENTRIES, encoder), tmp_path)
    edited = [*ENTRIES[:-1], make_entry(6, "AFK", "Otra respuesta distinta.")]
    messages: list[str] = []
    ix = ensure_index(edited, encoder, tmp_path, log=messages.append)
    assert any("rebuilding" in m for m in messages)
    assert json.loads((tmp_path / "manifest.json").read_text())["content_hash"] == ix.manifest["content_hash"]
    # the rebuilt index was written, so the next load succeeds without rebuilding
    assert load_index(edited, encoder.name, tmp_path).manifest["content_hash"] == ix.manifest["content_hash"]


def test_ensure_index_uses_matching_index_without_encoding(tmp_path, encoder):
    save_index(build_index(ENTRIES, encoder), tmp_path)

    class Exploding(FakeEncoder):
        def encode(self, texts):
            raise AssertionError("the encoder must not run when the index matches")

    assert ensure_index(ENTRIES, Exploding(), tmp_path).manifest["entries"] == len(ENTRIES)


def test_strict_mode_fails_with_the_command_to_run(tmp_path, encoder):
    with pytest.raises(RuntimeError, match=r"python -m backend\.ingest"):
        ensure_index(ENTRIES, encoder, tmp_path, strict=True)


def test_cli_check_validates_without_a_model(tmp_path, capsys):
    good = tmp_path / "kb.jsonl"
    good.write_text(Entry.model_validate(ENTRIES[0].model_dump()).model_dump_json() + "\n", encoding="utf-8")
    assert ingest.main(["--data", str(good), "--check"]) == 0
    bad = tmp_path / "bad.jsonl"
    bad.write_text("{}\n", encoding="utf-8")
    assert ingest.main(["--data", str(bad), "--check"]) == 1
    assert "invalid knowledge base" in capsys.readouterr().err
