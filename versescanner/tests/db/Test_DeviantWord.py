import unittest

from elisio.syllable import Syllable
from elisio.word import Weight, Word

from versescanner.util.utils import set_django

set_django()

from versescanner.bridge.DatabaseBridge import DatabaseBridge


class TestDeviantWord(unittest.TestCase):

    @staticmethod
    def construct_word(word):
        """ Construct a word object from a given text """
        constructed_word = Word(word)
        return constructed_word

    # TODO: build tests for words that are actually deviant (i.e. not names)
    # ----
    # this test class requires that a DeviantWord named aene[ai].*
    # be present in the database. If not, run syncdb or migrate
    """
    # unit tests
    def test_table(self):
        self.assertIsInstance(DeviantWord.find("aenean"), DeviantWord)

    def test_table_fail(self):
        self.assertIsNone(DeviantWord.find("aeneo"))
    def test_list(self):
        # TODO: not sure if this will always succeed
        lst = DeviantWord.words
        self.assertTrue(len(lst) == 0)
        DeviantWord.get_list()
        lst = DeviantWord.words
        self.assertTrue(len(lst)>0)


    # component tests
    def test_aeneas_works(self):
        word = Word("aeneas")
        self.assertTrue(word.split_from_deviant_word())

    def test_aeneas_capital_works(self):
        word = Word("Aenei")
        self.assertTrue(word.split_from_deviant_word())
    
    def test_aeneas_is_correct(self):
        word = Word("aeneas")
        expected = [Weight.HEAVY, Weight.HEAVY, Weight.HEAVY]
        self.assertEqual(expected, word.get_syllable_structure())

    def test_aenea_is_correct(self):
        word = Word("aenea")
        sylls = [Syllable("ae"), Syllable("ne"), Syllable("a")]
        self.assertEqual(weights, word.get_syllable_structure())
        self.assertEqual(sylls, word.syllables)

    def test_nonalphatic_fails(self):
        with self.assertRaises(WordException):
            word = Word("Aenei,")
    #"""

    def test_syllsplit_ianua(self):
        # TODO: deviant word ?
        word = Word('ianua')
        weights = [Weight.ANCEPS, Weight.LIGHT, Weight.HEAVY]
        sylls = [Syllable.make_empty_syllable('ia'), Syllable.make_empty_syllable('nu'), Syllable.make_empty_syllable('a')]
        word.split(DatabaseBridge())
        self.assertEqual(weights, word.get_syllable_structure())
        self.assertEqual(sylls, word.syllables)

    def test_word_split_semiv_enclitic(self):
        """ scan word with final -e as anceps """
        word = self.construct_word('cuique')
        syllable_list = [Syllable.make_empty_syllable('cui'), Syllable.make_empty_syllable('que')]
        word.split(DatabaseBridge())
        self.assertEqual(word.syllables, syllable_list)

    def test_word_split_lexical(self):
        """ common word must be in the dictionary """
        word = self.construct_word('cui')
        syllable_list = [Syllable.make_empty_syllable('cui')]
        word.split(DatabaseBridge())
        self.assertEqual(word.syllables, syllable_list)

    def test_word_split_lexical_exc(self):
        """ common word must be in the dictionary """
        word = self.construct_word('huic')
        syllable_list = [Syllable.make_empty_syllable('huic')]
        word.split(DatabaseBridge())
        self.assertEqual(word.syllables, syllable_list)

    def test_word_scan_weird_word_two(self):
        """ proper name scanning """
        word = self.construct_word('troas')
        weights = [Weight.HEAVY, Weight.HEAVY]
        word.split(DatabaseBridge())
        self.assertEqual(word.get_syllable_structure(), weights)

    def test_word_create_deviant(self):
        word = self.construct_word('lavinia')
        word.split(DatabaseBridge())
        expected = [Syllable.make_empty_syllable('la'), Syllable.make_empty_syllable('vin'), Syllable.make_empty_syllable('ia')]
        self.assertEqual(word.syllables, expected)

    def test_word_create_deviant_smvl(self):
        word = self.construct_word('lauinja')
        word.split(DatabaseBridge())
        expected = [Syllable.make_empty_syllable('la'), Syllable.make_empty_syllable('vin'), Syllable.make_empty_syllable('ia')]
        self.assertEqual(word.syllables, expected)

    def test_word_scan_weird_word(self):
        """ common name must be in the dictionary """
        word = self.construct_word('troiae')
        weights = [Weight.HEAVY, Weight.HEAVY]
        word.split(DatabaseBridge())
        self.assertEqual(word.get_syllable_structure(), weights)
