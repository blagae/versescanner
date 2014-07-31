import unittest
from Elisio.engine import Verse, Word
from Elisio.exceptions import ScansionException

typical_verse = "Arma virumque cano, Troiae qui primus ab oris"
words = ['Arma', 'virumque', 'cano', 'Troiae', 'qui', 'primus', 'ab', 'oris']
expected_word_list = []
for word in words:
    expected_word_list.append(Word(word))


class Test_Verse(unittest.TestCase):
    """ Test_Verse class
    Unit tests for splitting a verse into words
    commit 1 (blagae): BLI 9
    reason: creation
    """
    def constructVerse(self, text = typical_verse):
        """ Construct a verse object from a given text """
        constructedVerse = Verse(text)
        return constructedVerse

    def test_VerseConstruct(self):
        """ constructing a Verse must work """
        self.assertTrue(isinstance(self.constructVerse(), Verse))

    def test_VerseFail(self):
        with self.assertRaises(ScansionException):
            self.constructVerse(7)

    def test_VerseEqual(self):
        """ Two separate verses are equal if they carry the exact same text
        even if one is split and the other isn't
        """
        verse1 = self.constructVerse()
        verse2 = self.constructVerse()
        verse1.split()
        self.assertEqual(verse1, verse2)

    def test_VerseNotEqual(self):
        """ Two separate verses are equal only if they carry the exact same text
        """
        verse1 = self.constructVerse()
        verse2 = self.constructVerse(typical_verse.replace('cano', 'cono'))
        self.assertNotEqual(verse1, verse2)

    def test_VerseSplit(self):
        """ A normal verse must be split into words correctly """
        verse = self.constructVerse()
        verse.split()
        self.assertEqual(verse.words, expected_word_list)

    def test_VerseSplitPunctuation(self):
        """ A verse with unusual and heavy punctuation must be split into words correctly """
        verse = self.constructVerse("""(Arma'virumque,%cano.!Troiae^$qui";primus/ab oris)""")
        verse.split()
        self.assertEqual(verse.words, expected_word_list)

    def test_VerseSplitSpaces(self):
        """ A verse with unusual and heavy spacing must be split into words correctly """
        verse = self.constructVerse("""      Arma\tvirumque\rcano\nTroiae\r\nqui\n\rprimus  \b \r   ab    oris.  """)
        verse.split()
        self.assertEqual(verse.words, expected_word_list)


if __name__ == '__main__':
    unittest.main()
