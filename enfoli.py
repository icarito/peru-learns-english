#!/bin/env python2
# -*- coding: utf-8 -*-

# English For Fun
# Copyright © 2014 Sebastian Silva

# Secciones tomadas de:
#   Copyright (C) 2007 Andy Wingo <wingo@pobox.com>
#   Copyright (C) 2007 Red Hat, Inc.
#   Copyright (C) 2008-2010 Kushal Das <kushal@fedoraproject.org>

#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import pygst
pygst.require('0.10')
import gst
import gst.interfaces
import gtk
import gobject
import logging

class Navegacion(gtk.Notebook):
    """
    Esta clase se encarga de encapsular el resto de la funcionalidad.
    La navegación está sujeta a cambiar.
    """

    def __init__(self):
        gtk.Notebook.__init__(self)

        label2 = gtk.Label("Aquí va el lienzo de Pygame")
        label3 = gtk.Label("Aquí van los Flashcards")

        self.append_page(gtk.Label("2"),label2) # meter sugargame2 aqui
        self.append_page(gtk.Label("3"),label3) # inventarse algo como anki aqui

        self.set_tab_pos(gtk.POS_LEFT)

"""
 Tomado de jukeboxactivity.py
 Activity that plays media.
 Copyright (C) 2007 Andy Wingo <wingo@pobox.com>
 Copyright (C) 2007 Red Hat, Inc.
 Copyright (C) 2008-2010 Kushal Das <kushal@fedoraproject.org>
"""
class GstPlayer(gobject.GObject):

    __gsignals__ = {
        'error': (gobject.SIGNAL_RUN_FIRST, None, [str, str]),
        'eos': (gobject.SIGNAL_RUN_FIRST, None, []),
        'tag': (gobject.SIGNAL_RUN_FIRST, None, [str, str]),
        'stream-info': (gobject.SIGNAL_RUN_FIRST, None, [object])
    }

    def __init__(self, videowidget):
        gobject.GObject.__init__(self)

        self.playing = False
        self.error = False

        self.player = gst.element_factory_make("playbin", "player")

        r = gst.registry_get_default()
        l = [x for x in r.get_feature_list(gst.ElementFactory)
                if (gst.ElementFactory.get_klass(x) == "Visualization")]
        if len(l):
            e = l.pop()  # take latest plugin in the list
            vis_plug = gst.element_factory_make(e.get_name())
            self.player.set_property('vis-plugin', vis_plug)

        self.overlay = None
        videowidget.realize()
        self.videowidget = videowidget
        self.videowidget_xid = videowidget.window.xid
        self._init_video_sink()

        bus = self.player.get_bus()
        bus.enable_sync_message_emission()
        bus.add_signal_watch()
        bus.connect('sync-message::element', self.on_sync_message)
        bus.connect('message', self.on_message)

    def set_uri(self, uri):
        self.player.set_property('uri', uri)

    def on_sync_message(self, bus, message):
        if message.structure is None:
            return
        if message.structure.get_name() == 'prepare-xwindow-id':
            self.videowidget.set_sink(message.src, self.videowidget_xid)
            message.src.set_property('force-aspect-ratio', True)

    def on_message(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_ERROR:
            err, debug = message.parse_error()
            logging.debug("Error: %s - %s" % (err, debug))
            self.error = True
            self.emit("eos")
            self.playing = False
            self.emit("error", str(err), str(debug))
        elif t == gst.MESSAGE_EOS:
            self.emit("eos")
            self.playing = False
        elif t == gst.MESSAGE_TAG:
            tags = message.parse_tag()
            for tag in tags.keys():
                self.emit('tag', str(tag), str(tags[tag]))
        elif t == gst.MESSAGE_STATE_CHANGED:
            old, new, pen = message.parse_state_changed()
            if old == gst.STATE_READY and new == gst.STATE_PAUSED:
                self.emit('stream-info',
                        self.player.props.stream_info_value_array)

    def _init_video_sink(self):
        self.bin = gst.Bin()
        videoscale = gst.element_factory_make('videoscale')
        self.bin.add(videoscale)
        pad = videoscale.get_pad("sink")
        ghostpad = gst.GhostPad("sink", pad)
        self.bin.add_pad(ghostpad)
        videoscale.set_property("method", 0)

        caps_string = "video/x-raw-yuv, "
        r = self.videowidget.get_allocation()
        if r.width > 500 and r.height > 500:
            # Sigh... xvimagesink on the XOs will scale the video to fit
            # but ximagesink in Xephyr does not.  So we live with unscaled
            # video in Xephyr so that the XO can work right.
            w = 480
            h = float(w) / float(float(r.width) / float(r.height))
            caps_string += "width=%d, height=%d" % (w, h)
        else:
            caps_string += "width=480, height=360"
        caps = gst.Caps(caps_string)
        self.filter = gst.element_factory_make("capsfilter", "filter")
        self.bin.add(self.filter)
        self.filter.set_property("caps", caps)

        textoverlay = gst.element_factory_make('textoverlay')
        self.overlay = textoverlay
        self.bin.add(textoverlay)
        conv = gst.element_factory_make("ffmpegcolorspace", "conv")
        self.bin.add(conv)
        videosink = gst.element_factory_make('autovideosink')
        self.bin.add(videosink)
        gst.element_link_many(videoscale, self.filter, textoverlay, conv,
                videosink)
        self.player.set_property("video-sink", self.bin)

    def set_overlay(self, title, artist, album):
        text = "%s\n%s" % (title, artist)
        if album and len(album):
            text += "\n%s" % album
        self.overlay.set_property("text", text)
        self.overlay.set_property("font-desc", "sans bold 14")
        self.overlay.set_property("halignment", "right")
        self.overlay.set_property("valignment", "bottom")
        try:
            # Only in OLPC versions of gstreamer-plugins-base for now
            self.overlay.set_property("line-align", "left")
        except:
            pass

    def query_position(self):
        "Returns a (position, duration) tuple"
        try:
            position, format = self.player.query_position(gst.FORMAT_TIME)
        except:
            position = gst.CLOCK_TIME_NONE

        try:
            duration, format = self.player.query_duration(gst.FORMAT_TIME)
        except:
            duration = gst.CLOCK_TIME_NONE

        return (position, duration)

    def seek(self, location):
        """
        @param location: time to seek to, in nanoseconds
        """
        event = gst.event_new_seek(1.0, gst.FORMAT_TIME,
            gst.SEEK_FLAG_FLUSH | gst.SEEK_FLAG_ACCURATE,
            gst.SEEK_TYPE_SET, location,
            gst.SEEK_TYPE_NONE, 0)

        res = self.player.send_event(event)
        if res:
            self.player.set_new_stream_time(0L)
        else:
            logging.debug("seek to %r failed" % location)

    def pause(self):
        logging.debug("pausing player")
        self.player.set_state(gst.STATE_PAUSED)
        self.playing = False

    def play(self):
        logging.debug("playing player")
        self.player.set_state(gst.STATE_PLAYING)
        self.playing = True
        self.error = False

    def stop(self):
        self.player.set_state(gst.STATE_NULL)
        logging.debug("stopped player")

    def get_state(self, timeout=1):
        return self.player.get_state(timeout=timeout)

    def is_playing(self):
        return self.playing

"""
 Tomado de jukeboxactivity.py
 Activity that plays media.
 Copyright (C) 2007 Andy Wingo <wingo@pobox.com>
 Copyright (C) 2007 Red Hat, Inc.
 Copyright (C) 2008-2010 Kushal Das <kushal@fedoraproject.org>
"""
class VideoWidget(gtk.DrawingArea):
    def __init__(self):
        gtk.DrawingArea.__init__(self)
        self.set_events(gtk.gdk.POINTER_MOTION_MASK |
        gtk.gdk.POINTER_MOTION_HINT_MASK |
        gtk.gdk.EXPOSURE_MASK |
        gtk.gdk.KEY_PRESS_MASK |
        gtk.gdk.KEY_RELEASE_MASK)
        self.imagesink = None
        self.unset_flags(gtk.DOUBLE_BUFFERED)
        self.set_flags(gtk.APP_PAINTABLE)

    def do_expose_event(self, event):
        if self.imagesink:
            self.imagesink.expose()
            return False
        else:
            return True

    def set_sink(self, sink, xid):
        self.imagesink = sink
        self.imagesink.set_xwindow_id(xid)


if __name__ == '__main__':
    window = gtk.Window()
    window.connect("destroy", gtk.main_quit)

    notebook = Navegacion()

    View = VideoWidget()

    label1 = gtk.Label("Aquí va el Player de Video")

    notebook.prepend_page(View, label1)
    window.add(notebook)
    window.show_all()

    Player = GstPlayer(View)

    directorio_fuente = os.path.dirname(os.path.realpath(__file__))
    directorio_videos = os.path.join(directorio_fuente, "videos")

    Player.set_uri('file://' + directorio_videos + '/bunny-bonita-2.ogv')
    Player.play()

    gtk.main()
