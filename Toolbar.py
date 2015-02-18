#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Toolbar.py por:
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

from popupmenubutton import PopupMenuButton

from ConfigParser import SafeConfigParser

from Globales import COLORES

BASE_PATH = os.path.dirname(__file__)


class Toolbar(gtk.EventBox):

    __gsignals__ = {
    "activar": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING, )),
    "video": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING, ))}

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.set_border_width(4)

        toolbar = gtk.Toolbar()

        self.modify_bg(gtk.STATE_NORMAL, COLORES["toolbar"])
        toolbar.modify_bg(gtk.STATE_NORMAL, COLORES["toolbar"])
        toolbar.modify_fg(gtk.STATE_NORMAL, COLORES["text"])

        item = gtk.ToolItem()
        item.set_expand(True)
        imagen = gtk.Image()
        imagen.set_from_file("Imagenes/ple.png")

        self.homebutton = gtk.ToggleToolButton()
        self.homebutton.set_label_widget(imagen)
        self.homebutton.connect("toggled", self.__go_home)
        item.add(self.homebutton)
        toolbar.insert(item, -1)

        separador = gtk.SeparatorToolItem()
        separador.props.draw = True
        toolbar.insert(separador, -1)

        item = gtk.ToolItem()
        item.set_expand(True)
        label = gtk.Label("Instructions")
        label.modify_font(pango.FontDescription("DejaVu Sans Bold 16"))
        label.modify_fg(gtk.STATE_NORMAL, COLORES["text"])
        self.instructionsbutton = gtk.ToggleToolButton()
        self.instructionsbutton.set_label_widget(label)
        self.instructionsbutton.connect("toggled", self.__go_instructions)
        item.add(self.instructionsbutton)
        toolbar.insert(item, -1)
        separador = gtk.SeparatorToolItem()
        separador.props.draw = True
        toolbar.insert(separador, -1)

        self.menu = Menu()

        self.menubutton = PopupMenuButton("Topics")
        self.menubutton.child.modify_font(pango.FontDescription("DejaVu Sans Bold 16"))
        self.menubutton.child.modify_fg(gtk.STATE_NORMAL, COLORES["text"])
        self.menubutton.child.modify_bg(gtk.STATE_NORMAL, COLORES["toolbar"])
        self.menubutton.set_menu(self.menu)

        item = gtk.ToolItem()
        item.set_expand(True)
        item.add(self.menubutton)
        toolbar.insert(item, -1)

        self.add(toolbar)
        self.show_all()

        self.menu.connect("activar", self.__emit_accion_menu)

    def __emit_accion_menu(self, widget, topic):
        self.instructionsbutton.set_active(False)
        self.homebutton.set_active(False)
        self.emit("video", topic)

    def __go_home(self, widget):
        activo = widget.get_active()
        if activo:
            self.instructionsbutton.set_active(False)
            self.menubutton.set_active(False)
            self.emit("activar", "Home")
        else:
            self.homebutton.set_active(False)

    def __go_instructions(self, widget):
        activo = widget.get_active()
        if activo:
            self.emit("activar", "Instructions")
            self.menubutton.set_active(False)
            self.homebutton.set_active(False)
        else:
            self.instructionsbutton.set_active(False)


class Menu(gtk.Menu):

    __gsignals__ = {
    "activar": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING, ))}

    def __init__(self):
        gtk.Menu.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, COLORES["menu"])

        topics = os.path.join(BASE_PATH, "Topics")
        for arch in sorted(os.listdir(topics)):
            item = gtk.MenuItem()

            parser = SafeConfigParser()
            metadata = os.path.join(topics, arch, "topic.ini")
            parser.read(metadata)

            title = parser.get('topic', 'title')

            boton = gtk.Label(title)
            boton.modify_font(pango.FontDescription("DejaVu Sans Bold 16"))
            boton.modify_fg(gtk.STATE_NORMAL, COLORES["window"])
            boton.set_padding(xpad=5, ypad=20)
            item.add(boton)
            item.connect("activate", self.__emit_accion_menu, arch)
            item.show()
            boton.show()
            self.append(item)

    def __emit_accion_menu(self, widget, arch):
        label = arch
        self.emit("activar", os.path.join(BASE_PATH, "Topics", label))
