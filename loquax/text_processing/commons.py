import unicodedata

from loquax.abstractions import Phoneme


def has_macron(phoneme: Phoneme) -> bool:
    """Return True if any character in the phoneme's value has a macron accent."""
    return any("macron" in unicodedata.name(c, "").lower() for c in phoneme.val)


def has_trema(phoneme: Phoneme) -> bool:
    """Return True if any character in the phoneme's value has a trema (diaeresis) accent."""
    return any("diaeresis" in unicodedata.name(c, "").lower() for c in phoneme.val)


def has_acute(phoneme: Phoneme) -> bool:
    """Return True if any character in the phoneme's value has an acute accent."""
    return any("acute" in unicodedata.name(c, "").lower() for c in phoneme.val)


def has_grave(phoneme: Phoneme) -> bool:
    """Return True if any character in the phoneme's value has a grave accent."""
    return any("grave" in unicodedata.name(c, "").lower() for c in phoneme.val)


def has_tilde(phoneme: Phoneme) -> bool:
    """Return True if any character in the phoneme's value has a tilde accent."""
    return any("tilde" in unicodedata.name(c, "").lower() for c in phoneme.val)
