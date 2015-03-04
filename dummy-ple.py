import os
import datetime
import pprint
import difflib
import random

_dict = {
    "Nombre": "Dummy",
    "Apellido": "bot",
    "Edad": "",
    "Escuela": "",
     "Grado": ""}

topic = "Topics/Topic_4"

from Globales import get_vocabulario, guardar

def grabar(n=0):

    today = datetime.date.today()
    target = today + datetime.timedelta(n)

    vocabulario = get_vocabulario(topic, _dict, force_date=target)
    vocabulario = map(lambda x: x[1], vocabulario)

    for item in vocabulario:
        #if random.choice([True, False]):
        n = random.choice([3,5])
        guardar(_dict, os.path.abspath(topic), item, n, force_date=target)

def probar(n):

    for dias in range(0,n):

        today = datetime.date.today()
        target = today + datetime.timedelta(dias)

        try:
            old_vocab = vocabulario[:]
        except NameError:
            old_vocab = []

        vocabulario = get_vocabulario("Topics/Topic_4", _dict, force_date=target)
        vocabulario = map(lambda x: x[1], vocabulario)

        print "= Fecha", target

        #for item in vocabulario:

        #print list(difflib.unified_diff(old_vocab, vocabulario))
        print len(vocabulario)
        #pprint.pprint (vocabulario)
        grabar(n)


if __name__ == '__main__':
    #grabar()
    probar(45)
