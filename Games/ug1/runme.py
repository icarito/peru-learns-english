#!/bin/env python2
# *-* coding: utf-8 *-*

#   Juego UG1 por:
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
pygame.mixer.init()
import spyral
import random
import csv
import collections
pygame.mixer.init()

SIZE = (700, 700)
TILE = (64, 64)

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


class Escena(spyral.Scene):
    def __init__(self, topic=topic_dir):
        spyral.Scene.__init__(self, SIZE)

        self.topic = topic
        self.layers = ["abajo", "abajo2", "arriba", "primer"]

        self.img_orig = spyral.Image(filename=gamedir(
            "images/Peru_Machu_Picchu_Sunrise.jpg")).scale(self.scene.size)

        self.img = self.img_orig.copy()
        self.puntaje = 0

        n = pygame.Surface.convert_alpha(self.img._surf)
        # red at 50%
        n.fill((255, 0, 0, 127))
        self.img._surf.blit(n, (0, 0))

        self.background = self.img

        self.j = Jugador(self)
        self.l = Lluvia(self)

        self.tablero = Tablero(self, topic)
        self.terraza = Terraza(self)
        self.v = Visualizador(self)

        spyral.event.register("system.quit", spyral.director.pop, scene=self)
        spyral.event.register("director.scene.enter", self.l.llover, scene=self)
        spyral.event.register("input.keyboard.down.esc", self.escape, scene=self)
        spyral.event.register("Tablero.score", self.score)

    def score(self):
        self.puntaje = self.tablero.ganadas * 100 - self.tablero.perdidas
        if self.puntaje > CANT_PALABRAS * 100:
            self.scene.l.finalizar(ganamos=True)
            self.scene.v.stop_all_animations()
        try:
            Intro.gameview.update_score(self.puntaje)
        except AttributeError:
            pass

    def escape(self):
        spyral.event.unregister("Lluvia.y.animation.end", self.scene.l.finalizar)
        spyral.event.unregister("Lluvia.demora.animation.end", self.scene.l.sonar_explosion)
        self.scene.l.stop_all_animations()
        self.scene.l.stop_all_animations()
        self.scene.l.visible = False
        self.endgame()

    def endgame(self):
        #self.scene.background = self.scene.img_orig
        #spyral.event.unregister("Tablero.reset.animation.end", self.scene.tablero.reset)
        self.scene.tablero.visible = False
        #spyral.event.unregister("Lluvia.y.animation.end", self.scene.l.finalizar)
        #spyral.event.unregister("Lluvia.demora.animation.end", self.scene.l.sonar_explosion)
        #self.scene.l.stop_all_animations()
        #self.scene.l.stop_all_animations()
        #self.scene.l.visible = False
        self.scene.v.set_text("GAME OVER")
        self.scene.v.stop_all_animations()
        self.scene.j.set_mirame()
        spyral.event.unregister("input.keyboard.down.esc", self.escape)
        self.the_question = Dialogo(self, "Play again?", self.the_question_click)
        spyral.event.unregister("input.keyboard.down.*", self.tablero.procesar_tecla)
        #self.scene.j.set_deambular()

    def the_question_click(self, pos):
        if self.the_question.collide_point(pos):
            self.the_question.goplay()


class Terraza(spyral.Sprite):

    def __init__(self, scene):

        spyral.Sprite.__init__(self, scene)

        self.anchor = "midbottom"
        self.layer = "abajo"
        self.image = spyral.Image(filename=gamedir("images/terraza.png"))
        self.pos = (scene.width / 2, scene.height)

    def temblar(self):
        m = spyral.Animation("x", spyral.easing.Iterate(
            [-3, 0, 3], 5), 2, shift=self.x)
        self.animate(m)


