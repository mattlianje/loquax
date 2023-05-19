from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import reduce
from typing import Optional, List, Callable, Tuple, TypeVar, Generic, Union
from loquax.abstractions.constants import Constants

# This can be any type that the Rule is supposed to operate on, e.g., Syllable or Phoneme
T = TypeVar("T")


class Tokenizer(ABC):
    """
    Abstract base class for a tokenizer.
    """

    @abstractmethod
    def tokenize(self, text: str) -> List[str]:
        pass


@dataclass
class Rule(Generic[T]):
    """
    Represents a single rule that can be used to check if a given unit (e.g. syllable, phoneme)
    matches certain criteria. The rule can be defined using a check function, a specific value,
    or by being a wildcard.
    """

    check_fn: Optional[Callable[[T], bool]] = None
    val: Optional[str] = None
    wildcard: bool = False

    def matches(self, unit: T) -> bool:
        if self.wildcard:
            return True

        match_predicate = (
            lambda s: s.__repr__() == self.val
            if self.val is not None
            else self.check_fn(s)
        )
        return match_predicate(unit)


@dataclass
class RuleSequence(Generic[T]):
    """
    Represents a sequence of rules that can be used to match against a sequence of units (e.g. syllables, phonemes).
    The sequence is matched when all individual rules in the sequence match their corresponding units.
    """

    rules: List[Rule[T]]

    def matches(self, units: List[T]) -> bool:
        if len(units) < len(self.rules):
            return False

        return all(
            rule.matches(unit)
            for rule, unit in zip(self.rules, units[-len(self.rules):])
        )


@dataclass
class Morphism(Generic[T]):
    """
    Represents a transformation applied to units in a sequence based on
    specific criteria, such as the surrounding units or the presence of a certain pattern.
    """

    target: Rule[T]
    transformation: Union[Callable[[T], T], T]
    prefix: Optional[RuleSequence[T]] = None
    suffix: Optional[RuleSequence[T]] = None

    def matches(self, units: List[T], index: int) -> bool:
        return (
                (
                    self.prefix.matches(
                        units[max(0, index - len(self.prefix.rules)): index]
                    )
                    if self.prefix
                    else True
                )
                and self.target.matches(units[index])
                and (
                    self.suffix.matches(
                        units[index + 1: index + 1 + len(self.suffix.rules)]
                    )
                    if self.suffix
                    else True
                )
        )

    def apply(self, units: List[T]) -> List[T]:
        return [
            (
                self.transformation(unit)
                if callable(self.transformation)
                else self.transformation
            )
            if self.matches(units, i)
            else unit
            for i, unit in enumerate(units)
        ]


@dataclass
class MorphismStore(Generic[T]):
    """
    Represents a store for morphisms that can be applied to a sequence of units.
    The store holds a list of morphisms and provides a method to apply all morphisms to a given sequence.
    """

    morphisms: List[Morphism[T]]

    def apply_all(self, units: List[T]) -> List[T]:
        return reduce(lambda units, morph: morph.apply(units), self.morphisms, units)


@dataclass
class PhonemeSyllabificationRuleStore:
    """
    Represents a store for phoneme rules that are used in syllabification.
    These rules help to determine how to split a sequence of phonemes into syllables.
    """

    rules: List[RuleSequence["Phoneme"]]

    def apply_all(
            self, phonemes: List["Phoneme"]
    ) -> Tuple[List["Phoneme"], List["Phoneme"]]:
        if not phonemes:
            return [], []

        matching_rule = next(
            (
                rule
                for rule in self.rules
                if len(rule.rules) <= len(phonemes)
                   and rule.matches(phonemes[-len(rule.rules):])
            ),
            None,
        )

        if matching_rule is None:
            return [], []

        rule_length = len(matching_rule.rules)
        return phonemes[:-rule_length], phonemes[-rule_length:]


@dataclass
class Language:
    """
    Represents a language, containing information such as language name, constants, syllabification rules,
    morphisms, and an optional ISO 639 code. The Language class provides an organized way to store
    language-specific data for processing phoneme sequences.
    """

    language_name: str
    iso_639_code: str
    constants: Constants
    syllabification_rules: PhonemeSyllabificationRuleStore
    syllable_morphisms: MorphismStore["Syllable"]
    phoneme_morphisms: MorphismStore["Phoneme"]
    tokenizer: Tokenizer


@dataclass
class Phoneme:
    """
    Class to represent a single phoneme or sound unit in a word.
    """

    val: str
    lang: Language
    ipa: Optional[str] = None

    def __post_init__(self):
        if self.val not in self.lang.constants.equivalencies:
            raise ValueError(
                f"The symbol '{self.val}' is not a valid phoneme in the language: '{self.lang.language_name}'."
            )
        # If ipa is not set, use the first IPA equivalent from equivalencies
        if self.ipa is None:
            self.ipa = self.lang.constants.equivalencies[self.val][0]
        elif self.ipa not in self.lang.constants.equivalencies[self.val]:
            raise ValueError(
                f"""The IPA symbol '{self.ipa}' is not a valid equivalent for phoneme '{self.val}' 
                in the language: '{self.lang.language_name}'."""
            )

    @property
    def is_diphthong(self) -> bool:
        return self.val in self.lang.constants.diphthongs

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

    def set_ipa(self, new_ipa: str) -> "Phoneme":
        # Ensure the new IPA is a valid equivalent for this phoneme
        if new_ipa not in self.lang.constants.equivalencies[self.val]:
            raise ValueError(
                f"""The IPA symbol '{new_ipa}' is not a valid equivalent for phoneme '{self.val}' 
                in the language: '{self.lang.language_name}'."""
            )
        # Return a new Phoneme with the same val and lang, but with the new IPA
        return Phoneme(val=self.val, lang=self.lang, ipa=new_ipa)

    def to_str(self, ipa: bool = False):
        if ipa:
            return self.val
        else:
            return self.ipa

    def __repr__(self) -> str:
        return self.val

    def __str__(self) -> str:
        return self.__repr__()


@dataclass
class Syllable:
    """
    Class to represent a syllable in a word.
    Syllable: List of Phonemes with an Onset, Nucleus, and Coda.
    O-N-C (Nucleus is a vowel, Onset and Coda are optional groups of consonants).
    """

    phonemes: List[Phoneme]
    lang: Language
    is_long: bool = False

    def __post_init__(self):
        num_vowels = len([p for p in self.phonemes if p.is_vowel])
        if num_vowels > 1:
            raise ValueError(
                f"Invalid syllable: {self.phonemes} contains more than one vowel phoneme."
            )

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
            return self.phonemes[first_vowel_index + 1:]
        return None

    @property
    def val(self) -> str:
        return "".join([phoneme.val for phoneme in self.phonemes])

    def _find_first_vowel_index(self) -> Optional[int]:
        return next((i for i, p in enumerate(self.phonemes) if p.is_vowel), None)

    def scansion_str(self, ipa: bool = False) -> str:
        symbol = "U" if not self.is_long else "—"
        return symbol.center(len(self.__repr__() if ipa else self.__str__()))

    def to_str(self, ipa: bool = False) -> str:
        return "".join(
            [phoneme.ipa if ipa else phoneme.val for phoneme in self.phonemes]
        )

    def __repr__(self):
        return "".join([phoneme.val for phoneme in self.phonemes])

    def __str__(self):
        return self.__repr__()
