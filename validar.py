#!/bin/env python2
# *-* coding: utf-8 *-*

# Validamos que tengamos todo lo que decimos que tenemos, y nada más.
import csv
import os
import glob
import datetime

from ConfigParser import SafeConfigParser

from jinja2 import Template

from pprint import pprint

basedir = "Topics"

template = """
<html>
<head>
<style>
table {
    border: 1px solid black;
    }
.container>div {
    display:inline-block;
    vertical-align:top;
    text-align: center;
    float: lefft}
</style>
</head>
<body>
<table id="vocab_tabla"> <!-- style="background-color: grey"-->
<h1>PLE Flashcards Inventory: {{fecha}}</h1>
{% for topic in vocabulario.keys()|sort %}
    <tr>
    <td>
    <br />
    <!-- br /-->
    <div align="center">
        <h1>{{ topic }}</h1>
    <div>
    <div class="container">
    {% for item in vocabulario[topic] %}
        <div style="border: 1px solid black; margin: 10px; padding: 10px"> 
        <img src="{{item.url}}" height="150px" width="150px"/><br />
        <b>{{ item.term }}</b></br>
        <br />
        {{ item.preg_alt }}<br />
        {{ item.resp_alt }}<br />
        </div>
    {% endfor %}
    </div>
    </td>
    </tr>
{% endfor %}
</table>
<body>
</html>
"""

def obtener_vocabularios():
    
    result = {}
    for folder in os.listdir(basedir):
        orig_folder = folder
        folder = os.path.join(basedir, folder)

        parser = SafeConfigParser()
        metadata = os.path.join(folder, "topic.ini")
        parser.read(metadata)

        title = parser.get('topic', 'title')

        if os.path.isdir(folder):
            vocabulario_file = os.path.join(folder, "vocabulario.csv")
            if os.path.exists(vocabulario_file):
                tabla = csv.DictReader(file(vocabulario_file))
                for linea in tabla:
                    img_folder = os.path.join(folder, "Imagenes")
                    linea["filename"] = os.path.join(img_folder, linea["id"]+".png")
                    linea["url"] = "file://" + os.path.abspath(linea["filename"])
                    if not linea.get("preg_alt"):
                        linea["preg_alt"] = "What is this?"
                    try:
                        result[title].append(linea)
                    except KeyError:
                        result[title] = [linea]
    
    return result

def validar_vocabularios(vocabulario):
    
    faltantes = []
    existentes = glob.glob("Topics/*/Imagenes/*.png")
    for topic in vocabulario.keys():
        for item in vocabulario[topic]:
            if item['filename'] in existentes:
                #print item['term'], "OK"
                existentes.pop(existentes.index(item['filename']))
            else:
                url = "file://" + os.path.abspath(item["filename"])
                faltantes.append( {"url": url, "term": item['filename']} )

    huerfanas = []
    dirname = ""
    for imagen in sorted(existentes):
        # USE PARA CREAR REGISTROS CSV
        #if os.path.dirname(imagen) != dirname:
        #    print " ====", os.path.dirname(imagen)
        #    dirname = os.path.dirname(imagen)
        #print os.path.basename(imagen)[:-4] + "," + \
        #      os.path.basename(imagen)[:-4] + ",,"
              
        url = "file://" + os.path.abspath(imagen)
        huerfanas.append( {"url":url, "term": imagen} )
    return faltantes, huerfanas

plantilla = Template(template)

vocabulario = obtener_vocabularios()
faltantes, huerfanas = validar_vocabularios(vocabulario)

if faltantes:
    vocabulario["FILES REFERENCED BUT NO IMAGE FOUND"] = faltantes
if huerfanas:
    vocabulario["IMAGES FOUND WITHOUT REFERENCE"] = huerfanas
#pprint (vocabulario)

now = datetime.datetime.now()
fecha = "%i/%i/%i" % (now.day, now.month, now.year)

print plantilla.render(vocabulario=vocabulario, fecha=fecha)

