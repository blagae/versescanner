from django.db.models import (BooleanField, CharField, ForeignKey,
                              IntegerField, Max, Model)
from django.db.models.deletion import CASCADE
from elisio.parser.versefactory import VerseForm, VerseType
from enumfields import EnumField


class Period(Model):
    """ model class that contains a Period """
    name = CharField(max_length=20)
    start_year = IntegerField()
    end_year = IntegerField()
    description = CharField(max_length=200)

    def __repr__(self):
        return self.name


class Author(Model):
    """ model class that contains an Author """
    full_name = CharField(max_length=45)
    short_name = CharField(max_length=18)
    abbreviation = CharField(max_length=10)
    period = ForeignKey(Period, CASCADE)
    birth_year = IntegerField()
    dying_year = IntegerField()
    floruit_start = IntegerField()
    floruit_end = IntegerField()

    def get_parent(self):
        return None

    def __repr__(self):
        return self.short_name


class Genre(Model):
    """ model class that contains a Genre """
    name = CharField(max_length=20)
    description = CharField(max_length=200)

    def __repr__(self):
        return self.name


class Opus(Model):
    class Meta:
        verbose_name_plural = "opera"

    """ model class that contains an Opus """
    full_name = CharField(max_length=40)
    abbreviation = CharField(max_length=10)
    alternative_name = CharField(max_length=40)
    author = ForeignKey(Author, CASCADE)
    publication = IntegerField()
    genre = ForeignKey(Genre, CASCADE)

    def get_parent(self):
        return self.author

    def __repr__(self):
        return self.full_name


class Book(Model):
    """ model class that contains a Book """
    opus = ForeignKey(Opus, CASCADE)
    number = IntegerField()

    def get_parent(self):
        return self.opus

    def __repr__(self):
        return f"{self.opus} {self.number}"


class Poem(Model):
    """ model class that contains a Poem """
    book = ForeignKey(Book, CASCADE)
    number = IntegerField()
    nickname = CharField(max_length=20)
    verseForm = EnumField(VerseForm, default=VerseForm.HEXAMETRIC)

    def get_parent(self):
        return self.book

    def __repr__(self):
        return str(self.number)


class Verse(Model):
    """ model class that contains a Verse """
    poem = ForeignKey(Poem, CASCADE)
    number = IntegerField()
    alternative = CharField(max_length=1)
    contents = CharField(max_length=70)
    saved = BooleanField(default=False)
    verseType = EnumField(VerseType, default=VerseType.HEXAMETER)

    def get_parent(self):
        return self.poem

    def get_verse(self) -> str:
        """ create a Verse object from this Verse """
        return self.contents

    @staticmethod
    def get_maximum_verse_num(poem):
        """ get the highest verse number in this poem """
        return Verse.objects.filter(poem=poem).aggregate(Max('number'))['number__max']

    @staticmethod
    def get_verse_from_db(poem, verse):
        """ django.core.serializers requires this return value to be iterable (i.e. a resultset) """
        return Verse.objects.get(poem=poem, number=verse)
