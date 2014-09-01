import copy
import enum
import re
from Elisio.exceptions import ScansionException

class LetterTypes(enum.Enum):
    VOWEL = 0
    CONSONANT = 1
    SEMIVOWEL = 2
    HEAVYMAKER = 3

class SyllableWeights(enum.Enum):
    NONE = 0
    LIGHT = 1
    HEAVY = 2
    ANCEPS = 3

    labels = {
        NONE: 'None',
        LIGHT: 'Light',
        HEAVY: 'Heavy',
        ANCEPS: 'Anceps'
    }


class Word(object):
    """ Word class
    A word is the representation of the Latin word
    It has extensive knowledge of its sounds, which it can join into syllables
    """
    shortEndVowels = ['e']
    longEndVowels = ['i', 'o', 'u']
    def __init__(self, text):
        """ construct a Word by its contents """
        self.syllables = []
        if not (isinstance(text, str) and text.isalpha()):
            raise ScansionException("Word must be initialized with alphatic data")
        self.text = text.lower()
        
    def __repr__(self):
        return self.syllables
    def __str__(self):
        return self.syllables

    def split(self, testDeviant = True):
        """ splits a word into syllables by using a few static methods from the Syllable class """
        if testDeviant and self.splitFromDeviantWord():
            return
        sounds = self.findSounds()
        temporarySyllables = Word.joinIntoSyllables(sounds)
        self.syllables = Word.redistribute(temporarySyllables)
        self.checkConsistency()

    def splitFromDeviantWord(self):
        """ if the word can be found the repository of Deviant Words, we should use that instead """
        from Elisio.models import Deviant_Word
        deviant = Deviant_Word.find(self.text)
        if deviant:
            self.syllables = deviant.getSyllables()
            txt = self.text
            for syll in self.syllables:
                if len(syll.syllable) >= 1:
                    txt = txt.replace(syll.getText(), '', 1)
            if len(txt) > 0:
                wrd = Word(txt)
                wrd.split(False)
                for sl in wrd.syllables:
                    self.syllables.append(sl)
            # TODO This might be problematic because there is no content given for the final syllables
            return True

    def findSounds(self):
        """ find the sequence of sounds from the textual representation of the word """
        return Word.findSoundsForText(self.text)
    
    def __eq__(self, other): 
        """ Words are equal if they have exactly the same characters
        Case insensitivity is enforced by the constructor
        """
        return self.__dict__ == other.__dict__

    def getSyllableStructure(self, nextWord = None):
        """ get the list of syllable weights based on the syllable list """
        ss = []
        if self.syllables == []:
            self.split()
        for count, syllable in enumerate(self.syllables):
            try:
                ss.append(syllable.getWeight(self.syllables[count+1]))
            except IndexError:
                ss.append(syllable.getWeight())
        if nextWord and isinstance(nextWord, Word):
        # new functionality: word contact
            lastSyllable = self.syllables[-1]
            nextWord.split()
            firstSyllable = nextWord.syllables[0]
            if lastSyllable.canElideIfFinal() and firstSyllable.startsWithVowel():
                # elision
                ss[-1] = SyllableWeights.NONE
            elif lastSyllable.endsWithConsonant() and firstSyllable.startsWithVowel():
                # consonant de facto redistributed
                ss[-1] = SyllableWeights.ANCEPS
            elif lastSyllable.endsWithVowel() and firstSyllable.startsWithConsonantCluster():
                ss[-1] = SyllableWeights.HEAVY
        return ss

    def checkConsistency(self):
        for syllable in self.syllables:
            if not syllable.isValid():
                word = Word(syllable.getText())
                word.split()
                index = self.syllables.index(syllable)
                self.syllables.remove(syllable)
                for syll in reversed(word.syllables):
                    self.syllables.insert(index, syll)
    
    @classmethod
    def findSoundsForText(cls, text):
        """ iteratively allocate all text to a sound
        """
        i = 0
        sounds = []
        while i < len(text):
            addedSounds=Sound.createFromText(text[i:i+3])
            for sound in addedSounds:
                sounds.append(sound)
                i += len(sound.letters)
        return sounds

    @classmethod
    def joinIntoSyllables(cls, sounds):
        """ join a list of sounds into a preliminary syllables
        keep adding sounds to the syllable until it becomes illegal or the word ends
        at either point, save the syllable and count e new one
        """
        syllables = []
        currentSyllable = Syllable("", False)
        for sound in sounds:
            try:
                currentSyllable.addSound(sound)
            except ScansionException:
                syllables.append(currentSyllable)
                currentSyllable = Syllable("", False)
                currentSyllable.addSound(sound)
        syllables.append(currentSyllable)
        return syllables

    @classmethod
    def redistribute(cls, syllables):
        """ redistribute the sounds of a list of syllables
        in order to use the correct syllables, not the longest possible
        """
        for count in range(len(syllables)-1):
            if count == len(syllables)-2 and syllables[count+1] == Syllable('ve'):
                continue
            if syllables[count].endsWithVowel() and syllables[count+1].startsWithConsonantCluster():
                Word.switchSound(syllables[count], syllables[count+1], True)
            elif syllables[count].endsWithConsonant() and syllables[count+1].startsWithVowel(False):
                Word.switchSound(syllables[count], syllables[count+1], False)
        return syllables

    @classmethod
    def switchSound(cls, syllable1, syllable2, toFirst):
        """ switch sounds from one syllable to another
        if toFirst is True, switch from the second to the first
        if toFirst is False, switch from the first to the second
        """
        if toFirst:
            givenSound = syllable2.sounds[0]
            syllable2.sounds.remove(givenSound)
            syllable1.sounds.append(givenSound)
        else:
            givenSound = syllable1.sounds[-1]
            syllable1.sounds.reverse()
            syllable1.sounds.remove(givenSound)
            syllable1.sounds.reverse()
            syllable2.sounds.insert(0, givenSound)

