'''
Common utilities for testing Makefile.venv
'''


import os
import sys
from shutil import copyfile
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

    def make(self, *args, makefile=None, debug=False, dry_run=False, returncode=0):
        '''Execute Makefile.venv with GNU Make in temporary directory'''
        if makefile is None:
            makefile = self.MAKEFILE
        command = [self.MAKE, '-C', self.tmpdir.name, '-f', os.path.abspath(makefile)]
        if debug:
            command.append('-drR')
        if dry_run:
            command.append('-n')
        command.extend(args)

        process = run(command, stdout=PIPE, stderr=PIPE, timeout=self.TIMEOUT)
        process.stdout, process.stderr = (output.decode(sys.stdout.encoding)
                                          for output in (process.stdout, process.stderr))
        if returncode is not None:
            self.check_returncode(process, returncode)
        return process

    def check_returncode(self, process, returncode=0):
        '''Check subprocess return code in automated tests'''
        self.assertEqual(
            process.returncode,
            returncode,
            msg='\n'.join(
                part for part in (
                    '{} exited with code {} (expected {})'.format(self.MAKE, process.returncode, returncode),
                    '\nstdout:',
                    process.stdout,
                    'stderr:',
                    process.stderr,
                )
                if part.strip()
            )
        )

    def copy_data(self, name, makefile=False, data_dir='tests/data'):
        '''Copy test data to temporary directory. Return full path to resulting file'''
        src = os.path.join(data_dir, name)
        dest = os.path.join(self.tmpdir.name, name)
        if makefile:
            with open(src) as source:
                content = source.read()
            with open(dest, 'w') as output:
                output.write(content.replace(
                    '{{ Makefile.venv }}',
                    os.path.abspath(self.MAKEFILE)
                ))
        else:
            copyfile(src, dest)
        return dest

    def setUp(self):
        self.tmpdir = TemporaryDirectory(prefix='Makefile.venv_test_')
        for variable in ('WORKDIR', 'VENVDIR', 'REQUIREMENTS_TXT'):
            if variable in os.environ:  # Clear environment variables for tests
                os.environ.pop(variable)

    def tearDown(self):
        self.tmpdir.cleanup()
        del self.tmpdir
