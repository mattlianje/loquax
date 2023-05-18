from loquax.languages import Latin
from loquax.languages.latin_conf.rules import latin_syllable_morphisms
from loquax.abstractions import (
    MorphismStore,
    Syllable,
    PhonemeSyllabificationRuleStore,
    Morphism,
    Rule,
    RuleSequence,
    Phoneme,
)

import unittest


class TestMorphism(unittest.TestCase):
    def setUp(self):
        self.lang = Latin
        self.phoneme_a = Phoneme("a", self.lang)
        self.phoneme_b = Phoneme("b", self.lang)
        self.phoneme_c = Phoneme("c", self.lang)
        self.phoneme_d = Phoneme("d", self.lang)
        self.morphism_1 = Morphism[Phoneme](
            target=Rule[Phoneme](check_fn=lambda p: p == self.phoneme_b),
            transformation=lambda p: self.phoneme_d if p == self.phoneme_b else p,
            prefix=RuleSequence[Phoneme](
                [Rule[Phoneme](check_fn=lambda p: p == self.phoneme_a)]
            ),
            suffix=RuleSequence[Phoneme](
                [Rule[Phoneme](check_fn=lambda p: p == self.phoneme_c)]
            ),
        )
        self.morphism_2 = Morphism[Phoneme](
            target=Rule[Phoneme](check_fn=lambda p: p == self.phoneme_d),
            transformation=lambda p: self.phoneme_a if p == self.phoneme_d else p,
            prefix=RuleSequence[Phoneme](
                [Rule[Phoneme](check_fn=lambda p: p == self.phoneme_a)]
            ),
        )

    def test_morphism_apply_with_prefix_suffix(self):
        seq = [self.phoneme_a, self.phoneme_b, self.phoneme_c]

        morphism = Morphism[Phoneme](
            # Both of the targets are equivalent
            # target=Rule[Phoneme](check_fn=lambda p: p == self.phoneme_b),
            target=Rule[Phoneme](val=self.phoneme_b.val),
            transformation=Phoneme("d", self.lang),
            prefix=RuleSequence[Phoneme]([Rule[Phoneme](val="a")]),
            suffix=RuleSequence[Phoneme](
                [Rule[Phoneme](check_fn=lambda p: p == self.phoneme_c)]
            ),
        )

        result = morphism.apply(seq)
        expected = [self.phoneme_a, self.phoneme_d, self.phoneme_c]
        self.assertEqual(result, expected)

    def test_morphism_apply_with_no_prefix_suffix(self):
        seq = [self.phoneme_a, self.phoneme_b, self.phoneme_c]

        morphism = Morphism[Phoneme](
            target=Rule[Phoneme](check_fn=lambda p: p == self.phoneme_b),
            transformation=self.phoneme_d,
        )

        result = morphism.apply(seq)
        expected = [self.phoneme_a, self.phoneme_d, self.phoneme_c]
        self.assertEqual(result, expected)

    def test_morphism_store_apply_morphisms_with_prefix_suffix(self):
        seq = [self.phoneme_a, self.phoneme_b, self.phoneme_c]

        morphism_1 = Morphism(
            target=Rule[Phoneme](val="b"),
            transformation=self.phoneme_d,
            prefix=RuleSequence[Phoneme]([Rule[Phoneme](val="a")]),
            suffix=RuleSequence[Phoneme]([Rule[Phoneme](val="c")]),
        )

        morphism_2 = Morphism(
            target=Rule[Phoneme](val="d"),
            transformation=self.phoneme_a,
            prefix=RuleSequence[Phoneme]([Rule[Phoneme](val="a")]),
        )

        morphism_store = MorphismStore(morphisms=[morphism_1, morphism_2])

        result = morphism_store.apply_all(seq)
        expected = [self.phoneme_a, self.phoneme_a, self.phoneme_c]
        self.assertEqual(result, expected)


class TestSyllable(unittest.TestCase):
    def setUp(self):
        self.lang = Latin

    def test_onset_nucleus_coda(self):
        # Test syllable with an onset, nucleus, and coda
        phonemes = [
            Phoneme("c", self.lang),
            Phoneme("a", self.lang),
            Phoneme("t", self.lang),
        ]
        syllable = Syllable(phonemes, self.lang)
        self.assertEqual(syllable.onset, [Phoneme("c", self.lang)])
        self.assertEqual(syllable.nucleus, [Phoneme("a", self.lang)])
        self.assertEqual(syllable.coda, [Phoneme("t", self.lang)])

    def test_onset_nucleus(self):
        # Test syllable with an onset and nucleus
        phonemes = [Phoneme("b", self.lang), Phoneme("a", self.lang)]
        syllable = Syllable(phonemes, self.lang)
        self.assertEqual(syllable.onset, [Phoneme("b", self.lang)])
        self.assertEqual(syllable.nucleus, [Phoneme("a", self.lang)])
        self.assertEqual(syllable.coda, [])

    def test_nucleus_coda(self):
        # Test syllable with a nucleus and coda
        phonemes = [Phoneme("i", self.lang), Phoneme("t", self.lang)]
        syllable = Syllable(phonemes, self.lang)
        self.assertEqual(syllable.coda, [Phoneme("t", self.lang)])

    def test_nucleus(self):
        # Test syllable with only a nucleus
        phonemes = [Phoneme("a", self.lang)]
        syllable = Syllable(phonemes, self.lang)
        self.assertEqual(syllable.onset, [])
        self.assertEqual(syllable.nucleus, [Phoneme("a", self.lang)])
        self.assertEqual(syllable.coda, [])

    def test_no_vowels(self):
        # Test syllable with no vowels
        phonemes = [Phoneme("s", self.lang), Phoneme("t", self.lang)]
        syllable = Syllable(phonemes, self.lang)
        self.assertEqual(
            syllable.onset, [Phoneme("s", self.lang), Phoneme("t", self.lang)]
        )
        self.assertEqual(syllable.nucleus, None)
        self.assertEqual(syllable.coda, None)


