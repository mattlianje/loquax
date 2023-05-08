from loquax.constants import Constants
from loquax.languages.latin.latin_constants import *
from loquax.languages.latin.latin_rules import (
    latin_syllabification_rule_store,
    latin_morphism_store,
)
from loquax.entities import Language

latin = Language(
    language_name="Classical Latin",
    constants=Constants(
        vowel_equivalencies=latin_vowel_equivalencies,
        consonant_equivalencies=latin_consonant_equivalencies,
        aspirates=latin_aspirates,
        diphtongs=latin_diphtongs,
        liquid_letters=latin_liquid_letters,
        stop_letters=latin_stop_letters,
    ),
    syllabification_rules=latin_syllabification_rule_store,
    morphisms=latin_morphism_store,
    iso_639_code="lat",
)
