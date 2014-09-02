import unittest
from Elisio.engine.verseProcessor import *
from Elisio.engine.wordProcessor import *
from Elisio.exceptions import ScansionException

typical_word = "recentia"
syllables = ['re', 'cen', 'ti', 'a']
expected_syllable_list = []
expected_weights = [SyllableWeights.ANCEPS, SyllableWeights.HEAVY, SyllableWeights.LIGHT, SyllableWeights.ANCEPS]
for syllable in syllables:
    expected_syllable_list.append(Syllable(syllable))

class Test_Word(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        setDjango()

    def constructWord(self, word=typical_word):
        """ Construct a word object from a given text """
        constructedWord = Word(word)
        return constructedWord

    def test_WordConstruct(self):
        self.assertTrue(isinstance(self.constructWord(), Word))

    def test_WordFail(self):
        with self.assertRaises(ScansionException):
            self.constructWord(7)

    def test_WordEqual(self):
        word1 = self.constructWord()
        word2 = self.constructWord()
        self.assertEqual(word1, word2)

    def test_WordEqualCaseInsensitive(self):
        word1 = self.constructWord(typical_word.lower())
        word2 = self.constructWord(typical_word.upper())
        self.assertEqual(word1, word2)

    def test_WordFailInitialSpace(self):
        with self.assertRaises(ScansionException):
            self.constructWord(' '.join(typical_word))

    def test_WordFailFinalSpace(self):
        with self.assertRaises(ScansionException):
            self.constructWord(typical_word.join(' '))

    def test_WordFailInternalSpace(self):
        with self.assertRaises(ScansionException):
            self.constructWord(typical_word.replace(typical_word[4], ' '))

    def test_WordFailNonAlpha(self):
        with self.assertRaises(ScansionException):
            self.constructWord(typical_word.replace(typical_word[5], '%'))

    def test_WordSplitRegular(self):
        word = self.constructWord()
        word.split()
        self.assertEqual(word.syllables, expected_syllable_list)
        
    def test_WordScansionRegular(self):
        word = self.constructWord()
        word.split()
        self.assertEqual(word.getSyllableStructure(), expected_weights)

    def test_WordScansionClosedSemivowels(self):
        word = self.constructWord('iurgus')
        weights = [SyllableWeights.HEAVY, SyllableWeights.HEAVY]
        word.split()
        self.assertEqual(word.getSyllableStructure(), weights)
        
    def test_WordSplitClosedSemivowels(self):
        word = self.constructWord('iurgus')
        syllable_list = [Syllable('iur'), Syllable('gus')]
        word.split()
        self.assertEqual(word.syllables, syllable_list)
        
    def test_WordSplitInitialClusters(self):
        word = self.constructWord('sphrostrurbs')
        syllable_list = [Syllable('sphros'), Syllable('trurbs', False)]
        word.split()
        self.assertEqual(word.syllables, syllable_list)
        
    def test_WordScansionInitialClusters(self):
        word = self.constructWord('sphrostrurbs')
        weights = [SyllableWeights.HEAVY, SyllableWeights.HEAVY]
        word.split()
        self.assertEqual(word.getSyllableStructure(), weights)
    
    def test_WordSplitOpenSemivowels(self):
        word = self.constructWord('imus')
        syllable_list = [Syllable('i'), Syllable('mus')]
        word.split()
        self.assertEqual(word.syllables, syllable_list, word.syllables)

    def test_WordScansionOpenSemivowels(self):
        word = self.constructWord('imus')
        weights = [SyllableWeights.ANCEPS, SyllableWeights.HEAVY]
        word.split()
        self.assertEqual(word.getSyllableStructure(), weights)
        
    def test_WordSplitInitialSemivowels(self):
        word = self.constructWord('uilis')
        syllable_list = [Syllable('ui'), Syllable('lis')]
        word.split()
        self.assertEqual(word.syllables, syllable_list)
        
    def test_WordScansionInitialSemivowels(self):
        word = self.constructWord('uilis')
        weights = [SyllableWeights.ANCEPS, SyllableWeights.HEAVY]
        word.split()
        self.assertEqual(word.getSyllableStructure(), weights)

    def test_WordSplitShortenedSemivowels(self):
        word = self.constructWord('pius')
        syllable_list = [Syllable('pi'), Syllable('us')]
        word.split()
        self.assertEqual(word.syllables, syllable_list)

    def test_WordScansionShortenedSemivowels(self):
        word = self.constructWord('pius')
        weights = [SyllableWeights.LIGHT, SyllableWeights.HEAVY]
        word.split()
        self.assertEqual(word.getSyllableStructure(), weights)
    
    def test_WordSplitGeminate(self):
        word = self.constructWord('eius')
        syllable_list = [Syllable('e'), Syllable('ius')]
        word.split()
        self.assertEqual(word.syllables, syllable_list)
        
    def test_WordSplitGeminateOrRareDiphthong(self):
        word = self.constructWord('cuius')
        syllable_list = [Syllable('cu'), Syllable('ius')]
        word.split()
        self.assertEqual(word.syllables, syllable_list)
        
    def test_WordSplitLexicalException(self):
        word = self.constructWord('cui')
        syllable_list = [Syllable('cui', False)]
        word.split()
        self.assertEqual(word.syllables, syllable_list)
        
    def test_WordSplitLexicalExceptionBis(self):
        word = self.constructWord('huic')
        syllable_list = [Syllable('huic', False)]
        word.split()
        self.assertEqual(word.syllables, syllable_list)

    def test_WordSplitWeirdWord(self):
        word = self.constructWord('troiae')
        syllable_list = [Syllable('tro'), Syllable('iae')]
        word.split()
        self.assertEqual(word.syllables, syllable_list)
        
    def test_WordScansionWeirdWord(self):
        word = self.constructWord('troiae')
        weights = [SyllableWeights.HEAVY, SyllableWeights.HEAVY]
        word.split()
        self.assertEqual(word.getSyllableStructure(), weights)

    def test_WordSplitNotALexicalException(self):
        word = self.constructWord('prout')
        syllable_list = [Syllable('pro'), Syllable('ut')]
        word.split()
        self.assertEqual(word.syllables, syllable_list)
        
    def test_WordSplitSamevowels(self):
        word = self.constructWord('mortuus')
        syllable_list = [Syllable('mor'), Syllable('tu'), Syllable('us')]
        word.split()
        self.assertEqual(word.syllables, syllable_list)
        
    def test_WordScansionSamevowels(self):
        word = self.constructWord('mortuus')
        weights = [SyllableWeights.HEAVY, SyllableWeights.LIGHT, SyllableWeights.HEAVY]
        word.split()
        self.assertEqual(word.getSyllableStructure(), weights)
        
    def test_WordSplitWithQ(self):
        word = self.constructWord('antiquus')
        syllable_list = [Syllable('an'), Syllable('ti'), Syllable('quus')]
        word.split()
        self.assertEqual(word.syllables, syllable_list)

    def test_WordScansionWithQ(self):
        word = self.constructWord('antiquus')
        weights = [SyllableWeights.HEAVY, SyllableWeights.ANCEPS, SyllableWeights.HEAVY]
        word.split()
        self.assertEqual(word.getSyllableStructure(), weights)

    def test_WordSplitWithH(self):
        word = self.constructWord('pathos')
        syllable_list = [Syllable('pa'), Syllable('thos')]
        word.split()
        self.assertEqual(word.syllables, syllable_list)

    def test_WordScansionAncepsH(self):
        word = self.constructWord('pathos')
        weights = [SyllableWeights.ANCEPS, SyllableWeights.HEAVY]
        word.split()
        self.assertEqual(word.getSyllableStructure(), weights)

    def test_WordSplitLotsOfConsonants(self):
        word = self.constructWord('Urbs')
        syllable_list = [Syllable('urbs', False)]
        word.split()
        self.assertEqual(word.syllables, syllable_list)
        
    def test_WordSplitWithMutaCumLiquida(self):
        word = self.constructWord('patris')
        syllable_list = [Syllable('pa'), Syllable('tris')]
        word.split()
        self.assertEqual(word.syllables, syllable_list)
        
    def test_WordScansionMutaCumLiquidaAnceps(self):
        word = self.constructWord('patris')
        weights = [SyllableWeights.ANCEPS, SyllableWeights.HEAVY]
        word.split()
        self.assertEqual(word.getSyllableStructure(), weights)

    def test_WordSplitWithEnclitic(self):
        word = self.constructWord('quidve')
        syllable_list = [Syllable('quid'), Syllable('ue')]
        word.split()
        self.assertEqual(word.syllables, syllable_list)

    def test_WordScansionSemivowelInternal(self):
        word = self.constructWord('italiam')
        weights = [SyllableWeights.ANCEPS, SyllableWeights.ANCEPS, SyllableWeights.LIGHT, SyllableWeights.HEAVY]
        word.split()
        self.assertEqual(word.getSyllableStructure(), weights)
        
    def test_WordSplitSemivowelInternalFakeDiphthong(self):
        word = self.constructWord('lavus')
        syllable_list = [Syllable('la'), Syllable('vus')]
        word.split()
        self.assertEqual(word.syllables, syllable_list)
        
    def test_WordScansionSemivowelInternalFakeDiphthong(self):
        word = self.constructWord('lavus')
        weights = [SyllableWeights.ANCEPS, SyllableWeights.HEAVY]
        word.split()
        self.assertEqual(word.getSyllableStructure(), weights)

    def test_WordSplitSemivowelInternalConsonantal(self):
        word = self.constructWord('civis')
        syllable_list = [Syllable('ci'), Syllable('vis')]
        word.split()
        self.assertEqual(word.syllables, syllable_list)

    def test_WordScansionSemivowelInternalConsonantal(self):
        word = self.constructWord('civis')
        weights = [SyllableWeights.ANCEPS, SyllableWeights.HEAVY]
        word.split()
        self.assertEqual(word.getSyllableStructure(), weights)

    def test_WordSplitMultipleIdenticalSounds(self):
        word = self.constructWord('memor')
        syllable_list = [Syllable('me'), Syllable('mor')]
        word.split()
        self.assertEqual(word.syllables, syllable_list)
        
    def test_WordScansionMultipleIdenticalSounds(self):
        word = self.constructWord('memor')
        weights = [SyllableWeights.ANCEPS, SyllableWeights.HEAVY]
        word.split()
        self.assertEqual(word.getSyllableStructure(), weights)

    def test_WordScansionWithH(self):
        word = self.constructWord('zephyrus')
        weights = [SyllableWeights.ANCEPS, SyllableWeights.ANCEPS, SyllableWeights.HEAVY]
        word.split()
        self.assertEqual(word.getSyllableStructure(), weights)

    def test_WordScansionWeirdWordTwo(self):
        word = self.constructWord('troas')
        weights = [SyllableWeights.HEAVY, SyllableWeights.HEAVY]
        word.split()
        self.assertEqual(word.getSyllableStructure(), weights)

    def test_WordScansionInitialShortEndVowelClosed(self):
        word = self.constructWord('uiles')
        weights = [SyllableWeights.ANCEPS, SyllableWeights.HEAVY]
        word.split()
        self.assertEqual(word.getSyllableStructure(), weights)
        
    def test_WordScansionShortenedH(self):
        word = self.constructWord('maher')
        weights = [SyllableWeights.LIGHT, SyllableWeights.HEAVY]
        word.split()
        self.assertEqual(word.getSyllableStructure(), weights)
        
    def test_WordSplitNotADiphthong(self):
        word = self.constructWord('deum')
        syllable_list = [Syllable('de'), Syllable('um')]
        word.split()
        self.assertEqual(word.syllables, syllable_list)
        
    def test_WordScansionNotADiphthong(self):
        word = self.constructWord('deum')
        weights = [SyllableWeights.LIGHT, SyllableWeights.HEAVY]
        word.split()
        self.assertEqual(word.getSyllableStructure(), weights)

    def test_WordSplitMonosyllabic(self):
        word = self.constructWord('iam')
        syllable_list = [Syllable('iam')]
        word.split()
        self.assertEqual(word.syllables, syllable_list)
        
    def test_WordScansionMonosyllabic(self):
        word = self.constructWord('iam')
        weights = [SyllableWeights.HEAVY]
        word.split()
        self.assertEqual(word.getSyllableStructure(), weights)
        
    def test_WordSplitWithGU(self):
        word = self.constructWord('sanguine')
        syllable_list = [Syllable('san'), Syllable('gui'), Syllable('ne')]
        word.split()
        self.assertEqual(word.syllables, syllable_list)
        
    def test_WordScansionWithGU(self):
        word = self.constructWord('sanguine')
        weights = [SyllableWeights.HEAVY, SyllableWeights.ANCEPS, SyllableWeights.LIGHT]
        word.split()
        self.assertEqual(word.getSyllableStructure(), weights)

if __name__ == '__main__':
    unittest.main()
