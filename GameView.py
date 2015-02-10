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
import gobject
import gtk
import pango

installed_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(1, os.path.join(installed_dir, "Lib/"))

import sugargame2
import sugargame2.canvas
import spyral
import pygame

from ConfigParser import SafeConfigParser
from Globales import COLORES

class GameMenu(gtk.EventBox):

    __gsignals__ = {
    "video": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING, ))}

    def __init__(self):

        gtk.EventBox.__init__(self)

        vb = gtk.VBox()

        self.modify_bg(gtk.STATE_NORMAL, COLORES["contenido"])
        self.set_border_width(4)

        self.inside_vb = gtk.VBox()

        self.ug1 = gtk.Button()
        imagen = gtk.Image()
        imagen.set_from_file("Imagenes/juego1_banner.png")
        self.ug1.modify_bg(gtk.STATE_NORMAL, COLORES["toolbar"])
        self.ug1.add(imagen)

        self.ug2 = gtk.Button()
        imagen = gtk.Image()
        imagen.set_from_file("Imagenes/juego2_banner.png")
        self.ug2.modify_bg(gtk.STATE_NORMAL, COLORES["toolbar"])
        self.ug2.add(imagen)

        self.ug3 = gtk.Button()
        imagen = gtk.Image()
        imagen.set_from_file("Imagenes/juego3_banner.png")
        self.ug3.modify_bg(gtk.STATE_NORMAL, COLORES["toolbar"])
        self.ug3.add(imagen)

        butt = gtk.Button()
        img = gtk.Image()
        img.set_from_file("Imagenes/go_back_disabled.png")
        butt.set_relief(gtk.RELIEF_NONE)
        butt.set_image(img)
        butt.set_label("")
        butt.modify_bg(gtk.STATE_NORMAL, COLORES["toolbar"])
        butt.connect("clicked", self.__emit_video)
        butt.connect("enter-notify-event", self.__color)
        butt.connect("leave-notify-event", self.__decolor)
        img.show()
        butt.show()
        self.back = gtk.Alignment(1, 1, 0, 0)
        self.back.add(butt)

        self.titulo = gtk.Label("Título")
        self.titulo.set_property("justify", gtk.JUSTIFY_CENTER)
        self.titulo.modify_font(pango.FontDescription("DejaVu Sans Bold 20"))
        self.titulo.modify_fg(gtk.STATE_NORMAL, COLORES["window"])
        self.titulo.set_padding(xpad=20, ypad=50)

        index = 0
        for butt in self.ug1, self.ug2, self.ug3:
            butt.modify_bg(gtk.STATE_NORMAL, COLORES["toolbar"])
            butt.modify_fg(gtk.STATE_NORMAL, COLORES["text"])
            butt.child.modify_font(pango.FontDescription(
                "DejaVu Sans Bold 12"))
            align = gtk.Alignment(0.5, 0.5, 0.3, 0.2)
            align.add(butt)
            self.inside_vb.add(align)
            butt.connect("clicked", self.start_game, index)
            index += 1

        self.inside_vb.add(self.back)

        vb.pack_start(self.titulo, expand=False, fill=False)
        vb.add(self.inside_vb)

        self.gameview = GameView()
        vb.pack_end(self.gameview, True, True, 0)
        self.add(vb)

    def stop(self):
        self.gameview.stop()
        self.hide()

    def run(self, topic):
        parser = SafeConfigParser()
        metadata = os.path.join(topic, "topic.ini")
        parser.read(metadata)

        self.titulo.set_text("Play Practice: " + parser.get('topic', 'title'))
        self.topic = topic
        self.show_all()
        self.gameview.hide()

    def start_game(self, widget, index):
        self.inside_vb.hide()
        self.titulo.hide()
        self.gameview.run(self.topic, index)

    def __decolor(self, widget, event):
        widget.get_image().set_from_file("Imagenes/go_back_disabled.png")

    def __color(self, widget, event):
        widget.get_image().set_from_file("Imagenes/go_back.png")

    def __emit_video(self, widget):
        self.emit("video", self.topic)


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
        self.firstrun = True

        self.pygamecanvas = sugargame2.canvas.PygameCanvas(self)

        grupo1 = gtk.Alignment(0.5, 1, 0, 0)
        separador = gtk.HSeparator()
        grupo1.add(separador)

        grupo2 = gtk.Alignment(1, 0.5, 0, 0)
        grupo2.add(self.pygamecanvas)

        grupo3 = gtk.Alignment(1, 1, 0, 0)
        vbox = gtk.VBox()

        butt = gtk.Button()
        img = gtk.Image()
        img.set_from_file("Imagenes/go_back_disabled.png")
        butt.set_relief(gtk.RELIEF_NONE)
        butt.set_image(img)
        butt.set_label("")
        butt.modify_bg(gtk.STATE_NORMAL, COLORES["toolbar"])
        butt.connect("clicked", self.__reset_menu)
        butt.connect("enter-notify-event", self.__color)
        butt.connect("leave-notify-event", self.__decolor)
        img.show()
        butt.show()
        vbox.add(butt)

        self.score_label = gtk.Label("SCORE\n0")
        self.score_label.set_property("justify", gtk.JUSTIFY_RIGHT)
        self.score_label.modify_font(pango.FontDescription(
            "DejaVu Sans Mono 22"))
        self.score_label.modify_fg(gtk.STATE_NORMAL, COLORES["window"])
        self.score_label.set_padding(xpad=30, ypad=30)
        self.score_label.show()
        vbox.add(self.score_label)

        butt = gtk.ToggleButton()
        butt.set_active(False)
        butt.set_relief(gtk.RELIEF_NONE)
        butt.modify_bg(gtk.STATE_NORMAL, COLORES["toolbar"])
        img = gtk.Image()
        img.set_from_file("Iconos/stock_volume-max.svg")
        butt.set_image(img)
        butt.set_label("")
        img.show()
        butt.show()
        butt.connect("toggled", self.update_volume)
        self.volbtn = butt

        vbox.add(butt)
        grupo3.add(vbox)

        hb = gtk.HBox()
        hb.pack_start(grupo1)
        hb.add(grupo2)
        hb.pack_end(grupo3)

        self.add(hb)

        self.connect("size-allocate", self.__reescalar)
        self.show_all()

    def update_score(self, score):
        self.score_label.set_text("SCORE\n%s" % str(score))

    def update_volume(self, widget):
        if not widget.get_active():
            if self.game:
                self.game.mute(False)
            iconfile = "Iconos/stock_volume-max.svg"
            self.pygamecanvas.grab_focus()
        else:
            self.game.mute(True)
            iconfile = "Iconos/stock_volume-mute.svg"
            pygame.mixer.fadeout(300)
            self.pygamecanvas.grab_focus()
        widget.get_image().set_from_file(iconfile)

    def __decolor(self, widget, event):
        widget.get_image().set_from_file("Imagenes/go_back_disabled.png")

    def __color(self, widget, event):
        widget.get_image().set_from_file("Imagenes/go_back.png")

    def __reset_menu(self, widget):
        self.stop()
        self.parent.show_all()
        self.hide()

    def __reescalar(self, widget, event):
        if self.game:
            rect = self.get_allocation()
            # FIXME: El juego debe reescalarse a: rect.width, rect.height

    def __run_game_1(self):
        from Games.ug1.runme import Intro

        rect = self.get_allocation()
        self.lado = min(rect.width-8, rect.height-8)
        print self.lado
        self.pygamecanvas.set_size_request(self.lado, self.lado)
        spyral.director.init((self.lado, self.lado),
            fullscreen=False, max_fps=30)
        self.game = Intro(self.topic, self)
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
        print self.lado
        self.pygamecanvas.set_size_request(self.lado, self.lado)
        spyral.director.init((self.lado, self.lado),
            fullscreen=False, max_fps=30)
        self.game = Escena(self.topic, self)
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
        print self.lado
        self.pygamecanvas.set_size_request(self.lado, self.lado)
        spyral.director.init((self.lado, self.lado),
            fullscreen=False, max_fps=30)
        self.game = Escena(self.topic, gameview=self)
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
            pygame.mixer.music.stop()
            spyral.director.pop()
            self.game = False
        self.hide()

    def run(self, topic, game):
        self.update_score(0)
        self.volbtn.set_active(False)
        self.volbtn.get_image().set_from_file("Iconos/stock_volume-max.svg")
        self.topic = topic
        self.pygamecanvas.grab_focus()
        self.show()
        if game==0:
            gamestart=self.__run_game_1
        elif game==1:
            gamestart=self.__run_game_2
        elif game==2:
            gamestart=self.__run_game_3
        if self.firstrun:
            self.firstrun = False
            gobject.idle_add(self.pygamecanvas.run_pygame(gamestart))
        else:
            gobject.idle_add(gamestart())
