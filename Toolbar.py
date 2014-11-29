#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import gtk
import gobject
import pango
import gobject

from Globales import COLORES
from Globales import describe_archivo

BASE_PATH = os.path.dirname(__file__)


class Toolbar(gtk.EventBox):

    __gsignals__ = {
    "activar": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,
        gobject.TYPE_BOOLEAN)),
    "video": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING, ))}

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.set_border_width(4)

        toolbar = gtk.Toolbar()

        self.modify_bg(gtk.STATE_NORMAL, COLORES["toolbar"])
        self.modify_fg(gtk.STATE_NORMAL, COLORES["text"])
        toolbar.modify_bg(gtk.STATE_NORMAL, COLORES["toolbar"])
        toolbar.modify_fg(gtk.STATE_NORMAL, COLORES["text"])

        self.buttons = []
        for text in ["Home", "Instructions", "Credits"]:
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
            separador = gtk.SeparatorToolItem()
            separador.props.draw = True
            toolbar.insert(separador, -1)

        self.menubar = MenuBar()

        item = gtk.ToolItem()
        item.set_expand(True)
        item.add(self.menubar)
        toolbar.insert(item, -1)

        self.add(toolbar)
        self.show_all()

        self.menubar.connect("activar", self.__emit_accion_menu)

    def __emit_accion_menu(self, widget, video_path):
        self.emit("video", video_path)

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


class MenuBar(gtk.MenuBar):

    __gsignals__ = {
    "activar": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING, ))}

    def __init__(self):

        gtk.MenuBar.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, COLORES["toolbar"])
        self.modify_fg(gtk.STATE_NORMAL, COLORES["text"])
        self.modify_font(pango.FontDescription("Purisa 20"))

        itemmenu = gtk.MenuItem("Topics")
        itemmenu.child.modify_font(pango.FontDescription("Purisa 20"))
        itemmenu.child.modify_fg(gtk.STATE_NORMAL, COLORES["text"])
        itemmenu.child.modify_bg(gtk.STATE_NORMAL, COLORES["toolbar"])

        menu = gtk.Menu()
        menu.modify_font(pango.FontDescription("Purisa 12"))
        menu.modify_bg(gtk.STATE_NORMAL, COLORES["toolbar"])
        menu.modify_fg(gtk.STATE_NORMAL, COLORES["text"])
        itemmenu.set_submenu(menu)
        self.append(itemmenu)

        self.boton0 = gtk.RadioButton()
        video_path = os.path.join(BASE_PATH, "Video")
        for arch in sorted(os.listdir(video_path)):
            path = os.path.join(video_path, arch)
            tipo = describe_archivo(path)
            if 'video' in tipo or 'application/ogg' in tipo:
                item = gtk.MenuItem()
                try:
                    item.get_child().destroy()
                except:
                    pass
                boton = gtk.RadioButton()
                boton.set_group(self.boton0)
                boton.set_label(arch)
                item.add(boton)
                item.connect("activate", self.__emit_accion_menu)
                menu.append(item)
        self.boton0.set_active(True)

    def __emit_accion_menu(self, widget):
        widget.get_children()[0].set_active(True)
        label = widget.get_children()[0].get_label()
        video_path = os.path.join(BASE_PATH, "Video", label)
        self.emit("activar", video_path)
