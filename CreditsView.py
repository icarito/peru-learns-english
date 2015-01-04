#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   CreditsView.py por:
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

from Globales import COLORES

TEXT = [
    "Peru Learns English",
    "===================",
    "HHH",
    "### English ###",
    "HHH",
    "Peru Learns English (PLE) is a system for engaging young people in the acquisition of vocabulary,",
    "by means of appealing to multi-sensory stimuli in audiovisual cinematic scenes as well",
    "as fun videogames.",
    "HHH",
    "A simplified [spaced repetition tool](http://en.wikipedia.org/wiki/Spaced_repetition)",
    "is provided, that is able to measure progress and eventually provide feedback to the learner",
    "Spaced repetition is demonstrably [1] effective at helping engaged students to memorize vocabulary.",
    "HHH",
    "HHH",
    "PLE is being designed and put together by the SomosAzucar R&D Team in collaboration with specialists",
    "from the Ministry of Education of Peru.",
    "HHH",
    "### Español ###",
    "HHH",
    "Peru Learns English (PLE) es un sistema para involucrar a jóvenes en la adquisición de vocabulario,",
    "apelando a estímulos con escenas audiovisuales cinemáticas así como a videojuegos divertidos.",
    "HHH",
    "Se proporciona una [herramienta de repaso espaciado] (http://es.wikipedia.org/wiki/Repaso_espaciado),",
    "el cual es capaz de medir elprogreso y eventualmente proporcionar retroalimentación al aprendiz.",
    "El repaso espaciado es demostradamente [1] eficaz para ayudar a estudiantes comprometidos",
    "para memorizar vocabulario.",
    "HHH",
    "PLE está siendo desarrollado por el equipo de I&D SomosAzúcar en colaboración con especialistas",
    "del Ministerio de Educación de Perú.",
    "HHH",
    "1. [\"The spacing effect: A case study in the failure to apply the results of psychological",
    "research.\"](http://psycnet.apa.org/journals/amp/43/8/627/),",
    "Dempster, Frank N., 1988.",
    "HHH",
    "### Diseño (Design) ###",
    "HHH",
    "© 2014-2015 Laura Vargas - CC BY-SA 3.0",
    "HHH",
    "Con aportes de Koke Contreras, Sebastian Silva, Flavio Danesse,",
    "Cecilia Bustamante y Maria Elisa de la Vega.",
    "HHH",
    "Reconocimiento de Obras (Attribution  of Works)",
    "-----------------------------------------------",
    "HHH",
    "*We can only achieve quality, sustainable educational software by standing in the",
    "shoulders of giants and to contribute to the global common library of Free Software.*",
    "HHH",
    "*Sólo podemos lograr software educativo de calidad y sustentable, irguiéndonos",
    "sobre hombros de gigantes y contribuyendo a la biblioteca mundial común de Software Libre.*",
    "HHH",
    "### Código ###",
    "* Interfase © 2014-2015 Flavio Danesse <fdanesse@gmail.com> Uruguay - GPLv2+",
    "* Videojuego 1 © 2014-2015 Sebastian Silva <sebastian@fuentelibre.org> - GPLv3",
    "* popupmenubutton.py - Copyright 2008-2011 Zuza Software Foundation - GPLv2+",
    "HHH",
    "Obras utilizadas",
    "----------------",
    "HHH",
    "### Videos ###",
    "HHH",
    "#### Bunny Bonita “Feelings” - CC BY-NC",
    "#### Bunny Bonita “Family” - CC BY-NC",
    " Ministerio de Educación Nacional República de Colombia",
    "HHH",
    " © 2008-2013 T&T Teaching and Tutoring y Faldita Films Bunny Bonita",
    "HHH",
    "#### Art4Apps “Pete the Athlete” - CC BY-SA",
    "Art4Apps “Trish the Fish” CC BY-SA",
    "Art4Apps “A Shell at the Shore” CC BY-SA",
    "HHH",
    " © 2012—2014 Smart4kids LLC",
    "HHH",
    "#### QuestionCopyright “Copying is not Theft” - Public Domain",
    "Nina Paley",
    "HHH",
    "### Videojuego 1: Asteroide ###",
    "HHH",
    "Obras visuales tomadas con licencia de [OpenGameArt.Org](http://opengameart.org/).",
    "HHH",
    "* golden-border.png - nicubunu - Public Domain",
    "* LPC Space Base Tube Passage - © 2013 Xenodora - CC BY SA 3.0 - GPLv3",
    "* Universal LPC Sprite Sheet Character Generator - © 2010-2014 Varios Autores - GPLv3 - CC BY-SA 3.0",
    "* Simple Explosion -  © 2014  Bleed - http://remusprites.carbonmade.com/ - CC BY 3.0",
    "* Golden Menu - © 2013 - Janna - Public Domain",
    "* Asteroid - © 2014 - GGo - CC BY 3.0",
    "* Small Objects & Generic Background - Lanea Zimmerman (AKA Sharm) - CC BY-SA 3.0",
    "HHH",
    "Fotografía tomada con licencia de [Wikipedia](http://wikipedia.org/).",
    "HHH",
    "* Peru_Machu_Picchu_Sunrise.jpg - © 2007 Flamurai - CC BY 2.0",
    "HHH",
    "#### Biblioteca para Videojuegos: [\"Spyral\"](http://platipy.org/) GPLv2.1",
    " © 2014 Robert Deaton, Austin Bart.",
    ]

