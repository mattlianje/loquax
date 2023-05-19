import unittest

from loquax.abstractions import Syllable, Phoneme
from loquax.languages import Latin
from loquax.abstractions.syllabification import get_syllables_from_token
from loquax.text_processing import Document


class TestSyllabifyToken(unittest.TestCase):
    def setUp(self):
        self.lang = Latin

    def test_get_syllables(self):
        tokens = ["", "suprā", "patrem", "dominōrum", "amāvissem", "aquila", "lesbia"]
        results = [
            [str(syl) for syl in get_syllables_from_token(token, self.lang)]
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
        self.assertEqual(results, expected)

    def test_syllable_creation_invalid(self):
        invalid_syllable_phonemes = [
            Phoneme("a", self.lang),
            Phoneme("m", self.lang),
            Phoneme("a", self.lang),
        ]
        with self.assertRaises(ValueError):
            Syllable(invalid_syllable_phonemes, self.lang)
