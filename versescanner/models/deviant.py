import re

from django.db.models import CharField, ForeignKey, IntegerField, Model
from django.db.models.deletion import CASCADE
from elisio.exceptions import WordException
from elisio.syllable import Syllable, Weight
from enumfields import EnumField

from versescanner.util.utils import set_django

set_django()

class DeviantWord(Model):
    """ model class for the Engine: highest level """
    words = []
    stem = CharField(max_length=25)

    @staticmethod
    def find(text):
        """ check for a regex in the db that matches this word """
        DeviantWord.get_list()
        result = [word for word in DeviantWord.words
                  if re.compile(word.stem).match(text)]
        if len(result) > 1:
            raise WordException
        if not result:
            return None
        return result[0]

    def get_syllables(self):
        """ get the syllables for this deviant word """
        sylls = DeviantSyllable.objects.filter(word=self).order_by('sequence')
        result = []
        for syll in sylls:
            result.append(Syllable.make_empty_syllable(syll.contents, syll.weight))  # TODO may break
        return result

    @staticmethod
    def get_list():
        """ get full list of deviant words in memory """
        if len(DeviantWord.words) < 1:
            DeviantWord.words = DeviantWord.objects.all()


class DeviantSyllable(Model):
    """ model class for the Engine: lowest level """
    word = ForeignKey(DeviantWord, CASCADE)
    weight = EnumField(Weight)
    contents = CharField(max_length=8)
    sequence = IntegerField()
    index_together = [["word", "sequence"]]
