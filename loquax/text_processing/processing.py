from dataclasses import dataclass
from functools import reduce
from typing import List, Callable

from loquax.abstractions import Language, Syllable
from loquax.abstractions.syllabification import get_syllables_from_token


@dataclass
class Token:
    """
    Class to represent a token or sequence of symbols meaningful to a sentence
    """

    value: str
    language: Language

    @property
    def syllables(self) -> List[Syllable]:
        return get_syllables_from_token(self.value, self.language)

    def to_str(self, ipa: bool = False, scansion: bool = False) -> str:
        syllable_reprs: List[str] = list(
            map(lambda syl: syl.to_str(ipa), self.syllables)
        )
        syllable_repr_str: str = reduce(
            lambda acc, repr: acc + "." + repr, syllable_reprs
        )

        if scansion:
            center_scansion: Callable[
                [str, Syllable], str
            ] = lambda syllable_repr, syllable: syllable.scansion_str(ipa).center(
                len(syllable_repr)
            )

            scansion_reprs: List[str] = list(
                map(center_scansion, syllable_reprs, self.syllables)
            )
            scansion_repr_str: str = "\n" + reduce(
                lambda acc, repr: acc + " " + repr, scansion_reprs
            )

            return syllable_repr_str + scansion_repr_str

        return syllable_repr_str


@dataclass
class Document:
    """
    Class to represent a text or sequence of tokens.
    """

    val: str
    language: Language

    @property
    def tokens(self) -> List[Token]:
        return [
            Token(token, self.language)
            for token in self.language.tokenizer.tokenize(self.val)
        ]

    def to_str(self, ipa: bool = False, scansion: bool = False) -> str:
        join_syllables: Callable[[Token], str] = lambda token: ".".join(
            map(lambda syl: syl.to_str(ipa), token.syllables)
        )

        token_syllable_reprs: List[str] = list(map(join_syllables, self.tokens))
        token_syllable_repr_str: str = reduce(
            lambda acc, repr: acc + "    " + repr, token_syllable_reprs
        )

        if scansion:
            join_scansion: Callable[[Token], str] = lambda token: " ".join(
                map(
                    lambda syl: syl.scansion_str(ipa).center(len(syl.to_str(ipa))),
                    token.syllables,
                )
            )

            token_scansion_reprs: List[str] = list(map(join_scansion, self.tokens))
            token_scansion_repr_str: str = "\n" + reduce(
                lambda acc, repr: acc + "    " + repr, token_scansion_reprs
            )

            return token_syllable_repr_str + token_scansion_repr_str

        return token_syllable_repr_str
