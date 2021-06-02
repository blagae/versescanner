import re
from typing import Optional

from django.db.models import CharField, ForeignKey, IntegerField, Model
from django.db.models.deletion import CASCADE
from elisio.exceptions import WordException
from elisio.syllable import Syllable, Weight
from enumfields import EnumField

from ..util.utils import set_django

set_django()

class DeviantWord(Model):
    """ model class for the Engine: highest level """
    stem = CharField(max_length=25)

    @staticmethod
    def find(text) -> Optional["DeviantWord"]:
        """ check for a regex in the db that matches this word """
        result = [word for word in DeviantWord.objects.all() if re.compile(word.stem).match(text)]
        if result:
            return result[0]
        return None

    def get_syllables(self) -> list[Syllable]:
        """ get the syllables for this deviant word """
        sylls = DeviantSyllable.objects.filter(word=self).order_by('sequence')
        return [Syllable.make_empty_syllable(syll.contents, syll.weight) for syll in sylls]


class DeviantSyllable(Model):
    """ model class for the Engine: lowest level """
    word = ForeignKey(DeviantWord, CASCADE)
    weight = EnumField(Weight)
    contents = CharField(max_length=8)
    sequence = IntegerField()
    index_together = [["word", "sequence"]]
