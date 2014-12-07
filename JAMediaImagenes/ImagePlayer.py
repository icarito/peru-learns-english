#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   ImagePlayer.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   Uruguay
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""
Descripción:
    Visor de Imágenes en base a gstreamer.

    Recibe un widget gtk para dibujar sobre él.

    Utilice la función: load(file_path)
        para cargar el archivo a dibujar.

    Utilice la función: stop()
        para detener la reproducción

    Utilice la función: rotar("Derecha") o rotar("Izquierda")
        para rotar la imágen
"""

import os
import gobject
import gtk


class ImagePlayer(gobject.GObject):

    def __init__(self, ventana):

        gobject.GObject.__init__(self)

        self.ventana = ventana
        self.src_path = ""
        self.pixbuf = False

        self.ventana.connect("expose-event", self.__set_size)

    def __set_size(self, widget, event):
        if not self.pixbuf:
            return
        rect = self.ventana.get_allocation()
        ctx = self.ventana.get_property("window").cairo_create()
        ctx.rectangle(event.area.x, event.area.y,
            event.area.width, event.area.height)
        ctx.clip()
        temp_pixbuf = self.pixbuf.scale_simple(
            rect.width, rect.height, gtk.gdk.INTERP_TILES)
        ctx.set_source_pixbuf(temp_pixbuf, 0, 0)
        ctx.paint()
        return True

    def load(self, uri):
        self.src_path = False
        self.pixbuf = False
        if os.path.exists(uri):
            self.src_path = uri
            self.pixbuf = gtk.gdk.pixbuf_new_from_file(self.src_path)
            self.ventana.queue_draw()

    def stop(self):
        try:
            self.ventana.disconnect_by_func(self.__set_size)
        except:
            pass
