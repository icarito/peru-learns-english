### CISC374 Test Launcher

__author__ = "Robert Deaton"
__version__ = "0.3"
__license__ = "MIT"

import sys
sys.path.insert(1, "../../Lib/")

import gettext
import sys
import os
#import libraries
#libraries.setup_path()
from optparse import OptionParser
import spyral
try:
    import json
except ImportError:
    import simplejson as json

def format_columns(message, data):
    first_width = max([len(x[0]) for x in data])
    second_width = max([len(x[1]) for x in data])
    total_width = first_width + second_width + 8

    # calculate a format string for the output lines
    format_str = "%%-%ds        %%-%ds" % (first_width, second_width)

    print message
    print "=" * max(total_width, len(message))
    for x in data:
        print format_str % x

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-f", "--fullscreen", action="store_true", dest="fullscreen", default=False, help="Run in fullscreen mode. Default is windowed mode.")
    parser.add_option("-r", "--resolution", type="int", nargs=2, dest="res", help="Specify the resolution. Default is 0 0, which uses the screen's resolution.", metavar="WIDTH HEIGHT", default=(0,0))
    parser.add_option("-s", "--fps", type="int", dest="fps", help="Specify the fps cap. Default is 30", metavar="FPS", default=30)
    parser.add_option("-l", "--locale", type="str", dest="locale", help="Specify the locale to launch the game with. Default uses the system's locale settings.", default="default")
    parser.add_option("-t", "--list-translations", action="store_true", dest="list", default=False, help="List the available translations.")
    parser.add_option("-p", "--profile", action="store_true", dest="profile", default=False,help="Enable profiling via cProfile. Individual profiles for each scene will be output. If graphviz is installed on your system, callgrind style output images will be created.")
    parser.add_option("-o", "--output", type="string", dest="profile_output", default=None, help="Specify an output directory for profiling data. By default, output will be placed in profiles/%d-%m-%Y %H-%M-%S/")
    parser.add_option("-g", "--graphviz", action="store_true", dest="graphviz", default=False, help="Use graphviz if available to generate png callgraphs if profiling is enabled.")
    (options, args) = parser.parse_args()

    languages = None
    if os.path.exists('./locale'):
        languages = [file for file in os.listdir('./locale') if os.path.isdir('./locale/%s' % file) and os.path.isfile('./locale/%s/activity.linfo' % file)]

    if options.list:
        if languages:
            print 'Available translations: %s' % ', '.join(languages)
        else:
            print 'No available translations'
        sys.exit()
        
    if options.graphviz and not options.profile:
        print 'Graphiz option '
    
    if options.locale != 'default':
        lang = gettext.translation("org.laptop.community.cisc374.mathadder", "./locale", languages=[options.locale])
        lang.install()
    else:
        gettext.install("org.laptop.community.cisc374.mathadder", "./locale")
 
    if options.profile_output is not None:
        output_dir = options.profile_output
    elif options.profile:
        import time
        d = time.strftime("%d-%m-%Y %H-%M-%S")
        output_dir = os.path.join('profiles', d)
            
    def launch():
        import runme
        runme.main()
    
    ## Let's output some friendly information at the top
    output = [
        ("launcher version:", __version__),
        ("spyral version:", spyral.__version__),
        ("resolution:", "Autodetect" if options.res == (0,0) else str(options.res[0]) + " x " + str(options.res[1])),
        ("fullscreen:", "True" if options.fullscreen else "False"),
        ("Max FPS:", str(options.fps)),
        ("Locale:", options.locale),
        ("Profiling:", "Enabled" if options.profile else "Disabled")
        ]
    if options.profile:
        output.append(("Profile output:", output_dir))
    format_columns("CISC374 Launcher", output)
    
    if not options.profile:
        try:
            spyral.director.init(options.res, fullscreen = options.fullscreen, max_fps = options.fps)
            launch()
            spyral.director.run()
        except KeyboardInterrupt:
            spyral.quit()
        spyral.quit()
        sys.exit()

    # We now handle if profiling is enabled.
    import cProfile
    import envoy
    from collections import defaultdict
    scenes = defaultdict(lambda: 0)
    files = []
    
    try:
        os.mkdir(output_dir)
    except OSError:
        pass

    spyral.director.init(options.res, fullscreen = options.fullscreen, max_fps = options.fps)
    launch()

    def run():
        spyral.director.run(profiling = True)

    while spyral.director.get_scene():
        scene = spyral.director.get_scene().__class__.__name__
        scenes[scene] += 1
        output = '%s/%s-%d' % (output_dir, scene, scenes[scene])
        try:
            cProfile.run('run()', '%s.pstats' % (output,))
        except KeyboardInterrupt:
            spyral.quit()
        files.append(output)
    spyral.quit()
        
    try:
        for file in files:
            r = envoy.run('python libraries/gprof2dot.py -f pstats "%s.pstats" | dot -Tpng -o "%s.png"' % (file, file))
            
    except Exception:
        print 'Could not generate image outputs from profiling. Is graphviz installed?'
        sys.exit()
