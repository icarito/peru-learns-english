#!/bin/env python2
# *-* coding: utf-8 *-*

import sys
sys.path.insert(1, "../../Lib/")

import pygame
import spyral
import os
import random
import csv

SIZE = (700, 700)
TILE = (64, 64)

game_dir = os.path.abspath(os.path.dirname(__file__))


def gamedir(archivo):
    return os.path.join(game_dir, archivo)


font_path = gamedir("fonts/SourceCodePro-Regular.ttf")
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

    def __init__(self, window=None, topic=topic_dir):

        spyral.Scene.__init__(self, SIZE, 20, 20)

        self.layers = ["abajo", "arriba", "primer"]

        img = spyral.Image(filename=gamedir(
            "images/Peru_Machu_Picchu_Sunrise.jpg")).scale(self.scene.size)

        n = pygame.Surface.convert_alpha(img._surf)
        # red at 50%
        n.fill((255, 0, 0, 127))
        img._surf.blit(n, (0, 0))

        self.background = img

        self.j = Jugador(self)
        self.l = Lluvia(self)

        self.tablero = Tablero(self, topic)
        self.terraza = Terraza(self)
        self.v = Visualizador(self)

        spyral.event.register("system.quit", spyral.director.pop)
        #spyral.event.register("director.scene.enter", self.entrar)
        spyral.event.register("director.scene.enter", self.l.llover)

        #spyral.event.register("director.update", self.chequea)

    #No funcionó en la XO Fedora 11
    #def entrar(self):
    #    self.j.set_caminar(self.scene.width / 2)


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
        self.acertadas = ""
        self.layer = "abajo"
        self.ganadas = 0

        self.topic = topic

        font_path = gamedir("fonts/SourceCodePro-Regular.ttf")
        self.font = spyral.Font(font_path, 60, (0, 0, 0))
        self.palabra, self.archivo_img = obtener_palabra(self.topic)
        self.text = self.palabra
        self.image = self.font.render("")

        self.anchor = 'midbottom'

        self.x = self.scene.width / 2
        self.y = self.scene.height - 128

        self.mostrar(self.text, "")

        spyral.event.register("input.keyboard.down.*", self.procesar_tecla)
        spyral.event.register("Tablero.reset.animation.end", self.reset)

    def reset(self):
        self.ganadas = self.ganadas + 1
        self.palabra_anterior = self.palabra
        while self.palabra_anterior == self.palabra:
            self.palabra, self.archivo_img = obtener_palabra(self.topic)
        self.text = self.palabra
        self.acertadas = ""
        self.mostrar(self.palabra, self.acertadas)
        self.scene.l.reset()
        self.scene.v.reset()
        spyral.event.register("input.keyboard.down.*", self.procesar_tecla)

    def set_text(self, text):
        self.image = self.font.render(text)
        self.text = text

    def mostrar(self, frase, acertadas):
        total = 0
        estado = ""
        for letra in frase:
            if letra in acertadas:
                estado = estado + " " + letra
                total = total + 1
            else:
                estado = estado + " _"

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

        self.mostrar(self.palabra, self.acertadas)

        if self.check_completos():
            spyral.event.unregister(
                "input.keyboard.down.*", self.procesar_tecla)
            self.scene.l.stop_all_animations()
            self.scene.l.stop_all_animations()  # spyral, please?
            tiempo = self.scene.j.set_caminar(self.scene.l.x - 20, True)
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

        spyral.event.register("Lluvia.y.animation.end", self.finalizar)
        self.scale = 2

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
        p = spyral.Animation("y",
            spyral.easing.CubicIn(0, self.scene.height - 75),
            duration=2 * len(self.scene.tablero.palabra) + 3)
        self.animate(p)

    def finalizar(self):
        if not self.scene.tablero.check_completos():
            spyral.event.unregister("input.keyboard.down.*",
                self.scene.tablero.procesar_tecla)
            self.scene.tablero.set_text(
                "SCORE: " + str(self.scene.tablero.ganadas * 100))
            self.scene.v.set_text("GAME OVER")
            self.explotar()
            self.scene.terraza.temblar()
            self.scene.j.set_caer()

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

    def reset(self):
        self.stop_all_animations()
        self.text = self.scene.tablero.palabra
        self.palabra_png = self.scene.tablero.archivo_img

        image1 = self.image.copy()
        image1.draw_image(self.render_image(self.palabra_png),
            position=(25, 0), anchor="midleft")
        image2 = self.image.copy()

        nueva = spyral.Image(size=(self.width - self.margen,
            self.height - self.margen)).fill((255, 255, 255))
        image2.draw_image(nueva,
            position=(self.margen / 2, 0), anchor="midleft")
        image2.draw_image(self.render_text("Press a letter !"),
            position=(0, 0), anchor="midleft")
        a = spyral.Animation("image", spyral.easing.Iterate([image1, image2], 6), 6)
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
        lineas = self.wrap(text, caracteres).splitlines()

        altura = len(lineas) * self.line_height
        bloque = spyral.Image(size=(self.width, altura))

        ln = 0
        for linea in lineas:
            bloque.draw_image(image=self.font.render(linea),
                position=(0, ln * self.line_height), anchor="midtop")
            ln = ln + 1
        return bloque

    def wrap(self, text, length):
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


class Jugador(spyral.Sprite):

    def __init__(self, scene):

        spyral.Sprite.__init__(self, scene)

        self.full_image = spyral.Image(filename=gamedir("images/user2.png"))
        self.estado = "nuevo"
        self.y = scene.height - 138
        self.x = scene.width / 2
        self.velocidad = 90
        self.anchor = "midtop"
        self.layer = "arriba"
        self.north = self.full_image.copy().crop((0, 8 * 64), TILE)

        self.east = []
        for i in range(0, 8):
            self.east.append(
                self.full_image.copy().crop((i * 64, 11 * 64), TILE))

        self.west = []
        for i in range(0, 8):
            self.west.append(
                self.full_image.copy().crop((i * 64, 9 * 64), TILE))

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

        self.quieto = self.north

        # saltar
        #spyral.event.register("input.keyboard.down.up", self.set_saltar)
        #spyral.event.register("Jugador.y.animation.end", self.set_quieto)

        # trasladar
        #spyral.event.register("input.keyboard.up.right", self.frenar)
        #spyral.event.register("input.keyboard.up.left", self.frenar)
        #spyral.event.register("input.keyboard.down.right", self.derecha)
        #spyral.event.register("input.keyboard.down.left", self.izquierda)

        self.set_quieto()
        self.scale = 2

    def frenar(self):
        self.stop_all_animations()
        self.set_quieto()

    def derecha(self):
        self.set_caminar(self.scene.width - 32)

    def izquierda(self):
        self.set_caminar(32)

    def set_quieto(self):
        self.estado = "quieto"
        self.image = self.quieto

    def set_caer(self):
        self.stop_all_animations()
        z = spyral.Animation("image", spyral.easing.Iterate(self.caer, 1), 5)
        self.animate(z)

    def set_caminar(self, x, disparar=False):
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
        self.animate(c)
        self.estado = "caminando"
        return tiempo

def main():
    spyral.director.push(Escena())

if __name__ == "__main__":
    spyral.director.init(SIZE, fullscreen=False)
    main()
    spyral.director.run(profiling=True)
