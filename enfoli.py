#!/bin/env python2
# -*- coding: utf-8 -*-

import os
import gtk
import sys
import gobject

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
        self.set_resizable(True)
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
        self.connect("delete-event", self.__salir)

        self.resize(640, 480)
        gobject.idle_add(self.__switch, False, "Home", True)

    def __switch(self, widget, label, activo):
        map(ocultar, self.vbox.get_children()[1:])
        if label == "Home":
            self.homeview.run()
        elif label == "Instructions":
            self.instructionsview.run()
        elif label == "Credits":
            self.creditsview.run()
        elif label == "Topics":
            self.videoview.run()
        return False

    def __salir(self, widget=None, senial=None):
        gtk.main_quit()
        sys.exit(0)


if __name__ == '__main__':
    Main()
    gtk.main()
