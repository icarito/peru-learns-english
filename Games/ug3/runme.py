
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
sys.path.insert(1, gamedir("../../"))

from Globales import decir
import gtk

import pygame
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

        self.num_stars = 256 
        self.max_depth = 16 

        self.layer = "abajo"
        self.speed = 0.2

        self.back_img = spyral.Image(filename=gamedir(
            "imagenes/below_the_ocean_by_arghus-d4t62um_1.jpg")).scale(self.scene.size)
        #self.back_img2 = spyral.Image(filename=gamedir(
        #    "imagenes/below_the_ocean_by_arghus-d4t62um_2.jpg")).scale(self.scene.size)
        #self.back_img3 = spyral.Image(filename=gamedir(
        #    "imagenes/below_the_ocean_by_arghus-d4t62um_3.jpg")).scale(self.scene.size)

        #self.back_img = spyral.Image(size=(700,700)).fill((0,0,48))
        self.image = self.back_img.copy()
        self.init_stars()
        self.init_animations()

        spyral.event.register("director.update", self.update)
        spyral.event.register("director.pre_update", self.predraw)

    def init_animations(self):
        self.top = 0.3
        self.low = 0.03
        self.slowdown_anim = spyral.Animation("speed",
                                spyral.easing.CubicOut(self.top, self.low), duration=3)

        self.speedup_anim = spyral.Animation("speed",
                                spyral.easing.QuadraticOut(self.low, self.top), duration=3)

    def speedup(self):
        try:
            self.animate(self.speedup_anim)
        except ValueError:
            self.stop_all_animations()
            a = spyral.Animation("speed",
                                spyral.easing.Linear(self.speed, self.top), duration=1)
            self.animate(a)

    def slowdown(self):
        try:
            self.animate(self.slowdown_anim)
        except ValueError:
            self.stop_all_animations()
            a = spyral.Animation("speed",
                                spyral.easing.Linear(self.speed, self.low), duration=1)
            self.animate(a)

    def update(self):
        """ Move and draw the stars """
        origin_x = self.width / 2
        origin_y = self.height / 2

        for star in self.stars:
            # The Z component is decreased on each frame.
            star[2] -= self.speed

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
                self.image.draw_circle((shade/2,shade/2,shade),(x,y),int(size))

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


class Bloque (spyral.Sprite):

    def __init__(self, scene, PALABRA="The Chakana Cross", ARCHIVO=None):
        # spritesheet color: yellow, green, orange, blue, brown
        spyral.Sprite.__init__(self, scene)

        self.layer = "arriba"

        self.PALABRA = PALABRA
        self.ARCHIVO = ARCHIVO
        self.font = spyral.Font(font_path, 28, (0, 0, 0))
        self.line_height = self.font.linesize

        self.mode = "TARJETA"

        self.anchor = "center"

        self.margin = 15
        self.marco = spyral.Image(filename=gamedir("imagenes/marco_1.png"))
        self.image = self.marco

        self.scale = 0.91
        self.pos = spyral.Vec2D(scene.size)/2
        self.showself()

    def set_word(self, PALABRA, ARCHIVO):
        self.PALABRA = PALABRA
        self.ARCHIVO = ARCHIVO
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
                self.image.width - self.margin, self.image.height - self.margin))
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
    def __init__(self, scene, topic):
        spyral.View.__init__(self, scene)

        self.topic = topic
        self.reset_words()

        self.n = Bloque(self, *self.palabras[0])
        self.n.pos += spyral.Vec2D(0, -150)

        self.s = Bloque(self, *self.palabras[1])
        self.s.pos += spyral.Vec2D(0, +150)

        self.o = Bloque(self, *self.palabras[2])
        self.o.pos += spyral.Vec2D(-150, 0)

        self.e = Bloque(self, *self.palabras[3])
        self.e.pos += spyral.Vec2D(+150, 0)

        self.visible = False
        self.estado = "reset"

        self.init_animations()
        spyral.event.register("input.keyboard.down.space", self.reset)

        spyral.event.register("input.keyboard.down.down", self.control_s)
        spyral.event.register("input.keyboard.down.up", self.control_n)
        spyral.event.register("input.keyboard.down.left", self.control_o)
        spyral.event.register("input.keyboard.down.right", self.control_e)

        spyral.event.register("Bloque.wait.animation.end", self.clear)

    def reset(self):
        self.reset_words()
        self.n.set_word(*self.palabras[0])
        self.s.set_word(*self.palabras[1])
        self.o.set_word(*self.palabras[2])
        self.e.set_word(*self.palabras[3])
        decir(170, 50, 0, "en-gb", self.e.PALABRA)
        self.invade()

    def reset_words(self):
        self.palabras = obtener_set(self.topic)

    def init_animations(self):
        self.invasion_anim = spyral.Animation("scale", spyral.easing.QuadraticIn(0.1, 1), duration=15)
        self.delay_anim = DelayAnimation(15)
        self.delay_anim.property = "wait"

    def invade(self):
        if self.estado == "invade":
            self.clear()

        self.estado = "invade"

        self.n.animate(self.invasion_anim)
        self.e.animate(self.invasion_anim)
        self.s.animate(self.invasion_anim)
        self.o.animate(self.invasion_anim)

        self.visible = True
        self.scene.campo.slowdown()

        self.o.stop_animation(self.delay_anim)
        self.o.animate(self.delay_anim)

    def clear(self):
        self.estado = "reset"
        for bloque in self.n,self.s,self.e,self.o:
            bloque.stop_animation(self.invasion_anim)
        self.o.stop_animation(self.delay_anim)
        self.visible = False
        self.scene.campo.speedup()

    def control_n(self):
        self.clear()

    def control_s(self):
        self.clear()

    def control_e(self):
        self.clear()

    def control_o(self):
        self.clear()

class Escena(spyral.Scene):
    def __init__(self, topic=topic_dir, fake_gtk=False):
        spyral.Scene.__init__(self, SIZE)

        self.layers = ["abajo", "arriba", "primer"]

        #img = spyral.Image(filename=gamedir(
        #    "imagenes/Crux-20100220.jpg")).scale(self.scene.size)
        img = spyral.Image(size=(700, 700))

        #n = pygame.Surface.convert_alpha(img._surf)
        #n.fill((64, 0, 0, 127))
        #img._surf.blit(n, (0, 0))

        self.background = img

        self.nave = Nave(self, topic)
        self.campo = CampodeEstrellas(self)

        #self.tablero = Tablero(self, topic, mapa=MAPA1)

        spyral.event.register("system.quit", spyral.director.pop, scene=self)

        if fake_gtk:
            gtk.threads_init()
            spyral.event.register("director.update", self.gtk_main_iteration)

    def mute(self, value):
        Escena.MUTE = value

    def gtk_main_iteration(self):
        gtk.main_iteration(False)

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
    spyral.director.push(Escena(fake_gtk=True))

if __name__ == "__main__":
    spyral.director.init(SIZE, fullscreen=False)
    main()
    spyral.director.run()
