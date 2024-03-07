import pytest

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


@pytest.fixture
def lang():
    return Latin


@pytest.fixture
def phonemes():
    lang = Latin
    return {
        "a": Phoneme("a", lang),
        "b": Phoneme("b", lang),
        "c": Phoneme("c", lang),
        "d": Phoneme("d", lang),
    }


@pytest.fixture
def morphisms(phonemes):
    morphism_1 = Morphism[Phoneme](
        target=Rule[Phoneme](check_fn=lambda p: p == phonemes["b"]),
        transformation=lambda p: phonemes["d"] if p == phonemes["b"] else p,
        prefix=RuleSequence[Phoneme](
            [Rule[Phoneme](check_fn=lambda p: p == phonemes["a"])]
        ),
        suffix=RuleSequence[Phoneme](
            [Rule[Phoneme](check_fn=lambda p: p == phonemes["c"])]
        ),
    )
    morphism_2 = Morphism[Phoneme](
        target=Rule[Phoneme](check_fn=lambda p: p == phonemes["d"]),
        transformation=lambda p: phonemes["a"] if p == phonemes["d"] else p,
        prefix=RuleSequence[Phoneme](
            [Rule[Phoneme](check_fn=lambda p: p == phonemes["a"])]
        ),
    )
    return morphism_1, morphism_2


