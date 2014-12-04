#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   VideoView.py por:
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
import gtk
import gobject

from VideoPlayer.VideoPlayer import VideoPlayer
from JAMediaImagenes.ImagePlayer import ImagePlayer

from Globales import COLORES
from Globales import get_vocabulario


class VideoView(gtk.EventBox):

    __gsignals__ = {
    "flashcards": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING, ))}

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, COLORES["toolbar"])
        self.set_border_width(4)

        self.topic = False

        tabla = gtk.Table(rows=10, columns=3, homogeneous=True)
        tabla.set_property("column-spacing", 5)
        tabla.set_property("row-spacing", 5)
        tabla.set_border_width(4)

        self.titulo = gtk.Label("Título")
        self.videoplayer = VideoPlayer()
        self.links = gtk.Label("Links")

        tabla.attach(self.titulo, 0, 2, 0, 1)
        tabla.attach(self.videoplayer, 0, 2, 1, 9)
        tabla.attach(self.links, 0, 2, 9, 10)

        flashcards = gtk.Button("FlashCards")

        self.imagen_juego = DrawingArea()
        tabla.attach(self.imagen_juego, 2, 3, 0, 4)
        tabla.attach(flashcards, 2, 3, 4, 6)
        tabla.attach(DrawingArea(), 2, 3, 6, 10)

        self.add(tabla)
        self.show_all()

        flashcards.connect("clicked", self.__emit_flashcards)

    def __emit_flashcards(self, widget):
        self.emit("flashcards", self.topic)

    def stop(self):
        self.videoplayer.stop()
        self.hide()

    def run(self, topic):
        self.show()
        self.topic = topic
        self.videoplayer.load(os.path.join(self.topic, "video.ogv"))
        gobject.idle_add(self.imagen_juego.load, topic)


class DrawingArea(gtk.DrawingArea):

    def __init__(self):

        gtk.DrawingArea.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, COLORES["text"])

        self.vocabulario = []
        self.index_select = 1
        self.imagenplayer = False
        self.path = False

        self.show_all()

    def load(self, topic):
        csvfile = os.path.join(topic, "vocabulario.csv")
        self.vocabulario = get_vocabulario(csvfile)
        self.index_select = 1
        self.path = os.path.join(topic, "Imagenes",
            "%s.png" % self.vocabulario[self.index_select][0])
        if self.imagenplayer:
            self.imagenplayer.stop()
            del(self.imagenplayer)
            self.imagenplayer = False
        self.imagenplayer = ImagePlayer(self)
        self.imagenplayer.load(self.path)
        return False
