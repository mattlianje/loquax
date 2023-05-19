from dataclasses import dataclass
from itertools import chain
from typing import Dict, List, Set


@dataclass
class Constants:
    vowel_equivalencies: Dict[str, List[str]]
    consonant_equivalencies: Dict[str, List[str]]
    aspirates: Set[str]
    diphthongs: Set[str]
    liquid_letters: Set[str]
    stop_letters: Set[str]

    def get_distinct_elements(self, d: Dict) -> set:
        """
        Get the set of distinct elements from the keys and values of a dictionary.
        If a value is a list, its elements will be included in the output set.

        :param d (dict): the input dictionary
        :return: the set of distinct elements
        """
        return set(
            chain(d.keys(), *(v if isinstance(v, list) else [v] for v in d.values()))
        )

    @property
    def equivalencies(self) -> Dict[str, List[str]]:
        return self.vowel_equivalencies | self.consonant_equivalencies

    @property
    def vowels(self) -> Set[str]:
        return set(self.get_distinct_elements(self.vowel_equivalencies))

    @property
    def consonants(self) -> Set[str]:
        return set(self.get_distinct_elements(self.consonant_equivalencies))

    @property
    def symbol_groups(self) -> Set[str]:
        return set(
            filter(
                lambda x: len(x) > 1,
                set(
                    self.aspirates.union(
                        self.diphthongs,
                        self.liquid_letters,
                        self.stop_letters,
                        self.vowels,
                        self.consonants,
                    )
                ),
            )
        )
