from typing import List

from loquax.abstractions import Language, Syllable, Phoneme
from loquax.abstractions.phonology import get_phonemes


def get_syllables_from_phonemes(token: List[Phoneme], lang: Language) -> List[Syllable]:
    # Helper function to create a Syllable based on current, previous, and next vowel indices
    def _create_syllable(
        tkn: List[Phoneme],
        current_index: int,
        prev_vowel_index: int,
        next_vowel_index: int,
    ):
        # Define the consonant ranges between the current and adjacent vowels (if they exist)
        prev_consonant_range = tkn[prev_vowel_index + 1 : vowel_indices[current_index]]
        next_consonant_range = tkn[vowel_indices[current_index] + 1 : next_vowel_index]

        # Apply syllabification rules to the consonant ranges
        rules = lang.syllabification_rules
        onset = rules.apply_all(prev_consonant_range)[1]
        coda = rules.apply_all(next_consonant_range)[0]

        # Create a Syllable based on the current index and syllabification rules
        match current_index:
            case 0:
                return Syllable(tkn[: vowel_indices[current_index] + 1] + coda, lang)
            case index if index == len(vowel_indices) - 1:
                return Syllable(onset + tkn[vowel_indices[current_index] :], lang)
            case _:
                return Syllable(
                    onset + [tkn[vowel_indices[current_index]]] + coda, lang
                )

    # Get the indices of all vowels in the token
    vowel_indices = [i for i, phoneme in enumerate(token) if phoneme.is_vowel]

    # Create syllables based on the number of vowels and their positions
    match len(vowel_indices):
        case num_vowels if num_vowels <= 1:
            return lang.syllable_morphisms.apply_all([Syllable(token, lang)])
        case _:
            syllables: List[Syllable] = [
                _create_syllable(
                    token,
                    index,
                    vowel_indices[index - 1] if index > 0 else 0,
                    vowel_indices[index + 1]
                    if index < len(vowel_indices) - 1
                    else len(token),
                )
                for index in range(len(vowel_indices))
            ]

            return lang.syllable_morphisms.apply_all(syllables)


def get_syllables_from_token(token: str, lang: Language) -> List[Syllable]:
    return lang.syllable_morphisms.apply_all(
        get_syllables_from_phonemes(get_phonemes(token, lang), lang)
    )
