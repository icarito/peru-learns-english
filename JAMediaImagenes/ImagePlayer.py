#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   ImagePlayer.py por:
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

"""
Descripción:
    Visor de Imágenes en base a gstreamer.

    Recibe un widget gtk para dibujar sobre él.

    Utilice la función: load(file_path)
        para cargar el archivo a dibujar.

    Utilice la función: stop()
        para detener la reproducción

    Utilice la función: rotar("Derecha") o rotar("Izquierda")
        para rotar la imágen
"""

import os
import gobject
import gst

PR = False

gobject.threads_init()


class ImagePlayer(gobject.GObject):

    def __init__(self, ventana):

        gobject.GObject.__init__(self)

        self.ventana = ventana
        self.src_path = ""

        rect = self.ventana.get_allocation()
        self.width = rect.width
        self.height = rect.height

        self.xid = self.ventana.get_property('window').xid
        self.player = PlayerBin(self.xid, self.width, self.height)

        self.ventana.connect("expose-event", self.__set_size)

    def __set_size(self, widget, event):
        rect = self.ventana.get_allocation()
        self.width = rect.width
        self.height = rect.height
        if self.src_path:
            self.load(self.src_path)

    def load(self, uri):
        self.src_path = uri
        if self.player:
            self.player.stop()
            del(self.player)
            self.player = False
        self.player = PlayerBin(self.xid, self.width, self.height)
        self.player.load(self.src_path)

    def stop(self):
        self.player.stop()
        try:
            self.ventana.disconnect_by_func(self.__set_size)
        except:
            pass


class PlayerBin(gobject.GObject):

    def __init__(self, ventana_id, width, height):

        gobject.GObject.__init__(self)

        self.ventana_id = ventana_id
        self.player = None
        self.bus = None

        self.player = gst.element_factory_make("playbin2", "player")
        self.video_bin = Video_Out(width, height)
        self.player.set_property('video-sink', self.video_bin)

        self.bus = self.player.get_bus()
        self.bus.add_signal_watch()
        self.bus.enable_sync_message_emission()
        self.bus.connect('sync-message', self.__sync_message)

    def __sync_message(self, bus, message):
        if message.type == gst.MESSAGE_ELEMENT:
            if message.structure.get_name() == 'prepare-xwindow-id':
                message.src.set_xwindow_id(self.ventana_id)
        elif message.type == gst.MESSAGE_ERROR:
            err, debug = message.parse_error()
            if PR:
                print "ImagePlayer ERROR:"
                print "\t%s" % err
                print "\t%s" % debug

    def __play(self):
        self.player.set_state(gst.STATE_PLAYING)

    def stop(self):
        self.player.set_state(gst.STATE_NULL)

    def load(self, uri):
        self.stop()
        if not uri:
            return
        if os.path.exists(uri):
            direccion = "file://" + uri
            self.player.set_property("uri", direccion)
            self.__play()
        return False


class Video_Out(gst.Pipeline):

    def __init__(self, width, height):

        gst.Pipeline.__init__(self)

        self.set_name('video_out')

        videoconvert = gst.element_factory_make(
            'ffmpegcolorspace', 'ffmpegcolorspace')

        caps = gst.Caps(
            'video/x-raw-rgb, width=%s,height=%s' % (width, height))
        filtro = gst.element_factory_make("capsfilter", "filtro")
        filtro.set_property("caps", caps)

        ximagesink = gst.element_factory_make('ximagesink', "ximagesink")
        ximagesink.set_property("force-aspect-ratio", True)

        self.add(videoconvert)
        self.add(filtro)
        self.add(ximagesink)

        videoconvert.link(filtro)
        filtro.link(ximagesink)

        self.ghost_pad = gst.GhostPad(
            "sink", videoconvert.get_static_pad("sink"))

        self.ghost_pad.set_target(videoconvert.get_static_pad("sink"))

        self.add_pad(self.ghost_pad)
