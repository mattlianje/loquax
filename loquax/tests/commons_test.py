import unittest

from loquax.abstractions import Phoneme
from loquax.text_processing.commons import has_macron
from loquax.languages import Latin


class TestAccentDetection(unittest.TestCase):
    def setUp(self):
        self.lang = Latin

    def test_macron(self):
        phoneme_with_macron = Phoneme("ā", self.lang)
        phoneme_without_macron = Phoneme("a", self.lang)
        self.assertTrue(has_macron(phoneme_with_macron))
        self.assertFalse(has_macron(phoneme_without_macron))
