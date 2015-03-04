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
import random

game_dir = os.path.abspath(os.path.dirname(__file__))
def gamedir(archivo):
    return os.path.join(game_dir, archivo)

sys.path.insert(1, gamedir("../../Lib/"))
sys.path.insert(1, gamedir("../../"))

from Globales import decir
import gtk
gtk.threads_init()

import pygame
pygame.mixer.init()
import spyral
from random import randrange, randint
import csv
import collections

SIZE = (700, 700)
TILE = (64, 64)

def play(res):
    if not Escena.MUTE:
        res.play()

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
topic_dir = gamedir("../../Topics/Topic_3/")

VOCABULARIO = []
CANT_PALABRAS = 0

def obtener_palabra(topic_dir=topic_dir):
    global VOCABULARIO, CANT_PALABRAS

    if not VOCABULARIO:
        archivo = os.path.join(topic_dir, "vocabulario.csv")
        tabla = csv.DictReader(file(archivo))
        for linea in tabla:
            VOCABULARIO.append(linea)
        CANT_PALABRAS = len(VOCABULARIO)

    indice = random.randint(0, len(VOCABULARIO) - 1)

    palabra = VOCABULARIO[indice]["term"]
    uid = VOCABULARIO[indice]["id"]
    palabra_png = os.path.join(topic_dir, "Imagenes", uid + '.png')

    VOCABULARIO.pop(indice)

    return palabra, palabra_png

