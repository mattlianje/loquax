<p align="left">
    <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black"></a>
    <a href="https://codecov.io/gh/mattlianje/loquax"><img src="https://codecov.io/gh/mattlianje/loquax/branch/main/graph/badge.svg?token=EBMEFP40QL" alt="codecov"></a>
</p>

<div align="center">
    <img src="pix/loquax_with_github.png" width="400"/>
</div>

# Loquax
Loquax, (Latin for "chatty"), is an extensible, zero-dependency, FP-style Python library for phonological analysis. Eventually the python package will be soft-deprecated and this repo will house the compiler for the Loquax DSL. The [loquax web client](https://nargothrond.xyz/loquax).

## Features
- [Syllabification/tokenization](#syllabification-and-tokenization)
- [Phoneme analysis](#phoneme-analysis)
- [Morphological transformations](#morphological-transformations)
- [IPA transliteration](#ipa-transliteration)
- [Scansion](#scansion)
- [Extensibility](#extensibility)

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

morphism_store = MorphismStore([morphism1, morphism2, morphism3])
syllables_sequence = [syllable1, syllable2, syllable3]
transformed_sequence = morphism_store.apply_all(syllables_sequence)
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
from loquax.languages import Latin
from loquax.abstractions import (
    PhonemeSyllabificationRuleStore, Language, 
    Constants, Tokenizer, MorphismStore, 
    Syllable, Morphism, Phoneme
)

syllabification_rules = PhonemeSyllabificationRuleStore(...)
constants = Constants(...)
tokenizer = Tokenizer(...)
syllable_morphisms = MorphismStore[Syllable]([...])
phoneme_morphisms = MorphismStore[Phoneme]([...])

my_lang = Language(
    language_name='MyLang',
    iso_639_code='myl', 
    constants,
    syllabification_rules,
    syllable_morphisms,
    phoneme_morphisms,
    tokenizer,
)

```

