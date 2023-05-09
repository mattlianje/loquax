from dataclasses import dataclass
from typing import Optional, List, Tuple, Callable

from loquax.constants import Constants


@dataclass
class PhonemeRule:
    """
    Represents a single rule that can be used to check if a given phoneme matches certain criteria.
    The rule can be defined using a check function, a specific phoneme value, or by being a wildcard.
    """

    check_fn: Optional[Callable[["Phoneme"], bool]] = None
    phoneme_val: Optional[str] = None
    wildcard: bool = False

    def matches(self, phoneme: "Phoneme") -> bool:
        if self.wildcard:
            return True

        match_predicate = (
            lambda p: p.val == self.phoneme_val
            if self.phoneme_val is not None
            else self.check_fn(p)
        )
        return match_predicate(phoneme)


@dataclass
class PhonemeRuleSequence:
    """
    Represents a sequence of phoneme rules that can be used to match against a sequence of phonemes.
    The sequence is matched when all individual rules in the sequence match their corresponding phonemes.
    """

    phoneme_rules: List[PhonemeRule]

    def matches(self, phonemes: List["Phoneme"]) -> bool:
        if len(phonemes) < len(self.phoneme_rules):
            return False

        return all(
            rule.matches(phoneme)
            for rule, phoneme in zip(
                self.phoneme_rules, phonemes[-len(self.phoneme_rules) :]
            )
        )


@dataclass
class PhonemeSyllabificationRuleStore:
    """
    Represents a store for phoneme rules that are used in syllabification.
    These rules help to determine how to split a sequence of phonemes into syllables.
    """

    rules: List[PhonemeRuleSequence]

    def apply_rules(
        self, phonemes: List["Phoneme"]
    ) -> Tuple[List["Phoneme"], List["Phoneme"]]:
        if not phonemes:
            return [], []

        matching_rule = next(
            (
                rule
                for rule in self.rules
                if len(rule.phoneme_rules) <= len(phonemes)
                and rule.matches(phonemes[-len(rule.phoneme_rules) :])
            ),
            None,
        )

        if matching_rule is None:
            return [], []

        rule_length = len(matching_rule.phoneme_rules)
        return phonemes[:-rule_length], phonemes[-rule_length:]


@dataclass
class Morphism:
    """
    Represents a morphism, which is a transformation applied to phonemes in a sequence based on
    specific criteria, such as the surrounding phonemes or the presence of a certain pattern.
    A morphism is defined by a value to match, a new value to replace the matched value, and optional
    prefix and suffix rules to further specify the criteria for applying the morphism.
    """

    val: PhonemeRuleSequence
    new_val: List["Phoneme"]
    prefix: PhonemeRuleSequence = PhonemeRuleSequence([])
    suffix: PhonemeRuleSequence = PhonemeRuleSequence([])

    def apply(self, seq: List["Phoneme"]) -> List["Phoneme"]:
        def matches_prefix_suffix(morph, subseq, index):
            return (
                morph.prefix.matches(
                    subseq[max(0, index - len(morph.prefix.phoneme_rules)) : index]
                )
                and morph.val.matches(
                    subseq[index : index + len(morph.val.phoneme_rules)]
                )
                and morph.suffix.matches(
                    subseq[
                        index
                        + len(morph.val.phoneme_rules) : index
                        + len(morph.val.phoneme_rules)
                        + len(morph.suffix.phoneme_rules)
                    ]
                )
            )

        def apply_morphism_helper(morph, subseq, index=0):
            if index > len(subseq):
                return subseq
            match matches_prefix_suffix(morph, subseq, index):
                case True:
                    new_seq = (
                        subseq[:index]
                        + morph.new_val
                        + subseq[index + len(morph.val.phoneme_rules) :]
                    )
                    return apply_morphism_helper(
                        morph, new_seq, index + len(morph.new_val)
                    )
                case _:
                    return apply_morphism_helper(morph, subseq, index + 1)

        return apply_morphism_helper(self, seq)


@dataclass
class MorphismStore:
    """
    Represents a store for morphisms that can be applied to a sequence of phonemes.
    The store holds a list of morphisms and provides a method to apply all morphisms to a given sequence.
    """

    morphisms: List[Morphism]

    def apply_morphisms(self, seq: List["Phoneme"]) -> List["Phoneme"]:
        def apply_morphisms_helper(
            morphisms: List[Morphism], seq: List["Phoneme"]
        ) -> List["Phoneme"]:
            match not morphisms:
                case True:
                    return seq
                case _:
                    current_morphism = morphisms[0]
                    new_seq = current_morphism.apply(seq)
                    return apply_morphisms_helper(morphisms[1:], new_seq)

        return apply_morphisms_helper(self.morphisms, seq)


@dataclass
class Language:
    """
    Represents a language, containing information such as language name, constants, syllabification rules,
    morphisms, and an optional ISO 639 code. The Language class provides an organized way to store
    language-specific data for processing phoneme sequences.
    """

    language_name: str
    constants: Constants
    syllabification_rules: PhonemeSyllabificationRuleStore
    morphisms: MorphismStore
    # ISO 639 code if applicable
    iso_639_code: str


@dataclass
class Phoneme:
    """
    Class to represent a single phoneme or sound unit in a word.
    """

    val: str
    lang: Language

    def __post_init__(self):
        if self.val not in self.lang.constants.equivalencies:
            raise ValueError(
                f"The symbol '{self.val}' is not a valid phoneme in the language: '{self.lang.language_name}'."
            )

    @property
    def ipa(self) -> list[str]:
        return self.lang.constants.equivalencies[self.val]

    @property
    def is_diphtong(self) -> bool:
        return self.val in self.lang.constants.diphtongs

    @property
    def is_stop(self) -> bool:
        return self.val in self.lang.constants.stop_letters

    @property
    def is_liquid(self) -> bool:
        return self.val in self.lang.constants.liquid_letters

    @property
    def is_aspirate(self) -> bool:
        return self.val in self.lang.constants.aspirates

    @property
    def is_vowel(self) -> bool:
        return self.val in self.lang.constants.vowels

    @property
    def is_consonant(self) -> bool:
        return self.val in self.lang.constants.consonants

    def __repr__(self) -> str:
        return self.val


@dataclass
class Syllable:
    """
    Class to represent a syllable in a word.
    Syllable: List of Phonemes with an Onset, Nucleus, and Coda.
    O-N-C (Nucleus is a vowel, Onset and Coda are optional groups of consonants).
    """

    phonemes: List[Phoneme]

    def _find_first_vowel_index(self) -> Optional[int]:
        return next((i for i, p in enumerate(self.phonemes) if p.is_vowel), None)

    @property
    def nucleus(self) -> Optional[List[Phoneme]]:
        first_vowel_index = self._find_first_vowel_index()
        if first_vowel_index is not None:
            return [self.phonemes[first_vowel_index]]
        return None

    @property
    def onset(self) -> Optional[List[Phoneme]]:
        first_vowel_index = self._find_first_vowel_index()
        if first_vowel_index is not None:
            return self.phonemes[:first_vowel_index]
        return self.phonemes

    @property
    def coda(self) -> Optional[List[Phoneme]]:
        first_vowel_index = self._find_first_vowel_index()
        if first_vowel_index is not None:
            return self.phonemes[first_vowel_index + 1 :]
        return None

    def __repr__(self):
        return "".join([phoneme.val for phoneme in self.phonemes])


@dataclass
class Token:
    """
    Class to represent a token or sequence of symbols meaningful to a sentence
    """

    token: List[Syllable]
