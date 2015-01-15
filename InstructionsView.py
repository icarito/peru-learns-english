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

from Globales import COLORES


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

        es_tit = gtk.Label(u"¡Bienvenidos!")
        es_tit.modify_font(pango.FontDescription("DejaVu Sans Bold 22"))
        es_tit.modify_fg(gtk.STATE_NORMAL, COLORES["window"])

        es_body = gtk.Label("Peru Learns English (PLE) es un sistema para involucrar a jóvenes en la adquisición de vocabulario, apelando a estímulos con escenas audiovisuales cinemáticas así como a videojuegos divertidos.")
        es_body.set_line_wrap(True)
        es_body2 = gtk.Label("Se proporciona una herramienta de repaso espaciado, el cual es capaz de medir el progreso y eventualmente proporcionar retroalimentación al aprendiz. El repaso espaciado es demostradamente eficaz para ayudar a estudiantes comprometidos para memorizar vocabulario.")
        es_body2.set_line_wrap(True)

        en_tit = gtk.Label(u"Welcome!")
        en_tit.modify_font(pango.FontDescription("DejaVu Sans Bold 22"))
        en_tit.modify_fg(gtk.STATE_NORMAL, COLORES["window"])

        en_body = gtk.Label("Peru Learns English (PLE) is a system for engaging young people in the acquisition of vocabulary, by means of appealing to multi-sensory stimuli in audiovisual cinematic scenes as well as fun videogames.")
        en_body.set_line_wrap(True)
        en_body2 = gtk.Label("A simplified spaced repetition tool is provided, that is able to measure progress and eventually provide feedback to the learner. Spaced repetition is demonstrably effective at helping engaged students to memorize vocabulary.")
        en_body2.set_line_wrap(True)

        for label in es_body, es_body2, en_body, en_body2:
            label.modify_font(pango.FontDescription("DejaVu Sans 8"))

        tabla = gtk.Table(rows=4, columns=2, homogeneous=True)
        tabla.attach(es_tit, 0, 1, 0, 1)
        tabla.attach(es_body, 0, 1, 1, 2)
        tabla.attach(es_body2, 0, 1, 2, 3)

        tabla.attach(en_tit, 1, 2, 0, 1)
        tabla.attach(en_body, 1, 2, 1, 2)
        tabla.attach(en_body2, 1, 2, 2, 3)

        bb = gtk.HButtonBox()
        bb.set_layout(gtk.BUTTONBOX_SPREAD)

        b = gtk.Button("")
        b.set_relief(gtk.RELIEF_NONE)
        b.modify_bg(gtk.STATE_NORMAL, COLORES["toolbar"])
        b.connect("enter-notify-event", self.__color, "manual")
        b.connect("leave-notify-event", self.__decolor, "manual")
        img = gtk.Image()
        img.set_from_file("Imagenes/manual_disabled.png")
        b.set_image(img)
        bb.add(b)

        b = gtk.Button("")
        b.set_relief(gtk.RELIEF_NONE)
        b.modify_bg(gtk.STATE_NORMAL, COLORES["toolbar"])
        b.connect("enter-notify-event", self.__color, "contributors")
        b.connect("leave-notify-event", self.__decolor, "contributors")
        b.connect("clicked", self.__credits)
        img = gtk.Image()
        img.set_from_file("Imagenes/contributors_disabled.png")
        b.set_image(img)
        bb.add(b)

        b = gtk.Button("")
        b.set_relief(gtk.RELIEF_NONE)
        b.modify_bg(gtk.STATE_NORMAL, COLORES["toolbar"])
        b.connect("clicked", self.__start)
        #b.connect("enter-notify-event", self.__color, "start")
        #b.connect("leave-notify-event", self.__decolor, "start")
        img = gtk.Image()
        img.set_from_file("Imagenes/start.png")
        b.set_image(img)
        bb.add(b)

        tabla.attach(bb, 0, 2, 3, 4)

        self.add(tabla)
        self.show_all()

    def __decolor(self, widget, event, filestub):
        img = gtk.Image()
        img.set_from_file("Imagenes/%s_disabled.png" % filestub)
        widget.set_image(img)

    def __color(self, widget, event, filestub):
        img = gtk.Image()
        img.set_from_file("Imagenes/%s.png" % filestub)
        widget.set_image(img)

    def __credits(self, widget):
        self.emit("credits")

    def __start(self, widget):
        self.emit("start")

    def stop(self):
        self.hide()

    def run(self):
        self.show()
