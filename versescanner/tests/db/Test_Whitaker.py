import unittest
from whitakers_words.parser import Parser
from versescanner.util.utils import set_django

set_django()

from versescanner.models.metadata import DatabaseVerse


class TestWhitaker(unittest.TestCase):

    def test_whitaker_all(self):
        parser = Parser()
        # verses = DatabaseVerse.objects.all()
        verses = DatabaseVerse.objects.filter(id__lte=500)
        for verse in verses:
            for word in verse.contents.split():
                try:
                    floo = ''.join(x for x in word if x.isalpha())
                    if floo:
                        parser.parse(floo)