class Tablero(spyral.Sprite):

    def __init__(self, scene, topic=topic_dir):

        spyral.Sprite.__init__(self, scene)

        self.completo = False
        self.acertadas = " "
        self.layer = "abajo"
        self.ganadas = 0
        self.perdidas = 0
        spyral.event.queue("Tablero.score")

        self.topic = topic

        font_path = gamedir("../fonts/DejaVuSans.ttf")
        self.font = spyral.Font(font_path, 60, (0, 0, 0))
        self.palabra, self.archivo_img = obtener_palabra(self.topic)
        self.text = self.palabra
        self.image = self.font.render("")

        self.anchor = 'midbottom'

        self.x = self.scene.width / 2
        self.y = self.scene.height - 128

        self.mostrar(self.text, "")

        spyral.event.register("input.keyboard.down.*", self.procesar_tecla, scene=self.scene)
        spyral.event.register("Tablero.reset.animation.end", self.reset, scene=self.scene)

        self.blup_snd = pygame.mixer.Sound(gamedir("sonidos/Randomize3.ogg"))
        self.hit_snd = pygame.mixer.Sound(gamedir("sonidos/Pickup_Coin.ogg"))

    def reset(self):
        spyral.event.queue("Tablero.score")
        self.ganadas = self.ganadas + 1
        self.palabra_anterior = self.palabra
        while self.palabra_anterior == self.palabra:
            self.palabra, self.archivo_img = obtener_palabra(self.topic)
        self.text = self.palabra
        self.acertadas = " "
        self.mostrar(self.palabra, self.acertadas)
        self.scene.l.reset()
        self.scene.v.reset()
        spyral.event.register("input.keyboard.down.*", self.procesar_tecla, scene=self.scene)

    def set_text(self, text):
        self.image = self.font.render(text)
        self.text = text

    def mostrar(self, frase, acertadas, letra=None):
        total = 0
        estado = ""
        for letra in frase:
            if letra in acertadas:
                estado = estado + " " + letra
                total = total + 1
            else:
                estado = estado + u" _"

        if total == len(frase):
            self.completo = True

        self.set_text(estado)

    def check_completos(self):
        for c in self.palabra:
            if c not in self.acertadas:
                return False
        return True

    def procesar_tecla(self, key):
        if not 0 < key < 255:
            return

        respuesta = chr(key)

        if respuesta not in self.acertadas:
            self.acertadas = self.acertadas + respuesta

        if respuesta in self.palabra:
            if not Intro.MUTE:
                self.hit_snd.play()
        else:
            self.perdidas += 1
            spyral.event.queue("Tablero.score")
            if not Intro.MUTE:
                self.blup_snd.play()

        self.mostrar(self.palabra, self.acertadas)

        if self.check_completos():
            spyral.event.unregister(
                "input.keyboard.down.*", self.procesar_tecla)
            self.scene.l.stop_all_animations()
            self.scene.l.stop_all_animations()  # spyral, please?
            tiempo = self.scene.j.set_caminar_x(self.scene.l.x - 20, True)
            self.scene.l.explotar(tiempo + 1)

            d = DelayAnimation(tiempo + 3)
            d.property = "reset"
            self.animate(d)


