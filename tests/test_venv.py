import os
import sys
from subprocess import run, PIPE
from tempfile import TemporaryDirectory
from unittest import TestCase, skipIf


slow_test = skipIf(
    os.environ.get('SKIP_SLOW_TESTS', False),
    'slow test'
)


class MakefileTestCase(TestCase):
    '''Base class for Makefile.venv tests'''

    MAKEFILE = 'Makefile.venv'
    MAKE = 'make'
    TIMEOUT = 60 # seconds

    def make(self, *args, debug=False, dry_run=False):
        '''Execute Makefile.venv with GNU Make in temporary directory'''
        command = [self.MAKE, '-C', self.tmpdir.name, '-f', os.path.abspath(self.MAKEFILE)]
        if debug:
            command.append('-drR')
        if dry_run:
            command.append('-n')
        command.extend(args)
        return run(command, stdout=PIPE, stderr=PIPE, timeout=self.TIMEOUT)

    def check_returncode(self, process, returncode=0):
        '''Check subprocess return code in automated tests'''
        self.assertEqual(
            process.returncode,
            returncode,
            msg='\n'.join(
                part for part in (
                    '\nstdout:',
                    process.stdout.decode(sys.stdout.encoding),
                    'stderr:',
                    process.stderr.decode(sys.stdout.encoding),
                )
                if part.strip()
            )
        )

    def setUp(self):
        self.tmpdir = TemporaryDirectory(prefix='Makefile.venv_test_')
        for variable in ('WORKDIR', 'VENVDIR', 'REQUIREMENTS_TXT'):
            if variable in os.environ:  # Clear environment variables for tests
                os.environ.pop(variable)

    def tearDown(self):
        self.tmpdir.cleanup()
        del self.tmpdir


class TestInvocation(MakefileTestCase):

    def test_gnu_make(self):
        make = self.make('--version')
        self.check_returncode(make)
        self.assertTrue('gnu make' in make.stdout.decode(sys.stdout.encoding).lower())

    @slow_test
    def test_creating(self):
        make = self.make('venv')
        self.check_returncode(make)
        self.assertTrue(os.path.isdir(os.path.join(self.tmpdir.name, '.venv')))
