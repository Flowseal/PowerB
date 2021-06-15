import glob, imp
from os.path import join, basename, splitext

modules = {}

def do(dir):
    global modules
    modules.update(dict( _load(path) for path in glob.glob(join(dir,'[!_]*.py')) if not basename(path).startswith('demo') ))
    return modules

def _load(path):
    name, ext = splitext(basename(path))
    return name, imp.load_source(name, path)

def get_modules():
    return modules