#!/bin/env python2
# -*- coding: utf-8 -*-

# English For Fun
# Copyright © 2014 Sebastian Silva

# This software is under GPLv3 or later

import gtk

class Navegacion(gtk.Notebook):
    """
    Esta clase se encarga de encapsular el resto de la funcionalidad.
    La navegación está sujeta a cambiar.
    """

    def __init__(self):
        gtk.Notebook.__init__(self)
        label1 = gtk.Label("Aquí va el Player de Video")
        label2 = gtk.Label("Aquí va el lienzo de Pygame")
        label3 = gtk.Label("Aquí van los Flashcards")

        self.append_page(gtk.Label("1"),label1) # meter jamedia player aqui
        self.append_page(gtk.Label("2"),label2) # meter sugargame2 aqui
        self.append_page(gtk.Label("3"),label3) # inventarse algo como anki aqui

        self.set_tab_pos(gtk.POS_LEFT)

window = gtk.Window()
window.connect("destroy", gtk.main_quit)
notebook = Navegacion()
window.add(notebook)
window.show_all()

gtk.main()
