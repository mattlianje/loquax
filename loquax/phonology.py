from loquax.latin_grammar import (
    is_vowel,
    is_aspirate,
    is_diphtong,
    is_stop,
    is_liquid,
    latin_letter_groups,
)

"""
Syllabic decomposition rules used:
http://www.wheelockslatin.com/chapters/introduction/introduction_syllables.html

"""


class Phoneme:
    """
    Class to represent a single phoneme or sound unit in a word.
    """

    def __init__(self, val):
        """
        Initializes the Phoneme object with the given value and sets its attributes.
        """
        self.val = val
        self.is_diphtong = is_diphtong(val)
        self.is_stop = is_stop(val)
        self.is_liquid = is_liquid(val)
        self.is_aspirate = is_aspirate(val)
        self.is_vowel = is_vowel(val)
        self.prev = None
        self.next = None

        self.features = {
            "is_diphtong": self.is_diphtong,
            "is_stop": self.is_stop,
            "is_liquid": self.is_liquid,
            "is_aspirate": self.is_aspirate,
            "is_vowel": self.is_vowel,
        }


class Syllable:
    """
    Class to represent a syllable in a word.
    Syllable: List of Phonemes with an Onset, Nucleus and Coda.
    O-N-C (Nucleus is a vowel, Onset and Coda are optional groups of consonants).
    """

    def __init__(self, nucleus=None, onset=None, coda=None):
        if nucleus is None:
            self.nucleus = []
        if onset is None:
            self.onset = []
        if coda is None:
            self.coda = []


class Word:
    """
    Class to represent a word composed of syllables.
    """

    def __init__(self, syllables=None):
        if syllables is None:
            self.syllables = []


def get_ipa_for_token(token: str, equivalencies: dict) -> list[dict[str, list[str]]]:
    """
    This function takes in a word string and a dictionary of equivalencies
    and returns the IPA representation of the word.

    Args:
    word (str): the word to be converted to IPA
    equivalencies (dict): a dictionary of equivalencies mapping substrings of the word to their IPA representation
    longest_token (int): the length of the longest token in the equivalencies dictionary
    token_corpus (set): a set of all tokens in the equivalencies dictionary

    Returns:
    list: a list of IPA symbols or substrings representing the word

    Raises:
    Exception: if the current token is not in the equivalencies dictionary
    """

    def _get_ipa_helper(
            token: list[str],
            equivalencies: dict,
            longest_char: int,
            char_corpus: set,
            output: list[dict[str, list[str]]] = [],
    ) -> list:
        """
        Helper function used to accumulate the IPA representation of the word.

        Returns:
        A List of IPA symbols or substrings representing the word
        """
        if not token:
            return output

        current_char = token[0]
        remaining_word = token[1:]
        current_max_char_size = min(
            len(remaining_word) + len(current_char), longest_token
        )
        max_token_vs_current_delta = current_max_char_size - len(current_char)

        # Handles the final token of word
        max_extra_tokens = (
            max_token_vs_current_delta if max_token_vs_current_delta >= 0 else 0
        )

        if current_char in equivalencies:
            for i in reversed(range(max_extra_tokens + 1)):
                candidate_char = current_char + "".join(remaining_word[0:i])
                if candidate_char in char_corpus:
                    match = equivalencies[candidate_char]
                    if type(match) is list:
                        output.append({candidate_char: match})
                    else:
                        output.append(match)
                    return _get_ipa_helper(
                        remaining_word[i:],
                        equivalencies,
                        longest_token,
                        char_corpus,
                        output,
                    )
        else:
            raise Exception(f"Sorry, '{current_char}' is not in: {char_corpus}")

    longest_token = len(max(equivalencies.keys(), key=len)) if equivalencies else 0
    char_corpus = set([c for c in equivalencies.keys()])
    return _get_ipa_helper(
        [c for c in token], equivalencies, longest_token, char_corpus
    )


def split_token_into_phonemes(
        word: str, letter_groups: list[str] = latin_letter_groups
) -> list[Phoneme]:
    """
    Splits a token into phonetic elements (phonemes)

    Args:
    word (str): The word to be split into phonetic elements.
    letter_groups (List[str], optional): A list of strings representing the allowed letter groups.
    longest_group (int): an integer representing the length of the longest allowed letter group

    Returns:
    List[Phonemes]: A list of Phone objects representing the processed phonetic elements.
    """

    def _split_token(
            word: list[str],
            output: list[Phoneme],
            letter_groups: list[str],
            longest_group: int,
    ) -> list[Phoneme]:
        """
        _split_word is a helper called repeatedly until all letters in the word
        have been processed and added to the output list.

        Returns:
        List[Phoneme]: List of Phoneme objects representing the processed phonetic elements.
        """
        if not word:
            return output

        current_group = word[0]
        current_max_group_size = min(len(word[1:]) + len(current_group), longest_group)
        max_group_vs_current_delta = current_max_group_size - len(current_group)
        max_extra_letters = (
            max_group_vs_current_delta if max_group_vs_current_delta >= 0 else 0
        )

        for i in range(1, max_extra_letters + 1):
            candidate_group = current_group + "".join(word[1: i + 1])
            if candidate_group in letter_groups:
                return _split_token(
                    word[i + 1:],
                    output + [Phoneme(candidate_group)],
                    letter_groups,
                    longest_group,
                )

        return _split_token(
            word[1:], output + [Phoneme(current_group)], letter_groups, longest_group
        )

    longest_group = len(max(letter_groups, key=len)) if letter_groups else 0
    return _split_token([c for c in word], [], letter_groups, longest_group)
