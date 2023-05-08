import unittest

from loquax.languages.latin_specs import latin
from loquax.entities import (
    Morphism,
    PhonemeRuleSequence,
    PhonemeRule,
    MorphismStore,
    Syllable,
    PhonemeSyllabificationRuleStore,
)
from loquax.phonology import *

import unittest


class TestMorphism(unittest.TestCase):
    def setUp(self):
        self.lang = latin
        self.phoneme_a = Phoneme("a", self.lang)
        self.phoneme_b = Phoneme("b", self.lang)
        self.phoneme_c = Phoneme("c", self.lang)
        self.phoneme_d = Phoneme("d", self.lang)
        self.morphism_1 = Morphism(
            val=PhonemeRuleSequence([PhonemeRule(phoneme_val="b")]),
            new_val=[self.phoneme_d],
            prefix=PhonemeRuleSequence([PhonemeRule(phoneme_val="a")]),
            suffix=PhonemeRuleSequence([PhonemeRule(phoneme_val="c")]),
        )
        self.morphism_2 = Morphism(
            val=PhonemeRuleSequence([PhonemeRule(phoneme_val="d")]),
            new_val=[self.phoneme_a],
            prefix=PhonemeRuleSequence([PhonemeRule(phoneme_val="a")]),
        )

    def test_morphism_apply_with_prefix_suffix(self):
        seq = [self.phoneme_a, self.phoneme_b, self.phoneme_c]

        morphism = Morphism(
            val=PhonemeRuleSequence([PhonemeRule(phoneme_val="b")]),
            new_val=[self.phoneme_d],
            prefix=PhonemeRuleSequence([PhonemeRule(phoneme_val="a")]),
            suffix=PhonemeRuleSequence([PhonemeRule(phoneme_val="c")]),
        )

        result = morphism.apply(seq)
        expected = [self.phoneme_a, self.phoneme_d, self.phoneme_c]
        self.assertEqual(result, expected)

    def test_morphism_apply_with_no_prefix_suffix(self):
        seq = [self.phoneme_a, self.phoneme_b, self.phoneme_c]

        morphism = Morphism(
            val=PhonemeRuleSequence([PhonemeRule(phoneme_val="b")]),
            new_val=[self.phoneme_d],
        )

        result = morphism.apply(seq)
        expected = [self.phoneme_a, self.phoneme_d, self.phoneme_c]
        self.assertEqual(result, expected)

    def test_morphism_store_apply_morphisms_with_prefix_suffix(self):
        seq = [self.phoneme_a, self.phoneme_b, self.phoneme_c]

        morphism_1 = Morphism(
            val=PhonemeRuleSequence([PhonemeRule(phoneme_val="b")]),
            new_val=[self.phoneme_d],
            prefix=PhonemeRuleSequence([PhonemeRule(phoneme_val="a")]),
            suffix=PhonemeRuleSequence([PhonemeRule(phoneme_val="c")]),
        )

        morphism_2 = Morphism(
            val=PhonemeRuleSequence([PhonemeRule(phoneme_val="d")]),
            new_val=[self.phoneme_a],
            prefix=PhonemeRuleSequence([PhonemeRule(phoneme_val="a")]),
        )

        morphism_store = MorphismStore(morphisms=[morphism_1, morphism_2])

        result = morphism_store.apply_morphisms(seq)
        expected = [self.phoneme_a, self.phoneme_a, self.phoneme_c]
        self.assertEqual(result, expected)


