#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gtk
from VideoPlayer.VideoPlayer import VideoPlayer

from Globales import COLORES


class VideoView(gtk.EventBox):

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, COLORES["toolbar"])
        self.set_border_width(4)

        tabla = gtk.Table(rows=10, columns=3, homogeneous=True)
        tabla.set_property("column-spacing", 5)
        tabla.set_property("row-spacing", 5)
        tabla.set_border_width(4)

        self.titulo = gtk.Label("Título")
        self.videoplayer = VideoPlayer()
        self.links = gtk.Label("Links")

        tabla.attach(self.titulo, 0, 2, 0, 1)
        tabla.attach(self.videoplayer, 0, 2, 1, 9)
        tabla.attach(self.links, 0, 2, 9, 10)

        tabla.attach(gtk.EventBox(), 2, 3, 0, 4)
        tabla.attach(gtk.EventBox(), 2, 3, 4, 6)
        tabla.attach(gtk.EventBox(), 2, 3, 6, 10)

        self.add(tabla)
        self.show_all()

    def stop(self):
        self.hide()

    def run(self):
        self.show()