class Syllable(object):
    """ Syllable class
    A syllable knows its sounds and can determine if the specific combination of them is a valid one
    """
    def __init__(self, syllable, test = True, weight = None):
        """ construct a Syllable by its contents """
        self.weight = weight
        self.syllable = syllable
        self.sounds = Word.findSoundsForText(syllable)
        if test and not self.isValid():
            raise ScansionException("invalid Syllable object")

    def __eq__(self, other):
        return self.sounds == other.sounds
    
    def __repr__(self):
        return str(self.sounds)

    def getText(self):
        result = ""
        for sound in self.sounds:
            result += sound.getText()
        return result

    def isValid(self):
        """ a syllable is valid if it contains:
            * at most one consonant after the vocalic sound, and
            * a single vowel or semivowel
            * a semivowel and a vowel in that order
        """
        containsFinalConsonant = containsVowel = containsSemivowel = False
        onlyConsonants = True
        for count, sound in enumerate(self.sounds):
            if isinstance(sound, ConsonantSound):
                if containsFinalConsonant:
                    pass
                    #return False
                if containsVowel or containsSemivowel:
                    containsFinalConsonant = True
            elif isinstance(sound, VowelSound):
                if containsVowel or (containsFinalConsonant and containsSemivowel):
                    return False
                containsVowel = True
                onlyConsonants = False
            elif isinstance(sound, SemivowelSound):
                if containsVowel or (containsFinalConsonant and containsSemivowel):
                    return False
                if count > 0:
                    containsVowel = True
                containsSemivowel = True
                onlyConsonants = False
        return containsVowel or containsSemivowel or onlyConsonants

    def endsWithConsonant(self):
        """ last sound of the syllable is consonantal """
        return self.sounds[-1].isConsonant()

    def canElideIfFinal(self):
        return (self.endsWithVowel() or
                (self.sounds[-1] == Sound.create('m') and 
                (self.sounds[-2].isVowel() or self.sounds[-2].isSemivowel()))
               )

    def endsWithVowel(self):
        """ last sound of the syllable is vocalic
        a final semivowel is always vocalic """
        return self.sounds[-1].isVowel() or self.sounds[-1].isSemivowel()
    
    def startsWithVowel(self, initial=True):
        """ first sound of the syllable is vocalic
        an initial semivowel is only vocalic if it is the syllable's only sound
        or if it is followed directly by a consonant
        """
        return (self.sounds[0].isVowel() or
                self.sounds[0].isH() or 
                (self.sounds[0].isSemivowel() and 
                 (not initial or len(self.sounds) == 1 or self.sounds[1].isConsonant()))
               )
    def startsWithConsonant(self):
        """ first sound of the syllable is consonantal 
        an initial semivowel is consonantal if it is followed by a consonant
        """
        return self.sounds[0].isConsonant() or (self.sounds[0].isSemivowel() and len(self.sounds) > 1 and self.sounds[1].isVowel())

    def startsWithConsonantCluster(self):
        """ first sounds of the syllable are all consonants """
        return (self.startsWithConsonant() and
                ((len(self.sounds) > 1 and self.sounds[1].isConsonant()) or
                 self.makesPreviousHeavy()
                )
               )

    def makesPreviousHeavy(self):
        """ first sound of the syllable is one of the double consonant letters """
        return self.sounds[0].isHeavyMaking()

    def getVowel(self):
        """ get the vocalic sound from a syllable """
        semivowel = None
        for sound in reversed(self.sounds):
            if sound.isVowel():
                return sound
            if sound.isSemivowel():
                if semivowel:
                    return semivowel
                semivowel = sound
        if semivowel:
            return semivowel
        raise ScansionException("no vowel found in Syllable"+str(self.sounds))

    def isHeavy(self, nextSyllable = None):
        """ determines whether the syllable is inherently heavy or not
        a syllable is heavy if it ends in a consonant
        or if the next syllable starts with a heavy-making consonant
        or if it contains a final diphthong which isn't shortened by the next syllable (with vocalic start)
        final syllables are long if they are O, U, or I, or a diphthong
        """
        vowel = self.getVowel()
        if nextSyllable and isinstance(nextSyllable, Syllable):
            return ((self.endsWithConsonant() or nextSyllable.makesPreviousHeavy()) or
                    (not self.isLight(nextSyllable) and vowel.isDiphthong()))
        return self.endsWithConsonant() or vowel.isDiphthong() or vowel.letters[0] in Word.longEndVowels

    def isLight(self, nextSyllable = None):
        """ determines whether the syllable is inherently light or not
        a syllable is always light if it is followed by a vowel in the next syllable
        final vowels are usually short if they are A or E
        """
        if nextSyllable and isinstance(nextSyllable, Syllable):
            return self.endsWithVowel() and nextSyllable.startsWithVowel()
        return (self.endsWithVowel() and
                not self.getVowel().isDiphthong() and
                self.getVowel().letters[0] in Word.shortEndVowels
                )

    def addSound(self, sound):
        """ add a sound to a syllable if the syllable stays valid by the addition """
        testSyllable = copy.deepcopy(self)
        testSyllable.sounds.append(sound)
        if testSyllable.isValid():
            self.sounds.append(sound)
        else:
            raise ScansionException("syllable invalidated by last addition")

    def getWeight(self, nextSyllable = None):
        """ try to determine the weight of the syllable, in the light of the next syllable
        if this doesn't succeed, assign the weight ANCEPS = undetermined
        """
        if self.weight:
            return self.weight
        if self.isLight(nextSyllable):
            return SyllableWeights.LIGHT
        elif self.isHeavy(nextSyllable):
            return SyllableWeights.HEAVY
        else:
            return SyllableWeights.ANCEPS

    @classmethod
    def createFromDatabase(cls, syll):
        from Elisio.models import Deviant_Syllable
        if not isinstance(syll, Deviant_Syllable):
            raise ScansionException("database error with Deviant Syllable")
        result = Syllable(syll.contents, False, syll.weight)
        return result

