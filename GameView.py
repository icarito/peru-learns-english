#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   GameView.py por:
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
from signal import SIGTERM
import sys
sys.path.insert(1, "Lib/")

import gtk

from Globales import COLORES

import subprocess

class GameView(gtk.EventBox):

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, COLORES["toolbar"])
        self.set_border_width(4)

        self.add(gtk.Label("Juego 1"))
        self.game = None
        self.show_all()

    def stop(self):
        if self.game:
            os.kill(self.game, SIGTERM)
        self.hide()

    def run(self, topic):
        p = subprocess.Popen("python2 Games/ug1/runme.py", shell=True)
        self.game = p.pid
        self.show()
