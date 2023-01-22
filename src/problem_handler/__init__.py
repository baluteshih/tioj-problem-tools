from os.path import join, basename, dirname
from glob import glob
from importlib import import_module

# get all *.py filenames in __file__'s folder that are not __file__.
files = [basename(f)[:-3] for f in glob(join(dirname(__file__), '*.py')) if basename(f) != basename(__file__)]

for func in files:
    import_module('.' + func, 'src.problem_handler')
    globals()[func] = getattr(globals()[func], func) # assign the function func.func to variable func
