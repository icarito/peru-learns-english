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

import commands
import csv
import gtk
from gtk import gdk

COLORES = {
    "window": gdk.color_parse("#ffffff"),
    "toolbar": gdk.color_parse("#778899"),
    "contenido": gdk.color_parse("#778899"),
    "title": gdk.color_parse("#FE8200"),
    "text": gdk.color_parse("#000000"),
    "rojo": gdk.color_parse("#ff0000"),
    "verde": gdk.color_parse("#00ff00"),
    "amarillo": gdk.color_parse("#ffff00"),
    }


def get_vocabulario(csvfile):
    reader = csv.reader(file(csvfile))
    return list(reader)


def decir(pitch, speed, word_gap, voice, text):
    wavpath = "/dev/shm/speak.wav"
    commands.getoutput('espeak -p%s -s%s -g%s -w%s -v%s \"%s\"' % (
        pitch, speed, word_gap, wavpath, voice, text))
    commands.getoutput(
        'gst-launch-0.10 playbin2 uri=file:///dev/shm/speak.wav')
    return False