def reset_vocabulario():
    global VOCABULARIO, CANT_PALABRAS
    VOCABULARIO = []
    CANT_PALABRAS = 0

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

        self.ESTADO = "bigbang"
        self.gone = False

        self.R = 0
        self.G = 0
        self.B = 48
        self.image = spyral.Image(size=(700,700)).fill((self.R,self.G,self.B))
        self.init_stars()
        self.init_animations()

        spyral.event.register("director.update", self.update)
        spyral.event.register("director.pre_update", self.predraw)

        self.delay = DelayAnimation(5)
        self.delay.property="demora"
        #self.defered_spawn()

        spyral.event.register("CampodeEstrellas.demora.animation.end", self.spawn)

    def forget(self):
        spyral.event.unregister("CampodeEstrellas.demora.animation.end", self.spawn)

    def defered_spawn(self, secs=1):
        if not self.ESTADO=="volando":
            delay = self.delay
            if secs:
                delay = DelayAnimation(secs)
                delay.property="demora"
            self.animate(delay)
            self.ESTADO = "volando"

    def spawn(self):
        if not self.gone:
            self.scene.nave.reset()
            self.ESTADO = "emergencia"

    def init_animations(self):
        self.top = 0.3
        self.low = 0.03
        self.slowdown_anim = spyral.Animation("speed",
                                spyral.easing.CubicOut(self.top, self.low), duration=3)

        self.speedup_anim = spyral.Animation("speed",
                                spyral.easing.QuadraticOut(self.low, self.top), duration=3)

        self.turnred_anim = (
                              (spyral.Animation("G", spyral.easing.Linear(0, 32), duration=5) &
                              spyral.Animation("B", spyral.easing.QuadraticOut(80, 0), duration=3)) +
                              spyral.Animation("R", spyral.easing.QuadraticOut(0, 128), duration=3))
        self.turnred_anim.property = "turnred"

        self.turnblue_anim = ( spyral.Animation("R", spyral.easing.Linear(192, 0), duration=3) &
                              spyral.Animation("G", spyral.easing.Linear(32, 0), duration=5) &
                              spyral.Animation("B", spyral.easing.Linear(0, 80), duration=3))
        self.turnblue_anim.property = "turnblue"

        self.turnblue_alt_anim = ( spyral.Animation("R", spyral.easing.Linear(128, 0), duration=2) & 
                  spyral.Animation("G", spyral.easing.Linear(192, 0), duration=3) &
                  spyral.Animation("B", spyral.easing.Linear(148, 80), duration=2))
        self.turnblue_alt_anim.property = "turnblue"

        self.goodbye_anim = ( spyral.Animation("R", spyral.easing.Linear(0, 0), duration=3) &
                              spyral.Animation("G", spyral.easing.Linear(0, 0), duration=5) &
                              spyral.Animation("B", spyral.easing.Linear(40, 80), duration=5))
        self.goodbye_anim.property = "goodbye"

    def goodbye(self):
        self.stop_all_animations()
        self.stop_all_animations()
        self.animate(self.goodbye_anim)
        a = spyral.Animation("speed",
                            spyral.easing.Linear(self.speed, self.top), duration=5)
        self.animate(a)

    def speedup(self, result):
        # EFECTO DE COLOR
        self.stop_all_animations()
        self.stop_all_animations()
        if result:
            self.animate(self.turnblue_alt_anim)
        else:
            self.animate(self.turnblue_anim)

        # EFECTO DE VELOCIDAD
        try:
            self.animate(self.speedup_anim)
        except ValueError:
            self.stop_all_animations()
            a = spyral.Animation("speed",
                                spyral.easing.Linear(self.speed, self.top), duration=5)
            self.animate(a)

    def slowdown(self, color=True):
        # EFECTO DE COLOR
        if color:
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

        self.result = None

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
        self.elegida = None

        spyral.event.register("TimeMaster.wait.animation.end", self.clear_and_loose)

        self.init_animations()

        spyral.event.register("TimeMaster.wait2.animation.end", self.repetir)
        spyral.event.register("TimeMaster.wait3.animation.end", self.repetir2)

        spyral.event.register("director.update", self.update)

        self.win_snd = pygame.mixer.Sound(gamedir("sonidos/Jump.ogg"))
        self.loose_snd = pygame.mixer.Sound(gamedir("sonidos/Laser2.ogg"))
        self.drown_snd = pygame.mixer.Sound(gamedir("sonidos/Explosion.ogg"))

    def update(self):
        self.pos = self.scene.T.offset

    def repetir(self):
        PALABRA, ARCHIVO = self.palabras[self.elegida]
        if self.result==None:
            decir(70, 57, 0, "en-gb", PALABRA)

    def repetir2(self, modifier=0):
        PALABRA, ARCHIVO = self.palabras[self.elegida]
        if self.result==None:
            decir(100, 37, 0, "en-gb", PALABRA)
        #elif self.result==True:
        #    decir(100, 37, 0, "en-gb", "correct!")
        #elif self.result==False:
        #    decir(50, 57, 0, "en-gb", "wrong!")
        self.result = None

    def reset(self):
        self.reset_words()

        self.elegida = randint(0,3)
        PALABRA, ARCHIVO = self.palabras[self.elegida]

        teclas = ("up", "down", "right", "left")
        teclas2 = ("keypad_8", "keypad_2", "keypad_6", "keypad_4")
        teclas3 = ("keypad_9", "keypad_3", "keypad_1", "keypad_7")

        for index in range(0,4):
            self.direcciones[index].set_word(*self.palabras[index])
            if index==self.elegida:
                spyral.event.register("input.keyboard.down." + teclas[index], self.gana)
                spyral.event.register("input.keyboard.down." + teclas2[index], self.gana)
                spyral.event.register("input.keyboard.down." + teclas3[index], self.gana)
            else:
                spyral.event.register("input.keyboard.down." + teclas[index], self.pierde)
                spyral.event.register("input.keyboard.down." + teclas2[index], self.pierde)
                spyral.event.register("input.keyboard.down." + teclas3[index], self.pierde)

        decir(50, 57, 0, "en-gb", PALABRA)
        self.invade()

    def next_level(self):
        spyral.event.unregister("TimeMaster.wait.animation.end", self.clear_and_loose)
        self.scene.T.stop_animation(self.delay_anim)
        self.clear()
        spyral.event.register("TimeMaster.wait.animation.end", self.clear_and_loose)

    def key_index(self, keycode):
        teclas = ("up", "down", "right", "left")
        teclas2 = ("keypad_8", "keypad_2", "keypad_6", "keypad_4")
        teclas3 = ("keypad_9", "keypad_3", "keypad_1", "keypad_7")

        for keyset in [teclas, teclas2, teclas3]:
            try:
                return keyset.index(pygame.key.name(keycode))
            except ValueError:
                pass

    def set_answer(self, ganamos, keycode=None):
        PALABRA, ARCHIVO = self.palabras[self.elegida]
        if keycode:
            PALABRA, ARCHIVO = self.palabras[self.key_index(keycode)]
        if ganamos:
            frase = '"' + PALABRA + "\" is correct"
        else:
            frase = '"' + PALABRA + "\" is wrong"
        nueva = self.scene.label.set_trans_text(frase, red=not ganamos)
        self.scene.label.image = nueva
        self.scene.label.blink()

    def pierde(self, event):
        self.set_answer(False, event.key)
        play(self.loose_snd)
        self.result = False
        self.next_level()
        self.scene.T.stop_animation(self.delay2_anim)
        self.scene.T.stop_animation(self.delay3_anim)

        castigo = -50
        self.scene.puntos += castigo
        if Escena.gameview:
            Escena.gameview.update_score(self.scene.puntos)

    def gana(self):
        global CANT_PALABRAS
        self.set_answer(True)
        play(self.win_snd)
        self.result = True
        self.next_level()
        self.scene.T.stop_animation(self.delay2_anim)
        self.scene.T.stop_animation(self.delay3_anim)

        #acertado = self.direcciones[self.elegida]

        recompensa = 200
        self.scene.puntos += recompensa

        if self.scene.puntos > CANT_PALABRAS * 200:
            self.scene.campo.gone = True
            self.scene.finalfinal()

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
        self.scene.label.visible = False
        direcciones = (self.n, self.s, self.e, self.o)

        #self.scene.label.visible = False
        for bloque in direcciones:
            bloque.animate(self.invasion_anim)

        self.visible = True
        self.scene.campo.slowdown()

        self.scene.T.stop_animation(self.delay_anim)
        self.scene.T.animate(self.delay_anim)
        self.scene.T.animate(self.delay2_anim)
        self.scene.T.animate(self.delay3_anim)
        self.scene.T.round()

    def clear_and_loose(self):
        play(self.drown_snd)
        dialog = Dialogo(self.scene, "GAME OVER", self.question)
        self.visible = False
        spyral.event.unregister("TimeMaster.wait.animation.end", self.clear)
        spyral.event.unregister("TimeMaster.wait.animation.end", self.clear_and_loose)
        spyral.event.unregister("TimeMaster.wait2.animation.end", self.repetir)
        spyral.event.unregister("TimeMaster.wait3.animation.end", self.repetir2)

    def forget(self):
        self.scene.label.kill()
        self.kill()
        self.scene.campo.forget()
        self.scene.campo.slowdown(color=False)
        spyral.event.unregister("TimeMaster.wait.animation.end", self.clear)
        spyral.event.unregister("TimeMaster.wait.animation.end", self.clear_and_loose)
        spyral.event.unregister("TimeMaster.wait2.animation.end", self.repetir)
        spyral.event.unregister("TimeMaster.wait3.animation.end", self.repetir2)

    def question(self):
        dialog = Dialogo(self.scene, "Play again?", self.reset_and_clear)
        spyral.event.register_multiple("input.keyboard.down.y", [dialog.die, self.reset_and_clear])

    def reset_and_clear(self):
        spyral.event.register("TimeMaster.wait.animation.end", self.clear_and_loose)
        spyral.event.unregister("input.keyboard.down.y", self.reset_and_clear)
        self.scene.puntos = 0
        if Escena.gameview:
            Escena.gameview.update_score(self.scene.puntos)
        self.visible = True
        self.clear()

    def clear(self, acertada=None):
        self.scene.T.stop_round()
        for bloque in self.n,self.s,self.e,self.o:
            bloque.stop_animation(self.invasion_anim)
        self.scene.T.stop_animation(self.delay_anim)
        self.visible = False
        
        self.scene.campo.speedup(self.result)
        self.scene.campo.defered_spawn(5)

        teclas = ("up", "down", "right", "left")
        teclas2 = ("keypad_8", "keypad_2", "keypad_6", "keypad_4")
        teclas3 = ("keypad_9", "keypad_3", "keypad_1", "keypad_7")

        if self.elegida is not None:
            for index in range(0,4):
                if index==self.elegida:
                    spyral.event.unregister("input.keyboard.down." + teclas2[index], self.gana)
                    spyral.event.unregister("input.keyboard.down." + teclas3[index], self.gana)
                    spyral.event.unregister("input.keyboard.down." + teclas[index], self.gana)
                else:
                    spyral.event.unregister("input.keyboard.down." + teclas2[index], self.pierde)
                    spyral.event.unregister("input.keyboard.down." + teclas3[index], self.pierde)
                    spyral.event.unregister("input.keyboard.down." + teclas[index], self.pierde)

