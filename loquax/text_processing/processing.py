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

    def to_string(self, ipa: bool = False, scansion: bool = False) -> str:
        syllable_reprs: List[str] = list(
            map(lambda syl: syl.to_string(ipa), self.syllables)
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

    def __repr__(self):
        return self.to_string(ipa=True)


@dataclass
class Document:
    """
    Class to represent a text or sequence of tokens.
    """

    val: str
    language: Language
    max_line_width: int = 90  # change this as per your requirement

    @property
    def tokens(self) -> List[Token]:
        return [
            Token(token, self.language)
            for token in self.language.tokenizer.tokenize(self.val)
        ]

    def to_string(self, ipa: bool = False, scansion: bool = False) -> str:
        def _create_lines(tokens, func, current_line="", lines=[]):
            if not tokens:
                return lines + [current_line]
            token_str = func(tokens[0])
            if len(current_line) + len(token_str) + 4 > self.max_line_width:
                return _create_lines(
                    tokens[1:], func, token_str, lines + [current_line]
                )
            else:
                new_line = (
                    current_line + "    " + token_str if current_line else token_str
                )
                return _create_lines(tokens[1:], func, new_line, lines)

        join_syllables: Callable[[Token], str] = lambda token: ".".join(
            map(lambda syl: syl.to_string(ipa), token.syllables)
        )
        syllable_lines = _create_lines(self.tokens, join_syllables)
        if scansion:
            join_scansion: Callable[[Token], str] = lambda token: " ".join(
                map(
                    lambda syl: syl.scansion_str(ipa).center(len(syl.to_string(ipa))),
                    token.syllables,
                )
            )
            scansion_lines = _create_lines(self.tokens, join_scansion)

            # join syllable_lines and scansion_lines alternatively
            combined_lines = [
                val for pair in zip(syllable_lines, scansion_lines) for val in pair
            ]
            return "\n".join(combined_lines)

        return "\n".join(syllable_lines)

    def __repr__(self):
        return self.to_string(ipa=True, scansion=True)
