#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Globales.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   Uruguay

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import os
import commands
import csv
import gtk
import datetime
import json
import codecs
from gtk import gdk

COLORES = {
    "window": gdk.color_parse("#ffffff"),
    "toolbar": gdk.color_parse("#778899"),
    "contenido": gdk.color_parse("#778899"),
    "menu": gdk.color_parse("#ff6600"),
    "title": gdk.color_parse("#FE8200"),
    "text": gdk.color_parse("#000000"),
    "rojo": gdk.color_parse("#ff0000"),
    "verde": gdk.color_parse("#00ff00"),
    "amarillo": gdk.color_parse("#ffff00"),
    }

"""
user
    topics
        flashcard
            dia - respuesta
            dia - respuesta
            dia - respuesta
            fecha - factor
        flashcard
            dia - respuesta
            dia - respuesta
            dia - respuesta
            fecha - factor
"""


def __get_dict(path):
    if not os.path.exists(path):
        return {}
    archivo = codecs.open(path, "r", "utf-8")
    _dict = json.JSONDecoder(encoding="utf-8").decode(archivo.read())
    archivo.close()
    return _dict


def __set_dict(path, _dict):
    archivo = open(path, "w")
    archivo.write(
        json.dumps(
            _dict,
            indent=4,
            separators=(", ", ":"),
            sort_keys=True))
    archivo.close()


def __read_cvs(topic):
    csvfile = os.path.join(topic, "vocabulario.csv")
    reader = csv.reader(file(csvfile))
    vocabulario = list(reader)
    return vocabulario[1:]


def guardar(topic, palabra, respuesta):
    dirpath = os.path.join(os.environ["HOME"], ".Ple")
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    filepath = os.path.join(dirpath, os.path.basename(topic))

    fecha = str(datetime.date.today())
    _dict = __get_dict(filepath)
    if not _dict.get(palabra, False):
        _dict[palabra] = {}
    _dict[palabra][fecha] = respuesta

    new = _dict[palabra].get("new", False)
    if new:
        new = float(new[1])
    else:
        new = 2.5
    new = new + (0.1 - (5 - respuesta) * (0.08 + (5 - respuesta) * 0.02))

    newdate = datetime.date.today() + datetime.timedelta(days=new)
    _dict[palabra]["new"] = [str(newdate.isoformat()), new]
    __set_dict(filepath, _dict)


def get_flashcards_previews(topic):
    return __read_cvs(topic)


def get_vocabulario(topic):
    vocabulario = __read_cvs(topic)

    # Cargar Persistencia
    dirpath = os.path.join(os.environ["HOME"], ".Ple")
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    filepath = os.path.join(dirpath, os.path.basename(topic))
    _dict = __get_dict(filepath)

    # Verificar Fechas
    hoy = datetime.date.today()
    hoy = datetime.datetime.strptime(str(hoy), "%Y-%m-%d")

    ret = []
    for item in vocabulario:
        pal = _dict.get(item[0], False)
        if pal:
            # Si hay persistencia para esta palabra
            fecha, ef = _dict[item[0]]["new"]
            fecha = datetime.datetime.strptime(fecha, "%Y-%m-%d")
            if fecha <= hoy:
                # FIXME: Se cargan todas las salteadas + las de hoy
                ret.append(item)
        else:
            ret.append(item)
    return ret


def decir(pitch, speed, word_gap, voice, text):
    wavpath = "/dev/shm/speak.wav"
    commands.getoutput('espeak -p%s -s%s -g%s -w%s -v%s \"%s\"' % (
        pitch, speed, word_gap, wavpath, voice, text))
    commands.getoutput(
        'gst-launch-0.10 playbin2 uri=file:///dev/shm/speak.wav')
    return False
