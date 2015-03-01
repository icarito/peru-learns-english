#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   VideoView.py por:
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
import gtk
import gobject
import pango
import string

from ConfigParser import SafeConfigParser
from glob import glob
from VideoPlayer.VideoPlayer import VideoPlayer

from Globales import COLORES, is_xo
from Globales import get_user_dict
from Globales import decir_demorado

GRADOS = ["1°", "2°", "3°", "4°", "5°", "6°"]
EDADES = range(5, 21, 1)

installed_dir = os.path.abspath(os.path.dirname(__file__))
parent_dir = installed_dir.rstrip("Tv/")
sys.path.insert(1, parent_dir)

BASE_PATH = parent_dir

class VideoView(gtk.EventBox):

    __gsignals__ = {
    "flashcards": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT, )),
    "game": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING, ))}

    def __init__(self, top=None):

        gtk.EventBox.__init__(self)

        if top:
            self.top_window = top

        self.modify_bg(gtk.STATE_NORMAL, COLORES["contenido"])
        self.set_border_width(4)

        self.full = False
        self.topic = False

        self.titulo = gtk.Label("Título")
        self.titulo.modify_font(pango.FontDescription("DejaVu Sans Bold 16"))
        self.titulo.modify_fg(gtk.STATE_NORMAL, COLORES["window"])
        self.videoplayer = VideoPlayer()

        self.tabla = gtk.Table(rows=6, columns=5, homogeneous=True)
        self.tabla.attach(self.titulo, 0, 3, 0, 1)
        self.tabla.set_border_width(10)
        #self.tabla.attach(flashcards, 0, 5, 0, 1)
        self.tabla.attach(self.videoplayer, 0, 3, 1, 6)
        self.videoplayer.connect("full", self.set_full)

        self.scrolled_window = gtk.ScrolledWindow(hadjustment=None, vadjustment=None)
        self.scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        self.scrolled_window.add_with_viewport(self.create_list())
        self.scrolled_window.get_child().modify_bg(gtk.STATE_NORMAL, COLORES["toolbar"])
        self.scrolled_window.get_child().set_shadow_type(gtk.SHADOW_NONE)

        self.tabla.attach(self.scrolled_window, 3, 5, 0, 6)
        self.add(self.tabla)
        self.show_all()

    def filtercat(self, widget, categoria):
        self.scrolled_window.get_child().destroy()
        self.scrolled_window.add_with_viewport(self.create_list(categoria))
        self.scrolled_window.get_child().modify_bg(gtk.STATE_NORMAL, COLORES["toolbar"])
        self.scrolled_window.show_all()

    def reset(self):
        self.scrolled_window.get_child().destroy()
        self.scrolled_window.add_with_viewport(self.create_list())
        self.scrolled_window.get_child().modify_bg(gtk.STATE_NORMAL, COLORES["toolbar"])
        self.scrolled_window.show_all()

    def create_list(self, folder=None):
        if not folder:
            pattern = "Videos/*/*.ogv"
        else:
            pattern = "Videos/" + folder + "/*.ogv"
        vbox = gtk.VBox()
        vbox.set_spacing(10)
        vbox.set_border_width(15)

        videos = sorted(glob(os.path.join(BASE_PATH, pattern)))

        avanzados = []
        for video in videos:
            if "Advanced" in video:
                avanzados.append(video)

        for item in avanzados:
            videos.pop(videos.index(item))

        videos = videos + avanzados

        for video in videos:
            name = os.path.basename(video)
            thumbnail = video[:-4] + ".png"
            if name[-4]==".":
                name = name[:-4]
            name = name.replace("_", " ")
            name = name[name.index(" "):]

            if os.path.isfile(video):
                bbox = gtk.VBox()

                btn = gtk.Button()
                label = gtk.Label(name)
                btn.connect("clicked", self.load, video)
                btn.modify_bg(gtk.STATE_NORMAL, COLORES["toolbar"])
                if is_xo():
                    label.modify_font(pango.FontDescription("DejaVu Sans Bold 8"))
                else:
                    label.modify_font(pango.FontDescription("DejaVu Sans Bold 12"))
                label.set_padding(xpad=5, ypad=15)

                if os.path.isfile(thumbnail):
                    img = gtk.Image()
                    img.set_from_file(thumbnail)
                else:
                    img = gtk.Image()
                    img.set_from_file("Imagenes/minitube.svg")

                bbox.add(img)
                bbox.add(label)
                btn.add(bbox)

                bbox.show_all()
                vbox.add(btn)

        if folder:
            self.run()
            self.top_window.instructionsview.stop()
            self.titulo.set_text(folder)
            self.videoplayer.stop()
            self.videoplayer.load(sorted(videos)[0])

        return vbox

    def __force_unfull(self, widget):
        if self.full:
            self.set_full(False)
        #self.videoplayer.stop()
        #self.videoplayer.load(os.path.join(self.topic, "video.ogv"))
        #self.videoplayer.pause()

    def set_full(self, widget):
        for child in self.tabla.children():
            child.hide()

        if self.full:
            #self.videoplayer.hide()
            self.tabla.set_homogeneous(True)
            self.tabla.set_property("column-spacing", 8)
            self.tabla.set_property("row-spacing", 8)
            self.show_all()
            self.full = False
        else:
            self.tabla.set_homogeneous(False)
            self.tabla.set_property("column-spacing", 0)
            self.tabla.set_property("row-spacing", 0)
            self.videoplayer.show()
            self.full = True

        #self.videoplayer.stop()
        #self.videoplayer.load(os.path.join(self.topic, "video.ogv"))

    def stop(self):
        self.videoplayer.stop()
        self.hide()

    def run(self):
        self.show()
        #self.videoplayer.load(os.path.join(self.topic, "video.ogv"))
        #self.imagen_juego.load(topic)

        self.titulo.set_text("Select a Video")
        try:
            self.reset()
        except AttributeError:
            pass #first time
        #self.full = False
        #self.set_full(False)

    def load(self, widget, filename):
        name = filename.replace("_", " ")
        name = name[name.index(" "):]
        if name[-4]==".":
            name = name[:-4]
        self.titulo.set_text(name)
        self.videoplayer.stop()
        self.videoplayer.load(os.path.join(filename))