class Lluvia(spyral.Sprite):

    def __init__(self, scene):

        spyral.Sprite.__init__(self, scene)

        self.font = spyral.Font(font_path, 28, (255, 255, 255))
        self.anchor = "center"
        self.x = scene.width / 2 + random.randint(0, 300) - 150

        self.layer = "primer"
        self.start_time = spyral.director.get_tick()

        # Asteroide
        self.asteroid_frames = []
        self.target_frames = []
        for i in range(0, 60):
            number = str(i).zfill(2)
            name = "Asteroid-A-10-" + number + ".png"
            self.asteroid_frames.append(spyral.Image(
                filename=gamedir("images/asteroid/" + name)))
            if int(i / 3) % 2 == 0:
                self.target_frames.append(spyral.Image(size=(75, 75)))
            else:
                self.target_frames.append(spyral.Image(
                    filename=gamedir("images/asteroid/" + name)))

        m = spyral.Animation("image", spyral.easing.Iterate(
            self.asteroid_frames, 1), 5, loop=True)

        self.animate(m)

        # Boom
        self.explosion_full = spyral.Image(
            filename=gamedir("images/explosion.png"))

        self.explosion_frames = []
        explosion_size = 205

        self.explosion_frames.append(
            self.explosion_full.copy().crop((13 * explosion_size, 0),
            (explosion_size, explosion_size)))

        for i in range(0, 13):
            self.explosion_frames.append(
                self.explosion_full.copy().crop((i * explosion_size, 0),
                (explosion_size, explosion_size)))

        spyral.event.register("Lluvia.y.animation.end", self.finalizar, scene=self.scene)
        spyral.event.register("Lluvia.demora.animation.end", self.sonar_explosion)
        self.scale = 2

        self.explotar_snd = pygame.mixer.Sound(gamedir("sonidos/Explosion.ogg"))
        self.alarm_snd = pygame.mixer.Sound(gamedir("sonidos/missile_alarm.ogg"))

    def reset(self):
        self.x = self.scene.width / 2 + random.randint(0, 600) - 300
        self.stop_all_animations()
        self.stop_all_animations()
        self.stop_all_animations()
        m = spyral.Animation("image", spyral.easing.Iterate(
            self.asteroid_frames, 1), 5, loop=True)
        self.animate(m)
        self.llover()

    def llover(self):
        if not Intro.MUTE:
            self.alarm_snd.play()

        tick = (spyral.director.get_tick() - self.start_time) / 300.0
        if tick>16:
            tick = 16
        p = spyral.Animation("y",
            spyral.easing.CubicIn(0, self.scene.height - 75),
            duration=10 + len(self.scene.tablero.palabra) * 3 - tick)
        self.animate(p)

    def finalizar(self, ganamos=False):
        if not self.scene.tablero.check_completos():
            spyral.event.unregister("input.keyboard.down.*",
                self.scene.tablero.procesar_tecla)
            self.scene.tablero.set_text("SCORE: " + str(self.scene.puntaje))
            if not ganamos:
                self.scene.v.set_text("GAME OVER")
                self.explotar()
                self.scene.terraza.temblar()
                self.scene.j.set_caer()
                self.scene.endgame()
            else:
                self.scene.background = self.scene.img_orig
                spyral.event.unregister("Lluvia.y.animation.end", self.finalizar)
                spyral.event.unregister("Lluvia.demora.animation.end", self.sonar_explosion)
                self.stop_all_animations()
                self.stop_all_animations()
                self.visible = False
                self.scene.v.set_text("YOU SAVED THE CITY!")
                self.scene.j.set_mirame()


    def explotar(self, wait=0):
        n = spyral.Animation("image", spyral.easing.Iterate(
            self.explosion_frames, 1), 2)
        if wait:
            m = spyral.Animation("image", spyral.easing.Iterate(
                self.target_frames, wait / 5.0), wait)
            n = m + n
            n.property = "tictac"
        self.stop_all_animations()
        self.animate(n)

        d = DelayAnimation(wait)
        d.property="demora"
        self.animate(d)


    def sonar_explosion(self):
        if not Intro.MUTE:
            self.explotar_snd.play()

class Visualizador(spyral.Sprite):

    def __init__(self, scene):
        spyral.Sprite.__init__(self, scene)

        self.image = spyral.Image(gamedir("images/golden-border.png"))
        self.layer = "abajo"

        self.font = spyral.Font(font_path, 28, (0, 0, 0))
        self.line_height = self.font.linesize
        self.margen = 50

        self.reset()

    def set_text(self, text):
        nueva = spyral.Image(size=(self.width - self.margen,
            self.height - self.margen)).fill((255, 255, 255))
        self.image.draw_image(nueva,
            position=(self.margen / 2, 0), anchor="midleft")
        self.image.draw_image(self.render_text(text),
            position=(0, 0), anchor="midleft")

    def reset(self, txt=None, img=None, loop=False):
        self.stop_all_animations()

        if not txt:
            self.text = "Please type the word"
        else:
            self.text = txt

        if not img:
            try:
                self.palabra_png = self.scene.tablero.archivo_img
            except AttributeError:
                self.palabra_png = spyral.Image(size=(self.width - self.margen,
                    self.height - self.margen)).fill((255, 255, 255))
        else:
            self.palabra_png = img

        image1 = self.image.copy()
        image1.draw_image(self.render_image(self.palabra_png),
            position=(25, 0), anchor="midleft")

        image2 = self.image.copy()

        nueva = spyral.Image(size=(self.width - self.margen,
            self.height - self.margen)).fill((255, 255, 255))
        image2.draw_image(nueva,
            position=(self.margen / 2, 0), anchor="midleft")
        image2.draw_image(self.render_text(self.text),
            position=(0, 0), anchor="midleft")
        a = spyral.Animation("image", spyral.easing.Iterate([image1, image2], 6), 6, loop=loop)
        self.animate(a)

    def render_image(self, image):
        try:
            nueva = spyral.Image(filename=image).scale((
                self.width - self.margen, self.height - self.margen))
        except pygame.error:
            nueva = spyral.Image(size=(self.width - self.margen,
                self.height - self.margen)).fill((255, 255, 255))
        return nueva

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


