from loquax.entities import (
    PhonemeSyllabificationRuleStore,
    PhonemeRuleSequence,
    PhonemeRule,
    MorphismStore,
)

# Latin rules used:
# http://www.wheelockslatin.com/chapters/introduction/introduction_syllables.html
latin_syllabification_rule_store = PhonemeSyllabificationRuleStore(
    [
        # Rule 1: A stop (p, b, t, d, c, g) plus a liquid (l,r)
        # generally count as a single consonant and go with the following vowel
        PhonemeRuleSequence(
            [
                PhonemeRule(lambda p: p.is_stop),
                PhonemeRule(lambda p: p.is_liquid),
            ]
        ),
        # Rule 2: Counted as single consonants are qu and the aspirates ch, ph, th,
        # which should never be separated in syllabification
        PhonemeRuleSequence([PhonemeRule(lambda p: p.is_aspirate)]),
        # Rule 3:  A single consonant between two vowels goes with the second vowel
        PhonemeRuleSequence([PhonemeRule(lambda p: p.is_consonant)]),
    ]
)

latin_morphism_store = MorphismStore([])
