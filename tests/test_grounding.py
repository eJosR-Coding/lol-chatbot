from backend import grounding
import pytest

from backend.kb import load_entries
from tests.conftest import ENTRIES, make_entry

TANK = ENTRIES[0]
Q = "¿Qué es un tanque?"


def check(rewrite: str, entry=TANK, msg=Q):
    return grounding.check_rewrite(rewrite, entry, msg)


def test_faithful_rewrite_passes():
    ok, why = check("Un tank es un campeón resistente que aguanta el daño en las peleas de equipo.")
    assert ok, why


def test_verbatim_source_passes():
    assert check(TANK.answer)[0]


def test_new_numbers_fail():
    ok, why = check("Un tank es un campeón resistente que absorbe 500 de daño en las peleas.")
    assert not ok and "numbers" in why


def test_numbers_from_the_source_are_fine():
    stun = ENTRIES[2]
    assert check("Stun aturde al enemigo 2 segundos.", stun, "¿Qué es un stun?")[0]


def test_invented_names_fail():
    ok, why = check("Un tank es un campeón resistente como Malphite que absorbe daño en las peleas de equipo.")
    assert not ok and "names" in why


def test_names_from_the_question_are_fine():
    ok, why = check(
        "Un tank como Malphite es un campeón resistente que absorbe daño en las peleas de equipo.",
        msg="¿Qué es un tank como Malphite?",
    )
    assert ok, why


def test_low_overlap_fails():
    ok, why = check("Es una estrategia muy popular entre jugadores profesionales durante torneos internacionales.")
    assert not ok and "overlap" in why


def test_other_scripts_empty_and_runaway_text_fail():
    assert not check("Un tank 是一个坦克 campeón resistente")[0]
    assert check("   ")[1] == "empty"
    assert check(TANK.answer * 6)[1] == "too long"


def test_clean_reply_removes_prompt_labels():
    assert grounding.clean_reply("R: [CONTEXTO]Un tank resiste.\n[FIN CONTEXTO]") == "Un tank resiste."
    assert grounding.clean_reply("RESPUESTA: Un tank resiste.") == "Un tank resiste."


def test_refusal_text_suggests_close_terms_when_there_are_any():
    assert "«un tank»" in grounding.refusal([TANK])
    assert "glosario" in grounding.refusal([])


def test_game_names_are_not_inventions():
    ok, why = check("En League of Legends, un tank es un campeón resistente que absorbe daño en las peleas de equipo.")
    assert ok, why
    ok, why = check("Un tank es un campeón resistente que absorbe daño en las peleas de equipo, en League of Legends.")
    assert ok, why


# --- the real glossary entry #93 -------------------------------------------------------------

@pytest.fixture(scope="module")
def kb():
    return load_entries()


@pytest.fixture(scope="module")
def vocab(kb):
    return grounding.domain_terms(kb)


def gank(kb):
    entry = next(e for e in kb if e.id == 93)
    assert "junglero" in entry.answer  # the word the bad rewrite lost
    return entry


GANK_SUBSTITUTED = (
    "Un gank es cuando el enemigo (u otro aliado) viene a tu carril para emboscar al enemigo. "
    "Es coordinado y termina en kill o flash."
)
GANK_FAITHFUL = (
    "Un gank es cuando el junglero (o un aliado) llega a tu carril para emboscar al enemigo. "
    "Es coordinado y normalmente termina en kill o flash."
)


def test_substituted_word_in_the_gank_answer_falls_back(kb, vocab):
    ok, why = grounding.check_rewrite(GANK_SUBSTITUTED, gank(kb), "¿Qué es un gank?", vocab)
    assert not ok
    assert why.startswith("dropped_term") and "jungl" in why  # jungla/junglero are jungler aliases


def test_substitution_is_also_caught_by_the_frequency_guard_alone(kb):
    entry = gank(kb)
    assert grounding.duplicated_word(GANK_SUBSTITUTED, entry.answer) == "enemigo"
    assert grounding.duplicated_word(GANK_FAITHFUL, entry.answer) is None


def test_faithful_gank_paraphrase_is_kept(kb, vocab):
    ok, why = grounding.check_rewrite(GANK_FAITHFUL, gank(kb), "¿Qué es un gank?", vocab)
    assert ok, why


def test_dropping_any_glossary_term_of_the_source_falls_back(kb, vocab):
    rewrite = GANK_FAITHFUL.replace(" o flash", "")
    ok, why = grounding.check_rewrite(rewrite, gank(kb), "¿Qué es un gank?", vocab)
    assert not ok and why == "dropped_term: 'flash'"


def test_domain_terms_group_names_by_entry(vocab):
    names = next(n for n in vocab if ("junglero",) in n)
    assert ("jungler",) in names and ("jungla",) in names
    assert any(("tanque",) in n and ("tank",) in n for n in vocab)


def test_another_name_of_the_same_concept_is_not_a_dropped_term():
    afk = make_entry(1, "AFK", "AFK (away from keyboard) es un jugador ausente.", ["away from keyboard"])
    vocab = grounding.domain_terms([afk])
    ok, why = grounding.check_rewrite("Un jugador AFK está ausente.", afk, "¿Qué es AFK?", vocab)
    assert ok, why
    ok, why = grounding.check_rewrite("Es un jugador ausente.", afk, "¿Qué es AFK?", vocab)
    assert not ok and why.startswith("dropped_term")