class TimeMaster(spyral.Sprite):
    def __init__(self, scene):
        spyral.Sprite.__init__(self, scene)

        self.ESTADO = "bigbang"

        self.image = spyral.Image(size=(1,1))
        self.pos = (-1,-1)

        self.offset = (0,0)

        self.offset_anim = spyral.Animation("offset", spyral.easing.Arc((0,0), 50), duration=5) + \
                            spyral.Animation("offset", spyral.easing.LinearTuple((50,0),(0,0)), duration=1)
        self.offset_anim.property = "offset"

        spyral.event.register("TimeMaster.offset.animation.end", self.endhandler)

    def endhandler(self):
        self.ESTADO = "quieto"

    def round(self):
        if not self.ESTADO=="rodando":
            self.animate(self.offset_anim)
            self.ESTADO = "rodando"

    def stop_round(self):
        if self.ESTADO=="rodando":
            self.stop_animation(self.offset_anim)


class Dialogo(spyral.Sprite):

    def __init__(self, scene, texto, callback=None, transparent=False):
        spyral.Sprite.__init__(self, scene)

        self.callback = callback
        self.anchor = 'center'
        self.pos = spyral.Vec2D(scene.size) / 2
        self.margen = 5
        self.layer = "primer"

        font_path = gamedir("../fonts/DejaVuSans.ttf")
        if transparent:
            self.font = spyral.Font(font_path, 20, (255, 255, 255))
            self.font_red = spyral.Font(font_path, 20, (255, 0, 0))
            self.line_height = self.font.linesize
            nueva = self.set_trans_text(texto)
            self.image = nueva
            self.scale = 2
        else:
            self.font = spyral.Font(font_path, 14, (0, 0, 0))
            self.line_height = self.font.linesize
            self.image = spyral.Image(filename=gamedir("imagenes/Menu_2.png"))
            nueva = self.set_text(texto)
            self.image.draw_image(nueva,
                position=(self.margen / 2, 0), anchor="midleft")

        if not transparent:
            spyral.event.register("input.mouse.down.left", self.go_callback)
            spyral.event.register("input.keyboard.down.return", self.go_callback)
            spyral.event.register("input.keyboard.down.space", self.go_callback)

    def die(self):
        self.callback = None
        self.go_callback()

    def go_callback(self):
        spyral.event.unregister("input.mouse.down.left", self.go_callback)
        spyral.event.unregister("input.keyboard.down.return", self.go_callback)
        spyral.event.unregister("input.keyboard.down.space", self.go_callback)
        if self.callback:
            self.callback()
        self.kill()

    def blink(self):
        blank = spyral.Image(size=(1,1)).fill((0,0,0,0))
        anim = spyral.Animation("image", spyral.easing.Iterate([blank, self.image], times=8), duration=3)
        self.visible = True
        self.animate(anim)

    def set_trans_text(self, text, red=False):
        if red:
            image=self.font_red.render(text)
        else:
            image=self.font.render(text)
        return image

    def set_text(self, text):
        self._text = text
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

        self.scale = 2

        return bloque

