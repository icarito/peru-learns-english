#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gtk

from Globales import COLORES


class HomeView(gtk.EventBox):

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, COLORES["toolbar"])
        self.set_border_width(4)

        self.add(gtk.Label("Home"))
        self.show_all()

    def stop(self):
        self.hide()

    def run(self):
        self.show()