class Jugador(spyral.Sprite):

    def __init__(self, scene):

        spyral.Sprite.__init__(self, scene)

        self.full_image = spyral.Image(filename=gamedir("images/user2.png"))
        self.estado = "nuevo"
        self.y = scene.height - 138
        self.x = scene.width / 2
        self.velocidad = 90
        self.anchor = "midtop"
        self.layer = "primer"
        self.northq = self.full_image.copy().crop((0, 8 * 64), TILE)
        self.southq = self.full_image.copy().crop((0, 10 * 64), TILE)

        self.east = []
        for i in range(0, 8):
            self.east.append(
                self.full_image.copy().crop((i * 64, 11 * 64), TILE))

        self.west = []
        for i in range(0, 8):
            self.west.append(
                self.full_image.copy().crop((i * 64, 9 * 64), TILE))

        self.south = []
        for i in range(0, 8):
            self.south.append(
                self.full_image.copy().crop((i * 64, 10 * 64), TILE))

        self.north = []
        for i in range(0, 8):
            self.north.append(
                self.full_image.copy().crop((i * 64, 8 * 64), TILE))

        self.fire = []
        for i in range(0, 7):
            self.fire.append(
                self.full_image.copy().crop((i * 64, 0 * 64), TILE))

        self.caer = []
        for i in range(0, 6):
            self.caer.append(
                self.full_image.copy().crop((i * 64, 20 * 64), TILE))

        self.caer.append(
            self.full_image.copy().crop((5 * 64, 20 * 64), TILE))

        for i in reversed(list(range(0, 6))):
            self.caer.append(
                self.full_image.copy().crop((i * 64, 20 * 64), TILE))

        self.quieto = self.northq

        self.set_quieto()
        self.scale = 2

    def frenar(self):
        self.stop_all_animations()
        self.set_quieto()

    def set_quieto(self):
        self.estado = "quieto"
        self.image = self.quieto

    def set_mirame(self):
        self.estado = "mirando"
        self.image = self.southq

    def set_caer(self):
        self.stop_all_animations()
        z = spyral.Animation("image", spyral.easing.Iterate(self.caer, 1), 5)
        self.animate(z)

    def set_deambular(self):
        if self.estado in ["caminando"]:
            self.stop_all_animations()

        tiempo = 16

        frames = self.east + self.west
        frames = collections.deque(frames)
        frames.rotate(-4)

        # Calculamos el tiempo para obtener una velocidad constante
        a = spyral.Animation("image",
            spyral.easing.Iterate(frames), duration=tiempo, loop=True)
        b = spyral.Animation("x", spyral.easing.Sine(100), shift=self.scene.width/2, duration=tiempo, loop=True)

        c = a & b
        c.property = "deambular"
        self.estado = "caminando"
        try:
            self.animate(c)
        except ValueError:
            pass


    def set_caminar_x(self, x, disparar=False):
        if self.estado in ["caminando"]:
            self.stop_all_animations()

        # Calculamos el tiempo para obtener una velocidad constante
        distancia = self.pos.distance((x, self.y))
        tiempo = distancia / self.velocidad

        if self.x < x:
            direccion = self.east
        else:
            direccion = self.west
        a = spyral.Animation("image",
            spyral.easing.Iterate(direccion, tiempo), tiempo)
        b = spyral.Animation("x", spyral.easing.Linear(self.x, x), tiempo)
        d = spyral.Animation("image",
            spyral.easing.Iterate([self.quieto], 0.1), 0.1)
        c = a & b
        c = c + d
        if disparar:
            z = spyral.Animation("image",
                spyral.easing.Iterate(self.fire, 1), 1)
            c = c + z
        c.property = "traslado"
        try:
            self.animate(c)
        except ZeroDivisionError:
            print "ZERODIVISIONERROR!!!!"
            print "self.x",self.x
            print "x",x
            print "tiempo", tiempo
            print "duracion", duracion

        self.estado = "caminando"
        return tiempo

    def set_caminar_y(self, y, disparar=False):
        if self.estado in ["caminando"]:
            self.stop_all_animations()

        # Calculamos el tiempo para obtener una velocidad constante
        distancia = self.pos.distance((y, self.x))
        tiempo = distancia / self.velocidad

        if self.y < y:
            direccion = self.south
            self.quieto = self.southq
        else:
            direccion = self.north
            self.quieto = self.northq

        a = spyral.Animation("image",
            spyral.easing.Iterate(direccion, tiempo), tiempo)
        b = spyral.Animation("y", spyral.easing.Linear(self.y, y), tiempo)
        d = spyral.Animation("image",
            spyral.easing.Iterate([self.quieto], 0.1), 0.1)
        c = a & b
        c = c + d

        if disparar:
            z = spyral.Animation("image",
                spyral.easing.Iterate(self.fire, 1), 1)
            c = c + z
        c.property = "traslado"
        self.animate(c)
        self.estado = "caminando"
        return tiempo


