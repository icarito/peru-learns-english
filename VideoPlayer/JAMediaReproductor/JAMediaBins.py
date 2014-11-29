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

import pygst
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

        self.config = {
            'saturacion': 50.0,
            'contraste': 50.0,
            'brillo': 50.0,
            'hue': 50.0,
            'gamma': 10.0,
            'rotacion': 0}

        convert = gst.element_factory_make('ffmpegcolorspace', 'convert')
        rate = gst.element_factory_make('videorate', 'rate')
        videobalance = gst.element_factory_make('videobalance', "videobalance")
        gamma = gst.element_factory_make('gamma', "gamma")
        videoflip = gst.element_factory_make('videoflip', "videoflip")
        pantalla = gst.element_factory_make('xvimagesink', "pantalla")
        pantalla.set_property("force-aspect-ratio", True)

        try: # FIXME: xo no posee esta propiedad
            rate.set_property('max-rate', 30)

        except:
            pass

        self.add(convert)
        self.add(rate)
        self.add(videobalance)
        self.add(gamma)
        self.add(videoflip)
        self.add(pantalla)

        convert.link(rate)
        rate.link(videobalance)
        videobalance.link(gamma)
        gamma.link(videoflip)
        videoflip.link(pantalla)

        self.ghost_pad = gst.GhostPad("sink", convert.get_static_pad("sink"))
        self.ghost_pad.set_target(convert.get_static_pad("sink"))
        self.add_pad(self.ghost_pad)

    def rotar(self, valor):
        videoflip = self.get_by_name("videoflip")
        rot = videoflip.get_property('method')

        if valor == "Derecha":
            if rot < 3:
                rot += 1

            else:
                rot = 0

        elif valor == "Izquierda":
            if rot > 0:
                rot -= 1

            else:
                rot = 3

        videoflip.set_property('method', rot)

    def set_balance(self, brillo=None, contraste=None,
        saturacion=None, hue=None, gamma=None):
        if brillo:
            self.config['brillo'] = brillo
            valor = (2.0 * brillo / 100.0) - 1.0
            self.get_by_name("videobalance").set_property('brightness', valor)

        if contraste:
            self.config['contraste'] = contraste
            valor = 2.0 * contraste / 100.0
            self.get_by_name("videobalance").set_property('contrast', valor)

        if saturacion:
            self.config['saturacion'] = saturacion
            valor = 2.0 * saturacion / 100.0
            self.get_by_name("videobalance").set_property('saturation', valor)

        if hue:
            self.config['hue'] = hue
            valor = (2.0 * hue / 100.0) - 1.0
            self.get_by_name("videobalance").set_property('hue', valor)

        if gamma:
            self.config['gamma'] = gamma
            valor = (10.0 * gamma / 100.0)
            self.get_by_name("gamma").set_property('gamma', valor)

    def get_balance(self):
        return self.config
