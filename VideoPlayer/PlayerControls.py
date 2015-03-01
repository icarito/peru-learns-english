#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   PlayerControls.py por:
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

from Globales import COLORES

BASE_PATH = os.path.dirname(__file__)


class PlayerControls(gtk.EventBox):

    __gsignals__ = {
    "accion-controls": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,))}

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, COLORES["window"])

        vbox = gtk.HBox()

        self.pix_play = gtk.gdk.pixbuf_new_from_file_at_size(
            os.path.join(BASE_PATH, "Iconos", "play.svg"), 24, 24)
        self.pix_paused = gtk.gdk.pixbuf_new_from_file_at_size(
            os.path.join(BASE_PATH, "Iconos", "pausa.svg"), 24, 24)

        self.play = JAMediaToolButton(pixels=24)
        archivo = os.path.join(BASE_PATH, "Iconos", "play.svg")
        self.play.set_imagen(archivo=archivo, flip=False, rotacion=False)
        self.play.set_tooltip_text("Reproducir")
        self.play.connect("clicked", self.__emit_accion, "pausa-play")
        vbox.pack_start(self.play, False, True, 0)

        self.stop = JAMediaToolButton(pixels=24)
        archivo = os.path.join(BASE_PATH, "Iconos", "stop.svg")
        self.stop.set_imagen(archivo=archivo, flip=False, rotacion=False)
        self.stop.set_tooltip_text("Detener Reproducción")
        self.stop.connect("clicked", self.__emit_accion, "stop_and_unfull")
        vbox.pack_start(self.stop, False, True, 0)

        # Cambiado por LV 20150226
        """
        self.full = JAMediaToolButton(pixels=24)
        archivo = os.path.join(BASE_PATH, "Iconos", "full.svg")
        self.full.set_imagen(archivo=archivo, flip=False, rotacion=False)
        self.full.set_tooltip_text("Full Screen")
        self.full.connect("clicked", self.__emit_accion, "full")
        vbox.pack_end(self.full, False, True, 0)
        """

        self.add(vbox)
        self.show_all()

    def __emit_accion(self, widget, accion):
        self.emit("accion-controls", accion)

    def set_paused(self):
        self.play.set_paused(self.pix_play)

    def set_playing(self):
        self.play.set_playing(self.pix_paused)


class JAMediaToolButton(gtk.ToolButton):

    def __init__(self, pixels=34):

        gtk.ToolButton.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, COLORES["window"])

        self.estado = False
        self.pixels = pixels
        self.imagen = gtk.Image()
        self.set_icon_widget(self.imagen)
        self.imagen.show()

        self.imagen.set_size_request(self.pixels, self.pixels)
        self.show_all()

    def set_imagen(self, archivo=None, flip=False, rotacion=False):
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(
            os.path.join(archivo), self.pixels, self.pixels)
        if flip:
            pixbuf = pixbuf.flip(True)
        if rotacion:
            pixbuf = pixbuf.rotate_simple(rotacion)
        self.imagen.set_from_pixbuf(pixbuf)

    def set_playing(self, pixbuf):
        if self.estado:
            return
        self.estado = True
        self.imagen.set_from_pixbuf(pixbuf)

    def set_paused(self, pixbuf):
        if not self.estado:
            return
        self.estado = False
        self.imagen.set_from_pixbuf(pixbuf)
