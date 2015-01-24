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
import pango

from ConfigParser import SafeConfigParser

from VideoPlayer.VideoPlayer import VideoPlayer
from JAMediaImagenes.ImagePlayer import ImagePlayer

from Globales import COLORES
from Globales import get_flashcards_previews


class VideoView(gtk.EventBox):

    __gsignals__ = {
    "flashcards": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, )),
    "game": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING, ))}

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, COLORES["contenido"])
        self.set_border_width(4)

        self.full = False
        self.topic = False

        tabla = gtk.Table(rows=10, columns=3, homogeneous=True)
        tabla.set_property("column-spacing", 8)
        tabla.set_property("row-spacing", 8)
        tabla.set_border_width(8)

        self.titulo = gtk.Label("Título")
        self.titulo.modify_font(pango.FontDescription("DejaVu Sans Bold 20"))
        self.titulo.modify_fg(gtk.STATE_NORMAL, COLORES["window"])
        self.videoplayer = VideoPlayer()

        self.links = gtk.LinkButton("http://pe.sugarlabs.org/", "Links")
        self.links.modify_font(pango.FontDescription("DejaVu Sans 18"))
        self.links.modify_fg(gtk.STATE_NORMAL, COLORES["text"])

        tabla.attach(self.titulo, 0, 2, 0, 1)
        tabla.attach(self.videoplayer, 0, 2, 1, 9)
        tabla.attach(self.links, 0, 2, 9, 10)

        flashcards = gtk.Button()
        flashcards.set_relief(gtk.RELIEF_NONE)
        imagen = gtk.Image()
        imagen.set_from_file("Imagenes/flashcards.png")
        flashcards.modify_bg(gtk.STATE_NORMAL, COLORES["toolbar"])
        flashcards.add(imagen)

        self.imagen_juego = GameImage()
        self.flashcards_preview = FlashCardsPreview()

        tabla.attach(self.imagen_juego, 2, 3, 1, 4)
        tabla.attach(flashcards, 2, 3, 4, 6)
        tabla.attach(self.flashcards_preview, 2, 3, 6, 10)

        self.add(tabla)
        self.show_all()

        flashcards.connect("clicked", self.__emit_flashcards)
        self.imagen_juego.connect("button-press-event", self.__emit_game)
        self.videoplayer.connect("full", self.set_full)
        self.videoplayer.connect("endfile", self.__force_unfull)

    def __force_unfull(self, widget):
        if self.full:
            self.set_full(False)
        self.videoplayer.pause()

    def __emit_game(self, widget, event):
        self.emit("game", self.topic)

    def __emit_flashcards(self, widget):
        dialog = DialogLogin(self.get_toplevel())
        ret = dialog.run()
        dialog.destroy()
        if ret == gtk.RESPONSE_ACCEPT:
            self.emit("flashcards", (self.topic, {"Nombre": "Andres", "Apellido": "Rodriguez", "edad": 8, "Escuela": "N° 35", "Grado": "4°"}))

    def set_full(self, widget):
        tabla = self.get_child()
        for child in tabla.children():
            child.hide()

        if self.full:
            self.videoplayer.hide()
            tabla.set_homogeneous(True)
            tabla.set_property("column-spacing", 8)
            tabla.set_property("row-spacing", 8)
            self.show_all()
            self.full = False
        else:
            tabla.set_homogeneous(False)
            tabla.set_property("column-spacing", 0)
            tabla.set_property("row-spacing", 0)
            self.videoplayer.show()
            self.full = True

        self.videoplayer.stop()
        self.videoplayer.load(os.path.join(self.topic, "video.ogv"))

    def stop(self):
        self.videoplayer.stop()
        self.imagen_juego.stop()
        self.flashcards_preview.stop()
        if self.flashcards_preview.control:
            gobject.source_remove(self.flashcards_preview.control)
            self.flashcards_preview.control = False
        self.hide()

    def run(self, topic):
        self.show()
        self.topic = topic
        self.videoplayer.load(os.path.join(self.topic, "video.ogv"))
        self.imagen_juego.load(topic)
        self.flashcards_preview.load(topic)

        parser = SafeConfigParser()
        metadata = os.path.join(topic, "topic.ini")
        parser.read(metadata)

        self.titulo.set_text("Topic: " + parser.get('topic', 'title'))
        self.links.set_uri(parser.get('topic', 'link'))
        self.links.set_label(parser.get('topic', 'link'))
        self.full = False
        self.set_full(False)


class GameImage(gtk.DrawingArea):

    def __init__(self):

        gtk.DrawingArea.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, COLORES["text"])
        self.add_events(gtk.gdk.BUTTON_PRESS_MASK)

        self.imagenplayer = False
        self.path = False

        self.show_all()

    def stop(self):
        if self.imagenplayer:
            self.imagenplayer.stop()
            del(self.imagenplayer)
            self.imagenplayer = False

    def load(self, topic):
        self.stop()
        self.path = os.path.abspath("Imagenes/juego1.png")
        self.imagenplayer = ImagePlayer(self)
        self.imagenplayer.load(self.path)
        return False


class FlashCardsPreview(gtk.EventBox):

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, COLORES["window"])

        self.vocabulario = []
        self.index_select = 0
        self.imagenplayer = False
        self.path = False
        self.control = False
        self.topic = False

        self.drawing = gtk.DrawingArea()
        self.label = gtk.Label("Text")
        self.drawing.modify_bg(gtk.STATE_NORMAL, COLORES["window"])
        self.label.modify_bg(gtk.STATE_NORMAL, COLORES["window"])
        self.label.modify_fg(gtk.STATE_NORMAL, COLORES["text"])
        self.label.modify_font(pango.FontDescription("DejaVu Sans 18"))

        tabla = gtk.Table(rows=1, columns=2, homogeneous=True)
        tabla.attach(self.drawing, 0, 1, 0, 1)
        tabla.attach(self.label, 1, 2, 0, 1)

        self.add(tabla)
        self.show_all()

    def __run_secuencia(self):
        self.stop()
        self.path = os.path.join(self.topic, "Imagenes",
            "%s.png" % self.vocabulario[self.index_select][0])
        self.imagenplayer = ImagePlayer(self.drawing)
        self.imagenplayer.load(self.path)
        self.label.set_text(self.vocabulario[self.index_select][1])
        if self.index_select < len(self.vocabulario) - 1:
            self.index_select += 1
        else:
            self.index_select = 0
        return True

    def stop(self):
        if self.imagenplayer:
            self.imagenplayer.stop()
            del(self.imagenplayer)
            self.imagenplayer = False

    def load(self, topic):
        self.stop()
        self.topic = topic
        self.vocabulario = get_flashcards_previews(self.topic)
        self.index_select = 0
        self.__run_secuencia()
        if not self.control:
            self.control = gobject.timeout_add(3000, self.__run_secuencia)
        return False


class DialogLogin(gtk.Dialog):

    def __init__(self, parent_window=None):

        gtk.Dialog.__init__(self, title="Loging", parent=parent_window,
            buttons= ("OK", gtk.RESPONSE_ACCEPT,
            "Cancelar", gtk.RESPONSE_CANCEL))

        # self.set_decorated(False)
        self.modify_bg(gtk.STATE_NORMAL, COLORES["window"])
        self.set_border_width(15)
