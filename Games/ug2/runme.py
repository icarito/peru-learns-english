
#!/bin/env python2
# -*- coding: utf-8 -*-

#   Juego UG2 por:
#   Sebastian Silva <sebastian@fuentelibre.org>
#   Planeta Tierra

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
import sys
import os

game_dir = os.path.abspath(os.path.dirname(__file__))
def gamedir(archivo):
    return os.path.join(game_dir, archivo)

sys.path.insert(1, gamedir("../../Lib/"))

import pygame
import spyral
import random
import csv
import collections

SIZE = (700, 700)
TILE = (64, 64)

MAPA1 = [
    [0, 0, 0, 1, 2],
    [0, 1, 3, 0, 0],
    [0, 0 ,0, 0, 0],
    [3, 4, 0, 0, 2],
    [5, 0, 5, 0, 4]]

def wrap(text, length):
    """
    Sirve para cortar texto en varias lineas
    """
    words = text.split()
    lines = []
    line = ''
    for w in words:
        if len(w) + len(line) > length:
            lines.append(line)
            line = ''
        line = line + w + ' '
        if w is words[-1]:
            lines.append(line)
    return '\n'.join(lines)


font_path = gamedir("../fonts/DejaVuSans.ttf")
topic_dir = gamedir("../../Topics/Topic_2/")


def obtener_palabra(topic_dir=topic_dir):
    archivo = os.path.join(topic_dir, "vocabulario.csv")
    tabla = csv.DictReader(file(archivo))
    lista = []
    for linea in tabla:
        uid = linea["id"]
        palabra_png = os.path.join(topic_dir, "Imagenes", uid + '.png')
        #if os.path.exists(palabra_png):
        lista.append(linea)

    indice = random.randint(0, len(lista) - 1)

    palabra = lista[indice]["term"]
    uid = lista[indice]["id"]
    palabra_png = os.path.join(topic_dir, "Imagenes", uid + '.png')

    return palabra, palabra_png

def obtener_set():
    conjunto = list()
    while len(conjunto)<5:
        nueva = obtener_palabra()
        if nueva not in conjunto:
            conjunto.append(nueva)
    return conjunto

class Marco(spyral.Sprite):
    def __init__(self, scene):
        spyral.Sprite.__init__(self, scene)

        self.image = spyral.Image(gamedir("imagenes/golden-border.png"))
        self.layer = "abajo"

        self.font = spyral.Font(font_path, 28, (0, 0, 0))
        self.line_height = self.font.linesize
        self.margen = 50
        self.full_width = self.image.width
        self.full_height = self.image.height

        self.visible = False
        self.set_text("")

        self.delay1 = None
        self.delay2 = None

        spyral.event.register("Marco.timeout1.animation.end", self.hideself)
        spyral.event.register("Marco.timeout2.animation.end", self.decolor)

        self.hide_animation = spyral.Animation("scale", spyral.easing.Linear(1, 0.01))
        self.show_animation = spyral.Animation("scale", spyral.easing.Linear(0.01, 1))

    def set_text(self, text):
        nueva = spyral.Image(size=(self.full_width - self.margen,
            self.full_height - self.margen)).fill((255, 255, 255))
        self.image.draw_image(nueva,
            position=(self.margen / 2, 0), anchor="midleft")
        self.image.draw_image(self.render_text(text),
            position=(0, 0), anchor="midleft")

    def render_text(self, text):
        ancho_promedio = self.font.get_size("X")[0]
        caracteres = (self.width - 2 * self.margen) / ancho_promedio
        lineas = wrap(text, caracteres).splitlines()

        altura = len(lineas) * self.line_height
        bloque = spyral.Image(size=(self.width, altura))

        ln = 0
        for linea in lineas:
            bloque.draw_image(image=self.font.render(linea),
                position=(0, ln * self.line_height), anchor="midtop")
            ln = ln + 1
        return bloque

    def best_pos(self, row, col):
        row_offset = 0
        col_offset = 1
        if row == 4:
            row_offset = -1
        if col == 3:
            col_offset = -2
        if col == 4:
            col_offset = -2

        #self.pos = (col + col_offset) * 131, (row + row_offset) * 131
        coords = (col + col_offset) * 131, (row + row_offset) * 131
        self.move ( *coords )

        if not self.delay1:
            self.delay1 = DelayAnimation(4)
            self.delay1.property = "timeout1"
        else:
            self.stop_animation(self.delay1)
        self.animate(self.delay1)

        if not self.delay2:
            self.delay2 = DelayAnimation(15)
            self.delay2.property = "timeout2"
        else:
            self.stop_animation(self.delay2)
        self.animate(self.delay2)

    def hideself(self):
        self.stop_animation (self.hide_animation)
        try:
            self.animate (self.hide_animation)
        except:
            pass
        spyral.event.queue("Bloque.close")

    def adapt_animation(self):
        return( spyral.Animation("scale", spyral.easing.Linear(float(self.scale), 1)) )

    def showself(self):
        self.stop_animation (self.show_animation)
        try:
            self.animate (self.show_animation)
        except:
            self.stop_animation (self.hide_animation)
            self.animate (self.adapt_animation())

    def decolor(self):
        spyral.event.queue("Bloque.decolor")

    def move(self, x, y):
        try:
            self.stop_animation(self.moving_animation)
            self.stop_animation(self.delay)
        except AttributeError:
            pass
        spyral.event.queue("Bloque.close")
        self.visible = True
        self.moving_animation = spyral.Animation("pos",
            spyral.easing.LinearTuple(self.pos, (x,y)))

        self.animate(self.moving_animation)

