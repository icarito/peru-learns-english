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

from Toolbar import Toolbar
from Globales import COLORES
from HomeView import HomeView
from VideoView import VideoView
from FlashCardView import FlashCardView
from GameView import GameView
from InstructionsView import InstructionsView
from CreditsView import CreditsView

BASE_PATH = os.path.dirname(__file__)


def ocultar(widget):
    widget.stop()


class Main(gtk.Window):

    def __init__(self):

        gtk.Window.__init__(self)

        #self.set_title("")
        #self.set_icon_from_file(os.path.join(BASE_PATH, "Iconos", ""))
        self.modify_bg(gtk.STATE_NORMAL, COLORES["window"])
        self.maximize()
        self.set_resizable(False)
        self.set_border_width(2)
        self.set_position(gtk.WIN_POS_CENTER)

        self.vbox = gtk.VBox()
        self.toolbar = Toolbar()
        self.vbox.pack_start(self.toolbar, False, False, 0)

        self.homeview = HomeView()
        self.vbox.pack_start(self.homeview, True, True, 0)

        self.videoview = VideoView()
        self.vbox.pack_start(self.videoview, True, True, 0)

        self.flashcards = FlashCardView()
        self.vbox.pack_start(self.flashcards, True, True, 0)

        self.gameview = GameView()
        self.vbox.pack_start(self.gameview, True, True, 0)

        self.instructionsview = InstructionsView()
        self.vbox.pack_start(self.instructionsview, True, True, 0)

        self.creditsview = CreditsView()
        self.vbox.pack_start(self.creditsview, True, True, 0)

        self.add(self.vbox)
        self.show_all()

        self.toolbar.connect("activar", self.__switch)
        self.toolbar.connect("video", self.__play_video)
        self.videoview.connect("flashcards", self.__play_flashcards)
        self.videoview.connect("game", self.__play_game)
        self.connect("delete-event", self.__salir)

        self.toolbar.buttons[0].set_active(True)

    def __play_game(self, widget, topic):
        self.__switch(False, "game", topic)

    def __play_flashcards(self, widget, topic):
        self.__switch(False, "flashcards", topic)

    def __play_video(self, widget, topic):
        self.__switch(False, "Topics", topic)

    def __switch(self, widget, label, data=False):
        map(ocultar, self.vbox.get_children()[1:])
        if label == "Home":
            self.homeview.run()
        elif label == "Instructions":
            self.instructionsview.run()
        elif label == "Credits":
            self.creditsview.run()
        elif label == "Topics":
            self.videoview.run(data)
        elif label == "flashcards":
            self.flashcards.run(data)
        elif label == "game":
            self.gameview.run(data)
        return False

    def __salir(self, widget=None, senial=None):
        gtk.main_quit()
        sys.exit(0)


if __name__ == '__main__':
    Main()
    gtk.main()
