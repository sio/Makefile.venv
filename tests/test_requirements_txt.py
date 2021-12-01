'''
Check edge cases for REQUIREMENTS_TXT value

Mentioned in:
    https://github.com/sio/Makefile.venv/issues/14#issuecomment-982578931
'''

from tests.common import MakefileTestCase


class TestRequirementsTxt(MakefileTestCase):

    def test_requirements_txt_empty(self):
        '''
        Empty value for REQUIREMENTS_TXT should result in ignoring
        requirements.txt even when it exists
        '''
        sample_makefile = '\n'.join((
            'REQUIREMENTS_TXT=',
            'include {{ Makefile.venv }}',
        ))
        makefile = self.copy(content=sample_makefile, makefile=True)
        self.copy('requirements.txt')
        make = self.make(makefile=makefile, dry_run=True)
        self.assertNotIn('/pip install', make.stdout)

    def test_requirements_txt_nonexistent(self):
        '''
        Nonexistent path for REQUIREMENTS_TXT should result in error because
        non-default values are treated as hard dependencies and are expected to
        be made via Makefile recipe
        '''
        sample_makefile = '\n'.join((
            'REQUIREMENTS_TXT=nonexistent.txt',
            'include {{ Makefile.venv }}',
        ))
        makefile = self.copy(content=sample_makefile, makefile=True)
        self.copy('requirements.txt')
        make = self.make(makefile=makefile, dry_run=True, returncode=None)
        self.assertEqual(make.returncode, 2)
        self.assertIn('no rule to make target', make.stderr.lower())
        self.assertNotIn('/pip install', make.stdout)