class TestSyllable(unittest.TestCase):
    def setUp(self):
        self.lang = latin

    def test_onset_nucleus_coda(self):
        # Test syllable with an onset, nucleus, and coda
        phonemes = [
            Phoneme("c", self.lang),
            Phoneme("a", self.lang),
            Phoneme("t", self.lang),
        ]
        syllable = Syllable(phonemes)
        self.assertEqual(syllable.onset, [Phoneme("c", self.lang)])
        self.assertEqual(syllable.nucleus, [Phoneme("a", self.lang)])
        self.assertEqual(syllable.coda, [Phoneme("t", self.lang)])

    def test_onset_nucleus(self):
        # Test syllable with an onset and nucleus
        phonemes = [Phoneme("b", self.lang), Phoneme("a", self.lang)]
        syllable = Syllable(phonemes)
        self.assertEqual(syllable.onset, [Phoneme("b", self.lang)])
        self.assertEqual(syllable.nucleus, [Phoneme("a", self.lang)])
        self.assertEqual(syllable.coda, [])

    def test_nucleus_coda(self):
        # Test syllable with a nucleus and coda
        phonemes = [Phoneme("i", self.lang), Phoneme("t", self.lang)]
        syllable = Syllable(phonemes)
        self.assertEqual(syllable.onset, [])
        self.assertEqual(syllable.nucleus, [Phoneme("i", self.lang)])
        self.assertEqual(syllable.coda, [Phoneme("t", self.lang)])

    def test_nucleus(self):
        # Test syllable with only a nucleus
        phonemes = [Phoneme("a", self.lang)]
        syllable = Syllable(phonemes)
        self.assertEqual(syllable.onset, [])
        self.assertEqual(syllable.nucleus, [Phoneme("a", self.lang)])
        self.assertEqual(syllable.coda, [])

    def test_no_vowels(self):
        # Test syllable with no vowels
        phonemes = [Phoneme("s", self.lang), Phoneme("t", self.lang)]
        syllable = Syllable(phonemes)
        self.assertEqual(
            syllable.onset, [Phoneme("s", self.lang), Phoneme("t", self.lang)]
        )
        self.assertEqual(syllable.nucleus, None)
        self.assertEqual(syllable.coda, None)


class TestPhonemeSyllabificationRuleStore(unittest.TestCase):
    def setUp(self):
        self.rule_store = PhonemeSyllabificationRuleStore(
            rules=[
                PhonemeRuleSequence(
                    [PhonemeRule(phoneme_val="c"), PhonemeRule(phoneme_val="ae")]
                ),
                PhonemeRuleSequence(
                    [PhonemeRule(phoneme_val="t"), PhonemeRule(phoneme_val="i")]
                ),
                PhonemeRuleSequence(
                    [
                        PhonemeRule(lambda p: p.is_stop),
                        PhonemeRule(lambda p: p.is_liquid),
                    ]
                ),
                PhonemeRuleSequence([PhonemeRule(lambda p: p.is_consonant)]),
            ]
        )
        self.lang = latin

    def test_apply_rules_no_match(self):
        phonemes = [
            Phoneme("a", self.lang),
        ]
        before, match = self.rule_store.apply_rules(phonemes)
        self.assertEqual(before, [])
        self.assertEqual(match, [])

    def test_apply_rules_no_match_no_cons(self):
        phonemes = []
        before, match = self.rule_store.apply_rules(phonemes)
        self.assertEqual(before, [])
        self.assertEqual(match, [])

    def test_apply_rules_single_match(self):
        phonemes = [
            Phoneme("s", self.lang),
            Phoneme("t", self.lang),
            Phoneme("i", self.lang),
        ]
        before, match = self.rule_store.apply_rules(phonemes)
        self.assertEqual(before, [Phoneme("s", self.lang)])
        self.assertEqual(match, [Phoneme("t", self.lang), Phoneme("i", self.lang)])

    def test_apply_rules_single_match_2(self):
        phonemes = [
            Phoneme("p", self.lang),
            Phoneme("r", self.lang),
        ]
        before, match = self.rule_store.apply_rules(phonemes)
        self.assertEqual(before, [])
        self.assertEqual(match, [Phoneme("p", self.lang), Phoneme("r", self.lang)])

    def test_apply_rules_multiple_matches(self):
        phonemes = [
            Phoneme("s", self.lang),
            Phoneme("c", self.lang),
            Phoneme("ae", self.lang),
            Phoneme("t", self.lang),
            Phoneme("i", self.lang),
        ]
        before, match = self.rule_store.apply_rules(phonemes)
        self.assertEqual(
            before,
            [
                Phoneme("s", self.lang),
                Phoneme("c", self.lang),
                Phoneme("ae", self.lang),
            ],
        )
        self.assertEqual(match, [Phoneme("t", self.lang), Phoneme("i", self.lang)])


if __name__ == "__main__":
    unittest.main()
