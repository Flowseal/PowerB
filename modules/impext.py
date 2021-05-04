import glob, imp
from os.path import join, basename, splitext

def do(dir):
    return dict( _load(path) for path in glob.glob(join(dir,'[!_]*.py')) if not basename(path).startswith('demo') )

def _load(path):
    name, ext = splitext(basename(path))
    return name, imp.load_source(name, path)