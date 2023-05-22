from typing import List, Set

from loquax.abstractions import Language, Phoneme


def get_phonemes(token: str, lang: Language) -> List[Phoneme]:
    def _find_match(token: str, max_len: int, letter_groups: Set[str]) -> str:
        return (
            token[:max_len]
            if max_len > 0 and token[:max_len] in letter_groups
            else _find_match(token, max_len - 1, letter_groups)
            if max_len > 0
            else token[0]
        )

    def _split_token(token: str, symbol_groups: Set[str]) -> List[Phoneme]:
        longest = (
            len(max(lang.constants.symbol_groups, key=len))
            if lang.constants.symbol_groups
            else 0
        )
        return (
            []
            if token == ""
            else [
                Phoneme(_find_match(token, longest, symbol_groups), lang),
                *_split_token(
                    token[len(_find_match(token, longest, symbol_groups)) :],
                    symbol_groups,
                ),
            ]
        )

    return _split_token(token, lang.constants.symbol_groups)
