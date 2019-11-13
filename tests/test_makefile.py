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
    def test_creating(self):
        '''Create empty virtual environment'''
        make = self.make('venv')
        self.assertTrue(os.path.isdir(os.path.join(self.tmpdir.name, '.venv')))

        version = self.make('show-venv')
        for line in ('python ', 'pip ', 'venv: '):
            with self.subTest(line=line):
                self.assertIn(line.lower(), version.stdout.lower())

        self.make('clean-venv')
        self.assertFalse(os.path.isdir(os.path.join(self.tmpdir.name, '.venv')))