class Dialogo(spyral.Sprite):

    def __init__(self, scene, texto, callback):
        spyral.Sprite.__init__(self, scene)

        self.anchor = 'center'
        self.pos = spyral.Vec2D(scene.size) / 2
        self.margen = 5
        self.layer = "primer"

        self.image = spyral.Image(filename=gamedir("images/Menu_1.png"))
        #self.image.draw_rect(color=(128,128,128),
        #        position=(0,0), size=(self.height,self.width))

        font_path = gamedir("../fonts/DejaVuSans.ttf")
        self.font = spyral.Font(font_path, 28, (0, 0, 0))
        self.line_height = self.font.linesize

        nueva = self.set_text(texto)
        self.image.draw_image(nueva,
            position=(self.margen / 2, -17), anchor="midleft")

        spyral.event.register("input.mouse.down.left", callback)
        spyral.event.register("input.keyboard.down.return", self.goplay)
        spyral.event.register("input.keyboard.down.y", self.goplay)

    def goplay(self):
        spyral.director.replace(Escena(self.scene.topic))
        spyral.director.run(sugar=True)

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


class Texto(spyral.Sprite):

    def __init__(self, scene, texto):
        spyral.Sprite.__init__(self, scene)

        self.anchor = 'center'
        self.pos = spyral.Vec2D(scene.size) / 2
        self.margen = 5
        self.layer = "primer"

        self.image = spyral.Image(filename=gamedir("images/Menu_2.png"))
        #self.image.draw_rect(color=(128,128,128),
        #        position=(0,0), size=(self.height,self.width))

        font_path = gamedir("../fonts/DejaVuSans.ttf")
        self.font = spyral.Font(font_path, 24, (0, 0, 0))
        self.line_height = self.font.linesize

        nueva = self.set_text(texto)
        self.image.draw_image(nueva,
            position=(self.margen / 2, 0), anchor="midleft")

        self.scale = 1.3

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

        return bloque


class Camino(spyral.Sprite):

    def __init__(self, scene):

        spyral.Sprite.__init__(self, scene)

        self.anchor = "midbottom"
        self.layer = "abajo2"
        self.image = spyral.Image(filename=gamedir("images/entrada.png"))
        self.pos = spyral.Vec2D(self.scene.size)/2

    def temblar(self):
        m = spyral.Animation("x", spyral.easing.Iterate(
            [-3, 0, 3], 5), 2, shift=self.x)
        self.animate(m)


