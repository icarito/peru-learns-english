#!/bin/env python2
# *-* coding: utf-8 *-*

# Validamos que tengamos todo lo que decimos que tenemos, y nada más.
import csv
import os
import glob
import datetime

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
<table id="vocab_tabla">
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
        <div> <!-- style="border: 1px solid black; margin: 0px; padding: 0px"--> 
        <img src="{{item.url}}" height="150px" width="150px"/><br />
        <b>{{ item.term }}</b></br>
        <!-- <br />
        {{ item.preg_alt }}<br />
        {{ item.resp_alt }}<br /> -->
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
                        result[orig_folder].append(linea)
                    except KeyError:
                        result[orig_folder] = [linea]
    
    return result

plantilla = Template(template)

vocabulario = obtener_vocabularios()
#pprint (vocabulario)

now = datetime.datetime.now()
fecha = "%i/%i/%i" % (now.day, now.month, now.year)

print plantilla.render(vocabulario=vocabulario, fecha=fecha)