class Sound(object):
    """ Sound class
    A sound is composed of one or several letters
    """
    def __init__(self, *letters):
        """ construct a Sound from a list of letters, or (a list of) text(s) """
        self.letters = []
        for letter in letters:
            if isinstance(letter, Letter):
                self.letters.append(letter)
            else:
                if isinstance(letter, str) and len(letter) > 1:
                    for let in letter:
                        self.letters.append(Letter(let))
                else:
                    self.letters.append(Letter(letter))
        if not self.isValidSound():
            raise ScansionException("not a valid sound given in constructor"+str(self.letters))
        
    @classmethod
    def create(cls, *letters):
        letterList = []
        for item in letters:
            if isinstance(item, Letter):
                letterList.append(item)
            else:
                for char in item:
                    letterList.append(Letter(char))

        return Sound.factory(letterList)

    @classmethod
    def factory(cls, letterList):
        isFirst = True
        for item in letterList:
            if isFirst:
                type = Letter.letters[item.letter]

                if type == LetterTypes.VOWEL:
                    sound = VowelSound(item)
                elif type == LetterTypes.CONSONANT:
                    sound = ConsonantSound(item)
                elif type == LetterTypes.SEMIVOWEL:
                    sound = SemivowelSound(item)
                elif type == LetterTypes.HEAVYMAKER:
                    sound = HeavyMakerSound(item)
                else:
                    raise ScansionException("not a valid letter"+str(item))
            
                isFirst = False
            else:
                if sound.isVowel():
                    sound = Diphthong(sound.letters[0], item)
                if sound.isConsonant():
                    sound.letters.append(item)

        
        if not sound.isValidSound():
            raise ScansionException("not a valid sound given in factory method")
        return sound

    def getText(self):
        result = ""
        for letter in self.letters:
            result += letter.__str__()
        return result

    def isValidSound(self):
        """ is a given sound a valid sound
        this is determined by the number of letters
        in case that number is 2, it must be one of a fixed list of combinations
        """
        return True

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
    
    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.letters)

    @classmethod
    def createFromText(cls, text):
        """ try to create a Sound from given text string of maximally 3 letters
        """
        # TODO: look at exceptions for ^ius$ ? see old application
        if len(text) > 3:
            raise ScansionException("too many letters in this text sample")
        elif len(text) == 3 and re.match("^[aeijouvy][ijuv][aeijouvy]$", text):
            sounds = []
            for i in text:
                s = Sound.create(i)
                sounds.append(s)
            return sounds
        try:
            sound = Sound.create(text[0:2])
        except ScansionException:
            sound = Sound.create(text[0])
        return [sound]
    
    def isVowel(self):
        """ determine whether a sound is unambiguously vocalic """
        return False
    def isSemivowel(self):
        """ it is impossible to determine on the sound level
        whether or not a semivowel is vocalic or consonantal
        therefore we keep the semivowel category separate
        """
        return False
    def isConsonant(self):
        """ does a sound contain a consonantal letter """
        return False
    def isDiphthong(self):
        return False
    def isHeavyMaking(self):
        """ does a sound contain a cluster-forming consonant letter """
        return False
    def isH(self):
        return False
    def getType(self):
        return Letter.letters[self.letters[0].letter]
    
