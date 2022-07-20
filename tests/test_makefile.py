'''
Test Makefile.venv invocation
'''


import os.path
from tests.common import MakefileTestCase, slow_test


class TestInvocation(MakefileTestCase):

    def test_gnu_make(self):
        '''Only GNU Make is supported'''
        make = self.make('--version')
        self.assertTrue('gnu make' in make.stdout.lower())

    @slow_test
    def test_creating(self, *cli_args):
        '''Create empty virtual environment'''
        make = self.make('debug-venv', 'venv', *cli_args)
        self.assertTrue(
            os.path.isdir(os.path.join(self.tmpdir.name, '.venv')),
            msg='Failed to create virtual environment',
        )

        version = self.make('show-venv', *cli_args)
        for line in ('python ', 'pip ', 'venv: '):
            with self.subTest(line=line):
                self.assertIn(line.lower(), version.stdout.lower())

        self.make('clean-venv', *cli_args)
        self.assertFalse(
            os.path.isdir(os.path.join(self.tmpdir.name, '.venv')),
            msg='Failed to remove virtual environment',
        )

    @slow_test
    def test_no_builtin_variables(self):
        '''
        Check that "make -R" does not break anything

        Thanks to @martinthomson:
            https://github.com/sio/Makefile.venv/issues/19
            https://github.com/sio/Makefile.venv/pull/20
        '''
        return self.test_creating('-R')
