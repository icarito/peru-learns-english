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
import math
import time

game_dir = os.path.abspath(os.path.dirname(__file__))
def gamedir(archivo):
    return os.path.join(game_dir, archivo)

sys.path.insert(1, gamedir("../../Lib/"))
sys.path.insert(1, gamedir("../../"))

from Globales import decir
import gtk

import pygame
pygame.mixer.init()
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
topic_dir = gamedir("../../Topics/Topic_5/")


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

def play(res):
    if not Escena.MUTE:
        res.play()

class CampodeEstrellas(spyral.Sprite):
    def __init__(self, scene):
        spyral.Sprite.__init__(self, scene)

        self.num_stars = 256
        self.max_depth = 16

        self.layer = "abajo"
        self.speed = 0.2
        self.pos = spyral.Vec2D(scene.size)/2
        self.anchor = "center"

        #self.back_img = spyral.Image(filename=gamedir(
        #    "imagenes/below_the_ocean_by_arghus-d4t62um_1.jpg")).scale(self.scene.size)
        #self.back_img2 = spyral.Image(filename=gamedir(
        #    "imagenes/below_the_ocean_by_arghus-d4t62um_2.jpg")).scale(self.scene.size)
        #self.back_img3 = spyral.Image(filename=gamedir(
        #    "imagenes/below_the_ocean_by_arghus-d4t62um_3.jpg")).scale(self.scene.size)

        self.offset = (0,0)

        self.R = 0
        self.G = 0
        self.B = 48
        self.image = spyral.Image(size=(500,500)).fill((self.R,self.G,self.B))
        self.init_stars()
        self.init_animations()

        spyral.event.register("director.update", self.update)
        spyral.event.register("director.pre_update", self.predraw)

        self.delay = DelayAnimation(3)
        self.delay.property="demora"
        self.animate(self.delay)

        spyral.event.register("CampodeEstrellas.demora.animation.end", self.spawn)

    def defered_spawn(self):
        self.animate(self.delay)

    def spawn(self):
        self.scene.nave.reset()

    def init_animations(self):
        self.top = 0.3
        self.low = 0.03
        self.slowdown_anim = spyral.Animation("speed",
                                spyral.easing.CubicOut(self.top, self.low), duration=3)

        self.speedup_anim = spyral.Animation("speed",
                                spyral.easing.QuadraticOut(self.low, self.top), duration=3)

        self.turnred_anim = (
                              (spyral.Animation("G", spyral.easing.Linear(0, 32), duration=5) &
                              spyral.Animation("B", spyral.easing.QuadraticOut(48, 0), duration=3)) +
                              spyral.Animation("R", spyral.easing.QuadraticOut(0, 128), duration=3))
        self.turnred_anim.property = "turnred"

        self.turnblue_anim = ( spyral.Animation("R", spyral.easing.Linear(128, 0), duration=3) &
                              spyral.Animation("G", spyral.easing.Linear(32, 0), duration=5) &
                              spyral.Animation("B", spyral.easing.Linear(0, 48), duration=3))
        self.turnblue_anim.property = "turnblue"

        self.offset_anim = spyral.Animation("offset", spyral.easing.Arc((0,0), 50), duration=5) + \
                            spyral.Animation("offset", spyral.easing.LinearTuple((50,0),(0,0)), duration=1)
        self.offset_anim.property = "offset"
        #self.offset_anim = spyral.Animation("offset", spyral.easing.Polar((0,0),
        #                            radius=lambda tetha: 50/(tetha+0.1)), duration=5)

    def round(self):
        self.animate(self.offset_anim)

    def speedup(self):
        # EFECTO DE COLOR
        try:
            self.animate(self.turnblue_anim)
        except ValueError:
            self.stop_all_animations()
            self.stop_all_animations()
            a = ( spyral.Animation("R", spyral.easing.Linear(self.R, 0), duration=1) &
                  spyral.Animation("G", spyral.easing.Linear(self.G, 0), duration=1) &
                  spyral.Animation("B", spyral.easing.Linear(self.B, 48), duration=1))
            a.property = "turnblue"
            self.animate(a)

        # EFECTO DE VELOCIDAD
        try:
            self.animate(self.speedup_anim)
        except ValueError:
            self.stop_all_animations()
            a = spyral.Animation("speed",
                                spyral.easing.Linear(self.speed, self.top), duration=5)
            self.animate(a)

    def slowdown(self):
        # EFECTO DE COLOR
        try:
            self.animate(self.turnred_anim)
        except ValueError:
            self.stop_all_animations()
            self.stop_all_animations()
            a = ( spyral.Animation("R", spyral.easing.Linear(self.R, 128), duration=3) &
                  spyral.Animation("G", spyral.easing.Linear(self.G, 32), duration=3) &
                  spyral.Animation("B", spyral.easing.Linear(self.B, 0), duration=3))

            a.property = "turnred"
            self.animate(a)

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
                self.image.draw_circle((shade,shade,shade),(x,y),int(size))

    def predraw(self):
        self.image.fill((self.R,self.G,self.B))
        #self.image = self.back_img.copy()

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

        #self.scale = 1.2
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
        self.n.pos += spyral.Vec2D(0, -190)

        self.s = Bloque(self, *self.palabras[1])
        self.s.pos += spyral.Vec2D(0, +190)

        self.o = Bloque(self, *self.palabras[2])
        self.o.pos += spyral.Vec2D(-190, 0)

        self.e = Bloque(self, *self.palabras[3])
        self.e.pos += spyral.Vec2D(+190, 0)

        self.direcciones = (self.n, self.s, self.e, self.o)

        self.visible = False
        self.estado = "reset"
        self.elegida = None

        self.init_animations()

        spyral.event.register("input.keyboard.down.down", self.control_s)
        spyral.event.register("input.keyboard.down.up", self.control_n)
        spyral.event.register("input.keyboard.down.left", self.control_o)
        spyral.event.register("input.keyboard.down.right", self.control_e)

        spyral.event.register("Bloque.wait.animation.end", self.clear)
        spyral.event.register("Bloque.wait2.animation.end", self.repetir)
        spyral.event.register("Bloque.wait3.animation.end", self.repetir2)

        spyral.event.register("director.update", self.update)

    def update(self):
        self.pos = self.scene.campo.offset

    def repetir(self):
        PALABRA, ARCHIVO = self.palabras[self.elegida]
        decir(70, 57, 0, "en-gb", PALABRA)

    def repetir2(self, modifier=0):
        PALABRA, ARCHIVO = self.palabras[self.elegida]
        decir(100, 37, 0, "en-gb", PALABRA)

    def reset(self):
        self.reset_words()
        teclas = ("up", "down", "right", "left")

        if self.elegida is not None:
            for index in range(0,4):
                if index==self.elegida:
                    spyral.event.unregister("input.keyboard.down." + teclas[index], self.gana)
                else:
                    spyral.event.unregister("input.keyboard.down." + teclas[index], self.pierde)

        self.elegida = randint(0,3)
        PALABRA, ARCHIVO = self.palabras[self.elegida]

        for index in range(0,4):
            self.direcciones[index].set_word(*self.palabras[index])
            if index==self.elegida:
                spyral.event.register("input.keyboard.down." + teclas[index], self.gana)
            else:
                spyral.event.register("input.keyboard.down." + teclas[index], self.pierde)

        decir(50, 57, 0, "en-gb", PALABRA)
        self.invade()

    def pierde(self):
        self.o.stop_animation(self.delay2_anim)
        self.o.stop_animation(self.delay3_anim)

        self.scene.campo.defered_spawn()

        print "PIERDE ",
        print self.elegida

    def gana(self):
        self.scene.campo.defered_spawn()

        self.o.stop_animation(self.delay2_anim)
        self.o.stop_animation(self.delay3_anim)

        acertado = self.direcciones[self.elegida]

        recompensa = 200

        self.scene.puntos += recompensa
        if Escena.gameview:
            Escena.gameview.update_score(self.scene.puntos)

    def reset_words(self):
        self.palabras = obtener_set(self.topic)

    def init_animations(self):
        ## TODO
        ## self.invasion_anim_1 = spyral.Animation("scale", spyral.easing.QuadraticOut(0.1, 1), duration=15)
        self.invasion_anim = spyral.Animation("angle", spyral.easing.Linear(0, math.pi * 2), duration=5) & \
                             spyral.Animation("scale", spyral.easing.QuadraticOut(0.1, 1.2), duration=15)
        ## self.invasion_anim = spyral.Animation("scale_x", spyral.easing.QuadraticOut(0, 0.9), duration=10)
        ## self.invasion_anim = spyral.Animation("scale_y", spyral.easing.QuadraticOut(0, 0.9), duration=10)
        self.invasion_anim.property = "invasion"

        self.delay_anim = DelayAnimation(15)
        self.delay_anim.property = "wait"

        self.delay2_anim = DelayAnimation(3)
        self.delay2_anim.property = "wait2"

        self.delay3_anim = DelayAnimation(6)
        self.delay3_anim.property = "wait3"

    def invade(self):
        if self.estado == "invade":
            self.clear()

        self.estado = "invade"

        direcciones = (self.n, self.s, self.e, self.o)

        for bloque in direcciones:
            bloque.animate(self.invasion_anim)

        self.visible = True
        self.scene.campo.slowdown()

        self.o.stop_animation(self.delay_anim)
        self.o.animate(self.delay_anim)
        self.o.animate(self.delay2_anim)
        self.o.animate(self.delay3_anim)
        self.scene.campo.round()

    def clear(self, acertada=None):
        self.estado = "reset"
        for bloque in self.n,self.s,self.e,self.o:
            if bloque==acertada:
                print bloque
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
    MUTE = False
    gameview = False

    def __init__(self, topic=topic_dir, fake_gtk=False, gameview=False):
        spyral.Scene.__init__(self, SIZE)

        self.layers = ["abajo", "arriba", "primer"]
        self.puntos = 0

        img = spyral.Image(filename=gamedir(
            "imagenes/Crux-20100220.jpg")).scale(self.scene.size)
        #img = spyral.Image(size=(700, 700))

        #n = pygame.Surface.convert_alpha(img._surf)
        #n.fill((64, 0, 0, 127))
        #img._surf.blit(n, (0, 0))

        self.background = img

        self.nave = Nave(self, topic)
        self.campo = CampodeEstrellas(self)

        #self.tablero = Tablero(self, topic, mapa=MAPA1)

        spyral.event.register("system.quit", spyral.director.pop, scene=self)

        pygame.mixer.music.load(gamedir('musica/ObservingTheStar.ogg'))
        pygame.mixer.music.play(-1)

        if gameview:
            Escena.gameview = gameview

        if fake_gtk:
            gtk.threads_init()
            spyral.event.register("director.update", self.gtk_main_iteration)

    def mute(self, value):
        if value==True:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.play()

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
