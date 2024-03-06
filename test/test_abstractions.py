import pytest

from loquax.languages import Latin
from loquax.abstractions.phonology import get_phonemes


@pytest.fixture
def lang():
    return Latin


def test_split_word_into_phonemes_valid_input(lang):
    word = "rosae"
    result = get_phonemes(word, lang)
    assert [str(phoneme) for phoneme in result] == ["r", "o", "s", "ae"]
    assert len(result) == 4


def test_split_word_into_phonemes_invalid_input(lang):
    word = "aaaa"
    result = get_phonemes(word, lang)
    assert [str(phoneme) for phoneme in result] == ["a", "a", "a", "a"]
    assert len(result) == 4


def test_split_word_into_phonemes_empty_input(lang):
    word = ""
    result = get_phonemes(word, lang)
    assert result == []


def test_get_ipa_from_phonemes(lang):
    word = "dominorum"
    expected = ["d", "ɔ", "m", "ɪ", "n", "ɔ", "r", "ʊ", "m"]
    assert [phoneme.ipa for phoneme in get_phonemes(word, lang)] == expected
