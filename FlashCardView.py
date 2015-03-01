#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   FlashCardView.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   Uruguay

#   Contribuciones de Sebastian Silva <sebastian@somosazucar.org>
#   Planeta Tierra

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

from ConfigParser import SafeConfigParser

from JAMediaImagenes.ImagePlayer import ImagePlayer

from Globales import COLORES
from Globales import get_vocabulario
from Globales import decir, decir_demorado
from Globales import guardar
from Globales import Dialog


class FlashCardView(gtk.EventBox):

    __gsignals__ = {
    "video": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING, ))}

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, COLORES["contenido"])
        self.set_border_width(4)

        self.user = False
        self.topic = False
        self.vocabulario = []
        self.imagenplayer = False
        self.index_select = 0
        self.click_event = True

        tabla = gtk.Table(rows=11, columns=5, homogeneous=True)
        tabla.set_property("column-spacing", 5)
        tabla.set_property("row-spacing", 5)
        tabla.set_border_width(4)

        self.cabecera = Cabecera()
        self.flashcard = FlashCard()

        tabla.attach(self.cabecera, 0, 5, 0, 2)
        tabla.attach(self.flashcard, 0, 3, 2, 11)

        self.derecha = Derecha()
        tabla.attach(self.derecha, 3, 5, 2, 10)
        self.statuslabel = gtk.Label("Flashcard 0 of 0")
        tabla.attach(self.statuslabel, 3, 5, 10, 11)

        self.add(tabla)
        self.show_all()

        self.derecha.connect("siguiente", self.__siguiente)
        self.derecha.connect("show_answer", self.__show_answer)

    def __show_answer(self, widget):
        index = self.index_select
        respuesta = self.vocabulario[index][3] if len(self.vocabulario[index]) > 3 else \
                    self.vocabulario[index][1]
        self.derecha.label.set_text(
            self.vocabulario[index][1].replace(" ", "\n"))
        self.cabecera.question_label.set_markup("<b>"+respuesta+"</b>")
        if self.click_event:
            self.flashcard.disconnect(self.click_event)
            self.click_event = None
        self.click_event = self.flashcard.connect("button-press-event", self.repetir_respuesta, respuesta)
        #self.cabecera.question_label.modify_fg(gtk.STATE_NORMAL, COLORES["rojo"])
        gobject.idle_add(self.__show_phrase, respuesta)

    def __show_phrase(self, respuesta):
        decir_demorado(170, 50, 0, "en-gb", respuesta)
        self.cabecera.question_label.modify_fg(gtk.STATE_NORMAL, COLORES["window"])
        self.cabecera.question_label.set_markup(respuesta)
        if not self.click_event:
            self.click_event = self.flashcard.connect("button-press-event", self.repetir_respuesta, respuesta)

    def __siguiente(self, widget, respuesta):
        """
        Continúa con siguiente palabra del vocabulario cargado.
        """
        r = 0
        if respuesta == 1:
            r = 5
        elif respuesta == 2:
            r = 3
        elif respuesta == 3:
            r = 0
        guardar(self.user, self.topic,
            self.vocabulario[self.index_select][0], r)
        if self.index_select < len(self.vocabulario) - 1:
            self.index_select += 1
            gobject.timeout_add(500, self.__load, self.index_select)
        else:
            dialog = Dialog("Congratulations!", self.get_toplevel(),
                ("OK", gtk.RESPONSE_ACCEPT),
                "Memorization task completed for today.")
            dialog.run()
            dialog.destroy()
            self.emit("video", self.topic)

    def __load(self, index):
        """
        Carga una nueva palabra del Vocabulario
        """
        path = os.path.join(self.topic, "Imagenes",
            "%s.png" % self.vocabulario[index][0])
        if self.imagenplayer:
            self.imagenplayer.stop()
            del(self.imagenplayer)
            self.imagenplayer = False
        self.imagenplayer = ImagePlayer(self.flashcard.drawing)
        self.imagenplayer.load(path)
        #self.cabecera.question_label.modify_fg(gtk.STATE_NORMAL, COLORES["rojo"])
        pregunta = self.vocabulario[index][2] if len(self.vocabulario[index]) > 2 else ""
        if pregunta == "":
            pregunta = "What is this?"
        self.cabecera.question_label.set_markup("<b>"+pregunta+"</b>")

        if self.click_event:
            self.flashcard.disconnect(self.click_event)
            self.click_event = None
        self.click_event = self.flashcard.connect("button-press-event", self.repetir_pregunta, pregunta)
        gobject.idle_add(self.__activar, pregunta)
        return False

    def repetir_pregunta(self, widget, event, pregunta):
        if self.click_event:
            self.flashcard.disconnect(self.click_event)
            self.click_event = None
        self.click_event = None
        self.cabecera.question_label.set_markup("<b>"+pregunta+"</b>")
        gobject.idle_add(self.__activar, pregunta)

    def repetir_respuesta(self, widget, event, respuesta):
        if self.click_event:
            self.flashcard.disconnect(self.click_event)
            self.click_event = None
        self.click_event = None
        self.cabecera.question_label.set_markup("<b>"+respuesta+"</b>")
        gobject.idle_add(self.__show_phrase, respuesta)

    def __activar(self, pregunta):
        decir_demorado(170, 50, 0, "en", pregunta)
        if not self.click_event:
            self.click_event = self.flashcard.connect("button-press-event", self.repetir_pregunta, pregunta)
        self.derecha.activar()
        self.cabecera.question_label.modify_fg(gtk.STATE_NORMAL, COLORES["window"])
        self.cabecera.question_label.set_markup(pregunta)
        self.statuslabel.set_text("Flashcard %i of %i" % (
            self.index_select + 1, len(self.vocabulario)))
        return False

    def stop(self):
        """
        Desactiva la vista de FlashCards.
        """
        self.hide()
        if self.imagenplayer:
            self.imagenplayer.stop()
            del(self.imagenplayer)
            self.imagenplayer = False

    def run(self, data):
        """
        Carga Vocabulario, pone widgets a estado inicial y
        carga primera palabra.
        """
        topic, _dict = data
        self.user = _dict
        parser = SafeConfigParser()
        metadata = os.path.join(topic, "topic.ini")
        parser.read(metadata)

        self.cabecera.titulo.set_text("Topic: " + parser.get('topic', 'title'))

        self.derecha.run()
        vocabulario = get_vocabulario(topic, _dict)
        if len(vocabulario) > 14:
            vocabulario = vocabulario[:15]
        self.show()
        if vocabulario:
            self.vocabulario = vocabulario
            self.topic = topic
            self.index_select = 0
            gobject.timeout_add(500, self.__load, self.index_select)
        else:
            self.topic = topic
            dialog = Dialog("Come back tomorrow!", self.get_toplevel(),
                ("OK", gtk.RESPONSE_ACCEPT),
                "You've memorized all flashcards for today.")
            dialog.run()
            dialog.destroy()
            self.emit("video", self.topic)


