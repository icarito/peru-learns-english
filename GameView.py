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
import gobject
import spyral
import pygame
import sugargame2
import sugargame2.canvas

from Globales import COLORES

from Games.ug1.runme import Escena


class GameView(gtk.EventBox):

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, COLORES["toolbar"])
        self.set_border_width(4)

        self.game = False
        self.pump = False

        self.pygamecanvas = sugargame2.canvas.PygameCanvas(self)
        self.pygamecanvas.set_flags(gtk.EXPAND)
        self.pygamecanvas.set_flags(gtk.FILL)

        self.add(self.pygamecanvas)

        self.connect("size-allocate", self.__reescalar)
        self.show_all()

    def __reescalar(self, widget, event):
        if self.game:
            rect = self.get_allocation()
            print "FIXME: El juego debe reescalarse a", rect.width, rect.height

    def __run_game(self):
        rect = self.get_allocation()
        spyral.director.init((rect.width, rect.height),
            fullscreen=False, max_fps=30)
        self.game = Escena(self)
        spyral.director.push(self.game)
        if self.pump:
            gobject.source_remove(self.pump)
            self.pump = False
        self.pump = gobject.timeout_add(300, self.__pump)
        spyral.director.run(sugar=True)

    def __pump(self):
        # FIXME: HACK porque sino pygame acumula demasiados eventos.
        # No es mejor hacer pygame.event.clear() ?
        pygame.event.pump()
        return True

    def stop(self):
        print "FIXME: El juego debe detenerse y eliminarse."
        if self.pump:
            gobject.source_remove(self.pump)
            self.pump = False
        if self.game:
            del(self.game)
            self.game = False
        self.hide()

    def run(self, topic):
        self.pygamecanvas.run_pygame(self.__run_game)
        self.show()

    def procesar_key_press_event(self, event):
        if self.game:
            key = gtk.gdk.keyval_name(event.keyval)
            try:
                keycode = getattr(pygame, 'K_'+key.lower())
            except:
                keycode = getattr(pygame, 'K_'+key.upper())
            else:
                print "ERROR: Falta Traducir:", gtk.gdk.keyval_name(event.keyval)
                return
            ukey = unichr(gtk.gdk.keyval_to_unicode(event.keyval))
            evt = pygame.event.Event(pygame.KEYDOWN, key=keycode, unicode=ukey, mod=0)
            pygame.event.post(evt)

    def procesar_key_release_event(self, event):
        if self.game:
            key = gtk.gdk.keyval_name(event.keyval)
            try:
                keycode = getattr(pygame, 'K_'+key.lower())
            except:
                keycode = getattr(pygame, 'K_'+key.upper())
            else:
                print "ERROR: Falta Traducir:", gtk.gdk.keyval_name(event.keyval)
                return
            ukey = unichr(gtk.gdk.keyval_to_unicode(event.keyval))
            evt = pygame.event.Event(pygame.KEYUP, key=keycode, unicode=ukey, mod=0)
            pygame.event.post(evt)
