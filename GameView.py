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

        self.modify_bg(gtk.STATE_NORMAL, COLORES["toolbar"])
        self.set_border_width(4)

        self.game_widget = GameBox()

        self.add(self.game_widget)
        self.show_all()

    def stop(self):
        self.game_widget.stop()
        self.hide()

    def run(self, topic):
        self.show()
        self.game_widget.load(topic)


class GameBox(gtk.VBox):
    def __init__(self):
        gtk.VBox.__init__(self)

        self.pygamecanvas = sugargame2.canvas.PygameCanvas(self)
        self.pygamecanvas.set_flags(gtk.EXPAND)
        self.pygamecanvas.set_flags(gtk.FILL)

        self.connect("visibility-notify-event", self.redraw)
        self.pygamecanvas.set_events(gtk.gdk.BUTTON_PRESS_MASK)
        self.pygamecanvas.connect("button-press-event", self.pygamecanvas.grab_focus)

        self.add(self.pygamecanvas)
        gobject.timeout_add(300, self.pump)

        self.show_all()
        self.pygamecanvas.run_pygame(self.run_game)

    def redraw(self, *args, **kwargs):
        scene = spyral.director.get_scene()
        if scene:
            scene.redraw()

    def pump(self):
        # Esto es necesario porque sino pygame acumula demasiados eventos.
        pygame.event.pump()

    def run_game(self):
        spyral.director.init((700,700), fullscreen=False, max_fps=30)
        self.game = Escena(self)
        spyral.director.push(self.game)
        self.start()

    def start(self):
        spyral.director.run(sugar = True)

    def load(self, topic):
        scene = spyral.director.get_scene()
        scene.redraw()
        self.show()

    def stop(self):
        p = PauseScene()
        spyral.director.push(p)
        self.hide()

class PauseScene(spyral.Scene):
    def __init__(self):
        spyral.Scene.__init__(self, (700, 700), 20, 20)
        self.background = spyral.Image(size=(800, 800)).fill((0, 0, 0))

        spyral.event.register("input.keyboard.down.*", spyral.director.pop)
