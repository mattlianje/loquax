from dataclasses import replace

from loquax.abstractions import (
    PhonemeSyllabificationRuleStore,
    MorphismStore,
    Rule,
    Syllable,
    RuleSequence,
    Morphism,
    Phoneme,
)
from loquax.text_processing import has_macron


"""
SYLLABIFICATION RULES

(http://www.wheelockslatin.com/chapters/introduction/introduction_syllables.html) 
"""

latin_syllabification_rules = PhonemeSyllabificationRuleStore(
    [
        # SYLLABIFICATION RULE 1: A stop (p, b, t, d, c, g) plus a liquid (l,r) generally count as a single consonant
        # and go with the following vowel
        RuleSequence[Phoneme](
            [
                Rule[Phoneme](lambda p: p.is_stop),
                Rule[Phoneme](lambda p: p.is_liquid),
            ]
        ),
        # SYLLABIFICATION RULE 2: Counted as single consonants are qu and the aspirates ch, ph, th, which should
        # never be separated in syllabification
        RuleSequence[Phoneme]([Rule[Phoneme](lambda p: p.is_aspirate)]),
        # SYLLABIFICATION RULE 3:  A single consonant between two vowels goes with the second vowel
        RuleSequence[Phoneme]([Rule[Phoneme](lambda p: p.is_consonant)]),
    ]
)

"""
SYLLABLE LENGTH RULES

(http://www.wheelockslatin.com/chapters/introduction/introduction_syllables.html) 
"""
long_nature_morphism = Morphism[Syllable](
    target=Rule[Syllable](
        check_fn=lambda s: s.nucleus
        and any(has_macron(p) or p.is_diphthong for p in s.nucleus)
    ),
    transformation=lambda s: replace(s, is_long=True),
)

long_position_morphism_1 = Morphism[Syllable](
    target=Rule[Syllable](check_fn=lambda s: s.nucleus and s.coda and len(s.coda) >= 2),
    transformation=lambda s: replace(s, is_long=True),
)

long_position_morphism_2 = Morphism[Syllable](
    target=Rule[Syllable](check_fn=lambda s: s.nucleus and s.coda and len(s.coda) >= 1),
    transformation=lambda s: replace(s, is_long=True),
    suffix=RuleSequence(
        [Rule[Syllable](check_fn=lambda s: s.coda and len(s.onset) >= 1)]
    ),
)

long_position_morphism_3 = Morphism[Syllable](
    target=Rule[Syllable](check_fn=lambda s: s.nucleus),
    transformation=lambda s: replace(s, is_long=True),
    suffix=RuleSequence(
        [
            Rule[Syllable](
                check_fn=lambda s: s.coda and len(s.coda) == 1 and s.coda[0].val == "x"
            )
        ]
    ),
)

long_position_morphism_4 = Morphism[Syllable](
    target=Rule[Syllable](check_fn=lambda s: s.nucleus),
    transformation=lambda s: replace(s, is_long=True),
    suffix=RuleSequence(
        [
            Rule[Syllable](
                check_fn=lambda s: s.onset
                and len(s.onset) >= 1
                and s.onset[0].val == "x"
            )
        ]
    ),
)
long_position_morphism_5 = Morphism[Syllable](
    target=Rule[Syllable](check_fn=lambda s: s.nucleus and not s.coda),
    transformation=lambda s: replace(s, is_long=True),
    suffix=RuleSequence(
        [Rule[Syllable](check_fn=lambda s: s.onset and len(s.onset) >= 2)]
    ),
)

# Morphism Store
latin_syllable_morphisms = MorphismStore[Syllable](
    [
        long_nature_morphism,
        long_position_morphism_1,
        long_position_morphism_2,
        long_position_morphism_3,
        long_position_morphism_4,
        long_position_morphism_5,
    ]
)

latin_phoneme_morphisms = MorphismStore([])
