from loquax.abstractions.constants import Constants
from loquax.languages.latin_conf.constants import *
from loquax.languages.latin_conf.rules import (
    latin_syllabification_rules,
    latin_syllable_morphisms,
    latin_phoneme_morphisms,
)
from loquax.abstractions import Language
from loquax.languages.latin_conf.tokenizer import LatinTokenizer

Latin = Language(
    language_name="Classical Latin",
    iso_639_code="lat",
    constants=Constants(
        vowel_equivalencies=latin_vowel_equivalencies,
        consonant_equivalencies=latin_consonant_equivalencies,
        aspirates=latin_aspirates,
        diphthongs=latin_diphthongs,
        liquid_letters=latin_liquid_letters,
        stop_letters=latin_stop_letters,
    ),
    syllabification_rules=latin_syllabification_rules,
    syllable_morphisms=latin_syllable_morphisms,
    phoneme_morphisms=latin_phoneme_morphisms,
    tokenizer=LatinTokenizer(),
)