class Tablero(spyral.View):
    def __init__(self, scene):
        spyral.View.__init__(self, scene)

        margin = (700 - (131 * 5)) / 2

        self.pos = (margin, margin)

        #self.estado = [[0 for i in range(5)] for j in range(5)]
        self.estado = MAPA1
        self.tablero = self.estado

        self.marco = Marco(self)
        self.palabras = obtener_set()

        for row in range(len(self.estado)):
            for col in range(len(self.estado[row])):
                estado = self.estado[row][col]
                if estado:
                    palabra = self.palabras[estado-1][0]
                    bloque = Bloque(self, row, col, COLOR=estado-1,
                                    PALABRA=palabra)
                    self.tablero[row][col] = bloque
                else:
                    nexo = Nexo(self, row, col)
                    self.tablero[row][col] = nexo

        spyral.event.register ("input.keyboard.down.space", self.blinkall)
        spyral.event.register ("input.keyboard.down.escape", self.closeall)

    def blinkall(self):
        spyral.event.queue("Bloque.blink")

    def closeall(self):
        spyral.event.queue("Bloque.close")

    #def update(self):
    #    for line in self.estado:
    #        self.


class Nexo (spyral.Sprite):
    def __init__(self, scene, row, col):
        spyral.Sprite.__init__(self, scene)

        # somos un nexo
        self.full_image = spyral.Image(
            filename=gamedir("imagenes/beams.png"))

        #self.north = spyra.Image(filename=gamedir("imagenes/canopy_north.png"))
        #self.south = spyra.Image(filename=gamedir("imagenes/canopy_south.png"))
        #self.west = spyra.Image(filename=gamedir("imagenes/canopy_west.png"))
        #self.east = spyra.Image(filename=gamedir("imagenes/canopy_east.png"))


        self.init_animations()

        self.pos = (row * 131 + 32, col * 131 + 32)
        self.image = self.tiled(0,0)

        self.ROW = row
        self.COL = col

        self.scale = 2

        #self.visible = False

        spyral.event.register("input.keyboard.down.return", self.blink)

    def init_animations(self):
        off_row = 0
        off_col = 0
        secuencia = [   self.tiled(0 + off_row, 0 + off_col),
                        self.tiled(0 + off_row, 1 + off_col),
                        self.tiled(0 + off_row, 2 + off_col),
                        self.tiled(1 + off_row, 0 + off_col),
                        self.tiled(1 + off_row, 1 + off_col),
                        self.tiled(1 + off_row, 2 + off_col)]

        self.animation = spyral.Animation("image", spyral.easing.Iterate(secuencia, times=1), 2)


    def blink(self):
        try:
            self.animate (self.animation)
        except:
            pass

    def tiled(self, x, y):
        MINITILE = spyral.Vec2D(32, 32)
        return self.full_image.copy().crop((x,y)*MINITILE, MINITILE)


