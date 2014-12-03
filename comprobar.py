#!/bin/env python2
# *-* coding: utf-8 *-*

import csv
import os

# contador y comprobador de vocabularios

flashcards = 0
images = 0
sounds = 0
videos = 0
topics = 0

archivos_csv = [f for f in os.listdir(".") if f.endswith("csv")]

for archivo in archivos_csv:
    id_topic = archivo[:-4]
    topics = topics + 1

    video = "../Video/" + id_topic + ".ogv"
    if os.path.exists(video):
        print "Existe " + video
        videos = videos + 1
    video = None

    r = csv.DictReader(file(archivo))
    for row in r:
        id = row['id']
        vocablo = row['term']
        imagen = "../Imagen/" + id_topic + "/" + id + ".png"
        if os.path.exists(imagen):
            print "Existe " + imagen
            images = images + 1
        audio = "../Audio/" + id_topic + "/" + id + ".ogg"
        if os.path.exists(audio):
            print "Existe " + audio
            sounds = sounds + 1
        flashcards = flashcards + 1
        audio = imagen = False

print "\n Reporte\n =========="
print
print " Topics = " + str(topics)
print " Videos = " + str(videos)
print " Términos = " + str(flashcards)
print " Imagenes = " + str(images)
print " Sonidos = " + str(sounds)
print
