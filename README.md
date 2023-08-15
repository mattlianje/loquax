# Loquax

A [Classical](https://en.wikipedia.org/wiki/Classical_antiquity) Phonology framework

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![codecov](https://codecov.io/gh/mattlianje/loquax/branch/main/graph/badge.svg?token=EBMEFP40QL)](https://codecov.io/gh/mattlianje/loquax)
![Build status](https://github.com/mattlianje/loquax/actions/workflows/main.yml/badge.svg)

Loquax, (Latin for "chatty"), is an extensible zero-dependency, FP-style Python library for phonological analysis.

- [Syllabification/tokenization](#syllabification-and-tokenization)
- [Phoneme analysis](#phoneme-analysis)
- [Morphological transformations](#morphological-transformations)
- [IPA transliteration](#ipa-transliteration)
- [Scansion](#scansion)
- [Extensibility](#extensibility)

## Loquax Web
Demo of a subset of loquax's features [here](https://nargothrond.xyz/loquax).

<img src="data/loquax_latin_online_demo.png" width="600">

## Languages
| Language/Dialect       | IPA  | Syllabification | Scansion |
|------------------------|------|-----------------|----------|
| **Latin/Classical**    | ✓    | ✓               | ✓        |
| **Greek/Classical**    | X    | X               | X        |

## Quickstart
```shell
pip install loquax
``` 

```python
from loquax import Document
from loquax.languages import Latin

catilinarian_orations = Document("Quoūsque tandem abutēre, Catilīna, patientiā nostrā?", Latin)
print(catilinarian_orations.to_string(ipa=True, scansion=True))

# outputs:
# kʷɔ.uːs.kʷɛ    tan.dɛm    a.bʊ.teː.rɛ    ka.tɪ.liː.na    pa.tɪ.ɛn.tɪ.aː    nɔs.traː
#  u   -   u      -   u     u u   -  u     u  u   -  u     u  u  u  u  -      u   -

```
## Syllabification, Tokenization
```python
print(catilinarian_orations.tokens)

# outputs:
# [kʷɔ.uːs.kʷɛ, tan.dɛm, a.bʊ.teː.rɛ, ka.tɪ.liː.na, pa.tɪ.ɛn.tɪ.aː, nɔs.traː]

print(catilinarian_orations.tokens[0].syllables)

# outputs:
# [quo, ūs, que]
```

## Phoneme Analysis
Understand unique sounds and their roles within words relative to a `Language`
```python
from loquax.abstractions import Phoneme
from loquax.languages import Latin

r = Phoneme('r', Latin)
print(r.is_consonant and r.is_liquid)  # outputs: True
```

## Morphology
**The central problem of phonology** is that linguistic units have changing features depending on their context and neighbours. 

Loquax allows users to tackle this by defining their own morphisms. 

```python
'''
In this example, we create a `Morphism` that targets syllables with a nucleus and at least one coda, 
then transforms them into long syllables. The transformation is only applied if the next syllable 
has an onset of length greater than or equal to one. 
'''

from loquax.morphisms import Morphism, Rule, RuleSequence
from loquax.syllables import Syllable
from dataclasses import replace

long_position_morphism = Morphism[Syllable](
    target=Rule[Syllable](check_fn=lambda s: s.nucleus and s.coda and len(s.coda) >= 1),
    transformation=lambda s: replace(s, is_long=True),
    suffix=RuleSequence(
        [Rule[Syllable](check_fn=lambda s: s.coda and len(s.onset) >= 1)]
    ),
)
```
`MorphismStore` lets you organize your morphisms and to apply all transformations in your MorphismStore to a given syllable or phoneme sequence:
```python
from loquax.abstractions import MorphismStore

# Assuming morphism1, morphism2, morphism3 are predefined Morphism objects...
morphism_store = MorphismStore([morphism1, morphism2, morphism3])

syllables_sequence = [syllable1, syllable2, syllable3]

# Apply all transformations stored in MorphismStore
transformed_sequence = morphism_store.apply_all(syllables_sequence)

# transformed_sequence now holds the syllables transformed by morphism1, morphism2, morphism3 in order.
```

## Ipa
To convert text into the International Phonetic Alphabet for universal comprehension, 
you can use the `to_string` function with `ipa=True`:
```python
print(catilinarian_orations.to_string(ipa=True))

# outputs:
# kʷɔ.uːs.kʷɛ    tan.dɛm    a.bʊ.teː.rɛ    ka.tɪ.liː.na    pa.tɪ.ɛn.tɪ.aː    nɔs.traː
```

## Scansion
Scansion is the process of marking the stresses in a poem, and dividing the lines into feet. 
It's a critical part of the study and enjoyment of classical verse, like in Latin and Ancient Greek poetry. 
Loquax makes it easy to integrate scansion into your language analysis pipeline.

Currently only differentiation between long and short syllables is made
```python
print(catilinarian_orations.to_string(scansion=True))

# outputs:
# quo.ūs.que    tan.dem    a.bu.tē.re    ca.ti.lī.na    pa.ti.en.ti.ā    nos.trā
#  u  -   u      -   u     u u  -  u     u  u  -  u     u  u  u  u  -     u   -
```

## Extensibility
Loquax allows for extensibility, so you can build and customize your own language rules 
for unique or theoretical languages. Here's an example of how to define custom rules and apply them:
```python
# Create your own custom language with unique rules and phonemes
from loquax.languages import Latin
from loquax.abstractions import (
    PhonemeSyllabificationRuleStore, Language, 
    Constants, Tokenizer, MorphismStore, 
    Syllable, Morphism, Phoneme
)

# Let's suppose we have defined custom syllabification rules and constants
syllabification_rules = PhonemeSyllabificationRuleStore(...)
constants = Constants(...)
tokenizer = Tokenizer(...)
syllable_morphisms = MorphismStore[Syllable]([...])
phoneme_morphisms = MorphismStore[Phoneme]([...])

# Creation of our language object we can instantiate new `Documents` and other abstractions with
my_lang = Language(
    language_name='MyLang',
    iso_639_code='myl', # Made-up ISO 639 code for our custom language
    constants,
    syllabification_rules,
    syllable_morphisms,
    phoneme_morphisms,
    tokenizer,
)

```

