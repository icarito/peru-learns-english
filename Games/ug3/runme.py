
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
import pygame.gfxdraw
import spyral
from random import randrange, randint
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
topic_dir = gamedir("../../Topics/Topic_4/")


def obtener_palabra(topic_dir):
    archivo = os.path.join(topic_dir, "vocabulario.csv")
    tabla = csv.DictReader(file(archivo))
    lista = []
    for linea in tabla:
        uid = linea["id"]
        palabra_png = os.path.join(topic_dir, "Imagenes", uid + '.png')
        #if os.path.exists(palabra_png):
        lista.append(linea)

    indice = randint(0, len(lista) - 1)

    palabra = lista[indice]["term"]
    uid = lista[indice]["id"]
    palabra_png = os.path.join(topic_dir, "Imagenes", uid + '.png')

    return palabra, palabra_png

def obtener_set(topic):
    conjunto = list()
    while len(conjunto)<5:
        nueva = obtener_palabra(topic)
        if nueva not in conjunto:
            conjunto.append(nueva)
    return conjunto

class CampodeEstrellas(spyral.Sprite):
    def __init__(self, scene):
        spyral.Sprite.__init__(self, scene)

        self.num_stars = 512
        self.max_depth = 32

        self.layer = "abajo"

        self.back_img = spyral.Image(filename=gamedir(
            "imagenes/Crux-20100220.jpg")).scale(self.scene.size)

        self.image = spyral.Image(size=(700,700)).fill((0,0,0))
        self.image = self.back_img.copy()
        self.init_stars()

        spyral.event.register("director.update", self.update)
        spyral.event.register("director.pre_update", self.predraw)

    def update(self):
        """ Move and draw the stars """
        origin_x = self.width / 2
        origin_y = self.height / 2
        
        for star in self.stars:
            # The Z component is decreased on each frame.
            star[2] -= 0.19

            # If the star has past the screen (I mean Z<=0) then we
            # reposition it far away from the screen (Z=max_depth)
            # with random X and Y coordinates.
            if star[2] <= 0:
                star[0] = randrange(-25,25)
                star[1] = randrange(-25,25)
                star[2] = self.max_depth

            # Convert the 3D coordinates to 2D using perspective projection.
            k = 128.0 / star[2]
            x = int(star[0] * k + origin_x)
            y = int(star[1] * k + origin_y)

            # Draw the star (if it is visible in the screen).
            # We calculate the size such that distant stars are smaller than
            # closer stars. Similarly, we make sure that distant stars are
            # darker than closer stars. This is done using Linear Interpolation.
            if 0 <= x < self.width and 0 <= y < self.height:
                size = (1 - float(star[2]) / self.max_depth) * 5
                shade = (1 - float(star[2]) / self.max_depth) * 255
                #self.image.draw_circle((shade,shade,shade),(x,y),int(size))

                pygame.gfxdraw.aacircle(self.image._surf, x, y, int(size), [shade/2]*3)
                pygame.gfxdraw.filled_circle(self.image._surf, x, y, int(size), [shade]*3)


    def predraw(self):
        #self.image.fill((0,0,0))
        self.image = self.back_img.copy()

    def init_stars(self):
        """ Create the starfield """
        self.stars = []
        for i in range(self.num_stars):
            # A star is represented as a list with this format: [X,Y,Z]
            star = [randrange(-25,25), randrange(-25,25), randrange(1, self.max_depth)]
            self.stars.append(star)


class Tablero(spyral.View):
    def __init__(self, scene, topic, mapa):
        spyral.View.__init__(self, scene)

        margin = (700 - (140 * 5)) / 2

        self.pos = (margin, margin)

        self.layers = ["abajo", "arriba", "primer"]

        self.tablero = mapa

        self.palabras = obtener_set(topic)
        self.cursor = Cursor(self)
        self.camino = []

        self.ACTIVADO = False
        self.mov_anterior = None

        for row in range(len(self.tablero)):
            for col in range(len(self.tablero[row])):
                tablero = self.tablero[row][col]
                if tablero:
                    palabra = self.palabras[tablero-1][0]
                    archivo = self.palabras[tablero-1][1]
                    bloque = Bloque(self, row, col, COLOR=tablero-1,
                                    PALABRA=palabra, ARCHIVO=archivo)
                    self.tablero[row][col] = bloque
                else:
                    nexo = Nexo(self, row, col)
                    self.tablero[row][col] = nexo


