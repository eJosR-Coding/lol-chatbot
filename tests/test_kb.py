import json

import pytest

from backend.kb import Entry, KBValidationError, content_hash, load_entries, parse_entries


def line(**over) -> str:
    base = {"id": 1, "term": "AFK", "question": "¿Qué significa AFK?", "answer": "Ausente.",
            "aliases": [], "category": "chat", "source": "test"}
    return json.dumps({**base, **over}, ensure_ascii=False)


def problems(*lines: str) -> list[str]:
    with pytest.raises(KBValidationError) as e:
        parse_entries(list(lines))
    return e.value.problems


def test_valid_line_parses_and_cleans_text():
    (e,) = parse_entries([line(answer="  Ausente \n del   juego. ", aliases=["Away", " away ", "", "ausente"])])
    assert e.answer == "Ausente del juego."
    assert e.aliases == ["Away", "ausente"]  # whitespace collapsed, duplicates and empties dropped


def test_missing_field_is_reported_with_line_number():
    bad = json.loads(line())
    del bad["answer"]
    assert any("line 1" in p and "answer" in p for p in problems(json.dumps(bad)))


def test_unknown_category_and_extra_field_are_rejected():
    out = problems(line(category="nonsense"), line(id=2, extra=1))
    assert any("category" in p for p in out)
    assert any("extra" in p for p in out)


def test_question_must_end_with_question_mark_and_text_must_not_be_empty():
    out = problems(line(question="Qué es AFK"), line(id=2, question="¿Otra?", answer="   "))
    assert any("must end with '?'" in p for p in out)
    assert any("answer" in p and "empty" in p for p in out)


def test_invalid_json_is_reported():
    assert any("not valid JSON" in p for p in problems("{oops"))


def test_duplicate_id_and_duplicate_question_are_errors():
    out = problems(line(), line(question="¿QUÉ significa AFK?"))
    assert any("duplicate id" in p for p in out)
    assert any("duplicate question" in p for p in out)


def test_content_hash_changes_with_any_field():
    a = parse_entries([line()])
    assert content_hash(a) == content_hash(parse_entries([line()]))
    assert content_hash(a) != content_hash(parse_entries([line(answer="Otra cosa.")]))
    assert content_hash(a) != content_hash(parse_entries([line(aliases=["away"])]))


def test_names_are_headwords_plus_aliases():
    e = Entry.model_validate_json(line(question="¿Qué es AA o autoataque?", aliases=["auto attack"]))
    assert e.names == ["aa", "autoataque", "auto attack"]


def test_shipped_knowledge_base_is_complete_and_valid():
    entries = load_entries()
    assert len(entries) == 239
    assert [e.id for e in entries] == list(range(1, 240))
    by_id = {e.id: e for e in entries}
    assert by_id[11].question == "¿Qué significa AFK?"
    assert by_id[24].question == "¿Qué es Baron Nashor?"
    assert "Baron es el monstruo neutral" in by_id[24].answer
    assert "tanque" in by_id[209].aliases
    assert all(e.aliases for e in entries[:20])
