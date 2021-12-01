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
    TIMEOUT = int(os.getenv('TEST_SUBPROCESS_TIMEOUT', 60)) # seconds
    TMPPREFIX = 'Makefile.venv_test_'

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

        env = os.environ.copy()
        env.update(dict(
            LANG='C',
        ))
        process = run(command, stdout=PIPE, stderr=PIPE, timeout=self.TIMEOUT, env=env)
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

    def copy(self, filename=None, content=None, makefile=False, data_dir='tests/data', dest_dir=None):
        '''Copy test data to temporary directory. Return full path to resulting file'''
        if not any([filename, content, makefile]):
            raise ValueError('At least one of parameters must be provided: filename, content, makefile')
        if content is None:
            src = os.path.join(data_dir, filename)
            with open(src) as source:
                content = source.read()
        if makefile and not filename:
            filename = 'Makefile'
        if dest_dir:
            dest_dir = os.path.join(self.tmpdir.name, dest_dir)
            if not os.path.exists(dest_dir):
                os.mkdir(dest_dir)
            dest = os.path.join(dest_dir, filename)
        else:
            dest = os.path.join(self.tmpdir.name, filename)
        if makefile:
            content = content.replace(
                    '{{ Makefile.venv }}',
                    os.path.abspath(self.MAKEFILE)
                )
        with open(dest, 'w') as output:
            output.write(content)
        return dest

    def setUp(self):
        self.tmpdir = TemporaryDirectory(prefix=self.TMPPREFIX)
        for variable in ('WORKDIR', 'VENVDIR', 'REQUIREMENTS_TXT'):
            if variable in os.environ:  # Clear environment variables for tests
                os.environ.pop(variable)

    def tearDown(self):
        self.tmpdir.cleanup()
        del self.tmpdir
