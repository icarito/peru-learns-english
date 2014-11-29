#!/usr/bin/env python
# -*- coding: utf-8 -*-

import commands
import gtk
from gtk import gdk

COLORES = {
    "window": gdk.color_parse("#ffffff"),
    "toolbar": gdk.color_parse("#778899"),
    "text": gdk.color_parse("#000000"),
    }


def describe_archivo(archivo):
    datos = commands.getoutput('file -ik %s%s%s' % ("\"", archivo, "\""))
    retorno = ""
    for dat in datos.split(":")[1:]:
        retorno += " %s" % (dat)
    return retorno
