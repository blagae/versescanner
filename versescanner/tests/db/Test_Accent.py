import unittest

from elisio.parser.versefactory import VerseFactory, VerseType

from versescanner.util.utils import set_django

set_django()

from versescanner.bridge.DatabaseBridge import DatabaseBridge


class TestAccent(unittest.TestCase):

    def test_accent_lavinia(self):
        verse = VerseFactory.create("Italiam fato profugus Laviniaque venit",
                                    bridge=DatabaseBridge(), creators=VerseType.HEXAMETER)
        verse.parse()
        # italiam
        self.assertEqual(verse.words[0].syllables[0].stressed, False)
        self.assertEqual(verse.words[0].syllables[1].stressed, True)
        self.assertEqual(verse.words[0].syllables[2].stressed, False)
        self.assertEqual(verse.words[0].syllables[3].stressed, False)
        # fato
        self.assertEqual(verse.words[1].syllables[0].stressed, True)
        self.assertEqual(verse.words[1].syllables[1].stressed, False)
        # profugus
        self.assertEqual(verse.words[2].syllables[0].stressed, True)
        self.assertEqual(verse.words[2].syllables[1].stressed, False)
        # Laviniaque
        self.assertEqual(verse.words[3].syllables[0].stressed, False)
        self.assertEqual(verse.words[3].syllables[1].stressed, True)
        self.assertEqual(verse.words[3].syllables[2].stressed, False)
        self.assertEqual(verse.words[3].syllables[3].stressed, False)
        # venit
        self.assertEqual(verse.words[4].syllables[0].stressed, True)
        self.assertEqual(verse.words[4].syllables[1].stressed, False)
