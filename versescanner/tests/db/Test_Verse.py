""" Test classes for Verse scanning """
import unittest

from elisio.parser.versefactory import VerseFactory
from elisio.word import Word

from versescanner.util.utils import set_django

set_django()

from versescanner.models.metadata import Verse

TYPICAL_VERSE = "Arma virumque cano, Troiae qui primus ab oris"
WORDS = ['Arma', 'virumque', 'cano', 'Troiae', 'qui', 'primus', 'ab', 'oris']
EXPECTED_WORD_LIST = []
for word in WORDS:
    EXPECTED_WORD_LIST.append(Word(word))


class TestVerse(unittest.TestCase):

    def test_verse_database(self):
        """ Checks to see if a database object exists
        Expects there to be a Database Verse object with primary key 1
        ==> PLEASE CHECK FIXTURES
        """
        db_verse = Verse.objects.get(pk=1)
        verse = db_verse.get_verse()
        self.assertTrue(isinstance(verse, str))