class Bloque (spyral.Sprite):
    def __init__(self, scene, row, col, COLOR=4, PALABRA="error"):
        # spritesheet color: yellow, green, orange, blue, brown
        spyral.Sprite.__init__(self, scene)

        self.COLOR = COLOR
        self.BGCOLOR = 4

        self.ROW = row
        self.COL = col
        self.PALABRA = PALABRA

        # Somos un ojo del espacio
        assert COLOR != -1

        self.full_image = spyral.Image(
            filename=gamedir("imagenes/eye-tiles.png"))

        self.pos = (col * 131, row * 131)
        self.ARMADO = 3
        self.CERRADO = 2
        self.CERRANDO = 1
        self.ABIERTO = 0

        self.image = self.tiled(self.ARMADO)
        self.abierto = False

        self.init_animations()

        spyral.event.register("Bloque.blink", self.blink)
        spyral.event.register("Bloque.close", self.iclose)
        spyral.event.register("Bloque.decolor", self.decolor)

        spyral.event.register ("input.mouse.down.left", self.check_click)

    def init_animations(self):
        # ABRIR
        secuencia = [self.tiled(self.ARMADO, self.COLOR)] + \
                    [self.tiled(self.CERRADO, self.COLOR)] * 6 + \
                    [self.tiled(self.CERRANDO, self.COLOR)] + \
                    [self.tiled(self.ABIERTO, self.COLOR)] * 6
        # Y CERRAR
        retro_secuencia = list(reversed(secuencia))
        toda_secuencia = secuencia + retro_secuencia

        self.open_animation = spyral.Animation("image", spyral.easing.Iterate(secuencia, times=0.9), 2)
        self.close_animation = spyral.Animation("image", spyral.easing.Iterate(retro_secuencia, times=0.9), 2)
        self.blink_animation = spyral.Animation("image", spyral.easing.Iterate(toda_secuencia), 4)

        # DESCOLORAMOS
        secuencia = [self.tiled(self.ARMADO, self.COLOR)] + \
                    [self.tiled(self.CERRADO, self.COLOR), self.tiled(self.CERRADO)] * 3 + \
                    [self.tiled(self.ARMADO)]

        self.decolor_animation = spyral.Animation("image", spyral.easing.Iterate(secuencia, times=0.9), 2)

        spyral.event.register("Bloque.image.animation.end", self.update)

    def tiled(self, x, COLOR=None):
        BIGTILE = (120, 120)
        if COLOR==None:
            COLOR = self.BGCOLOR
        return self.full_image.copy().crop((x * 132, COLOR * 132), BIGTILE)

    def check_click(self, pos):
        if self.collide_point(pos):
            self.toggle()

    def toggle(self):
        if self.abierto:
            self.iclose()
        else:
            self.iopen()

    def iopen(self):
        self.scene.tablero.marco.showself()
        self.scene.tablero.marco.set_text(self.PALABRA)
        self.scene.tablero.marco.best_pos(self.ROW, self.COL)
        self.BGCOLOR = self.COLOR
        try:
            self.animate (self.open_animation)
            self.abierto = True
        except:
            pass

    def iclose(self):
        if self.abierto:
            try:
                self.animate (self.close_animation)
                self.abierto = False
            except:
                pass

    def update(self):
        if self.abierto:
            self.image = self.tiled(self.ABIERTO, self.BGCOLOR)
        else:
            self.image = self.tiled(self.ARMADO, self.BGCOLOR)

    def blink(self):
        try:
            self.animate (self.blink_animation)
        except:
            pass

    def decolor(self):
        if self.BGCOLOR!=4:
            self.BGCOLOR = 4
            try:
                self.animate(self.decolor_animation)
            except:
                pass


class Escena(spyral.Scene):
    def __init__(self, topic=topic_dir):

        spyral.Scene.__init__(self, SIZE)

        self.layers = ["abajo", "arriba", "primer"]

        img = spyral.Image(filename=gamedir(
            "imagenes/Fazenda_Colorada.jpg")).scale(self.scene.size)

        n = pygame.Surface.convert_alpha(img._surf)
        # red at 50%
        n.fill((64, 0, 0, 127))
        img._surf.blit(n, (0, 0))

        self.background = img

        self.tablero = Tablero(self)

        spyral.event.register("system.quit", spyral.director.pop, scene=self)


# Tomado de Spyral
class DelayAnimation(spyral.Animation):
    """
    Animation which performs no actions. Useful for lining up appended
    and parallel animations so that things run at the right times.
    """
    def __init__(self, duration=1.0):
        self.absolute = False
        self.properties = set([])
        self.duration = duration
        self.loop = False

    def evaluate(self, sprite, progress):
        return {}


def main():
    spyral.director.push(Escena())

if __name__ == "__main__":
    spyral.director.init(SIZE, fullscreen=False)
    main()
    spyral.director.run()