class VowelSound(Sound):
    def __init__(self, *letters):
        super(VowelSound, self).__init__(*letters)
    def isVowel(self):
        return True
    def isValidSound(self):
        if len(self.letters) != 1:
            return False
        first = self.letters[0].letter
        return Letter.letters[first] == LetterTypes.VOWEL

class Diphthong(VowelSound):
    def __init__(self, *letters):
        super(Diphthong, self).__init__(*letters)
    def isDiphthong(self):
        return True
    def isValidSound(self):
        """ the possible diphthongs
        AU
        AE OE
        """
        if len(self.letters) == 1:
            return False
        first = self.letters[0].letter
        second = self.letters[1].letter
        return ((second == 'u' and first == 'a') or
                (second == 'e' and (first == 'a' or first == 'o')))
            
class SemivowelSound(Sound):
    def __init__(self, *letters):
        super(SemivowelSound, self).__init__(*letters)
    def isSemivowel(self):
        return True
    def isValidSound(self):
        if len(self.letters) != 1:
            return False
        first = self.letters[0].letter
        return Letter.letters[first] == LetterTypes.SEMIVOWEL

class ConsonantSound(Sound):
    def __init__(self, *letters):
        super(ConsonantSound, self).__init__(*letters)
    def isConsonant(self):
        return True
    def isValidSound(self):
        if len(self.letters) != 1:
            return self.isValidDoubleSound()
        first = self.letters[0].letter
        return Letter.letters[first] == LetterTypes.CONSONANT

    def isH(self):
        return self.letters[0] == 'h'
    
    def isMutaCumLiquida(self):
        if len(self.letters) < 2:
            return False
        first = self.letters[0].letter
        second = self.letters[1]
        return ((second == 'r' or second == 'l') and
                (first == 't' or first == 'd' or 
                 first == 'p' or first == 'b' or 
                 first == 'c' or first == 'g' or
                 first == 'f')
               )
    def isValidDoubleSound(self):
        """ the fixed list of combinations
        * QU
        * muta cum liquida
        * an aspirated consonant
        * a diphthong
        """
        if len(self.letters) != 2:
            return False
        first = self.letters[0].letter
        second = self.letters[1]
        return ((first == 'q' and second == 'u') or
                self.isMutaCumLiquida() or
               ((first == 't' or first == 'p' or first == 'c' or first == 'r') and second == 'h'))

