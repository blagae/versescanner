from elisio.Sound import SoundFactory
from elisio.Syllable import Weight
from elisio.bridge.Bridge import Bridge
from versescanner.models.deviant import DeviantWord
from versescanner.models.scan import WordOccurrence


class DatabaseBridge(Bridge):

    def __init__(self, use_dict=True):
        self.use_dict = use_dict

    def split_from_deviant_word(self, lexeme):
        """
        if the word can be found in the repository of Deviant Words,
        we should use that instead
        """
        deviant = DeviantWord.find(lexeme)
        if deviant:
            return deviant.get_syllables()
        return []

    def use_dictionary(self, word):
        if not self.use_dict:
            return []
        structs = []
        for hit in WordOccurrence.objects.filter(word=word):
            strc = hit.struct
            if len(strc) == 1 and strc[-1] == "0":
                continue
            if len(strc) > 1 and (strc[-1] == "3" or strc[-1] == "0"):
                strc = strc[:-1]
            if strc not in structs:
                structs.append(strc)
        return structs

    def make_entry(self, txt, strct, db_id):
        return WordOccurrence(word=txt, struct=strct, verse_id=db_id)

    def dump(self, entries):
        WordOccurrence.objects.bulk_create(entries)