@pytest.fixture
def rule_store():
    return PhonemeSyllabificationRuleStore(
        rules=[
            RuleSequence[Phoneme]([Rule[Phoneme](val="c"), Rule[Phoneme](val="ae")]),
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


@pytest.mark.usefixtures("lang", "phonemes", "morphisms")
@pytest.mark.morphism
class TestMorphism:
    def test_apply_with_prefix_suffix(self, phonemes):
        phoneme_a, phoneme_b, phoneme_c = phonemes["a"], phonemes["b"], phonemes["c"]
        seq = [phoneme_a, phoneme_b, phoneme_c]

        morphism = Morphism[Phoneme](
            target=Rule[Phoneme](val=phoneme_b.val),
            transformation=Phoneme("d", phoneme_b.lang),
            prefix=RuleSequence[Phoneme]([Rule[Phoneme](val="a")]),
            suffix=RuleSequence[Phoneme](
                [Rule[Phoneme](check_fn=lambda p: p == phoneme_c)]
            ),
        )

        result = morphism.apply(seq)
        expected = [phoneme_a, Phoneme("d", phoneme_b.lang), phoneme_c]
        assert result == expected

    def test_apply_with_no_prefix_suffix(self, phonemes):
        seq = [phonemes["a"], phonemes["b"], phonemes["c"]]

        morphism = Morphism[Phoneme](
            target=Rule[Phoneme](check_fn=lambda p: p == phonemes["b"]),
            transformation=phonemes["d"],
        )

        result = morphism.apply(seq)
        expected = [phonemes["a"], phonemes["d"], phonemes["c"]]
        assert result == expected

    def test_store_apply_morphisms_with_prefix_suffix(self, phonemes, morphisms):
        seq = [phonemes["a"], phonemes["b"], phonemes["c"]]
        morphism_1, morphism_2 = morphisms

        morphism_store = MorphismStore(morphisms=[morphism_1, morphism_2])
        result = morphism_store.apply_all(seq)
        expected = [phonemes["a"], phonemes["a"], phonemes["c"]]
        assert result == expected


'''
syllable logic must ...
'''
@pytest.mark.usefixtures("lang", "rule_store")
@pytest.mark.syllabification
class TestSyllabification:
    '''
    ... test syllables
    '''
    def test_onset_nucleus_coda(self, lang):
        phonemes = [
            Phoneme("c", lang),
            Phoneme("a", lang),
            Phoneme("t", lang),
        ]
        syllable = Syllable(phonemes, lang)
        assert syllable.onset == [Phoneme("c", lang)]
        assert syllable.nucleus == [Phoneme("a", lang)]
        assert syllable.coda == [Phoneme("t", lang)]

    def test_onset_nucleus(self, lang):
        phonemes = [Phoneme("b", lang), Phoneme("a", lang)]
        syllable = Syllable(phonemes, lang)
        assert syllable.onset == [Phoneme("b", lang)]
        assert syllable.nucleus == [Phoneme("a", lang)]
        assert syllable.coda == []

    def test_nucleus_coda(self, lang):
        phonemes = [Phoneme("i", lang), Phoneme("t", lang)]
        syllable = Syllable(phonemes, lang)
        assert syllable.onset == []
        assert syllable.nucleus == [Phoneme("i", lang)]
        assert syllable.coda == [Phoneme("t", lang)]

    def test_nucleus(self, lang):
        phonemes = [Phoneme("a", lang)]
        syllable = Syllable(phonemes, lang)
        assert syllable.onset == []
        assert syllable.nucleus == [Phoneme("a", lang)]
        assert syllable.coda == []

    def test_no_vowels(self, lang):
        phonemes = [Phoneme("s", lang), Phoneme("t", lang)]
        syllable = Syllable(phonemes, lang)
        assert syllable.onset == [Phoneme("s", lang), Phoneme("t", lang)]
        assert syllable.nucleus == None
        assert syllable.coda == None

    '''
    ... test syllable_rule_store
    '''
    def test_apply_rules_no_match(self, rule_store, lang):
        phonemes = [Phoneme("a", lang)]
        before, match = rule_store.apply_all(phonemes)
        assert before == []
        assert match == []

    def test_apply_rules_no_match_no_cons(self, rule_store, lang):
        phonemes = []
        before, match = rule_store.apply_all(phonemes)
        assert before == []
        assert match == []

    def test_apply_rules_single_match(self, rule_store, lang):
        phonemes = [Phoneme("s", lang), Phoneme("t", lang), Phoneme("i", lang)]
        before, match = rule_store.apply_all(phonemes)
        assert before == [Phoneme("s", lang)]
        assert match == [Phoneme("t", lang), Phoneme("i", lang)]

    def test_apply_rules_single_match_2(self, rule_store, lang):
        phonemes = [Phoneme("p", lang), Phoneme("r", lang)]
        before, match = rule_store.apply_all(phonemes)
        assert before == []
        assert match == [Phoneme("p", lang), Phoneme("r", lang)]

    def test_apply_rules_multiple_matches(self, rule_store, lang):
        phonemes = [
            Phoneme("s", lang),
            Phoneme("c", lang),
            Phoneme("ae", lang),
            Phoneme("t", lang),
            Phoneme("i", lang),
        ]
        before, match = rule_store.apply_all(phonemes)
        assert before == [
            Phoneme("s", lang),
            Phoneme("c", lang),
            Phoneme("ae", lang),
        ]
        assert match == [Phoneme("t", lang), Phoneme("i", lang)]

    '''
    ... test syllable_transformation_store
    '''
    def test_syllable_transformation_store(self, lang):
        def append_x_transformation(syllable: Syllable) -> Syllable:
            new_phonemes = syllable.phonemes + [Phoneme("x", syllable.lang)]
            return Syllable(new_phonemes, syllable.lang, syllable.is_long)

        def append_z_transformation(syllable: Syllable) -> Syllable:
            new_phonemes = syllable.phonemes + [Phoneme("z", syllable.lang)]
            return Syllable(new_phonemes, syllable.lang, syllable.is_long)

        syllables = [
            Syllable([Phoneme("b", lang)], lang),
            Syllable([Phoneme("a", lang)], lang),
            Syllable([Phoneme("c", lang)], lang),
            Syllable([Phoneme("a", lang)], lang),
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
        assert new_syllables[0].val == "b"
        assert new_syllables[1].val == "ax"
        assert new_syllables[2].val == "c"
        assert new_syllables[3].val == "az"

    '''
    ... test syllable quantities
    '''
    def test_long_nature_morphism(self, lang):
        s = Syllable([Phoneme("ā", lang=lang)], lang=lang)
        transformed_s = latin_syllable_morphisms.apply_all([s])[0]
        assert transformed_s.is_long == True

    def test_long_position_morphism(selfo, lang):
        s = Syllable([Phoneme("a", lang=lang)], lang=lang)
        s2 = Syllable(
            [
                Phoneme("c", lang=lang),
                Phoneme("c", lang=lang),
                Phoneme("a", lang),
            ],
            lang=lang,
        )
        transformed_s = latin_syllable_morphisms.apply_all([s, s2])[0]
        assert transformed_s.is_long == True
