'''
Test Makefile.venv invocation
'''


import os.path
import sys
from tests.common import MakefileTestCase, slow_test


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