class Bloque (spyral.Sprite):
    # RENDERED lleva la cuenta para todos los bloques,
    #          de que palabras ya salieron en pantalla.
    RENDERED = None

    def __init__(self, scene, PALABRA="The Chakana Cross", ARCHIVO=None):
        # spritesheet color: yellow, green, orange, blue, brown
        spyral.Sprite.__init__(self, scene)
        self.layer = "arriba"

        self.PALABRA = PALABRA
        self.ARCHIVO = ARCHIVO
        self.font = spyral.Font(font_path, 28, (0, 0, 0))
        self.line_height = self.font.linesize

        self.mode = "PALABRA"
        if Bloque.RENDERED and (PALABRA in Bloque.RENDERED):
            self.mode = "TARJETA"
        elif not Bloque.RENDERED:
            Bloque.RENDERED = [ PALABRA ]
        else:
            Bloque.RENDERED.append( PALABRA )

        self.anchor = "center"

        self.margin = 2
        self.marco = spyral.Image(filename=gamedir("imagenes/marco_1.png"))
        self.image = self.marco

        self.scale = 0.91
        self.pos = spyral.Vec2D(scene.size)/2
        self.showself()

    def render_text(self, text):
        ancho_promedio = self.font.get_size("X")[0]
        caracteres = (self.width - 2 * self.margin) / ancho_promedio
        lineas = wrap(text, caracteres).splitlines()

        altura = len(lineas) * self.line_height
        bloque = spyral.Image(size=(self.width, altura))

        ln = 0
        for linea in lineas:
            bloque.draw_image(image=self.font.render(linea),
                position=(0, ln * self.line_height), anchor="midtop")
            ln = ln + 1

        nueva = spyral.Image(size=(self.width - self.margin,
            self.height - self.margin)).fill((255, 255, 255))
        nueva.draw_image(bloque,
            position=(0, 0), anchor="midleft")

        return nueva

    def render_image(self, image):
        try:
            nueva = spyral.Image(filename=image).scale((
                self.width - self.margin, self.height - self.margin))
        except ValueError, pygame.error:
            nueva = spyral.Image(size=(self.width - self.margin,
                self.height - self.margin)).fill((255, 255, 255))
        return nueva

    def showself(self):
        self.image = self.marco
        if self.mode == "TARJETA":
            self.image.draw_image(self.render_image(self.ARCHIVO),
                position=(0, 0), anchor="center")
        elif self.mode == "PALABRA":
            self.image.draw_image(self.render_text(self.PALABRA),
                position=(0, 0), anchor="center")


class Nave (spyral.View):
    def __init__(self, scene):
        spyral.View.__init__(self, scene)
        
        self.n = Bloque(self)
        self.s = Bloque(self)
        self.e = Bloque(self)
        self.o = Bloque(self)

class Escena(spyral.Scene):
    def __init__(self, topic=topic_dir):
        spyral.Scene.__init__(self, SIZE)

        self.layers = ["abajo", "arriba", "primer"]

        img = spyral.Image(filename=gamedir(
            "imagenes/Crux-20100220.jpg")).scale(self.scene.size)

        #n = pygame.Surface.convert_alpha(img._surf)
        #n.fill((64, 0, 0, 127))
        #img._surf.blit(n, (0, 0))

        self.background = img

        self.nave = Nave(self)
        self.campo = CampodeEstrellas(self)
        
        #self.tablero = Tablero(self, topic, mapa=MAPA1)

        spyral.event.register("system.quit", spyral.director.pop, scene=self)

    def mute(self, value):
        Escena.MUTE = value


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
