﻿import unittest
from Elisio.engine.Verse import Verse, Foot, set_django
from Elisio.engine.Hexameter import Hexameter
from Elisio.engine.VerseFactory import VerseFactory
from Elisio.tests.Test_Verse import TYPICAL_VERSE
from Elisio.exceptions import HexameterException, VerseException

set_django()

from Elisio.models import DatabaseVerse

class TestHexameter(unittest.TestCase):
    """ testing specifically for the hexameter """
    def construct_hexameter(self, text=TYPICAL_VERSE):
        """ Construct a Hexameter object from a given text """
        constructed_verse = VerseFactory.create(text)

        return constructed_verse

    def test_hexameter_construct(self):
        """ constructing a Hexameter must work """
        self.assertTrue(isinstance(self.construct_hexameter(), Verse))
        self.assertTrue(isinstance(self.construct_hexameter(), Hexameter))

    def test_hexameter_scan_basic_case(self):
        """ Aen. 1, 1 must scan correctly imo """
        expected_feet = [Foot.DACTYLUS, Foot.DACTYLUS,
                         Foot.SPONDAEUS, Foot.SPONDAEUS,
                         Foot.DACTYLUS, Foot.SPONDAEUS]
        verse = self.construct_hexameter()
        self.assertEqual(verse.feet, expected_feet)

    def test_hexameter_scan_all(self):
        """ frivolous check to see how many verses work """
        save = False
        threshold = 9 if save else 11.5
        dbverses = DatabaseVerse.objects.all()
        worked = 0
        failed = 0
        for dbverse in dbverses:
            try:
                verse = VerseFactory.create(dbverse.contents, save)
            except VerseException:
                try:
                    verse = VerseFactory.create(dbverse.contents, False, True)
                except VerseException as exc:
                    failed += 1
                    verse = VerseFactory.get_split_syllables(dbverse.contents)
                    print("{3}({0}: {1}): {2}"
                            .format(dbverse.number, verse, exc, type(exc)))
                else:
                    worked += 1
            else:
                worked += 1
        # canary test: over 91% of verses must succeed
        result = str(worked) + " worked, " + str(failed) + " failed"
        if worked / failed < threshold:
            self.fail(result)
        # canary test: if no verses fail, then we are probably too lax
        elif failed == 0:
            self.fail("improbable result: " + result)
        else:
            print(result)

    def test_hexameter_scan_for_debug(self):
        dbverse = DatabaseVerse.objects.get(pk=700)
        verse = VerseFactory.create(dbverse.contents, False, True)