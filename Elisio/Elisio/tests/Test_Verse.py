""" Test classes for Verse scanning """
import unittest
from Elisio.engine.Verse import Verse, Foot, set_django
from Elisio.engine.Word import Word
from Elisio.engine.Syllable import Weight
from Elisio.exceptions import ScansionException

set_django()

from Elisio.models import DatabaseVerse

TYPICAL_VERSE = "Arma virumque cano, Troiae qui primus ab oris"
WORDS = ['Arma', 'virumque', 'cano', 'Troiae', 'qui', 'primus', 'ab', 'oris']
EXPECTED_WORD_LIST = []
for word in WORDS:
    EXPECTED_WORD_LIST.append(Word(word))


class TestVerse(unittest.TestCase):
    """ Test_verse class
    Unit tests for splitting a verse into words
    commit 1 (blagae): BLI 9
    reason: creation
    """

    def construct_verse(self, text=TYPICAL_VERSE):
        """ Construct a verse object from a given text """
        constructed_verse = Verse(text)
        return constructed_verse

    def test_verse_construct(self):
        """ constructing a Verse must work """
        self.assertTrue(isinstance(self.construct_verse(), Verse))
        self.assertTrue(isinstance(self.construct_verse(), Verse))

    def test_verse_fail(self):
        """ fail on invalid input """
        with self.assertRaises(ScansionException):
            self.construct_verse(7)

    def test_verse_equal(self):
        """ Two separate verses are equal if they carry the exact same text
        even if one is split and the other isn't
        """
        verse1 = self.construct_verse()
        verse2 = self.construct_verse()
        verse1.split()
        self.assertEqual(verse1, verse2)

    def test_verse_not_equal(self):
        """ Two separate verses are equal only if they carry the exact same text
        """
        verse1 = self.construct_verse()
        verse2 = self.construct_verse(TYPICAL_VERSE.replace('cano', 'cono'))
        self.assertNotEqual(verse1, verse2)

    def test_verse_split(self):
        """ A normal verse must be split into words correctly """
        verse = self.construct_verse()
        verse.split()
        self.assertEqual(verse.words, EXPECTED_WORD_LIST)

    def test_verse_split_punctuation(self):
        """ A verse with unusual and heavy punctuation
        must be split into words correctly """
        verse = self.construct_verse(
            """(Arma'virumque,%cano.!Troiae^$qui";primus/ab oris)""")
        verse.split()
        self.assertEqual(verse.words, EXPECTED_WORD_LIST)

    def test_verse_split_spaces(self):
        """ A verse with unusual and heavy spacing
        must be split into words correctly """
        verse = self.construct_verse(
            """      Arma\tvirumque\rcano\nTroiae
            \r\nqui\n\rprimus  \b \r   ab    oris.  """)
        verse.split()
        self.assertEqual(verse.words, EXPECTED_WORD_LIST)

    def test_verse_split_unusual_char(self):
        """
        A verse with unusual characters (diacritics)
        must be split into words correctly
        """
        # TODO: aena should have a diaeresis
        """
        verse = self.constructVerse("litore aena locant "
                                    "alii flammasque ministrant.")
        verse.split()
        expected_list = ["litore","aena","locant",
                         "alii","flammasque","ministrant."]
        self.assertEqual(verse.words, expected_list)
        """

    def test_verse_scan_elis_reg(self):
        """ normal elision """
        verse = self.construct_verse('multo ille')
        expected_result = [[Weight.HEAVY, Weight.NONE],
                           [Weight.HEAVY, Weight.ANCEPS]]
        verse.split()
        self.assertEqual(verse.get_syllable_weights(), expected_result)

    def test_verse_scan_elis_um(self):
        """ special cases should be not so special """
        verse = self.construct_verse('multum ille')
        expected_result = [[Weight.HEAVY, Weight.NONE],
                           [Weight.HEAVY, Weight.ANCEPS]]
        verse.split()
        self.assertEqual(verse.get_syllable_weights(), expected_result)

    def test_verse_scan_elis_h(self):
        """ special cases should be not so special """
        verse = self.construct_verse('multo hillo')
        expected_result = [[Weight.HEAVY, Weight.NONE],
                           [Weight.HEAVY, Weight.HEAVY]]
        verse.split()
        self.assertEqual(verse.get_syllable_weights(), expected_result)

    def test_verse_scan_elis_semivwl_h(self):
        """ special cases should be not so special """
        verse = self.construct_verse('multu hille')
        expected_result = [[Weight.HEAVY, Weight.NONE],
                           [Weight.HEAVY, Weight.ANCEPS]]
        verse.split()
        self.assertEqual(verse.get_syllable_weights(), expected_result)

    def test_verse_scan_elis_um_hi(self):
        """ special cases should be not so special """
        verse = self.construct_verse('multum hille')
        expected_result = [[Weight.HEAVY, Weight.NONE],
                           [Weight.HEAVY, Weight.ANCEPS]]
        verse.split()
        self.assertEqual(verse.get_syllable_weights(), expected_result)

    def test_verse_scan_final_anceps(self):
        """ non-heavy final syllable marked anceps if a word follows """
        verse = self.construct_verse('multus ille')
        expected_result = [[Weight.HEAVY, Weight.ANCEPS],
                           [Weight.HEAVY, Weight.ANCEPS]]
        verse.split()
        self.assertEqual(verse.get_syllable_weights(), expected_result)

    def test_verse_scan_heavy_maker(self):
        """ heavymaker makes previous syllable heavy """
        verse = self.construct_verse('esse Zephyrumque')
        expected_result = [[Weight.HEAVY, Weight.HEAVY],
                           [Weight.ANCEPS, Weight.ANCEPS,
                            Weight.HEAVY, Weight.ANCEPS]]
        verse.split()
        self.assertEqual(verse.get_syllable_weights(), expected_result)

    def test_verse_scan_cluster(self):
        """ initial cluster makes previous syllable heavy """
        verse = self.construct_verse('esse strabo')
        expected_result = [[Weight.HEAVY, Weight.HEAVY],
                           [Weight.ANCEPS, Weight.HEAVY]]
        verse.split()
        self.assertEqual(verse.get_syllable_weights(), expected_result)

    def test_verse_scan_full(self):
        """ A regular verse must get all relevant scansion information
        Example:
        arma virumque cano troiae qui primus ab oris
        _  x  x _   u  x _   _ _    _   x x  x  x _
        Note that this archetypical verse does not test for a lot
        """
        verse = self.construct_verse()
        expected_result = [[Weight.HEAVY, Weight.ANCEPS,],
                           [Weight.ANCEPS, Weight.HEAVY, Weight.LIGHT,],
                           [Weight.ANCEPS, Weight.HEAVY,],
                           [Weight.HEAVY, Weight.HEAVY,],
                           [Weight.HEAVY,],
                           [Weight.ANCEPS, Weight.ANCEPS,],
                           [Weight.ANCEPS,],
                           [Weight.ANCEPS, Weight.HEAVY]]
        verse.split()
        self.assertEqual(verse.get_syllable_weights(), expected_result)


    def test_verse_database(self):
        """ Checks to see if a database object exists
        Expects there to be a Database Verse object with primary key 1
        ==> PLEASE CHECK FIXTURES
        """
        db_verse = DatabaseVerse.objects.get(pk=1)
        verse = db_verse.get_verse()
        self.assertTrue(isinstance(verse, Verse))

    def test_verse_letter_frequencies(self):
        """ routine created for scanning optimizations """
        letterlist = {}
        db_verses = DatabaseVerse.objects.all()
        for db_verse in db_verses:
            verse = db_verse.get_verse()
            verse.split()
            for wording in verse.words:
                for letter in wording.text:
                    if not letter in letterlist:
                        letterlist[letter] = 0
                    else:
                        letterlist[letter] += 1
        letterlist = None