class Intro(spyral.Scene):

    MUTE = False
    gameview = False

    def __init__(self, topic=topic_dir, gameview=False):
        spyral.Scene.__init__(self, SIZE)

        reset_vocabulario()

        global topic_dir
        topic_dir = topic
        self.topic = topic

        self.layers = ["abajo", "abajo2", "arriba", "primer"]

        img = spyral.Image(filename=gamedir(
            "images/Peru_Machu_Picchu_Sunrise.jpg")).scale(self.scene.size)
        self.background = img

        self.titulo = Title(self)
        self.camino = Camino(self)
        self.camino.y = 0
        self.terraza = Terraza(self)

        spyral.event.register("system.quit", spyral.director.pop, scene=self)
        spyral.event.register("input.keyboard.down.space", self.goplay, scene=self)
        spyral.event.register("director.scene.enter", self.intro0, scene=self)

        pygame.mixer.music.load(gamedir('musica/alienblues.ogg'))
        pygame.mixer.music.play(-1)

        if gameview:
            Intro.gameview = gameview

    def mute(self, value):
        if value==True:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.play()

        Intro.MUTE = value

    def goplay(self):
        spyral.director.replace(Escena(self.topic))
        spyral.director.run(sugar=True)

    def intro0(self):
        a = spyral.Animation("y", spyral.easing.Linear(self.camino.y, self.scene.height), duration=4)
        self.camino.animate(a)

        spyral.event.register("Camino.y.animation.end", self.intro1, scene=self)

    def intro1(self):
        spyral.event.unregister("Camino.y.animation.end", self.intro1)
        self.j = Jugador(self)
        self.j.x = self.width / 2
        self.j.y = -64
        self.j.set_mirame()

        self.mensaje = Texto(self, "Hello children of Peru")
        self.mensaje.y = 95
        self.mensaje.x = 115

        self.j.set_caminar_y(self.scene.height/2)
        spyral.event.register("Jugador.traslado.animation.end", self.intro2, scene=self)

    def intro2(self):
        spyral.event.unregister("Jugador.traslado.animation.end", self.intro2)
        self.mensaje.kill()
        self.scene.titulo.kill()
        self.mensaje = Texto(self, "There is no time to explain")
        self.mensaje.y = self.height / 2 - 70

        self.d = DelayAnimation(3)
        self.d.property="demora"
        self.j.animate(self.d)

        spyral.event.register("Jugador.demora.animation.end", self.intro3, scene=self)

    def intro3(self):
        spyral.event.unregister("Jugador.demora.animation.end", self.intro3)
        self.j.set_caminar_y(self.scene.height-self.j.height)
        spyral.event.register("Jugador.traslado.animation.end", self.intro4, scene=self)

    def intro4(self):
        spyral.event.unregister("Jugador.traslado.animation.end", self.intro4)
        self.mensaje.kill()
        self.mensaje = Texto(self, "An asteroid is coming!")
        self.mensaje.y = self.height - 200

        self.d = DelayAnimation(3)
        self.d.property="demora"
        self.j.animate(self.d)

        spyral.event.register("Jugador.demora.animation.end", self.intro5, scene=self)

    def intro5(self):
        spyral.event.unregister("Jugador.demora.animation.end", self.intro5)
        a = spyral.Animation("y", spyral.easing.Linear(self.scene.height, 0), duration=4)
        self.camino.animate(a)

        img = spyral.Image(filename=gamedir(
        "images/Peru_Machu_Picchu_Sunrise.jpg")).scale(self.scene.size)

        self.v = Visualizador(self)
        self.v.reset("Press space to begin.", loop=True)

        n = pygame.Surface.convert_alpha(img._surf)
        # red at 50%
        n.fill((255, 0, 0, 127))
        img._surf.blit(n, (0, 0))

        self.scene.background = img

        self.j.set_deambular()


class Title(spyral.Sprite):

    def __init__(self, scene):
        spyral.Sprite.__init__(self, scene)

        self.image = spyral.Image(gamedir("images/juego1_titulo.png"))
        self.layer = "primer"
        self.pos = (scene.width / 2, scene.height / 2)
        self.anchor = "center"

def main():
    spyral.director.push(Intro())

if __name__ == "__main__":
    spyral.director.init(SIZE, fullscreen=False)
    main()
    spyral.director.run()
