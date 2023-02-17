from loquax.commons import *
from loquax.latin_grammar import latin_letter_groups


def get_ipa_for_token(token: str, equivalencies: dict) -> list[dict[str, list[str]]]:
    """Return a list of dictionaries where each dictionary maps a token to its corresponding IPA symbols.

    Args:
        token (str): The word to be converted to IPA.
        equivalencies (dict): A dictionary of equivalencies mapping substrings of the word
                              to their IPA representation.

    Returns:
        list: A list of IPA symbols or substrings representing the word.
    """

    def _get_ipa_helper(
        _token: list[str],
        _equivalencies: dict,
        _max_phoneme_len: int,
        _char_corpus: set,
        _output: list[dict[str, list[str]]] = [],
    ) -> list:
        """Helper function used to accumulate the IPA representation of the word.

        Args:
            _token (list[str]): A list of tokens representing the word.
            _equivalencies (dict): A dictionary mapping tokens to their corresponding IPA symbols.
            _max_phoneme_len (int): The maximum allowed length of a single IPA symbol.
            _char_corpus (set): A set containing all the valid tokens.
            _output (list[dict[str, list[str]]]): A list of dictionaries,
                    where each dictionary maps a token to its corresponding IPA symbols.

        Returns:
            A List of IPA symbols or substrings representing the word.
        """
        match _token:
            case []:
                # If we have processed all the tokens, return the output
                return _output
            case t:
                # Otherwise, process the next token
                current_char = t[0]
                remaining_word = t[1:]
                current_max_char_size = min(
                    len(remaining_word) + len(current_char), _max_phoneme_len
                )
                max_token_vs_current_delta = current_max_char_size - len(current_char)
                max_extra_chars = (
                    max_token_vs_current_delta if max_token_vs_current_delta >= 0 else 0
                )
                match current_char in _equivalencies:
                    # Ensures current token has an IPA symbol
                    case True:
                        match max_extra_chars:
                            case 0:
                                # If there are no remaining characters to process, add token to output
                                k, v = current_char, _equivalencies[current_char]
                                new_output = _output + [{k: v}]
                                return _get_ipa_helper(
                                    remaining_word,
                                    _equivalencies,
                                    _max_phoneme_len,
                                    _char_corpus,
                                    new_output,
                                )
                            case x if x > 0:
                                # If there are remaining characters, form a candidate token
                                candidate_char = current_char + "".join(
                                    remaining_word[0:x]
                                )
                                match candidate_char in _char_corpus:
                                    case True:
                                        # If the new token is valid, add it to the output
                                        k, v = (
                                            candidate_char,
                                            _equivalencies[candidate_char],
                                        )
                                        new_output = _output + [{k: v}]
                                        return _get_ipa_helper(
                                            remaining_word[x:],
                                            _equivalencies,
                                            _max_phoneme_len,
                                            _char_corpus,
                                            new_output,
                                        )
                                    case _:
                                        # If the new token is not valid, add the current token to output
                                        k, v = (
                                            current_char,
                                            _equivalencies[current_char],
                                        )
                                        new_output = _output + [{k: v}]
                                        return _get_ipa_helper(
                                            remaining_word,
                                            _equivalencies,
                                            _max_phoneme_len,
                                            _char_corpus,
                                            new_output,
                                        )
                    case False:
                        raise Exception(
                            f"Sorry, '{current_char}' is not in: {_char_corpus}"
                        )

    longest = len(max(equivalencies.keys(), key=len)) if equivalencies else 0
    char_corpus = set([c for c in equivalencies.keys()])
    return _get_ipa_helper([c for c in token], equivalencies, longest, char_corpus)


def split_token_into_phonemes(
    word: str, letter_groups: list[str] = latin_letter_groups
) -> list[Phoneme]:
    """Splits a token into phonetic elements (phonemes)

    Args:
    word (str): The word to be split into phonetic elements.
    letter_groups (List[str], optional): A list of strings representing the allowed letter groups.

    Returns:
    List[Phonemes]: A list of Phoneme objects representing the processed phonetic elements.
    """

    def _split_token(
        _word: list[str],
        _output: list[Phoneme],
        _letter_groups: list[str],
        _longest_group: int,
    ) -> list[Phoneme]:
        """Helper function used to split a token into phonemes.

        Args:
            _word: A list of strings representing the token to be split.
            _output: A list of `Phoneme` objects representing the processed phonetic elements.
            _letter_groups: A list of valid letter groups.
            _longest_group: The length of the longest valid letter group.
        """

        def _split_token_helper(_word, _output, _letter_groups, _longest_group, i=1):
            """Helper function used to split a token into phonemes.

            Args:
                _word: A list of strings representing the token to be split.
                _output: A list of `Phoneme` objects representing the processed phonetic elements.
                _letter_groups: A list of valid letter groups.
                _longest_group: The length of the longest valid letter group.
                i: The index of the current character in the token.
            """
            # Process the first character in the word
            _current_group = _word[0]
            # If we have reached the end of the word, return the output
            match i > (_longest_group - len(_word[0])):
                case True:
                    return _split_token(
                        _word[1:],
                        _output + [Phoneme(_word[0])],
                        _letter_groups,
                        _longest_group,
                    )
                case False:
                    # Try to form a new letter group by appending more letters to the current group
                    _candidate_group = _current_group + "".join(_word[1 : i + 1])
                    # If the new group is valid, add it to the output and continue processing the remaining letters
                    match _candidate_group in _letter_groups:
                        case True:
                            return _split_token(
                                _word[i + 1 :],
                                _output + [Phoneme(_candidate_group)],
                                _letter_groups,
                                _longest_group,
                            )
                        case False:
                            # If the new group is not valid, increment i and try again
                            return _split_token_helper(
                                _word, _output, _letter_groups, _longest_group, i + 1
                            )

        match _word:
            case []:
                # If we have processed all the characters in the word, return the output
                return _output
            case _:
                return _split_token_helper(
                    _word, _output, _letter_groups, _longest_group, 1
                )

    longest = len(max(letter_groups, key=len)) if letter_groups else 0
    return _split_token([c for c in word], [], letter_groups, longest)
