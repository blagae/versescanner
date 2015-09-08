""" Test classes for Syllable """
import unittest
from Elisio.engine.Syllable import Syllable, WordAnalyzer
from Elisio.engine.Sound import SoundFactory
from Elisio.exceptions import ScansionException

class TestSyllable(unittest.TestCase):
    """ Test class for Syllable """
    def construct_syllable(self, text):
        """ convenience method """
        constructed_syllable = Syllable(text)
        return constructed_syllable

    def test_syll_constr_init(self):
        """ regular syllable """
        self.assertTrue(isinstance(self.construct_syllable('ti'), Syllable))

    def test_syll_constr_free(self):
        """ regular syllable """
        self.assertTrue(isinstance(self.construct_syllable('o'), Syllable))

    def test_syll_constr_diph(self):
        """ regular syllable with diphthong """
        self.assertTrue(isinstance(self.construct_syllable('aen'), Syllable))

    def test_syll_constr_semivwl(self):
        """ regular syllable with initial semivowel """
        self.assertTrue(isinstance(self.construct_syllable('iu'), Syllable))

    def test_syll_constr_cons_cluster(self):
        """ regular syllable with initial consonant cluster """
        self.assertTrue(isinstance(self.construct_syllable('sphroc'), Syllable))

    def test_syll_fail_non_diph(self):
        """ this is not a single syllable """
        with self.assertRaises(ScansionException):
            self.construct_syllable('tia')

    def test_syll_fail_mult_vwl(self):
        """ this is not a single syllable """
        with self.assertRaises(ScansionException):
            self.construct_syllable('aeu')

    def test_syll_fail_mult_syll(self):
        """ this is not a single syllable """
        with self.assertRaises(ScansionException):
            self.construct_syllable('inos')

    def test_syll_fail_too_rare(self):
        """
        while it is technically possible to make this sound a diphthong,
        is exceedingly rare and must be seen as a lexical exception
        """
        with self.assertRaises(ScansionException):
            self.construct_syllable('prout')

    def test_syll_lexical_exception(self):
        """ ui is not usually a diphthong but it is attested in the forms
        cui and huic, which are consistently monosyllabic.
        these should be considered lexical exceptions
        this is not typical of the Syllable, so these syllables must fail
        """
        with self.assertRaises(ScansionException):
            self.construct_syllable('cui')

    def test_sound_finder(self):
        """ integration test for finding sounds """
        sound1 = SoundFactory.create('f')
        sound2 = SoundFactory.create('o')
        sound3 = SoundFactory.create('r')
        sound4 = SoundFactory.create('s')
        expected_sounds = []
        expected_sounds.append(sound1)
        expected_sounds.append(sound2)
        expected_sounds.append(sound3)
        expected_sounds.append(sound4)
        sounds = WordAnalyzer.find_sounds_for_text('fors')
        self.assertEqual(sounds, expected_sounds)

    def test_sound_finder_digraphs(self):
        """ digraphs must work out well """
        sound1 = SoundFactory.create('qu')
        sound2 = SoundFactory.create('ae')
        expected_sounds = []
        expected_sounds.append(sound1)
        expected_sounds.append(sound2)
        sounds = WordAnalyzer.find_sounds_for_text('quae')
        self.assertEqual(sounds, expected_sounds)

if __name__ == '__main__':
    unittest.main()
