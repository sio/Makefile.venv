'''
Tests for Python interpreter auto detection
'''

import os
import shutil
import sys
from pathlib import Path
from tests.common import MakefileTestCase, slow_test
from textwrap import dedent


class TestPyAutoDetect(MakefileTestCase):

    MAKE = shutil.which('make')  # use abspath because we mangle the PATH later

    UNIX_WRAPPER = '''\
        #!/bin/sh
        [ "$1" -eq "-3" ] && shift
        {executable} "$@"
        '''
    WINDOWS_WRAPPER = '''\
        if "%1"=="-3" shift
        {executable} %*
        '''

    def __init__(self, *a, **ka):
        super().__init__(*a, **ka)
        if sys.platform == 'win32':
            script = self.WINDOWS_WRAPPER
        else:
            script = self.UNIX_WRAPPER
        self.script = dedent(script)

    def setUp(self):
        '''Tests in this module require PY to be unset'''
        super().setUp()
        os.environ.pop('PY', None)

    def save_script(self, relative_path: str, executable=None):
        '''Save Python interpreter entry point to provided relative path'''
        if executable is None:
            executable = sys.executable
        dest = Path(self.tmpdir.name) / relative_path
        dest.parent.mkdir(parents=True, exist_ok=True)
        with dest.open('w') as out:
            out.write(self.script.format(executable=executable))
        dest.chmod(0o777)

    def test_autodetect_happy_path(self):
        '''Check that 'python3' is used by default'''
        self.save_script('bin/python3')
        self.save_script('bin/py')
        self.save_script('bin/python')
        os.environ['PATH'] = 'bin'
        make = self.make('debug-venv')
        self.assertIn('PY="python3"', make.stdout)

    @slow_test
    def test_autodetect_venv(self):
        '''Check that VENV interpreter is used if exists'''
        create = self.make('venv')
        os.environ['PATH'] = ''
        make = self.make('debug-venv')
        self.assertIn('PY="./.venv/', make.stdout)

    def test_autodetect_py_3(self):
        '''Check that 'py -3' is used when appropriate'''
        self.save_script('bin/py')
        self.save_script('bin/python')
        os.environ['PATH'] = 'bin'
        make = self.make('debug-venv')
        self.assertIn('PY="py -3"', make.stdout)

    def test_autodetect_worst_path(self):
        '''Check that 'python' is used if nothing else is there'''
        self.save_script('bin/python')
        os.environ['PATH'] = 'bin'
        make = self.make('debug-venv')
        self.assertIn('PY="python"', make.stdout)

    def test_autodetect_failure(self):
        '''Check that autodetect failure is raised to the top'''
        os.environ['PATH'] = 'bin'
        make = self.make('debug-venv', returncode=None)
        self.assertEqual(make.returncode, 2)
        self.assertIn('Could not detect Python interpreter', make.stderr)
