#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gtk
from PlayerControls import PlayerControls
from Globales import COLORES


class VideoPlayer(gtk.EventBox):

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, COLORES["text"])

        vbox = gtk.VBox()
        self.visor = Visor()
        self.control = PlayerControls()

        vbox.pack_start(self.visor, True, True, 0)
        vbox.pack_start(self.control, False, True, 0)

        self.add(vbox)
        self.show_all()

        self.control.connect("accion-controls", self.__control)

    def __control(self, widget, accion):
        print accion


class Visor(gtk.DrawingArea):

    def __init__(self):

        gtk.DrawingArea.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, COLORES["text"])

        self.show_all()
