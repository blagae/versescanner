""" module for creating an xml file from given input """
from elisio.exceptions import ScansionException, VerseException
from elisio.parser.verse import Foot
from elisio.parser.versefactory import VerseFactory, VerseType

from ..bridge.DatabaseBridge import DatabaseBridge
from ..models.metadata import Verse
from ..models.scan import (Batch, DatabaseBatchItem, ObjectType,
                                      BatchRun, BatchRunResult)


def find_all_verses_containing(regex, must_be_parsed=False):
    import re
    dbverses = Verse.objects.all()
    total = []
    for dbverse in dbverses:
        words = VerseFactory.split(dbverse.contents)
        boolean = False
        for word in words:
            boolean = boolean or re.compile(regex).match(word.text)
        if must_be_parsed:
            try:
                VerseFactory.create(dbverse.contents).parse()
            except ScansionException:
                continue
        if boolean:
            total.append(dbverse.contents)
    return total


def scan_verses(dbverses, initiator):
    batch = Batch()
    batch.save()
    batch_item = DatabaseBatchItem()
    batch_item.batch = batch
    batch_item.object_type = ObjectType.ALL
    batch_item.object_id = 0
    batch_item.save()
    session = BatchRun()
    #session.batch = batch
    #session.initiator = initiator
    session.save()
    return scan_session(dbverses, session)


def scan_session(dbverses, session):
    worked = 0
    worked_without_dict = 0
    failed = 0
    for dbverse in dbverses:
        verse_saved = dbverse.saved
        scan_result = BatchRunResult()
        scan_result.session = session
        scan_result.verse = dbverse
        scan_result.scanned_as = dbverse.verseType
        try:
            verse = VerseFactory.create(dbverse.contents, dbverse.id, DatabaseBridge(False), creators=dbverse.verseType)
            dbverse.saved = True
            scan_result.structure = verse.structure()
            worked_without_dict += 1
        except VerseException:
            try:
                verse = VerseFactory.create(dbverse.contents, dbverse.id, DatabaseBridge(), creators=dbverse.verseType)
                dbverse.saved = True
                scan_result.structure = verse.structure()
            except VerseException as exc:
                failed += 1
                dbverse.saved = False
                try:
                    scan_result.failure = exc.exceptions[0].message[:69]
                except IndexError:
                    scan_result.failure = exc.message[:69]
                scan_result.structure = ""
            else:
                worked += 1
        except ScansionException as exc:
            failed += 1
            scan_result.failure = exc.message[:69]
            dbverse.saved = False
            scan_result.structure = ""
        else:
            worked += 1
        if verse_saved != dbverse.saved or scan_result.failure:
            dbverse.save()
        scan_result.save()
    return worked, failed, worked_without_dict


def scan_batch_from_flat_file(file):
    with open(file, "r", encoding='utf-8') as file:
        j = 0
        for dbverse in file.readlines():
            try:
                verse = VerseFactory.create(dbverse, DatabaseBridge(), creators=VerseType.HEXAMETER)
                d = "\t"
                for i in range(4):
                    if verse.feet[i] == Foot.DACTYLUS:
                        d += "D"
                    else:
                        d += "S"
                print(str(j) + d)
            except VerseException:
                print(str(j) + "\tfailed")
            j += 1
