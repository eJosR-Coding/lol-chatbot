from backend import grounding
from tests.conftest import ENTRIES

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


def test_game_names_and_plurals_of_known_words_are_not_inventions():
    ok, why = check("En League of Legends, un tank es un campeón resistente que absorbe daño en las peleas de equipo.")
    assert ok, why
    ok, why = check("Los Tanks son campeones resistentes que absorben daño en las peleas de equipo.")
    assert ok, why
