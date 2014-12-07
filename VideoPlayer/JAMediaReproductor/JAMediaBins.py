#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaBins.py por:
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

import gst
import gobject

gobject.threads_init()


class JAMedia_Audio_Pipeline(gst.Pipeline):

    def __init__(self):

        gst.Pipeline.__init__(self)

        self.set_name('jamedia_audio_pipeline')

        convert = gst.element_factory_make("audioconvert", "convert")
        sink = gst.element_factory_make("autoaudiosink", "sink")

        self.add(convert)
        self.add(sink)

        convert.link(sink)

        self.add_pad(gst.GhostPad("sink", convert.get_static_pad("sink")))


class JAMedia_Video_Pipeline(gst.Pipeline):

    def __init__(self):

        gst.Pipeline.__init__(self)

        self.set_name('jamedia_video_pipeline')

        convert = gst.element_factory_make('ffmpegcolorspace', 'convert')
        rate = gst.element_factory_make('videorate', 'rate')
        pantalla = gst.element_factory_make('xvimagesink', "pantalla")
        pantalla.set_property("force-aspect-ratio", True)

        try:  # FIXME: xo no posee esta propiedad
            rate.set_property('max-rate', 30)
        except:
            pass

        self.add(convert)
        self.add(rate)
        self.add(pantalla)

        convert.link(rate)
        rate.link(pantalla)

        self.ghost_pad = gst.GhostPad("sink", convert.get_static_pad("sink"))
        self.ghost_pad.set_target(convert.get_static_pad("sink"))
        self.add_pad(self.ghost_pad)