class FlashCard(gtk.EventBox):

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, COLORES["contenido"])
        self.set_border_width(10)

        self.drawing = gtk.DrawingArea()
        self.drawing.modify_bg(gtk.STATE_NORMAL, COLORES["text"])

        self.add(self.drawing)
        self.show_all()


class Cabecera(gtk.EventBox):

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, COLORES["contenido"])

        tabla = gtk.Table(rows=2, columns=5, homogeneous=True)
        tabla.set_property("column-spacing", 2)
        tabla.set_property("row-spacing", 2)
        tabla.set_border_width(4)

        self.titulo = gtk.Label("Título")
        self.titulo.modify_font(pango.FontDescription("DejaVu Sans Bold 14"))
        self.titulo.modify_fg(gtk.STATE_NORMAL, COLORES["window"])

        self.question_label = gtk.Label("What is This?")
        self.question_label.modify_font(pango.FontDescription("DejaVu Sans 16"))
        self.question_label.modify_fg(gtk.STATE_NORMAL, COLORES["window"])

        tabla.attach(self.titulo, 0, 3, 0, 1)
        tabla.attach(self.question_label, 0, 3, 1, 2)

        self.add(tabla)
        self.show_all()


class Derecha(gtk.EventBox):

    __gsignals__ = {
    "siguiente": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_INT, )),
    "show_answer": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, [])}

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, COLORES["contenido"])

        tabla = gtk.Table(rows=4, columns=3, homogeneous=True)
        tabla.set_property("column-spacing", 5)
        tabla.set_property("row-spacing", 5)
        tabla.set_border_width(4)

        self.label = gtk.Label("")
        self.label.set_property("justify", gtk.JUSTIFY_CENTER)
        self.label.modify_font(pango.FontDescription("DejaVu Sans Bold 20"))
        self.label.modify_fg(gtk.STATE_NORMAL, COLORES["text"])
        tabla.attach(self.label, 0, 3, 0, 2)
        self.label.set_line_wrap(True)

        button0 = MyButton("Show me\nthe answer",
            pango.FontDescription("DejaVu Sans 16"))
        button0.connect("clicked", self.__show_answer)
        tabla.attach(button0, 0, 3, 0, 2, ypadding=5)

        button1 = MyButton("I\nknew\nit !",
            pango.FontDescription("DejaVu Sans 10"))
        button1.modify_bg(gtk.STATE_NORMAL, COLORES["verde"])
        button1.connect("clicked", self.__seguir)
        tabla.attach(button1, 0, 1, 2, 4)

        button2 = MyButton("I\nwasn't\nsure.",
            pango.FontDescription("DejaVu Sans 10"))
        button2.modify_bg(gtk.STATE_NORMAL, COLORES["amarillo"])
        button2.connect("clicked", self.__seguir)
        tabla.attach(button2, 1, 2, 2, 4)

        button3 = MyButton("I\nhad\nno idea !",
            pango.FontDescription("DejaVu Sans 10"))
        button3.modify_bg(gtk.STATE_NORMAL, COLORES["rojo"])
        button3.connect("clicked", self.__seguir)
        tabla.attach(button3, 2, 3, 2, 4)

        self.buttons = [button0, button1, button2, button3]

        self.add(tabla)
        self.show_all()

    def __seguir(self, button):
        self.run()
        self.emit("siguiente", self.buttons.index(button))

    def __show_answer(self, button):
        self.emit("show_answer")
        self.label.show()
        self.buttons[0].hide()
        self.buttons[1].show()
        self.buttons[2].show()
        self.buttons[3].show()

    def run(self):
        self.buttons[0].set_sensitive(False)
        self.label.set_text("")
        self.label.hide()
        self.buttons[0].show()
        self.buttons[1].hide()
        self.buttons[2].hide()
        self.buttons[3].hide()

    def activar(self):
        self.buttons[0].set_sensitive(True)


class MyButton(gtk.Button):

    def __init__(self, text, font):

        gtk.Button.__init__(self)

        label = gtk.Label(text)
        label.set_property("justify", gtk.JUSTIFY_CENTER)
        label.modify_font(font)
        self.set_property("child", label)
        self.show_all()
