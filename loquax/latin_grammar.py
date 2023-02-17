"""
Syllabic decomposition rules used:
http://www.wheelockslatin.com/chapters/introduction/introduction_syllables.html

IPA mappings used:
https://en.wikipedia.org/wiki/Help:IPA/Latin
"""


latin_vowel_equivalencies = {
    "a": ["a"],
    "ā": ["aː"],
    "e": ["ɛ"],
    "ē": ["eː"],
    "i": ["ɪ"],
    "ī": ["iː"],
    "o": ["ɔ"],
    "ō": ["oː"],
    "u": ["ʊ"],
    "ū": ["uː"],
    "y": ["ʏ"],
    "ȳ": ["yː"],
    "ae": ["ae̯"],
    "oe": ["oe̯"],
    "au": ["au̯"],
    "eu": ["eu̯"],
    "ui": ["ui̯"],
}

latin_consonant_equivalencies = {
    "b": ["b"],
    "d": ["d"],
    "f": ["f"],
    "ɡ": ["g", "ŋ"],
    "h": ["h"],
    "j": ["j"],
    "c": ["k"],
    "ch": ["kʰ"],
    "qu": ["kʷ", "kᶣ"],
    "l": ["l", "ɫ"],
    "m": ["m"],
    "n": ["n", "ŋ"],
    "gn": ["ɲ"],
    "p": ["p"],
    "ph": ["pʰ"],
    "r": ["r"],
    "s": ["s"],
    "t": ["t"],
    "th": ["tʰ"],
    "z": ["z"],
    "q": ["k"],
    "g": ["g"],
}


latin_equivalencies = latin_vowel_equivalencies | latin_consonant_equivalencies


latin_aspirates = {"qu", "ch", "ph", "th", "kʷ", "kʰ", "pʰ", "tʰ"}
latin_diphtongs = {
    "ae",
    "au",
    "ei",
    "eu",
    "oe",
    "ui",
    "ae̯",
    "oe̯",
    "au̯",
    "eu̯",
    "ui̯",
}
latin_liquid_letters = {"l", "r"}
latin_stop_letters = {"p", "b", "t", "d", "c", "g"}


def get_distinct_elements(d: dict) -> set:
    """
    Get the set of distinct elements from the keys and values of a dictionary.
    If a value is a list, its elements will be included in the output set.

    :param d (dict): the input dictionary
    :return: the set of distinct elements
    """
    return set(
        [k for k in d.keys()]
        + (
            [i for v in d.values() if isinstance(v, list) for i in v]
            + [v for v in d.values() if not isinstance(v, list)]
        )
    )


latin_vowels: set = set(get_distinct_elements(latin_vowel_equivalencies))
latin_consonants = set(get_distinct_elements(latin_consonant_equivalencies))


def is_diphtong(s, diphtongs=latin_diphtongs):
    return s in diphtongs


def is_stop(s, stop_letters=latin_stop_letters):
    return s in stop_letters


def is_liquid(s, liquid_letters=latin_liquid_letters):
    return s in liquid_letters


def is_aspirate(s, aspirates=latin_aspirates):
    return s in aspirates


def is_vowel(s, vowels=latin_vowels):
    return s in vowels


latin_letter_groups = set(
    filter(
        lambda x: len(x) > 1,
        set(
            latin_aspirates.union(
                latin_diphtongs, latin_liquid_letters, latin_stop_letters, latin_vowels
            )
        ),
    )
)