class HeavyMakerSound(ConsonantSound):
    def __init__(self, *letters):
        super(HeavyMakerSound, self).__init__(*letters)
    def isHeavyMaking(self):
        return True
    def isValidSound(self):
        if len(self.letters) != 1:
            return False
        first = self.letters[0].letter
        return Letter.letters[first] == LetterTypes.HEAVYMAKER

class Letter(object):
    """ Letter class
    commit 1 (blagae): BLI 10
    reason: creation of stub for interaction with Word
    """
    letters = {
        'e' : LetterTypes.VOWEL,
        'a' : LetterTypes.VOWEL,
        'i' : LetterTypes.SEMIVOWEL,
        'u' : LetterTypes.SEMIVOWEL,
        't' : LetterTypes.CONSONANT,
        's' : LetterTypes.CONSONANT,
        'r' : LetterTypes.CONSONANT,
        'n' : LetterTypes.CONSONANT,
        'o' : LetterTypes.VOWEL,
        'm' : LetterTypes.CONSONANT,
        'c' : LetterTypes.CONSONANT,
        'l' : LetterTypes.CONSONANT,
        'p' : LetterTypes.CONSONANT,
        'd' : LetterTypes.CONSONANT,
        'q' : LetterTypes.CONSONANT,
        'b' : LetterTypes.CONSONANT,
        'g' : LetterTypes.CONSONANT,
        'f' : LetterTypes.CONSONANT,
        'h' : LetterTypes.CONSONANT,
        'x' : LetterTypes.HEAVYMAKER,
        'y' : LetterTypes.VOWEL,
        'k' : LetterTypes.CONSONANT,
        'z' : LetterTypes.HEAVYMAKER
        }

    def __init__(self, letter):
        """ construct a Letter by its contents """
        if not (len(letter) == 1 and isinstance(letter, str) and letter.isalpha()):
            raise ScansionException("wrong number of letters or not a valid character")
        self.letter = letter.lower()
        if self.letter == 'v':
            self.letter = 'u'
        elif self.letter == 'j':
            self.letter = 'i'
        if not self.isValidLetter():
            raise ScansionException("not a valid letter")

    def __eq__(self, other): 
        """ Letters are equal if they have exactly the same character
        Case insensitivity is enforced by the constructor
        """
        return self.__str__() == other.__str__()
    
    def __str__(self):
        return self.letter
    def __repr__(self):
        return self.letter

    def isValidLetter(self):
        """ a letter is only valid if it figures in the list of legal characters
        currently the only invalid (Roman) letters are W, V and J
        but V and J are replaced by their vocalic values U and I in the constructor
        """
        return self.letter in Letter.letters