import re
from unittest import TestCase, skipIf
from subprocess import run, PIPE


VERSION_PATTERN = re.compile(r'\b(v\d{4}\.\d{2}\.\d{2}(?:-\w+|))\b', re.IGNORECASE)


def get_version(filename, pattern=VERSION_PATTERN):
    with open(filename) as f:
        match = pattern.search(f.read())
    if not match:
        raise ValueError('version pattern not found in {}'.format(filename))
    return match.group(1)


skip_dev = skipIf(
    get_version('Makefile.venv').endswith('-dev'),
    'not a final release'
)


class TestVersion(TestCase):

    pattern = VERSION_PATTERN
    readme = 'README.md'
    makefile = 'Makefile.venv'
    changelog = 'CHANGELOG.md'

    @skip_dev
    def test_version(self):
        '''Check that versions in README and in Makefile.venv match'''
        self.assertEqual(
                get_version(self.readme),
                get_version(self.makefile),
        )

    @skip_dev
    def test_git_tag(self):
        '''Check that git tag contains valid version information'''
        cmd = 'git log -1 --format=%D --'.split() + [self.makefile]
        process = run(cmd, stdout=PIPE)
        git_log = process.stdout.decode()
        match = self.pattern.search(git_log)
        if not match:
            raise ValueError('version pattern not found in {!r}'.format(' '.join(cmd)))
        git_version = match.group(1)
        self.assertEqual(git_version, get_version(self.makefile))

    @skip_dev
    def test_changelog(self):
        '''Check that changelog contains an entry for current version'''
        version = get_version(self.makefile)
        header = '## %s' % version
        with open(self.changelog) as changelog:
            for line in changelog:
                if line.startswith(header):
                    break
            else:
                raise AssertionError('header not found in {changelog}: {header!r}'.format(
                    header=header,
                    changelog=self.changelog,
                ))
