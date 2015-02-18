#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup
from glob import glob

#from datafiles import data_files
import mkdatafiles
data_files = mkdatafiles.get_data_files()
data_files.append(("/usr/share/applications/", ["Peru_Learns_English.desktop"]))

setup(
	name = "Peru_Learns_English",
	version = "1.0",
	author = "SomosAzucar",
	author_email = "laura@somosazucar.org",
	url = "http://pe.sugarlabs.org/ir/Peru%20Learns%20English",
	license = "GPL3",

	scripts = ["peru_learns_english", "peru_learns_english_uninstall"],

        data_files = data_files
	#py_modules = ["enfoli"],

                        )

#import subprocess 
#subprocess.check_output("chmod -R 755 /usr/local/share/Peru_Learns_English", shell=True)
#subprocess.check_output("chmod 755 /usr/share/applications/Peru_Learns_English.desktop", shell=True)
