import functools
import unittest

from whitakers_words.parser import Parser

from versescanner.util.utils import set_django

set_django()

from versescanner.models.metadata import Verse


def wat(a, b):
    c = max(a, b[1])
    if c > a:
        print(b[0])
    return c

class TestWhitaker(unittest.TestCase):

    def test_whitaker_all(self):
        parser = Parser()
        dicc = {}
        # verses = Verse.objects.filter(id__lte=500)
        verses = Verse.objects.all()
        for verse in verses:
            for word in verse.contents.split():
                floo = ''.join(x for x in word if x.isalpha())
                if floo and floo not in dicc:
                    result = parser.parse(floo)
                    dicc[floo] = 0
                    for form in result.forms:
                        dicc[floo] += len(form.analyses)
        