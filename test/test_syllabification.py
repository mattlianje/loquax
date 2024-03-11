import pytest

from loquax.abstractions import Syllable, Phoneme
from loquax.languages import Latin
from loquax.abstractions.syllabification import get_syllables_from_token


@pytest.fixture
def lang():
    return Latin


@pytest.mark.usefixtures("lang")
@pytest.mark.syllabification_e2e
class TestSyllabificationE2E:
    def test_get_syllables(self, lang):
        tokens = [
            "",
            "suprā",
            "patrem",
            "dominōrum",
            "amāvissem",
            "aquila",
            "lesbia",
        ]
        results = [
            [str(syl) for syl in get_syllables_from_token(token, lang)]
            for token in tokens
        ]
        expected = [
            [""],
            ["su", "prā"],
            ["pa", "trem"],
            ["do", "mi", "nō", "rum"],
            ["a", "mā", "vis", "sem"],
            ["a", "qui", "la"],
            ["les", "bi", "a"],
        ]
        assert (
            results == expected
        ), "The syllabification did not produce the expected results."

    def test_syllable_creation_invalid(self, lang):
        invalid_syllable_phonemes = [
            Phoneme("a", lang),
            Phoneme("m", lang),
            Phoneme("a", lang),
        ]
        with pytest.raises(ValueError):
            Syllable(invalid_syllable_phonemes, lang)
