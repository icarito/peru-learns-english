#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaReproductor.py por:
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
import gst

from JAMediaBins import JAMedia_Audio_Pipeline
from JAMediaBins import JAMedia_Video_Pipeline

PR = False

gobject.threads_init()


class JAMediaReproductor(gobject.GObject):

    __gsignals__ = {
    "endfile": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, []),
    "estado": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,)),
    "newposicion": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_INT,)),
    "video": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_BOOLEAN,)),
    "loading-buffer": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_INT, )),
        }

    # Estados: playing, paused, None

    def __init__(self, ventana_id):

        gobject.GObject.__init__(self)

        self.nombre = "JAMediaReproductor"

        self.video = False
        self.ventana_id = ventana_id
        self.progressbar = True
        self.estado = None
        self.duracion = 0.0
        self.posicion = 0.0
        self.actualizador = False
        self.player = None
        self.bus = None

        self.player = gst.element_factory_make("playbin2", "player")

        self.audio_bin = JAMedia_Audio_Pipeline()
        self.video_bin = JAMedia_Video_Pipeline()

        self.player.set_property('video-sink', self.video_bin)
        self.player.set_property('audio-sink', self.audio_bin)

        self.bus = self.player.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message', self.__on_mensaje)
        self.bus.enable_sync_message_emission()
        self.bus.connect('sync-message', self.__sync_message)

    def __sync_message(self, bus, message):
        if message.type == gst.MESSAGE_ELEMENT:
            if message.structure.get_name() == 'prepare-xwindow-id':
                message.src.set_xwindow_id(self.ventana_id)
        elif message.type == gst.MESSAGE_STATE_CHANGED:
            old, new, pending = message.parse_state_changed()
            if self.estado != new:
                self.estado = new
                if new == gst.STATE_PLAYING:
                    self.emit("estado", "playing")
                    self.__new_handle(True)
                elif new == gst.STATE_PAUSED:
                    self.emit("estado", "paused")
                    self.__new_handle(False)
                elif new == gst.STATE_NULL:
                    self.emit("estado", "None")
                    self.__new_handle(False)
                else:
                    self.emit("estado", "paused")
                    self.__new_handle(False)
        elif message.type == gst.MESSAGE_TAG:
            taglist = message.parse_tag()
            datos = taglist.keys()
            if 'video-codec' in datos:
                if self.video == False or self.video == None:
                    self.video = True
                    self.emit("video", self.video)
        elif message.type == gst.MESSAGE_LATENCY:
            self.player.recalculate_latency()
        elif message.type == gst.MESSAGE_ERROR:
            err, debug = message.parse_error()
            if PR:
                print "JAMediaReproductor ERROR:"
                print "\t%s" % err
                print "\t%s" % debug
            self.__new_handle(False)

    def __on_mensaje(self, bus, message):
        if message.type == gst.MESSAGE_EOS:
            self.__new_handle(False)
            self.emit("endfile")
        elif message.type == gst.MESSAGE_ERROR:
            err, debug = message.parse_error()
            if PR:
                print "JAMediaReproductor ERROR:"
                print "\t%s" % err
                print "\t%s" % debug
            self.__new_handle(False)
        elif message.type == gst.MESSAGE_BUFFERING:
            buf = int(message.structure["buffer-percent"])
            if buf < 100 and self.estado == gst.STATE_PLAYING:
                self.emit("loading-buffer", buf)
                self.pause()
            elif buf > 99 and self.estado != gst.STATE_PLAYING:
                self.emit("loading-buffer", buf)
                self.play()

    def __new_handle(self, reset):
        if self.actualizador:
            gobject.source_remove(self.actualizador)
            self.actualizador = False
        if reset:
            self.actualizador = gobject.timeout_add(500, self.__handle)

    def __handle(self):
        if not self.progressbar:
            return True
        duracion = self.player.query_duration(gst.FORMAT_TIME)[0] / gst.SECOND
        posicion = self.player.query_position(gst.FORMAT_TIME)[0] / gst.SECOND
        pos = posicion * 100 / duracion
        if self.duracion != duracion:
            self.duracion = duracion
        if pos != self.posicion:
            self.posicion = pos
            self.emit("newposicion", self.posicion)
        return True

    def play(self):
        self.player.set_state(gst.STATE_PLAYING)

    def pause_play(self):
        if self.estado == gst.STATE_PAUSED or self.estado == gst.STATE_NULL \
            or self.estado == gst.STATE_READY:
            self.play()
        elif self.estado == gst.STATE_PLAYING:
            self.pause()

    def stop(self):
        self.__new_handle(False)
        self.player.set_state(gst.STATE_NULL)
        self.emit("newposicion", 0)

    def load(self, uri):
        if not uri:
            return False
        self.duracion = 0.0
        self.posicion = 0.0
        self.emit("newposicion", self.posicion)
        self.emit("loading-buffer", 100)
        if os.path.exists(uri):
            direccion = "file://" + uri
            self.player.set_property("uri", direccion)
            # FIXME: Quitado por consideraciones de rendimiento en la XO
            #suburi = os.path.join(os.path.dirname(uri), "subtitulos.srt")
            #if os.path.exists(suburi):
            #    self.player.set_property("suburi", "file://" + suburi)
            #    self.player.set_property("subtitle-font-desc", "sans bold 18")
            self.progressbar = True
        else:
            if gst.uri_is_valid(uri):
                self.player.set_property("uri", uri)
                self.progressbar = False
        return False

    def set_position(self, posicion):
        if not self.progressbar:
            return
        if self.duracion < posicion:
            return
        if self.duracion == 0 or posicion == 0:
            return
        posicion = self.duracion * posicion / 100
        event = gst.event_new_seek(
            1.0, gst.FORMAT_TIME,
            gst.SEEK_FLAG_FLUSH | gst.SEEK_FLAG_ACCURATE,
            gst.SEEK_TYPE_SET, posicion * 1000000000,
            gst.SEEK_TYPE_NONE, self.duracion * 1000000000)
        self.player.send_event(event)

    def set_volumen(self, volumen):
        self.player.set_property('volume', volumen / 10)

    def get_volumen(self):
        return self.player.get_property('volume') * 10

    def pause(self):
        self.player.set_state(gst.STATE_PAUSED)
