import unittest
from loquax.phonology import *
from loquax.latin_grammar import latin_equivalencies


class TestSplitTokenIntoPhonemes(unittest.TestCase):
    def setUp(self):
        self.letter_groups = ["aaa", "ai", "b", "c", "d"]
        self.phonemes = [Phoneme("a"), Phoneme("a")]

    def test_split_word_into_phonemes_fp_valid_input(self):
        word = "aa"
        result = split_token_into_phonemes(word, self.letter_groups)
        self.assertEqual(result[0].val, "a")
        self.assertEqual(len(result), 2)

    def test_split_word_into_phonemes_fp_invalid_input(self):
        word = "aaaa"
        result = split_token_into_phonemes(word, self.letter_groups)
        self.assertEqual([result[0].val, result[1].val], ["aaa", "a"])

    def test_split_word_into_phonemes_fp_empty_input(self):
        word = ""
        result = split_token_into_phonemes(word, self.letter_groups)
        self.assertEqual(result, [])

    def test_split_word_into_phonemes_fp_no_letter_groups(self):
        word = "ab"
        letter_groups = []
        result = split_token_into_phonemes(word, letter_groups)
        self.assertEqual([result[0].val, result[1].val], ["a", "b"])


class TestGetIPA(unittest.TestCase):
    def setUp(self):
        self.equivalencies = latin_equivalencies

    def test_get_ipa_for_word_in_equivalencies(self):
        word = "rosae"
        expected = [{"r": ["r"]}, {"o": ["ɔ"]}, {"s": ["s"]}, {"ae": ["ae̯"]}]
        self.assertEqual(get_ipa_for_token(word, self.equivalencies), expected)

    def test_get_ipa_for_word_in_equivalencies_2(self):
        word = "dominorum"
        expected = [
            {"d": ["d"]},
            {"o": ["ɔ"]},
            {"m": ["m"]},
            {"i": ["ɪ"]},
            {"n": ["n", "ŋ"]},
            {"o": ["ɔ"]},
            {"r": ["r"]},
            {"u": ["ʊ"]},
            {"m": ["m"]},
        ]
        self.assertEqual(get_ipa_for_token(word, self.equivalencies), expected)

    def test_get_ipa_for_empty_word(self):
        word = ""
        expected = []
        self.assertEqual(get_ipa_for_token(word, self.equivalencies), expected)

    def test_get_ipa_for_empty_equivalencies(self):
        word = "한국어"
        equivalencies = {}
        with self.assertRaises(Exception) as context:
            get_ipa_for_token(word, equivalencies)
        self.assertEqual(str(context.exception), f"Sorry, '{word[0]}' is not in: set()")


if __name__ == "__main__":
    unittest.main()
