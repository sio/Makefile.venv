import os
from pathlib import Path
from time import sleep

from tests.common import MakefileTestCase, slow_test


def touch(filepath):
    Path(filepath).touch()


class TestDependencies(MakefileTestCase):

    @slow_test
    def test_requirements_txt(self):
        '''Check that requirements.txt is being processed correctly'''
        self.common_dependency_checks('requirements.txt')

    @slow_test
    def test_setup_py(self):
        '''Check that setup.py is being processed correctly'''
        self.common_dependency_checks('setup.py')

    def common_dependency_checks(self, dependency_list):
        '''Generic unit test for setup.py and requirements.txt'''
        dependencies = self.copy_data(dependency_list)
        hello = self.copy_data('hello.py')
        makefile = self.copy_data('dependencies.mk', makefile=True)

        # Create virtual environment with specified dependencies
        make = self.make('hello', makefile=makefile)
        for line in make.stdout.split('\n'):
            if line.strip() == 'hello':
                break
        else:
            raise AssertionError("'hello' not found in make stdout:\n{}".format(make.stdout))
        self.assertIn('Collecting pyfiglet', make.stdout)

        # Second invocation must not trigger dependencies installation
        second = self.make('hello', makefile=makefile)
        self.assertNotIn('Collecting pyfiglet', second.stdout)

        # When dependencies list was modified, venv has to be updated
        sleep(1)  # Ensure that timestamps differ significantly
        touch(dependencies)
        third = self.make('hello', makefile=makefile, dry_run=True)
        self.assertIn('--upgrade pip', third.stdout)
        self.assertTrue(any('pip install %s' % x in third.stdout for x in {'-r', '-e'}))

    @slow_test
    def test_requirements_txt_multiple(self):
        '''Check that multiple requirements.txt files are supported'''
        data = ['requirements.txt', 'requirements-extra.txt', 'hello.py']
        for name in data:
            self.copy_data(name)
        makefile = self.copy_data('dependencies.mk', makefile=True)

        os.environ['REQUIREMENTS_TXT'] = 'requirements.txt requirements-extra.txt'
        self.make('hello', makefile=makefile)
        freeze = self.make('freeze', makefile=makefile)
        for package in ['pyfiglet', 'console']:
            with self.subTest(package=package):
                self.assertIn('%s==' % package, freeze.stdout)
        for word in ['Collecting', 'installing', 'installed', 'cache']:
            with self.subTest(word=word):
                self.assertNotIn(word.lower(), freeze.stdout.lower())

    @slow_test
    def test_one_off(self):
        '''Check that one-off requirements are supported'''
        makefile = self.copy_data('dependencies.mk', makefile=True)
        make = self.make('oneoff', makefile=makefile)

        pyflakes_words = ['pyflakes', '--version', '--help']
        venv_words = ['Collecting pyflakes', 'Installing', 'Successfully']
        for word in pyflakes_words + venv_words:
            with self.subTest(word=word):
                self.assertIn(word, make.stdout)

        # Second invocation must not rebuild venv
        repeat = self.make('oneoff', makefile=makefile)
        for word in pyflakes_words:
            with self.subTest(word=word):
                self.assertIn(word, repeat.stdout)
        for word in venv_words:
            with self.subTest(word=word):
                self.assertNotIn(word, repeat.stdout)
