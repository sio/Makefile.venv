from time import sleep
from tests.common import MakefileTestCase, slow_test
from tests.test_dependencies import touch

class TestSetupPy(MakefileTestCase):

    def test_setup_py_empty(self):
        '''
        Empty value for SETUP_PY should result in ignoring the file
        even when it exists
        '''
        sample_makefile = '\n'.join((
            'SETUP_PY=',
            'include {{ Makefile.venv }}',
        ))
        makefile = self.copy(content=sample_makefile, makefile=True)
        self.copy('setup.py')
        make = self.make(makefile=makefile, dry_run=True)
        self.assertNotIn('/pip install', make.stdout)

    def test_setup_py_nonexistent(self):
        '''
        Nonexistent path for SETUP_PY should result in error
        because non-default values are treated as hard dependencies
        and are expected to be made via Makefile recipe
        '''
        sample_makefile = '\n'.join((
            'SETUP_PY=nonexistent.py',
            'include {{ Makefile.venv }}',
        ))
        makefile = self.copy(content=sample_makefile, makefile=True)
        self.copy('setup.py')
        make = self.make(makefile=makefile, dry_run=True, returncode=None)
        self.assertEqual(make.returncode, 2)
        self.assertIn('no rule to make target', make.stderr.lower())
        self.assertNotIn('/pip install', make.stdout)

    @slow_test
    def test_setup_py_multiple(self):
        '''
        Check that multiple setup.py files are supported
        '''
        files = [
            'setup.py',
            'hello.py',
        ]
        for dest_dir in ['one', 'two']:
            for filename in files:
                self.copy(filename, dest_dir=dest_dir)
        setup_content = '\n'.join((
            'from setuptools import setup',
            'setup(name="hello2", install_requires=["console",])'
        ))
        second_setup_py = self.copy(  # avoid package name collision
            'setup.py',
            content=setup_content,
            dest_dir='two',
        )
        makefile_content = '\n'.join((
            'SETUP_PY=one/setup.py two/setup.py',
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
