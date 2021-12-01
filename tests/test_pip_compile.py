'''
Tests for issue #8
https://github.com/sio/Makefile.venv/issues/8

Support for generated requirements.txt files
'''


from tests.common import MakefileTestCase, slow_test


class TestPipCompile(MakefileTestCase):

    @slow_test
    def test_issue8(self):
        '''Check that REQUIREMENTS_TXT can be generated with a Makefile recipe'''
        self.copy('requirements.in')
        makefile = self.copy('pip-compile.mk', makefile=True)

        make = self.make(makefile=makefile)
        for line in [
                'Collecting pyflakes',
                'show this help message and exit',
                'usage: pyflakes',
        ]:
            self.assertIn(line, make.stdout)

        # Second invokation must not need to rebuild venv
        repeat = self.make(makefile=makefile)
        self.assertIn('pyflakes --help', '\n'.join(repeat.stdout.splitlines()[:2]))

