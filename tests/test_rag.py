from backend.rag import Lexicon
from tests.conftest import ENTRIES, make_entry


def test_alias_matches_across_languages():
    lex = Lexicon(ENTRIES)
    assert lex.scores("¿Qué es un campeón tanque?").argmax() == 0  # alias "tanque" of "tank"
    assert lex.scores("me hicieron una emboscada").argmax() == 1
    assert lex.scores("¿Qué es un aturdimiento?").argmax() == 2


def test_no_term_no_lexical_score():
    assert not Lexicon(ENTRIES).scores("¿Cuál es la capital de Francia?").any()


def test_stem_match_is_weaker_than_exact():
    lex = Lexicon(ENTRIES)
    exact = lex.scores("un centinela")[3]
    stem = lex.scores("los centinelas")[3]
    assert exact > stem > 0


def test_short_terms_need_an_exact_token():
    lex = Lexicon([*ENTRIES, make_entry(7, "OP", "Demasiado fuerte.")])
    assert lex.scores("esto es op")[6] > 0
    assert lex.scores("operación")[6] == 0


def test_multi_word_phrase_outranks_a_single_shared_word():
    entries = [
        make_entry(1, "CD", "Tiempo de espera.", ["enfriamiento"]),
        make_entry(2, "CDR", "Reduce el tiempo de espera.", ["reducción de enfriamiento"]),
    ]
    scores = Lexicon(entries).scores("cómo funciona la reducción de enfriamiento")
    assert scores[1] > scores[0]


def test_retriever_finds_entry_through_alias(retriever):
    res = retriever.retrieve("¿Qué es un campeón tanque?")
    assert res["id"] == 1 and not res["below_threshold"]
    assert res["candidates"][0]["lexical"] > 0
    assert len(res["candidates"]) == 3


def test_retriever_scores_unrelated_text_below_the_gate(retriever):
    res = retriever.retrieve("¿Cuál es la capital de Francia?")
    assert res["below_threshold"] and res["score"] < 0.5


def test_unknown_capitalised_entity_is_detected(retriever):
    assert retriever.unknown_entities("¿Qué runas lleva Jinx?") == ["Jinx"]
    assert retriever.unknown_entities("¿Qué es un Stun?") == []
    assert retriever.unknown_entities("Qué es un stun en League of Legends?") == []
