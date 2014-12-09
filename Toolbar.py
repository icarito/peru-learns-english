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
        self.modify_fg(gtk.STATE_NORMAL, COLORES["text"])
        toolbar.modify_bg(gtk.STATE_NORMAL, COLORES["toolbar"])
        toolbar.modify_fg(gtk.STATE_NORMAL, COLORES["text"])

        item = gtk.ToolItem()
        item.set_expand(True)
        imagen = gtk.Image()
        imagen.set_from_file("Imagenes/ple.png")

        boton = gtk.ToolButton()
        boton.set_label_widget(imagen)
        boton.connect("clicked", self.__go_home)
        item.add(boton)
        toolbar.insert(item, -1)
        separador = gtk.SeparatorToolItem()
        separador.props.draw = True
        toolbar.insert(separador, -1)

        self.buttons = []

        for text in ["Instructions", "Credits"]:
            item = gtk.ToolItem()
            item.set_expand(True)
            label = gtk.Label(text)
            label.modify_font(pango.FontDescription("DejaVu Sans Bold 16"))
            boton = gtk.ToggleToolButton()
            boton.set_label_widget(label)
            boton.connect("toggled", self.__do_toggled)
            self.buttons.append(boton)
            item.add(boton)
            toolbar.insert(item, -1)
            separador = gtk.SeparatorToolItem()
            separador.props.draw = True
            toolbar.insert(separador, -1)

        self.menubar = MenuBar()

        item = gtk.ToolItem()
        item.set_expand(True)
        item.add(self.menubar)
        toolbar.insert(item, -1)

        self.add(toolbar)
        self.show_all()

        self.menubar.connect("activar", self.__emit_accion_menu)

    def __emit_accion_menu(self, widget, topic):
        self.emit("video", topic)

    def __go_home(self, widget):
        self.emit("activar", "Instructions")

    def __do_toggled(self, widget):
        label = widget.get_label_widget().get_text()
        activo = widget.get_active()
        if activo:
            for button in self.buttons:
                if label != button.get_label_widget().get_text():
                    button.set_active(False)
            self.emit("activar", label)
        else:
            for button in self.buttons:
                if button.get_active():
                    return
            self.buttons[0].set_active(True)


class MenuBar(gtk.MenuBar):

    __gsignals__ = {
    "activar": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING, ))}

    def __init__(self):

        gtk.MenuBar.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, COLORES["toolbar"])
        self.modify_fg(gtk.STATE_NORMAL, COLORES["text"])
        self.modify_font(pango.FontDescription("DejaVu Sans Bold 16"))

        itemmenu = gtk.MenuItem("Topics")
        itemmenu.child.modify_font(pango.FontDescription("DejaVu Sans Bold 16"))
        itemmenu.child.modify_fg(gtk.STATE_NORMAL, COLORES["text"])
        itemmenu.child.modify_bg(gtk.STATE_NORMAL, COLORES["toolbar"])

        menu = gtk.Menu()
        menu.modify_font(pango.FontDescription("DejaVu Sans 12"))
        menu.modify_bg(gtk.STATE_NORMAL, COLORES["toolbar"])
        menu.modify_fg(gtk.STATE_NORMAL, COLORES["text"])
        itemmenu.set_submenu(menu)
        self.append(itemmenu)

        topics = os.path.join(BASE_PATH, "Topics")
        for arch in sorted(os.listdir(topics)):
            item = gtk.MenuItem()
            try:
                item.get_child().destroy()
            except:
                pass
            boton = gtk.Label(arch)
            boton.modify_font(pango.FontDescription("DejaVu Sans Bold 16"))
            boton.set_padding(xpad=20, ypad=20)
            item.add(boton)
            item.connect("activate", self.__emit_accion_menu)
            menu.append(item)

    def __emit_accion_menu(self, widget):
        #widget.get_children()[0].set_active(True)
        label = widget.get_children()[0].get_label()
        self.emit("activar", os.path.join(BASE_PATH, "Topics", label))
