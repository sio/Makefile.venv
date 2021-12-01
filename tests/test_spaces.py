from tests.common import MakefileTestCase, slow_test


class TestSpacesInPath(MakefileTestCase):

    TMPPREFIX = 'Makefile.venv test with spaces '

    @slow_test
    def test_spaces(self):
        '''Check that spaces in project path do not break anything'''
        for filename in {'hello.py', 'requirements.txt'}:
            self.copy(filename)
        makefile = self.copy('dependencies.mk', makefile=True)

        make = self.make('hello', makefile=makefile)
        self.assertIn('Collecting pyfiglet', make.stdout)