FONT = "Monospace"
TAM = 40
RED = 0
GREEN = 0
BLUE = 0


class CreditsView(gtk.EventBox):

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, COLORES["window"])
        self.set_border_width(15)

        self.visor = Visor()

        self.add(self.visor)
        self.show_all()

    def stop(self):
        self.visor.new_handle(False)
        self.hide()

    def run(self):
        self.show()
        self.visor.new_handle(True)


class Visor(gtk.DrawingArea):

    def __init__(self):

        gtk.DrawingArea.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, COLORES["window"])

        self.posy = 300
        self.update = False
        self._dict = {}

        self.connect("expose-event", self.__expose)
        self.connect("realize", self.__realize)
        self.show_all()

    def __expose(self, widget, event):
        self.new_handle(False)
        self.__realize(False)
        cr = self.get_property("window").cairo_create()
        rect = self.get_allocation()
        new_tam = TAM

        for key in sorted(self._dict.keys()):
            tam = self._dict[key].get("tam", TAM)
            cr.select_font_face(self._dict[key].get("font", FONT))
            cr.set_font_size(tam)
            (x_bearing, y_bearing, width, height, x_advance, y_advance) = cr.text_extents(self._dict[key]["text"])
            while width > rect.width:
                tam -= 1
                cr.set_font_size(tam)
                (x_bearing, y_bearing, width, height, x_advance, y_advance) = cr.text_extents(self._dict[key]["text"])

            if tam < new_tam:
                new_tam = tam

        for key in sorted(self._dict.keys()):
            cr.select_font_face(self._dict[key].get("font", FONT))
            cr.set_font_size(new_tam)
            (x_bearing, y_bearing, width, height, x_advance, y_advance) = cr.text_extents(self._dict[key]["text"])

            self._dict[key]["height"] = height + (y_bearing * -1)
            self._dict[key]["width"] = width
            self._dict[key]["tam"] = new_tam

        self.new_handle(True)

    def __realize(self, widget):
        cr = self.get_property("window").cairo_create()

        _dict = {}
        cont = 0
        for line in TEXT:
            tam = TAM
            cr.select_font_face(FONT)
            cr.set_font_size(tam)

            (x_bearing, y_bearing, width, height, x_advance, y_advance) = cr.text_extents(line)

            titulos = ["Peru Learns English", "===================",
                "### English ###", "### Español ###",
                "### Diseño (Design) ###", "### Código ###", "### Videos ###"]
            color = (RED, GREEN, BLUE)

            if line in titulos:
                color = (0, 0, 255)

            _dict[cont] = {
                "text": line,
                "font": FONT,
                "tam": tam,
                "color": color,
                "height": height + (y_bearing * -1),
                "width": width,
                }

            cont += 1

        self._dict = _dict.copy()

    def __handle(self):
        self.posy -= 1
        cr = self.get_property("window").cairo_create()
        rect = self.get_allocation()

        cr.set_source_rgb(255, 255, 255)
        cr.paint()

        y = self.posy
        for key in sorted(self._dict.keys()):
            cr.select_font_face(self._dict[key].get("font", FONT))
            cr.set_font_size(self._dict[key].get("tam", TAM))
            r, g, b = self._dict[key].get("color", (RED, GREEN, BLUE))
            cr.set_source_rgb(r, g, b)

            w = self._dict[key].get("width", 0)
            h = self._dict[key].get("height", 0)
            if self._dict[key]["text"] == "Peru Learns English" or \
                self._dict[key]["text"] == "===================":
                cr.move_to(rect.width / 2 - w / 2, y)
            else:
                cr.move_to(10, y)

            if self._dict[key]["text"] != "HHH" and y > 0 and y < rect.height:
                cr.show_text(self._dict[key]["text"])

            y += h

        if y < 0:
            self.posy = rect.height

        return True

    def new_handle(self, reset):
        if self.update:
            gobject.source_remove(self.update)
            self.update = False
        if reset:
            self.posy = 300
            self.update = gobject.timeout_add(50, self.__handle)
