import unittest

from elisio.parser.versefactory import VerseFactory
from elisio.parser.versefactory import VerseType
from versescanner.util.utils import set_django

set_django()

from versescanner.util.batchutils import scan_verses
from versescanner.bridge.DatabaseBridge import DatabaseBridge
from versescanner.models.metadata import DatabaseVerse
from versescanner.models.scan import WordOccurrence


class TestHexameter(unittest.TestCase):

    def test_hexameter_scan_all(self):
        """ frivolous check to see how many verses work """
        save = WordOccurrence.objects.count() > 0
        threshold = 14 if save else 12
        # verses = DatabaseVerse.objects.all()
        verses = DatabaseVerse.objects.filter(id__lte=500)
        worked, failed, worked_wo_dict = scan_verses(verses, "test_hexameter_scan_all")
        # canary test: over 91% of verses must succeed
        result = str(worked_wo_dict) + " worked without dict, " + str(worked) + " worked, " + str(failed) + " failed"
        if worked / failed < threshold:
            self.fail(result)
        # canary test: if no verses fail, then we are probably too lax
        elif failed == 0:
            self.fail("improbable result: " + result)
        else:
            print(result)

    def test_hexameter_scan_for_debug(self):
        """
        12811: nascetur pulchra Troianus origine Caesar,
        """
        dbverse = DatabaseVerse.objects.get(pk=3306)
        VerseFactory.create(dbverse.contents, DatabaseBridge(), classes=VerseType.HEXAMETER)
