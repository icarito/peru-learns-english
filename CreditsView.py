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

import os
import cairo
import gtk
import gobject

from Globales import COLORES

TEXT = [
    "Peru Learns English / Perú Aprende Inglés",
    "=========================================",
    "HHH",
    "PLE está siendo desarrollado por el equipo de I&D SomosAzúcar en colaboración con especialistas del Ministerio de Educación de Perú.",
    "HHH",
    "*Sólo podemos lograr software educativo de calidad y sustentable, irguiéndonos",
    "sobre hombros de gigantes y contribuyendo a la biblioteca mundial común de Software Libre.*",
    "HHH",
    "Credits / Créditos",
    "------------------",
    "HHH",
    "### Code / Código ###",
    "* Interfase © 2014-2015 Flavio Danesse <fdanesse@gmail.com> Uruguay - GPLv2+",
    "* Videojuego 1 © 2014-2015 Sebastian Silva <sebastian@fuentelibre.org> - GPLv2+",
    "* Videojuego 2 © 2014-2015 Sebastian Silva <sebastian@fuentelibre.org> - GPLv2+",
    "* popupmenubutton.py - Copyright 2008-2011 Zuza Software Foundation - GPLv2+",
    "HHH",
    "### User Experience Design / Diseño de Experiencia de Usuario ###",
    "HHH",
    "PLE V1.0 Beta © 2014-2015 Laura Vargas - Colombia - CC BY-SA 3.0",
    "HHH",
    "Con aportes de Koke Contreras, Sebastian Silva, Flavio Danesse,",
    "Aliosh Neira, Cecilia Bustamante y Maria Elisa de la Vega, así",
    "como los demás funcionarios del Plan de Inglés del Ministerio",
    "de Educación del Perú.",
    "Plan Nacional Perú Bilingüe en Inglés 2021."
    "HHH",
    "Attribution  of Works / Reconocimiento de Obras",
    "-----------------------------------------------",
    "HHH",
    "### Videos and Images / Videos e Imágenes ###",
    "HHH",
    "#### Bunny Bonita “Feelings” - CC BY-NC",
    "#### Bunny Bonita “Family” - CC BY-NC",
    " Ministerio de Educación Nacional República de Colombia",
    "HHH",
    " © 2008-2013 T&T Teaching and Tutoring y Faldita Films Bunny Bonita",
    "HHH",
    "#### Art4Apps “Pete the Athlete” - CC BY-SA",
    "#### Art4Apps “Trish the Fish” CC BY-SA",
    "#### Art4Apps “A Shell at the Shore” CC BY-SA",
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
    "HHH",
    "#### Tipografías",
    "Logotipos y títulos elaborados en *Decade*, de \"Anthem Type\" (Joey Nelson)",
    ]

FONT = "Monospace"
TAM = 40
RED = 255
GREEN = 255
BLUE = 255

BASE_PATH = os.path.dirname(__file__)


class CreditsView(gtk.EventBox):

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, COLORES["window"])
        self.set_border_width(10)

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

        self.modify_bg(gtk.STATE_NORMAL, COLORES["text"])

        self.posy = 300
        self.update = False
        self.imagen = False

        self.connect("expose-event", self.__expose)
        self.connect("realize", self.__realize)
        self.show_all()

    def __expose(self, widget, event):
        self.new_handle(True)

    def __realize(self, widget):
        cr = self.window.cairo_create()
        self.imagen = cairo.ImageSurface.create_from_png(os.path.join(
            BASE_PATH, "Iconos", "creditos_ple.png"))

    def __handle(self):
        cr = self.window.cairo_create()
        x, y, w, h = self.get_allocation()
        cr.rectangle (x, y, w, h)
        cr.set_source_surface(self.imagen)
        cr.fill ()
        self.posy -= 1
        return True

    def new_handle(self, reset):
        if self.update:
            gobject.source_remove(self.update)
            self.update = False
        if reset:
            self.posy = 300
            self.update = gobject.timeout_add(50, self.__handle)
