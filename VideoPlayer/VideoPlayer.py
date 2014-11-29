#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   VideoPlayer.py por:
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

import gtk

from PlayerControls import PlayerControls
from ProgressPlayer import ProgressPlayer

from Globales import COLORES


class VideoPlayer(gtk.EventBox):

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, COLORES["text"])

        vbox = gtk.VBox()
        self.visor = Visor()
        self.progress = ProgressPlayer()
        self.control = PlayerControls()

        vbox.pack_start(self.visor, True, True, 0)
        vbox.pack_start(self.progress, False, True, 0)
        vbox.pack_start(self.control, False, True, 0)

        self.add(vbox)
        self.show_all()

        self.control.connect("accion-controls", self.__control)
        self.progress.connect("seek", self.__seek)
        self.progress.connect("volumen", self.__volumen)

    def __seek(self, widget, valor):
        print valor

    def __volumen(self, widget, valor):
        print valor

    def __control(self, widget, accion):
        print accion


class Visor(gtk.DrawingArea):

    def __init__(self):

        gtk.DrawingArea.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, COLORES["text"])

        self.show_all()
