import pytest

from loquax.abstractions import Phoneme
from loquax.text_processing.commons import has_macron
from loquax.languages import Latin

@pytest.mark.parametrize("phoneme_input,expected_output", [
    (Phoneme("ā", Latin), True),
    (Phoneme("a", Latin), False),
])
def test_macron(phoneme_input, expected_output):
    assert has_macron(phoneme_input) is expected_output
