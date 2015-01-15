#!/bin/env python2
# -*- coding: utf-8 -*-

#   Main.py por:
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
import sys

installed_dir = os.path.abspath(os.path.dirname(__file__))
os.chdir(installed_dir)

from Toolbar import Toolbar
from Globales import COLORES
from VideoView import VideoView
from FlashCardView import FlashCardView
from GameView import GameMenu
from GameView import GameView
from InstructionsView import InstructionsView
from CreditsView import CreditsView

BASE_PATH = os.path.dirname(__file__)

OLD_GTK = False
if gtk.pygtk_version[0]==2 and gtk.pygtk_version[1]<15:
    OLD_GTK = True

def ocultar(widget):
    widget.stop()


class Main(gtk.Window):

    def __init__(self):

        gtk.Window.__init__(self)

        self.set_title("English for Peru")
        self.set_icon_from_file(os.path.join(
            BASE_PATH , "Iconos", "icono.svg"))

        self.modify_bg(gtk.STATE_NORMAL, COLORES["window"])
        self.set_border_width(2)

        # FIXME: No funciona en la XO con fedora 11
        #self.set_resizable(False)

        if OLD_GTK:
            # Esto es un hack para que gtk viejo en la XO no se maree
            width = gtk.gdk.screen_width() - 6
            height = gtk.gdk.screen_height() - 100
            self.set_geometry_hints(self, width, height, width, height)
        else:
            self.maximize()

        self.vbox = gtk.VBox()
        self.toolbar = Toolbar()
        self.vbox.pack_start(self.toolbar, False, False, 0)

        self.videoview = VideoView()
        self.vbox.pack_start(self.videoview, True, True, 0)

        self.flashcards = FlashCardView()
        self.vbox.pack_start(self.flashcards, True, True, 0)

        self.gamemenu = GameMenu()
        self.vbox.pack_start(self.gamemenu, True, True, 0)

        self.instructionsview = InstructionsView()
        self.vbox.pack_start(self.instructionsview, True, True, 0)

        self.creditsview = CreditsView()
        self.vbox.pack_start(self.creditsview, True, True, 0)

        self.add(self.vbox)
        self.show_all()

        self.toolbar.connect("activar", self.__switch)
        self.toolbar.connect("video", self.__play_video)
        self.gamemenu.gameview.connect("video", self.__game_return_to_video)
        self.videoview.connect("flashcards", self.__play_flashcards)
        self.videoview.connect("game", self.__play_game)
        self.instructionsview.connect("credits", self.__play_credits)
        self.instructionsview.connect("start", self.__show_menu)
        self.connect("delete-event", self.__salir)

        self.toolbar.buttons[0].set_active(True)

        self.__switch(False, "Instructions", None)

    def __game_return_to_video(self, widget, topic):
        self.__play_video(widget, topic)
        self.videoview.set_full(False)

    def __play_game(self, widget, topic):
        self.__switch(False, "game", topic)

    def __play_flashcards(self, widget, topic):
        self.__switch(False, "flashcards", topic)

    def __play_video(self, widget, topic):
        self.__switch(False, "Topics", topic)

    def __play_credits(self, widget):
        self.__switch(False, "Credits")
        self.toolbar.buttons[0].set_active(False)

    def __show_menu(self, widget):
        self.toolbar.menubutton.popup()
        self.toolbar.menubutton.set_active(True)
        self.toolbar.buttons[0].set_active(False)

    def __switch(self, widget, label, data=False):
        map(ocultar, self.vbox.get_children()[1:])
        if label == "Instructions":
            self.instructionsview.run()
        elif label == "Credits":
            self.creditsview.run()
        elif label == "Topics":
            self.videoview.run(data)
        elif label == "flashcards":
            self.flashcards.run(data)
        elif label == "game":
            self.gamemenu.run(data)
        return False

    def __salir(self, widget=None, senial=None):
        self.videoview.stop()
        gtk.main_quit()
        sys.exit(0)


if __name__ == '__main__':
    Main()
    gtk.main()
