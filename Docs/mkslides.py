from landslide import generator
from glob import glob

g = generator.Generator("intro.md", relative=True, theme="theme")
jss = glob("theme/js/*.js")
css = glob("theme/css/*.css")
css.remove("theme/css/screen.css")
css.remove("theme/css/print.css")
g.add_user_js(jss)
g.add_user_css(css)
print g.render().encode("utf-8")
