#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   ProgressPlayer.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   Uruguay
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import os
import gobject
import gtk

from Globales import COLORES

BASE_PATH = os.path.dirname(__file__)


class ProgressPlayer(gtk.EventBox):

    __gsignals__ = {
    "seek": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_FLOAT, )),
    "volumen": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_FLOAT,))}

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, COLORES["window"])

        self.barraprogreso = BarraProgreso()
        self.volumen = ControlVolumen()

        hbox = gtk.HBox()
        hbox.pack_start(self.barraprogreso, True, True, 0)
        hbox.pack_start(self.volumen, False, False, 0)

        self.add(hbox)

        self.barraprogreso.connect("user-set-value", self.__user_set_value)
        self.volumen.connect("volumen", self.__set_volumen)

        self.show_all()

    def __user_set_value(self, widget=None, valor=None):
        self.emit("seek", valor)

    def __set_volumen(self, widget, valor):
        self.emit('volumen', valor)

    def set_progress(self, valor):
        self.barraprogreso.set_progress(valor)


class BarraProgreso(gtk.EventBox):
    """
    Barra de progreso para mostrar estado de reproduccion.
    """

    __gsignals__ = {
    "user-set-value": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_FLOAT, ))}

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, COLORES["window"])

        self.escala = ProgressBar(
            gtk.Adjustment(0.0, 0.0, 101.0, 0.1, 1.0, 1.0))

        self.valor = 0

        self.add(self.escala)
        self.show_all()

        self.escala.connect('user-set-value', self.__emit_valor)
        self.set_size_request(-1, 24)

    def __emit_valor(self, widget, valor):
        if self.valor != valor:
            self.valor = valor
            self.emit("user-set-value", self.valor)

    def set_progress(self, valor=0.0):
        if self.escala.presed:
            return

        if self.valor != valor:
            self.valor = valor
            self.escala.ajuste.set_value(valor)
            self.escala.queue_draw()


class ProgressBar(gtk.HScale):
    """
    Escala de SlicerBalance.
    """

    __gsignals__ = {
    "user-set-value": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_FLOAT, ))}

    def __init__(self, ajuste):

        gtk.HScale.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, COLORES["window"])

        self.ajuste = ajuste
        self.set_digits(0)
        self.set_draw_value(False)

        self.presed = False
        self.ancho, self.borde = (10, 10)

        icono = os.path.join(BASE_PATH, "Iconos", "controlslicer.svg")
        self.pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(icono, 24, 24)

        self.connect("button-press-event", self.__button_press_event)
        self.connect("button-release-event", self.__button_release_event)
        self.connect("motion-notify-event", self.__motion_notify_event)
        self.connect("expose_event", self.__expose)

        self.show_all()

    def __button_press_event(self, widget, event):
        self.presed = True

    def __button_release_event(self, widget, event):
        self.presed = False

    def __motion_notify_event(self, widget, event):
        """
        Cuando el usuario se desplaza por la barra de progreso.
        Se emite el valor en % (float).
        """

        if event.state == gtk.gdk.MOD2_MASK | gtk.gdk.BUTTON1_MASK:
            rect = self.get_allocation()
            valor = float(event.x * 100 / rect.width)

            if valor >= 0.0 and valor <= 100.0:
                self.ajuste.set_value(valor)
                self.queue_draw()
                self.emit("user-set-value", valor)

    def __expose(self, widget, event):
        """
        Dibuja el estado de la barra de progreso.
        """

        x, y, w, h = self.get_allocation()
        ancho, borde = (self.ancho, self.borde)

        gc = gtk.gdk.Drawable.new_gc(self.window)

        # todo el widget
        gc.set_rgb_fg_color(COLORES["window"])
        self.window.draw_rectangle(gc, True, x, y, w, h)

        # vacio
        gc.set_rgb_fg_color(COLORES["text"])
        ww = w - borde * 2
        xx = x + w / 2 - ww / 2
        hh = ancho
        yy = y + h / 2 - ancho / 2
        self.window.draw_rectangle(gc, True, xx, yy, ww, hh)

        # progreso
        ximage = int(self.ajuste.get_value() * ww / 100)
        gc.set_rgb_fg_color(COLORES["toolbar"])
        self.window.draw_rectangle(gc, True, xx, yy, ximage, hh)

        # borde de progreso
        gc.set_rgb_fg_color(COLORES["text"])
        self.window.draw_rectangle(gc, False, xx, yy, ww, hh)

        # La Imagen
        imgw, imgh = (self.pixbuf.get_width(), self.pixbuf.get_height())
        yimage = yy + hh / 2 - imgh / 2

        self.window.draw_pixbuf(gc, self.pixbuf, 0, 0, ximage, yimage,
            imgw, imgh, gtk.gdk.RGB_DITHER_NORMAL, 0, 0)

        return True


class ControlVolumen(gtk.VolumeButton):

    __gsignals__ = {
    "volumen": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_FLOAT,))}

    def __init__(self):

        gtk.VolumeButton.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, COLORES["window"])

        self.connect("value-changed", self.__value_changed)
        self.show_all()

        self.set_value(0.9)

    def __value_changed(self, widget, valor):
        """
        Cuando el usuario desplaza la escala.
        """

        valor = int(valor * 10)
        self.emit('volumen', valor)
