'''
Python entrypoint that returns absolute path to Makefile.venv
'''

try:
    from importlib.resources import as_file, files
    def path():
        with as_file(files(__name__).joinpath('Makefile.venv')) as f:
            return str(f.resolve())
except (ImportError, ModuleNotFoundError) as e:
    import pkg_resources
    def path():
        return pkg_resources.resource_filename(__name__, 'Makefile.venv')


def cli():
    '''Print Makefile.venv path to stdout'''
    print(path())
