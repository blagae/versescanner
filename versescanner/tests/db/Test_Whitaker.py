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
        """ this method is for stupid exploration testing """
        parser = Parser()
        dicc = dict()
        quoo = dict()
        i = 0
        # verses = Verse.objects.filter(id__lte=500)
        verses = Verse.objects.all()
        for verse in verses:
            croo = set()
            for word in verse.contents.split():
                floo = ''.join(x for x in word if x.isalpha())
                if floo and floo not in dicc:
                    result = parser.parse(floo)
                    dicc[floo] = 0
                    for form in result.forms:
                        if form.text not in quoo:
                            txts = {analysis.lexeme for analysis in form.analyses.values()}
                            quoo[form.text] = txts
                            for x in txts:
                                if x.id and x.id in croo:
                                    i += 1
                                croo.add(x.id)
                        dicc[floo] += len(form.analyses)
        shmoo = {k:v for k, v in quoo.items() if len(v) > 1}
        return dicc
