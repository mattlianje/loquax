import re
from functools import reduce
from typing import List

from loquax.abstractions import Tokenizer


class LatinTokenizer(Tokenizer):
    """
    Tokenizer for Classical Latin text.
    """

    def tokenize(self, text: str) -> List[str]:
        # This function takes multiple function arguments and composes
        # them into a single function. The composed function applies the given functions in sequence.
        compose = lambda *functions: reduce(
            lambda f, g: lambda x: f(g(x)), functions, lambda x: x
        )
        transformations = compose(
            str.lower,
            lambda s: re.sub(r"[^\w\s]", "", s),
            lambda s: re.sub(r"\d", "", s),
        )
        return transformations(text).split()
