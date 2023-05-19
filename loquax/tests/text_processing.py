import unittest

from loquax import Document
from loquax.abstractions import Phoneme
from loquax.languages import Latin
from loquax.text_processing import has_macron


class TestAccentDetection(unittest.TestCase):
    def setUp(self):
        self.lang = Latin

    def test_macron(self):
        phoneme_with_macron = Phoneme("ā", self.lang)
        phoneme_without_macron = Phoneme("a", self.lang)
        self.assertTrue(has_macron(phoneme_with_macron))
        self.assertFalse(has_macron(phoneme_without_macron))


class TestDocument(unittest.TestCase):
    def setUp(self):
        self.lang = Latin

    def test_get_syllables(self):
        doc = Document(
            "Quoūsque tandem abutēre, Catilīna, patientiā nostrā?",
            self.lang,
        )
        print(doc.__str__(ipa=False, scansion=True))