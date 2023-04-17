from time import sleep
from tests.common import MakefileTestCase, slow_test
from tests.test_dependencies import touch

class TestPyprojectToml(MakefileTestCase):

    def test_empty(self):
        '''
        Empty value for PYPROJECT_TOML should result in ignoring the file
        even when it exists
        '''
        sample_makefile = '\n'.join((
            'PYPROJECT_TOML=',
            'include {{ Makefile.venv }}',
        ))
        makefile = self.copy(content=sample_makefile, makefile=True)
        self.copy('pyproject.toml')
        make = self.make(makefile=makefile, dry_run=True)
        self.assertNotIn('/pip install', make.stdout)

    def test_nonexistent(self):
        '''
        Nonexistent path for PYPROJECT_TOML should result in error
        because non-default values are treated as hard dependencies
        and are expected to be made via Makefile recipe
        '''
        sample_makefile = '\n'.join((
            'PYPROJECT_TOML=nonexistent.toml',
            'include {{ Makefile.venv }}',
        ))
        makefile = self.copy(content=sample_makefile, makefile=True)
        self.copy('pyproject.toml')
        make = self.make(makefile=makefile, dry_run=True, returncode=None)
        self.assertEqual(make.returncode, 2)
        self.assertIn('no rule to make target', make.stderr.lower())
        self.assertNotIn('/pip install', make.stdout)

    @slow_test
    def test_multiple(self):
        '''
        Check that multiple pyproject.toml files are supported
        '''
        files = [
            'pyproject.toml',
            'hello.py',
        ]
        for dest_dir in ['one', 'two']:
            for filename in files:
                self.copy(filename, dest_dir=dest_dir)
        translate = {
            'name = "hello"': 'name = "hello2"',
            'pyfiglet': 'console'
        }
        with open('tests/data/pyproject.toml') as f:
            setup_content = f.read()
        for old, new in translate.items():
            setup_content = setup_content.replace(old, new)
        second_setup_py = self.copy(  # avoid package name collision
            'pyproject.toml',
            content=setup_content,
            dest_dir='two',
        )
        makefile_content = '\n'.join((
            'PYPROJECT_TOML=one/pyproject.toml two/pyproject.toml',
            'include {{ Makefile.venv }}',
        ))
        makefile = self.copy(content=makefile_content, makefile=True)

        # First invocation creates venv
        make = self.make('venv', makefile=makefile)
        self.assertIn('pip install -e', make.stdout)
        for package in ['pyfiglet', 'console']:
            self.assertIn('Collecting %s' % package, make.stdout)

        # Second should be a noop
        make = self.make('venv', makefile=makefile)
        self.assertNotIn('pip install', make.stdout)

        # Touching one of setup.cfg files should trigger venv update
        sleep(1)  # macOS mtime seems to happen in whole seconds
        touch(second_setup_py)
        make = self.make('venv', makefile=makefile, dry_run=True)
        self.assertIn('pip install -e', make.stdout)
