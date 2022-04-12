'''
Python entrypoint that returns absolute path to Makefile.venv
'''


import pkg_resources


def path():
    '''Return a string containing path to Makefile.venv'''
    return pkg_resources.resource_filename(__name__, 'Makefile.venv')


def cli():
    '''Print Makefile.venv path to stdout'''
    print(path())
