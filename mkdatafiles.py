
import os
import pprint

def get_data_files():
    reales = []
    # hacemos una lista de archivo
    for root, directorio, archivos in os.walk("."):
        if not root.startswith("./.git") and \
            not root.startswith("./Bocetos") and \
            not root.startswith("./Docs"):
            for archivo in archivos:
                if not archivo.endswith("pyc") and \
                        not archivo.startswith(".") and \
                        not archivo.endswith(".in") and \
                        not archivo.endswith("swp") and \
                        not archivo.endswith("py~"):
                    fullpath = os.path.join(root, archivo)
                    fullpath = fullpath[2:]
                    reales.append(fullpath)

    carpetas = {}
    for archivo in sorted(reales):
        directorio = os.path.dirname(archivo)
        if directorio in carpetas.keys():
            carpetas[directorio].append( archivo )
        else:
            carpetas[directorio] = []
            carpetas[directorio].append( archivo )

    new_data_files = []
    for directorio,archivos in carpetas.iteritems():
        if directorio:
            new_data_files.append( (directorio+"/", archivos) )
        else:
            new_data_files.append( ("", archivos) )

    return sorted(new_data_files)
