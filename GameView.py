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

import gtk

from Globales import COLORES


class GameView(gtk.EventBox):

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, COLORES["toolbar"])
        self.set_border_width(4)

        self.game_widget = DrawingWidget()

        self.add(self.game_widget)
        self.show_all()

    def stop(self):
        self.game_widget.stop()
        self.hide()

    def run(self, topic):
        self.show()
        self.game_widget.load(topic)


class DrawingWidget(gtk.DrawingArea):

    def __init__(self):

        gtk.DrawingArea.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, COLORES["text"])

        self.juego = False

        self.show_all()

    def __run_game(self, _dict):
        """
        Comienza a correr el Juego.
        """
        xid = self.get_property('window').xid
        os.putenv('SDL_WINDOWID', str(xid))
        #self.juego = Juego()
        #self.juego.run()

    def load(self, topic):
        # self.__run_game(_dict)
        pass

    def stop(self):
        if self.juego:
            self.juego.stop()
