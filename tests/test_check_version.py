import re
from unittest import TestCase


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
