from typing import List, Set

from loquax.entities import Language, Phoneme


def get_phonemes(word: str, lang: Language) -> List[Phoneme]:
    def find_match(word: str, max_len: int, letter_groups: Set[str]) -> str:
        return (
            word[:max_len]
            if max_len > 0 and word[:max_len] in letter_groups
            else find_match(word, max_len - 1, letter_groups)
            if max_len > 0
            else word[0]
        )

    def split_token(word: str, symbol_groups: Set[str]) -> List[Phoneme]:
        longest = (
            len(max(lang.constants.symbol_groups, key=len))
            if lang.constants.symbol_groups
            else 0
        )
        return (
            []
            if word == ""
            else [
                Phoneme(find_match(word, longest, symbol_groups), lang),
                *split_token(
                    word[len(find_match(word, longest, symbol_groups)) :], symbol_groups
                ),
            ]
        )

    return split_token(word, lang.constants.symbol_groups)