class Title(spyral.Sprite):

    def __init__(self, scene):
        spyral.Sprite.__init__(self, scene)

        self.image = spyral.Image(gamedir("imagenes/juego3_titulo.png"))
        self.layer = "primer"
        self.pos = (scene.width / 2, 100)
        self.anchor = "center"


class Ship(spyral.Sprite):

    def __init__(self, scene):
        spyral.Sprite.__init__(self, scene)

        self.image = spyral.Image(gamedir("imagenes/Cruiser.png"))
        self.layer = "primer"
        self.pos = (scene.width / 2, scene.height + 100)
        self.center = spyral.Vec2D(scene.size)/2
        self.anchor = "center"

        self.win_snd = pygame.mixer.Sound(gamedir("sonidos/Randomize4.ogg"))
        self.init_animations()

        spyral.event.register("Ship.goodbye.animation.end", self.thanks)
        spyral.event.register("Ship.demora.animation.end", self.burn)

    def burn(self):
        play(self.win_snd)

    def thanks(self):
        self.intro = Dialogo(self.scene, "You've won. Thanks for playing.", self.thanks)

    def init_animations(self):
        a = spyral.Animation("pos", spyral.easing.LinearTuple(self.pos, self.center), 3)
        b = spyral.Animation("scale_y", spyral.easing.Linear(1, 0.5), 1)
        c = spyral.Animation("scale_x", spyral.easing.QuadraticOut(1, 0.1), 2)
        top = (self.scene.width/2, -100)
        d = spyral.Animation("pos", spyral.easing.LinearTuple(self.center, top), 3)
        composition = a + b + (c & d)
        composition.property = "goodbye"
        self.scene.campo.goodbye()
        self.animate(composition)

        self.delay = DelayAnimation(4)
        self.delay.property="demora"
        self.animate(self.delay)

