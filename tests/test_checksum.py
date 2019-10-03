import re
from hashlib import sha256
from unittest import TestCase


def get_checksum(filename):
    pass


class TestChecksum(TestCase):
    makefile = 'Makefile.venv'
    readme = 'README.md'
    pattern = re.compile(r'\b[0-9a-f]{64}\b', re.IGNORECASE)

    def test_checksum(self):
        '''Check that installation instructions contain valid checksum'''
        with open(self.readme) as f:
            match = self.pattern.search(f.read())
        if not match:
            raise ValueError('checksum not found in {}'.format(self.readme))
        recorded = match.group()

        with open(self.makefile) as mk:
            checksum = sha256()
            for line in mk:
                checksum.update(line.encode())

        self.assertEqual(
            recorded.lower(),
            checksum.hexdigest(),
        )

