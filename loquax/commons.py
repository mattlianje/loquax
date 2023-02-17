from loquax.latin_grammar import is_vowel, is_aspirate, is_diphtong, is_stop, is_liquid


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


class Token:
    """
    Class to represent a token composed of syllables.
    """

    def __init__(self, syllables=None):
        if syllables is None:
            self.syllables = []
