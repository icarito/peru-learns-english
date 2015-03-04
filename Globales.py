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
import espeak

BASE_PATH = os.path.dirname(__file__)

COLORES = {
    "window": gdk.color_parse("#ffffff"),
    "toolbar": gdk.color_parse("#778899"),
    "contenido": gdk.color_parse("#778899"),
    "menu": gdk.color_parse("#ff6600"),
    "title": gdk.color_parse("#FE8200"),
    "text": gdk.color_parse("#000000"),
    "rojo": gdk.color_parse("#fe6e00"),
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


def get_user_dict(user):
    dirpath = os.path.join(os.environ["HOME"], ".Ple")
    userpath = os.path.join(dirpath, user, "User")
    return __get_dict(userpath)


def guardar(_dict, topic, palabra, respuesta, force_date=None):
    dirpath = os.path.join(os.environ["HOME"], ".Ple")
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    userpath = os.path.join(dirpath,
        "%s %s" % (_dict["Nombre"], _dict["Apellido"]))
    if not os.path.exists(userpath):
        os.mkdir(userpath)
        upath = os.path.join(userpath, "User")
        __set_dict(upath, _dict)
    filepath = os.path.join(userpath, os.path.basename(topic))

    if not force_date:
        fecha = str(datetime.date.today())
    else:
        fecha = str(force_date)
    _dict = __get_dict(filepath)
    if not _dict.get(palabra, False):
        _dict[palabra] = {}
    _dict[palabra][fecha] = respuesta

    # n es el numero de repeticion
    n = len(_dict[palabra])

    EF = _dict[palabra].get("EF", False)
    if EF:
        EF = float(EF[1])
    else:
        EF = 2.5
    #EF = EF + (0.1 - (5 - respuesta) * (0.08 + (5 - respuesta) * 0.02))
    if not respuesta < 3:
        EF = EF - 0.8 + 0.28 * respuesta - 0.02 * respuesta * respuesta
    if EF < 1.3:
        EF = 1.3

    def calc_I(n):
        if n==1:
            return 1
        elif n==2:
            return 6
        elif n>2:
            return calc_I(n-1) * EF

    I = calc_I(n)

    newdate = datetime.date.today() + datetime.timedelta(days=I)
    _dict[palabra]["EF"] = [str(newdate.isoformat()), EF]
    __set_dict(filepath, _dict)


def get_flashcards_previews(topic):
    return __read_cvs(topic)


def get_vocabulario(topic, _dict, force_date=None):
    vocabulario = __read_cvs(topic)

    # Cargar Persistencia
    dirpath = os.path.join(os.environ["HOME"], ".Ple")
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    userpath = os.path.join(dirpath,
        "%s %s" % (_dict["Nombre"], _dict["Apellido"]))
    if not os.path.exists(userpath):
        os.mkdir(userpath)
        upath = os.path.join(userpath, "User")
        __set_dict(upath, _dict)
    filepath = os.path.join(userpath, os.path.basename(topic))
    _dict = __get_dict(filepath)

    # Verificar Fechas
    if not force_date:
        hoy = datetime.date.today()
    else:
        hoy = force_date
    hoy = datetime.datetime.strptime(str(hoy), "%Y-%m-%d")

    ret = []
    for item in vocabulario:
        pal = _dict.get(item[0], False)
        if pal:
            # Si hay persistencia para esta palabra
            fecha, ef = _dict[item[0]]["EF"]
            fecha = datetime.datetime.strptime(fecha, "%Y-%m-%d")
            if fecha <= hoy:
                # FIXME: Se cargan todas las salteadas + las de hoy
                ret.append(item)
            else:
                continue
        else:
            ret.append(item)
    return ret


def decir_demorado(pitch, speed, word_gap, voice, text):
    wavpath = "/dev/shm/speak.wav"
    commands.getoutput('espeak -s%s -p%s -g%s -w%s -v%s \"%s\"' % (
        pitch, speed, word_gap, wavpath, voice, text))
    commands.getoutput(
        'gst-launch-0.10 playbin2 uri=file:///dev/shm/speak.wav')


def decir(pitch, speed, word_gap, voice, text):
    global _audio
    try:
        _audio.speak(text, pitch, speed, voice)
    except:
        _audio = espeak.AudioGrab()
        _audio.speak(text, pitch, speed, voice)

class Dialog(gtk.Dialog):

    def __init__(self, title, parent, buttons, text):

        gtk.Dialog.__init__(self, title=title, parent=parent, buttons=buttons)

        self.modify_bg(gtk.STATE_NORMAL, COLORES["window"])
        self.set_border_width(15)
        label = gtk.Label(text)
        label.show()
        self.vbox.pack_start(label, True, True, 5)
        self.connect("realize", self.__realize)

    def __realize(self, widget):
        decir(50, 57, 0, "en-gb", self.get_title())

def is_xo():
    return os.path.exists('/etc/olpc-release')