class Escena(spyral.Scene):
    MUTE = False
    gameview = False

    def __init__(self, topic=topic_dir, fake_gtk=False, gameview=False):
        spyral.Scene.__init__(self, SIZE)

        reset_vocabulario()

        self.T = TimeMaster(self)
        self.layers = ["abajo", "arriba", "primer"]
        self.puntos = 0

        #img = spyral.Image(filename=gamedir(
        #    "imagenes/Crux-20100220.jpg")).scale(self.scene.size)
        img = spyral.Image(size=(700, 700))

        #n = pygame.Surface.convert_alpha(img._surf)
        #n.fill((64, 0, 0, 127))
        #img._surf.blit(n, (0, 0))

        self.background = img

        self.nave = Nave(self, topic)
        self.campo = CampodeEstrellas(self)
        self.label = Dialogo(self, "WORD", transparent=True)
        self.label.visible = False
        self.label.layer = "primer"

        self.intro0()

        spyral.event.register("system.quit", spyral.director.pop, scene=self)

        pygame.mixer.music.load(gamedir('musica/ObservingTheStar.ogg'))
        pygame.mixer.music.play(-1)

        if gameview:
            Escena.gameview = gameview

        if fake_gtk:
            spyral.event.register("director.update", self.gtk_main_iteration)

    def intro0(self):
        self.intro = Dialogo(self, "Now I must get to my ship. It is at the bottom of the ocean.", self.intro1)
        self.titulo = Title(self)

    def intro1(self):
        self.intro = Dialogo(self, "Listen carefully and use the arrow keys to navigate in the right direction.", self.campo.defered_spawn)
        self.titulo.kill()

    def finalfinal(self):
        self.ship = Ship(self)
        self.nave.forget()

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
