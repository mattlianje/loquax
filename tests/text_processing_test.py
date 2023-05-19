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
        self.catilina = "Quoūsque tandem abutēre, Catilīna, patientiā nostrā?"

    def test_get_syllables_no_ipa_no_scansion(self):
        doc = Document(
            self.catilina,
            self.lang,
        )
        print(doc.to_str(ipa=False, scansion=False))

    def test_get_syllables_ipa_only(self):
        doc = Document(
            self.catilina,
            self.lang,
        )
        print(doc.to_str(ipa=True, scansion=False))

    def test_get_syllables_ipa_and_scansion(self):
        doc = Document(
            self.catilina,
            self.lang,
        )
        print(doc.to_str(ipa=True, scansion=True))
