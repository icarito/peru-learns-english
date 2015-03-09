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

import gtk
import gobject
import pango

from Globales import COLORES, is_xo


class WelcomeView(gtk.EventBox):

    __gsignals__ = {
    "instructions": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, ( )),
    "credits": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, ( )),
    "start": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, ( ))}

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, COLORES["contenido"])
        self.set_border_width(4)


        self.image = gtk.Image()
        self.image.set_from_file("Imagenes/ple.png")

        tabla = gtk.Table(rows=10, columns=2, homogeneous=False)
        tabla.set_border_width(16)
        tabla.attach(self.image, 0, 2, 0, 9)

        bb = gtk.HButtonBox()
        bb.set_layout(gtk.BUTTONBOX_SPREAD)

        b = gtk.Button("")
        b.set_relief(gtk.RELIEF_NONE)
        b.modify_bg(gtk.STATE_NORMAL, COLORES["toolbar"])
        b.connect("enter-notify-event", self.__color, "manual")
        b.connect("leave-notify-event", self.__decolor, "manual")
        b.connect("clicked", self.__instructions)
        img = gtk.Image()
        img.set_from_file("Imagenes/manual_disabled.png")
        b.set_image(img)
        bb.pack_start(b, True, True, 0)
        img.show()

        b = gtk.Button("")
        b.set_relief(gtk.RELIEF_NONE)
        b.modify_bg(gtk.STATE_NORMAL, COLORES["toolbar"])
        b.connect("enter-notify-event", self.__color, "contributors")
        b.connect("leave-notify-event", self.__decolor, "contributors")
        b.connect("clicked", self.__credits)
        img = gtk.Image()
        img.set_from_file("Imagenes/contributors_disabled.png")
        b.set_image(img)
        bb.pack_start(b, True, True, 0)
        img.show()
        bb.show_all()

        b = gtk.Button("")
        b.set_relief(gtk.RELIEF_NONE)
        b.modify_bg(gtk.STATE_NORMAL, COLORES["toolbar"])
        b.connect("clicked", self.__start)
        #b.connect("enter-notify-event", self.__color, "start")
        #b.connect("leave-notify-event", self.__decolor, "start")
        img = gtk.Image()
        img.set_from_file("Imagenes/start.png")
        b.set_image(img)
        bb.pack_start(b, True, True, 0)
        img.show()
        bb.show_all()

        tabla.attach(bb, 0, 2, 9, 10)

        self.add(tabla)
        self.show_all()

    def __decolor(self, widget, event, filestub):
        widget.get_image().set_from_file("Imagenes/%s_disabled.png" % filestub)

    def __color(self, widget, event, filestub):
        widget.get_image().set_from_file("Imagenes/%s.png" % filestub)

    def __instructions(self, widget):
        self.emit("instructions")

    def __credits(self, widget):
        self.emit("credits")

    def __start(self, widget):
        self.emit("start")

    def stop(self):
        self.hide()

    def fix_scale(self):
        pixbuf = gtk.gdk.pixbuf_new_from_file("Imagenes/welcome_slide.png")
        screen = self.parent.get_screen()
        offset = 220 if not is_xo() else 340
        desired_height = screen.get_height() - offset
        desired_width = pixbuf.get_height() / desired_height * pixbuf.get_width()
        pixbuf = pixbuf.scale_simple(desired_width , desired_height, gtk.gdk.INTERP_BILINEAR)
        self.image.set_from_pixbuf(pixbuf)

    def run(self):
        self.fix_scale()
        self.show()
