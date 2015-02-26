import os
import datetime
import pprint
import difflib

_dict = {
    "Nombre": "Dummy",
    "Apellido": "bot",
    "Edad": "",
    "Escuela": "",
     "Grado": ""}

topic = "Topics/Topic_4"

from Globales import get_vocabulario, guardar

def grabar():
    vocabulario = get_vocabulario(topic, _dict)

    for item in vocabulario[:5]:
        guardar(_dict, os.path.abspath(topic), item[0], 0)
    for item in vocabulario[5:10]:
        guardar(_dict, os.path.abspath(topic), item[0], 3)
    for item in vocabulario[10:]:
        guardar(_dict, os.path.abspath(topic), item[0], 5)

def probar(n=15):
    for dias in range(0,15):

        today = datetime.date.today()
        target = today + datetime.timedelta(dias)

        try:
            old_vocab = vocabulario[:]
        except NameError:
            old_vocab = []

        vocabulario = get_vocabulario("Topics/Topic_4", _dict, override_date=target)
        vocabulario = map(lambda x: x[1], vocabulario)

        print "= Fecha", target

        #for item in vocabulario:

        #print list(difflib.unified_diff(old_vocab, vocabulario))
        print len(vocabulario)
        #pprint.pprint (vocabulario)

if __name__ == '__main__':
    grabar()
    probar()
