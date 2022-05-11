import re
from hashlib import sha256
from unittest import TestCase

from .test_release_version import skip_dev, DEV_VERSION_EXPLAINED


def calculate_checksum(filename):
    with open(filename) as f:
        checksum = sha256()
        for line in f:
            checksum.update(line.encode())
    return checksum.hexdigest()


class TestChecksum(TestCase):
    makefile = 'Makefile.venv'
    readme = 'README.md'
    pattern = re.compile(r'\b[0-9a-f]{64}\b', re.IGNORECASE)

    def read_checksum(self, filename):
        with open(filename) as f:
            match = self.pattern.search(f.read())
        if not match:
            raise ValueError('checksum not found in {}'.format(filename))
        return match.group().lower()

    @skip_dev
    def test_checksum(self):
        '''
        Check that installation instructions contain valid checksum
        (versions ending with -dev suffix are skipped)
        '''
        recorded = self.read_checksum(self.readme)
        calculated = calculate_checksum(self.makefile)
        self.assertEqual(
            recorded,
            calculated,
            '{} but versions in README and in Makefile.venv do not match'.format(DEV_VERSION_EXPLAINED)
        )

