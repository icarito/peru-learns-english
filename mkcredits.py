#!/bin/env python2
# *-* coding:utf-8 *-*

from jinja2 import Template
import markdown as md

template = """
<html>
<head>
<meta charset="utf-8"> 
<style>
body {
    text-align: center;
}
</style>
<link rel='stylesheet' href='markdown1.css'/>
</head>
<body>
{{ credits }}
</body>
</html>
"""


plantilla = Template(template)

creditos = md.markdown(open("CREDITS.md").read())
#creditos.decode("utf-8")

open("Docs/CREDITS.html", "w").write(plantilla.render(credits=creditos))
