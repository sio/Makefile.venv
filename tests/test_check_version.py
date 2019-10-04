import re
from unittest import TestCase
from subprocess import run, PIPE


class TestVersion(TestCase):

    pattern = re.compile(r'\b(v\d{4}\.\d{2}\.\d{2})\b', re.IGNORECASE)
    readme = 'README.md'
    makefile = 'Makefile.venv'

    def get_version(self, filename):
        with open(filename) as f:
            match = self.pattern.search(f.read())
        if not match:
            raise ValueError('version pattern not found in {}'.format(filename))
        return match.group(1)

    def test_version(self):
        '''Check that versions in README and in Makefile.venv match'''
        self.assertEqual(
                self.get_version(self.readme),
                self.get_version(self.makefile),
        )

    def test_git_tag(self):
        '''Check that git tag contains valid version information'''
        cmd = 'git log -1 --format=%D --'.split() + [self.makefile]
        process = run(cmd, stdout=PIPE)
        git_log = process.stdout.decode()
        match = self.pattern.search(git_log)
        if not match:
            raise ValueError('version pattern not found in {!r}'.format(' '.join(cmd)))
        git_version = match.group(1)
        self.assertEqual(git_version, self.get_version(self.makefile))
