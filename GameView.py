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

import os
import sys
installed_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(1, os.path.join(installed_dir, "Lib/"))

import gtk
import pango

import sugargame2
import sugargame2.canvas
import spyral
import pygame

from Globales import COLORES

import gobject

class GameMenu(gtk.VBox):
    def __init__(self):
        gtk.VBox.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, COLORES["contenido"])
        self.set_border_width(4)

        self.hbox = gtk.HBox()

        self.ug1 = gtk.Button("Hello Asteroids")
        self.ug2 = gtk.Button("Reforestation Circuit")
        self.ug3 = gtk.Button("The Chakana Cross")

        index = 0
        for butt in self.ug1, self.ug2, self.ug3:
            butt.modify_bg(gtk.STATE_NORMAL, COLORES["toolbar"])
            butt.modify_fg(gtk.STATE_NORMAL, COLORES["text"])
            butt.child.modify_font(pango.FontDescription("DejaVu Sans Bold 16"))
            self.hbox.pack_start(butt)
            butt.connect("clicked", self.start_game, index)
            index += 1

        self.pack_start(self.hbox)

        self.gameview = GameView()
        self.pack_end(self.gameview, True, True, 0)

    def stop(self):
        self.gameview.stop()
        self.hide()

    def run(self, topic):
        self.topic = topic
        self.show_all()
        self.gameview.hide()

    def start_game(self, widget, index):
        self.gameview.run(self.topic, index)
        self.hbox.hide()

class GameView(gtk.EventBox):

    __gsignals__ = {
    "video": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING, ))}

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, COLORES["contenido"])
        self.set_border_width(4)

        self.game = False
        self.pump = False

        self.pygamecanvas = sugargame2.canvas.PygameCanvas(self)
        #self.pygamecanvas.set_flags(gtk.EXPAND)
        #self.pygamecanvas.set_flags(gtk.FILL)

        grupo1 = gtk.Alignment(0.5, 0, 0,0)
        butt = gtk.Button()
        img = gtk.Image()
        img.set_from_stock(gtk.STOCK_GO_BACK, gtk.ICON_SIZE_DIALOG)
        butt.set_image(img)
        butt.set_label("")
        butt.modify_bg(gtk.STATE_NORMAL, COLORES["toolbar"])
        butt.modify_fg(gtk.STATE_NORMAL, COLORES["text"])
        butt.connect("clicked", self.__emit_video)
        grupo1.add(butt)

        grupo2 = gtk.Alignment(0.5, 0.5, 0,0)
        grupo2.add(self.pygamecanvas)

        hb = gtk.HBox()
        hb.pack_start(grupo1, expand=False, fill=False)
        hb.pack_end(grupo2)

        self.add(hb)

        self.connect("size-allocate", self.__reescalar)
        self.show_all()

    def __emit_video(self, widget):
        self.emit("video", self.topic)

    def __reescalar(self, widget, event):
        if self.game:
            rect = self.get_allocation()
            # FIXME: El juego debe reescalarse a: rect.width, rect.height

    def __run_game_1(self):
        from Games.ug1.runme import Intro

        rect = self.get_allocation()
        self.lado = min(rect.width-8, rect.height-8)
        self.pygamecanvas.set_size_request(self.lado, self.lado)
        spyral.director.init((self.lado, self.lado),
            fullscreen=False, max_fps=30)
        self.game = Intro(self.topic)
        spyral.director.push(self.game)
        if self.pump:
            gobject.source_remove(self.pump)
            self.pump = False
        self.pump = gobject.timeout_add(300, self.__pump)
        try:
            spyral.director.run(sugar=True)
        except pygame.error:
            pass

    def __run_game_2(self):
        from Games.ug2.runme import Escena

        rect = self.get_allocation()
        self.lado = min(rect.width-8, rect.height-8)
        self.pygamecanvas.set_size_request(self.lado, self.lado)
        spyral.director.init((self.lado, self.lado),
            fullscreen=False, max_fps=30)
        self.game = Escena(self.topic)
        spyral.director.push(self.game)
        if self.pump:
            gobject.source_remove(self.pump)
            self.pump = False
        self.pump = gobject.timeout_add(300, self.__pump)
        try:
            spyral.director.run(sugar=True)
        except pygame.error:
            pass

    def __run_game_3(self):
        from Games.ug3.runme import Escena

        rect = self.get_allocation()
        self.lado = min(rect.width-8, rect.height-8)
        self.pygamecanvas.set_size_request(self.lado, self.lado)
        spyral.director.init((self.lado, self.lado),
            fullscreen=False, max_fps=30)
        self.game = Escena(self.topic)
        spyral.director.push(self.game)
        if self.pump:
            gobject.source_remove(self.pump)
            self.pump = False
        self.pump = gobject.timeout_add(300, self.__pump)
        try:
            spyral.director.run(sugar=True)
        except pygame.error:
            pass

    def __pump(self):
        pygame.event.pump()
        return True

    def stop(self):
        if self.pump:
            gobject.source_remove(self.pump)
            self.pump = False
        if self.game:
            try:
                pygame.event.clear()
                spyral.quit()
                del(self.game)
            except spyral.exceptions.GameEndException, pygame.error:
                pass
            finally:
                self.game = False
        self.hide()

    def run(self, topic, game):
        if game==0:
            gamestart=self.__run_game_1
        elif game==1:
            gamestart=self.__run_game_2
        elif game==2:
            gamestart=self.__run_game_3
        self.topic = topic
        self.pygamecanvas.run_pygame(gamestart)
        self.pygamecanvas.grab_focus()
        self.show()
