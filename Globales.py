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

import csv
import chardet
import gtk
from gtk import gdk

COLORES = {
    "window": gdk.color_parse("#ffffff"),
    "toolbar": gdk.color_parse("#778899"),
    "text": gdk.color_parse("#000000"),
    }


def get_vocabulario(csvfile):
    item = []
    archivo = open(csvfile, 'rb')
    encoding = chardet.detect(archivo.read())['encoding']
    archivo.seek(0)
    reader = csv.reader(archivo, dialect='excel', delimiter=',')
    for index, row in enumerate(reader):
        row = [x.decode(encoding) for x in row]
        item.append(row)
    return item
