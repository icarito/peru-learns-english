#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   InstructionsView.py por:
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
from glob import glob

from Globales import COLORES
from JAMediaImagenes.ImagePlayer import ImagePlayer


class HelpSlideShow(gtk.EventBox):

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, COLORES["toolbar"])
        #self.set_border_width(20)

        self.slides = []
        self.index_select = 0
        self.imagenplayer = False
        self.control = False

        self.drawing = gtk.DrawingArea()
        eventcontainer = gtk.EventBox()
        eventcontainer.modify_bg(gtk.STATE_NORMAL, COLORES["toolbar"])
        self.label = gtk.Label("Text")
        self.label.set_property("justify", gtk.JUSTIFY_CENTER)
        self.drawing.modify_bg(gtk.STATE_NORMAL, COLORES["toolbar"])
        self.label.modify_bg(gtk.STATE_NORMAL, COLORES["toolbar"])
        self.label.modify_fg(gtk.STATE_NORMAL, COLORES["window"])
        #self.label.modify_font(pango.FontDescription("DejaVu Sans 16"))
        eventcontainer.add(self.label)

        hbox = gtk.HBox()
        self.left = gtk.Button()
        self.left.unset_flags(gtk.CAN_FOCUS)
        self.left.set_relief(gtk.RELIEF_NONE)
        imagen = gtk.Image()
        imagen.set_from_file("Imagenes/flecha_izquierda.png")
        self.left.set_border_width(0)
        self.left.add(imagen)
        self.left.connect("clicked", self.go_left)
        hbox.pack_start(self.left)

        hbox.add(eventcontainer)

        self.right = gtk.Button()
        self.right.set_relief(gtk.RELIEF_NONE)
        self.right.unset_flags(gtk.CAN_FOCUS)
        imagen = gtk.Image()
        imagen.set_from_file("Imagenes/flecha_derecha.png")
        self.right.set_border_width(0)
        self.right.add(imagen)
        self.right.connect("clicked", self.go_right)
        hbox.pack_end(self.right)

        tabla = gtk.Table(rows=8, columns=1, homogeneous=True)
        tabla.attach(self.drawing, 0, 1, 0, 7, ypadding=5)
        tabla.attach(hbox, 0, 1, 7, 8)

        align = gtk.Alignment(0.5, 0.5, 0.7, 0.95)
        align.add(tabla)

        self.add(align)

    def go_right(self, widget):
        self.__run_secuencia()
        self.left.show()
        self.right.show()

    def go_left(self, widget):
        self.__run_secuencia(offset=-1)
        self.left.show()
        self.right.show()

    def __run_secuencia(self, widget=None, offset=1):
        self.stop()
        self.index_select += offset
        self.path = self.slides[self.index_select % len(self.slides)]
        self.imagenplayer = ImagePlayer(self.drawing)
        self.imagenplayer.load(self.path)
        self.label.set_text("Slide %i of %i" % (
            self.index_select % len(self.slides) + 1, len(self.slides)))

        #self.left.hide()
        #self.right.hide()
        return True

    def toggle(self):
        if self.control:
            gobject.source_remove(self.control)
            self.control = False
            self.modify_bg(gtk.STATE_NORMAL, COLORES['rojo'])
            self.left.show()
            self.right.show()
        else:
            self.modify_bg(gtk.STATE_NORMAL, COLORES['window'])
            self.play()
            self.left.hide()
            self.right.hide()

    def reset(self):
        self.modify_bg(gtk.STATE_NORMAL, COLORES['window'])
        self.play()

    def stop(self):
        if self.imagenplayer:
            self.imagenplayer.stop()
            del(self.imagenplayer)
            self.imagenplayer = False

    def play(self):
        if not self.control:
            self.control = gobject.timeout_add(10000, self.__run_secuencia)

    def load(self):
        self.stop()
        self.slides = sorted(glob("Imagenes/slides/slide*.png"))
        self.index_select = -1
        self.__run_secuencia()
        #self.play()
        return False


class InstructionsView(gtk.EventBox):

    __gsignals__ = {
    "credits": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, ( )),
    "start": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, ( ))}

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, COLORES["contenido"])
        self.set_border_width(4)

        self.helpslideshow = HelpSlideShow()

        self.add(self.helpslideshow)
        self.show_all()

    def __decolor(self, widget, event, filestub):
        widget.get_image().set_from_file("Imagenes/%s_disabled.png" % filestub)

    def __color(self, widget, event, filestub):
        widget.get_image().set_from_file("Imagenes/%s.png" % filestub)

    def __credits(self, widget):
        self.emit("credits")

    def __start(self, widget):
        self.fix_scale()
        self.emit("start")

    def stop(self):
        self.helpslideshow.stop()
        self.hide()

    def fix_scale(self):
        pixbuf = gtk.gdk.pixbuf_new_from_file("Imagenes/welcome_slide.png")
        screen = self.window.get_screen()
        desired_height = screen.get_height() - 180
        desired_width = pixbuf.get_height() / desired_height * pixbuf.get_width()
        pixbuf = pixbuf.scale_simple(desired_width , desired_height, gtk.gdk.INTERP_BILINEAR)
        self.image.set_from_pixbuf(pixbuf)

    def run(self):
        self.helpslideshow.load()
        self.show()
