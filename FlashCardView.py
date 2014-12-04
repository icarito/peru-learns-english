#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   FlashCardView.py por:
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
import pango
import gobject

from Globales import COLORES
from Globales import get_vocabulario


class FlashCardView(gtk.EventBox):

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, COLORES["toolbar"])
        self.set_border_width(4)

        self.topic = False
        self.vocabulario = []

        tabla = gtk.Table(rows=10, columns=5, homogeneous=True)
        tabla.set_property("column-spacing", 5)
        tabla.set_property("row-spacing", 5)
        tabla.set_border_width(4)

        cabecera = Cabecera()
        flashcard = FlashCard()

        tabla.attach(cabecera, 0, 3, 0, 2)
        tabla.attach(flashcard, 0, 3, 2, 10)

        self.derecha = Derecha()
        tabla.attach(self.derecha, 3, 5, 2, 10)

        self.add(tabla)
        self.show_all()

    def stop(self):
        self.hide()

    def run(self, topic):
        self.derecha.run()
        self.topic = topic
        csvfile = os.path.join(topic, "vocabulario.csv")
        self.vocabulario = get_vocabulario(csvfile)
        self.show()
        gobject.timeout_add(500, self.__load, 1)

    def __load(self, index):
        print self.vocabulario[index]
        return False


class FlashCard(gtk.EventBox):

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, COLORES["toolbar"])
        self.set_border_width(10)

        self.drawing = gtk.DrawingArea()
        self.drawing.modify_bg(gtk.STATE_NORMAL, COLORES["text"])

        self.add(self.drawing)
        self.show_all()


class Cabecera(gtk.EventBox):

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, COLORES["toolbar"])

        tabla = gtk.Table(rows=2, columns=2, homogeneous=True)
        tabla.set_property("column-spacing", 5)
        tabla.set_property("row-spacing", 5)
        tabla.set_border_width(4)

        self.titulo = gtk.Label("Título")
        label1 = gtk.Label("Keywords")
        label2 = gtk.Label("What is This?")

        tabla.attach(self.titulo, 0, 2, 0, 1)
        tabla.attach(label1, 0, 1, 1, 2)
        tabla.attach(label2, 1, 2, 1, 2)

        self.add(tabla)
        self.show_all()


class Derecha(gtk.EventBox):

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, COLORES["toolbar"])

        tabla = gtk.Table(rows=4, columns=3, homogeneous=True)
        tabla.set_property("column-spacing", 5)
        tabla.set_property("row-spacing", 5)
        tabla.set_border_width(4)

        button0 = MyButton("Show me the answer",
            pango.FontDescription("Purisa 12"))
        tabla.attach(button0, 0, 3, 1, 2)

        button1 = MyButton("Had not\nidea",
            pango.FontDescription("Purisa 8"))
        tabla.attach(button1, 0, 1, 2, 3)

        button2 = MyButton("Just What\nThougth",
            pango.FontDescription("Purisa 8"))
        tabla.attach(button2, 1, 2, 2, 3)

        button3 = MyButton("Thew it !",
            pango.FontDescription("Purisa 8"))
        tabla.attach(button3, 2, 3, 2, 3)

        self.buttons = [button0, button1, button2, button3]

        self.add(tabla)
        self.show_all()

    def run(self):
        self.buttons[0].set_sensitive(False)
        self.buttons[1].hide()
        self.buttons[2].hide()
        self.buttons[3].hide()


class MyButton(gtk.Button):

    def __init__(self, text, font):

        gtk.Button.__init__(self)

        label = gtk.Label(text)
        label.set_property("justify", gtk.JUSTIFY_CENTER)
        label.modify_font(font)
        self.set_property("child", label)
        self.show_all()