class TestPhonemeSyllabificationRuleStore(unittest.TestCase):
    def setUp(self):
        self.rule_store = PhonemeSyllabificationRuleStore(
            rules=[
                RuleSequence[Phoneme](
                    [Rule[Phoneme](val="c"), Rule[Phoneme](val="ae")]
                ),
                RuleSequence[Phoneme]([Rule[Phoneme](val="t"), Rule[Phoneme](val="i")]),
                RuleSequence[Phoneme](
                    [
                        Rule[Phoneme](lambda p: p.is_stop),
                        Rule[Phoneme](lambda p: p.is_liquid),
                    ]
                ),
                RuleSequence[Phoneme]([Rule[Phoneme](lambda p: p.is_consonant)]),
            ]
        )
        self.lang = Latin

    def test_apply_rules_no_match(self):
        phonemes = [
            Phoneme("a", self.lang),
        ]
        before, match = self.rule_store.apply_all(phonemes)
        self.assertEqual(before, [])
        self.assertEqual(match, [])

    def test_apply_rules_no_match_no_cons(self):
        phonemes = []
        before, match = self.rule_store.apply_all(phonemes)
        self.assertEqual(before, [])
        self.assertEqual(match, [])

    def test_apply_rules_single_match(self):
        phonemes = [
            Phoneme("s", self.lang),
            Phoneme("t", self.lang),
            Phoneme("i", self.lang),
        ]
        before, match = self.rule_store.apply_all(phonemes)
        self.assertEqual(before, [Phoneme("s", self.lang)])
        self.assertEqual(match, [Phoneme("t", self.lang), Phoneme("i", self.lang)])

    def test_apply_rules_single_match_2(self):
        phonemes = [
            Phoneme("p", self.lang),
            Phoneme("r", self.lang),
        ]
        before, match = self.rule_store.apply_all(phonemes)
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
        before, match = self.rule_store.apply_all(phonemes)
        self.assertEqual(
            before,
            [
                Phoneme("s", self.lang),
                Phoneme("c", self.lang),
                Phoneme("ae", self.lang),
            ],
        )
        self.assertEqual(match, [Phoneme("t", self.lang), Phoneme("i", self.lang)])


class TestSyllableTransformationStore(unittest.TestCase):
    def setUp(self) -> None:
        self.lang = Latin

    def test_apply_all(self):
        def append_x_transformation(syllable: Syllable) -> Syllable:
            new_phonemes = syllable.phonemes + [Phoneme("x", syllable.lang)]
            return Syllable(new_phonemes, syllable.lang, syllable.is_long)

        def append_z_transformation(syllable: Syllable) -> Syllable:
            new_phonemes = syllable.phonemes + [Phoneme("z", syllable.lang)]
            return Syllable(new_phonemes, syllable.lang, syllable.is_long)

        syllables = [
            Syllable([Phoneme("b", self.lang)], self.lang),
            Syllable([Phoneme("a", self.lang)], self.lang),
            Syllable([Phoneme("c", self.lang)], self.lang),
            Syllable([Phoneme("a", self.lang)], self.lang),
        ]

        store = MorphismStore[Syllable](
            [
                Morphism[Syllable](
                    target=Rule[Syllable](val="a"),
                    prefix=RuleSequence[Syllable]([Rule[Syllable](val="b")]),
                    suffix=RuleSequence[Syllable]([Rule[Syllable](val="c")]),
                    transformation=append_x_transformation,
                ),
                Morphism[Syllable](
                    target=Rule[Syllable](val="a"),
                    prefix=RuleSequence[Syllable]([Rule[Syllable](val="c")]),
                    suffix=RuleSequence[Syllable]([]),
                    transformation=append_z_transformation,
                ),
            ]
        )

        new_syllables = store.apply_all(syllables)
        self.assertEqual(new_syllables[0].val, "b")
        self.assertEqual(new_syllables[1].val, "ax")
        self.assertEqual(new_syllables[2].val, "c")
        self.assertEqual(new_syllables[3].val, "az")


class TestSyllableMorphisms(unittest.TestCase):
    def setUp(self) -> None:
        self.lang = Latin

    def test_long_nature_morphism(self):
        s = Syllable([Phoneme("ā", lang=self.lang)], lang=self.lang)
        transformed_s = latin_syllable_morphisms.apply_all([s])[0]
        self.assertEqual(transformed_s.is_long, True)

    def test_long_position_morphism(self):
        s = Syllable([Phoneme("a", lang=self.lang)], lang=self.lang)
        s2 = Syllable(
            [
                Phoneme("c", lang=self.lang),
                Phoneme("c", lang=self.lang),
                Phoneme("a", self.lang),
            ],
            lang=self.lang,
        )
        transformed_s = latin_syllable_morphisms.apply_all([s, s2])[0]
        self.assertEqual(transformed_s.is_long, True)


if __name__ == "__main__":
    unittest.main()
