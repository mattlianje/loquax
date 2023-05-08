import unittest

from loquax.languages.latin_specs import latin
from loquax.phonology import get_phonemes
from loquax.syllabification import get_syllables


class TestSplitTokenIntoPhonemes(unittest.TestCase):
    def setUp(self):
        self.lang = latin

    def test_split_word_into_phonemes_valid_input(self):
        word = "rosae"
        result = get_phonemes(word, self.lang)
        self.assertEqual([str(phoneme) for phoneme in result], ["r", "o", "s", "ae"])
        self.assertEqual(len(result), 4)

    def test_split_word_into_phonemes_invalid_input(self):
        word = "aaaa"
        result = get_phonemes(word, self.lang)
        self.assertEqual([str(phoneme) for phoneme in result], ["a", "a", "a", "a"])
        self.assertEqual(len(result), 4)

    def test_split_word_into_phonemes_empty_input(self):
        word = ""
        result = get_phonemes(word, self.lang)
        self.assertEqual(result, [])

    def test_get_ipa_from_phonemes(self):
        word = "dominorum"
        expected = [
            ["d"],
            ["ɔ"],
            ["m"],
            ["ɪ"],
            ["n", "ŋ"],
            ["ɔ"],
            ["r"],
            ["ʊ"],
            ["m"],
        ]
        self.assertEqual(
            [phoneme.ipa for phoneme in get_phonemes(word, self.lang)],
            expected,
        )


class TestSyllabifyToken(unittest.TestCase):
    def setUp(self):
        self.lang = latin

    def test_get_syllables(self):
        tokens = [
            "supra",
            "terra",
            "dominorum",
            "quosque",
            "rosae",
            "aquila",
            "cartago",
        ]
        results = [
            get_syllables(get_phonemes(token, self.lang), self.lang) for token in tokens
        ]
        print(results)


if __name__ == "__main__":
    unittest.main()
