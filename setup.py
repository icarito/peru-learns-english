#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup
from glob import glob

setup(
	name = "Peru_Learns_English",
	version = "0.1",
	author = "SomosAzucar",
	author_email = "todos@somosazucar.org",
	url = "",
	license = "GPL3",

	scripts = ["peru_learns_english_run", "peru_learns_english_uninstall"],

	#py_modules = ["enfoli"],

        data_files = [
		("/usr/share/applications/", ["Peru_Learns_English.desktop"]),

                    ("",[
			"enfoli.py",
			"peru_learns_english_run",
			"peru_learns_english_uninstall",
                        #"postinstall",
			"GameView.py",
			"Toolbar.py",
			"setup.py",
			"ApiProyecto.py",
			"VideoView.py",
			"FlashCardView.py",
			"Peru_Learns_English.desktop",
			"InstructionsView.py",
			"mksetup.py",
			"Globales.py",
			"CreditsView.py"]),

		("Imagenes/",[
			"Imagenes/play_practice.png",
			"Imagenes/juego1.png",
			"Imagenes/flashcards.png",
			"Imagenes/flashcards_disabled.png",
			"Imagenes/ple_disabled.png",
			"Imagenes/ple.png",
			"Imagenes/play_practice_disabled.png"]),

		("Games/",[
			"Games/__init__.py"]),

		("Topics/Topic_6/Imagenes/",[
			"Topics/Topic_6/Imagenes/truck.png",
			"Topics/Topic_6/Imagenes/boat.png",
			"Topics/Topic_6/Imagenes/bike.png",
			"Topics/Topic_6/Imagenes/bus.png",
			"Topics/Topic_6/Imagenes/motorcycle.png"]),

		("Iconos/",[
			"Iconos/icono.svg"]),

		("JAMediaImagenes/",[
			"JAMediaImagenes/__init__.py",
			"JAMediaImagenes/ImagePlayer.py"]),

		("VideoPlayer/Iconos/",[
			"VideoPlayer/Iconos/stop.svg",
			"VideoPlayer/Iconos/pausa.svg",
			"VideoPlayer/Iconos/controlslicer.svg",
			"VideoPlayer/Iconos/play.svg"]),

		("Lib/spyral/resources/fonts/",[
			"Lib/spyral/resources/fonts/AUTHORS",
			"Lib/spyral/resources/fonts/BUGS",
			"Lib/spyral/resources/fonts/README"]),

		("VideoPlayer/JAMediaReproductor/",[
			"VideoPlayer/JAMediaReproductor/__init__.py",
			"VideoPlayer/JAMediaReproductor/JAMediaReproductor.py",
			"VideoPlayer/JAMediaReproductor/JAMediaBins.py"]),

		("Lib/spyral/resources/images/",[
			"Lib/spyral/resources/images/button.down.focused.png",
			"Lib/spyral/resources/images/check.down.png",
			"Lib/spyral/resources/images/check.up.hovered.png",
			"Lib/spyral/resources/images/button.down.png",
			"Lib/spyral/resources/images/input.focused.png",
			"Lib/spyral/resources/images/input.unfocused.png",
			"Lib/spyral/resources/images/check.down.hovered.png",
			"Lib/spyral/resources/images/radio.on.png",
			"Lib/spyral/resources/images/Thumbs.db",
			"Lib/spyral/resources/images/radio.off.hovered.png",
			"Lib/spyral/resources/images/button.up.focused.png",
			"Lib/spyral/resources/images/radio.off.png",
			"Lib/spyral/resources/images/button.down.hovered.png",
			"Lib/spyral/resources/images/button.up.png",
			"Lib/spyral/resources/images/radio.on.hovered.png",
			"Lib/spyral/resources/images/check.up.png",
			"Lib/spyral/resources/images/button.up.hovered.png",
			"Lib/spyral/resources/images/README"]),

		("Topics/Topic_3/Imagenes/",[
			"Topics/Topic_3/Imagenes/skate.png",
			"Topics/Topic_3/Imagenes/athlete.png",
			"Topics/Topic_3/Imagenes/stretch.png",
			"Topics/Topic_3/Imagenes/climb.png",
			"Topics/Topic_3/Imagenes/judo.png",
			"Topics/Topic_3/Imagenes/jump.png"]),

		("Lib/sugargame2/",[
			"Lib/sugargame2/__init__.py",
			"Lib/sugargame2/event.py",
			"Lib/sugargame2/canvas.py"]),

		("Lib/spyral/",[
			"Lib/spyral/_style.py",
			"Lib/spyral/memoize.py",
			"Lib/spyral/image.py",
			"Lib/spyral/__init__.py",
			"Lib/spyral/rect.py",
			"Lib/spyral/dev.py",
			"Lib/spyral/sprite.py",
			"Lib/spyral/mouse.py",
			"Lib/spyral/event.py",
			"Lib/spyral/view.py",
			"Lib/spyral/form.py",
			"Lib/spyral/keyboard.py",
			"Lib/spyral/animation.py",
			"Lib/spyral/compat.py",
			"Lib/spyral/core.py",
			"Lib/spyral/widgets.py",
			"Lib/spyral/font.py",
			"Lib/spyral/scene.py",
			"Lib/spyral/director.py",
			"Lib/spyral/debug.py",
			"Lib/spyral/layertree.py",
			"Lib/spyral/vector.py",
			"Lib/spyral/weakmethod.py",
			"Lib/spyral/clock.py",
			"Lib/spyral/exceptions.py",
			"Lib/spyral/util.py",
			"Lib/spyral/easing.py",
			"Lib/spyral/actor.py"]),

		("Topics/Topic_2/Imagenes/",[
			"Topics/Topic_2/Imagenes/feet.png",
			"Topics/Topic_2/Imagenes/nose.png",
			"Topics/Topic_2/Imagenes/hair.png",
			"Topics/Topic_2/Imagenes/finger.png",
			"Topics/Topic_2/Imagenes/toe.png",
			"Topics/Topic_2/Imagenes/leg.png",
			"Topics/Topic_2/Imagenes/knee.png"]),

		("Topics/Topic_5/Imagenes/",[
			"Topics/Topic_5/Imagenes/cat.png",
			"Topics/Topic_5/Imagenes/llama.png",
			"Topics/Topic_5/Imagenes/dove.png",
			"Topics/Topic_5/Imagenes/dolphin.png",
			"Topics/Topic_5/Imagenes/left.png",
			"Topics/Topic_5/Imagenes/dog.png",
			"Topics/Topic_5/Imagenes/right.png",
			"Topics/Topic_5/Imagenes/crocodile.png",
			"Topics/Topic_5/Imagenes/crab.png"]),

		("Topics/Topic_4/Imagenes/",[
			"Topics/Topic_4/Imagenes/lake.png",
			"Topics/Topic_4/Imagenes/island.png",
			"Topics/Topic_4/Imagenes/water.png",
			"Topics/Topic_4/Imagenes/shore.png",
			"Topics/Topic_4/Imagenes/shell.png"]),

		("Games/ug1/fonts/",[
			"Games/ug1/fonts/DejaVuSans.ttf"]),

		("VideoPlayer/",[
			"VideoPlayer/__init__.py",
			"VideoPlayer/ProgressPlayer.py",
			"VideoPlayer/PlayerControls.py",
			"VideoPlayer/VideoPlayer.py"]),

		("Topics/Topic_1/Imagenes/",[
			"Topics/Topic_1/Imagenes/angry.png",
			"Topics/Topic_1/Imagenes/surprised.png",
			"Topics/Topic_1/Imagenes/bored.png",
			"Topics/Topic_1/Imagenes/sad.png",
			"Topics/Topic_1/Imagenes/happy.png"]),

		("Topics/Topic_5/",[
			"Topics/Topic_5/topic.ini",
			"Topics/Topic_5/vocabulario.csv",
			"Topics/Topic_5/video.ogv"]),

		("Topics/Topic_4/",[
			"Topics/Topic_4/topic.ini",
			"Topics/Topic_4/vocabulario.csv",
			"Topics/Topic_4/video.ogv"]),

		("Topics/Topic_6/",[
			"Topics/Topic_6/topic.ini",
			"Topics/Topic_6/subtitulos.srt",
			"Topics/Topic_6/vocabulario.csv",
			"Topics/Topic_6/video.ogv"]),

		("Topics/Topic_1/",[
			"Topics/Topic_1/topic.ini",
			"Topics/Topic_1/subtitulos.srt",
			"Topics/Topic_1/vocabulario.csv",
			"Topics/Topic_1/video.ogv"]),

		("Topics/Topic_3/",[
			"Topics/Topic_3/topic.ini",
			"Topics/Topic_3/vocabulario.csv",
			"Topics/Topic_3/video.ogv"]),

		("Topics/Topic_2/",[
			"Topics/Topic_2/topic.ini",
			"Topics/Topic_2/vocabulario.csv",
			"Topics/Topic_2/video.ogv"]),

		("Games/ug1/",[
			"Games/ug1/dev_launcher.py",
			"Games/ug1/__init__.py",
			"Games/ug1/runme_gui.py",
			"Games/ug1/runme.py"]),

		("Games/ug1/images/",[
			"Games/ug1/images/Menu_1.png",
			"Games/ug1/images/explosion.png",
			"Games/ug1/images/terraza.png",
			"Games/ug1/images/user2.png",
			"Games/ug1/images/golden-border.png",
			"Games/ug1/images/terraza.tmx",
			"Games/ug1/images/user.png",
			"Games/ug1/images/Peru_Machu_Picchu_Sunrise.jpg"]),

		("Games/ug1/images/asteroid/",[
			"Games/ug1/images/asteroid/Asteroid-A-10-51.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-57.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-37.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-33.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-00.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-27.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-31.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-59.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-08.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-15.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-13.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-46.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-25.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-12.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-43.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-58.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-26.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-07.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-20.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-40.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-21.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-28.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-32.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-45.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-16.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-38.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-49.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-23.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-01.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-42.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-19.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-48.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-06.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-09.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-54.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-34.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-52.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-39.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-22.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-30.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-44.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-17.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-03.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-02.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-14.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-36.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-04.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-53.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-55.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-47.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-35.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-05.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-29.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-56.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-50.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-18.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-10.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-24.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-11.png",
			"Games/ug1/images/asteroid/Asteroid-A-10-41.png"]),

		("Lib/spyral/resources/",[
			"Lib/spyral/resources/form_defaults.spys",
			"Lib/spyral/resources/style.parsley",
			"Lib/spyral/resources/default_key_mappings.txt",
			"Lib/spyral/resources/theme.cfg"])]
                        )

#import subprocess 
#subprocess.check_output("chmod -R 755 /usr/local/share/Peru_Learns_English", shell=True)
#subprocess.check_output("chmod 755 /usr/share/applications/Peru_Learns_English.desktop", shell=True)
