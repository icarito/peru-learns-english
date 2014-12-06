#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   GameView.py por:
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

import sys
sys.path.insert(1, "Lib/")

import gtk

from Globales import COLORES

import gobject
import sugargame2
import sugargame2.canvas
import spyral
import pygame
from Games.ug1.runme import Escena


class GameView(gtk.EventBox):

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, COLORES["contenido"])
        self.set_border_width(4)

        self.game = False
        self.pump = False

        self.pygamecanvas = sugargame2.canvas.PygameCanvas(self)
        #self.pygamecanvas.set_flags(gtk.EXPAND)
        #self.pygamecanvas.set_flags(gtk.FILL)

        grupo = gtk.Alignment(0.5, 0.5, 0,0)
        grupo.add(self.pygamecanvas)

        self.add(grupo)

        self.connect("size-allocate", self.__reescalar)
        self.show_all()

    def __reescalar(self, widget, event):
        if self.game:
            rect = self.get_allocation()
            print "FIXME: El juego debe reescalarse a", rect.width, rect.height

    def __run_game(self):
        rect = self.get_allocation()
        self.lado = min(rect.width-8, rect.height-8)
        self.pygamecanvas.set_size_request(self.lado, self.lado)
        spyral.director.init((self.lado, self.lado),
            fullscreen=False, max_fps=30)
        self.game = Escena(self, self.topic)
        spyral.director.push(self.game)
        if self.pump:
            gobject.source_remove(self.pump)
            self.pump = False
        self.pump = gobject.timeout_add(300, self.__pump)
        spyral.director.run(sugar=True)

    def __pump(self):
        pygame.event.pump()
        return True

    def stop(self):
        if self.pump:
            gobject.source_remove(self.pump)
            self.pump = False
        if self.game:
            spyral.quit()
            del(self.game)
            self.game = False
        self.hide()

    def run(self, topic):
        print topic
        self.topic = topic
        self.pygamecanvas.run_pygame(self.__run_game)
        self.pygamecanvas.grab_focus()
        self.show()
