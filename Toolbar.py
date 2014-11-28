#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gtk
import gobject
import pango
import gobject

from Globales import COLORES


class Toolbar(gtk.EventBox):

    __gsignals__ = {
    "activar": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,
        gobject.TYPE_BOOLEAN))}

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.set_border_width(4)

        toolbar = gtk.Toolbar()

        self.modify_bg(gtk.STATE_NORMAL, COLORES["toolbar"])
        toolbar.modify_bg(gtk.STATE_NORMAL, COLORES["toolbar"])

        self.buttons = []
        for text in ["Home", "Instructions", "Credits", "Topics"]:
            item = gtk.ToolItem()
            item.set_expand(True)
            label = gtk.Label(text)
            label.modify_font(pango.FontDescription("Purisa 20"))
            boton = gtk.ToggleToolButton()
            boton.set_label_widget(label)
            boton.connect("toggled", self.__do_toggled)
            self.buttons.append(boton)
            item.add(boton)
            toolbar.insert(item, -1)
            if text != "Topics":
                separador = gtk.SeparatorToolItem()
                separador.props.draw = True
                toolbar.insert(separador, -1)

        self.add(toolbar)
        self.show_all()

    def __do_toggled(self, widget):
        label = widget.get_label_widget().get_text()
        activo = widget.get_active()
        if activo:
            for button in self.buttons:
                if label != button.get_label_widget().get_text():
                    button.set_active(False)
            self.emit("activar", label, activo)
        else:
            for button in self.buttons:
                if button.get_active():
                    return
            self.buttons[0].set_active(True)
