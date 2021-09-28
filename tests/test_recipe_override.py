'''
Check that default recipe for $(VENV) can be safely overwritten by user

Some of our users rely upon this unofficial GNU Make feature

Documentation:
    https://www.gnu.org/software/make/manual/html_node/Multiple-Rules.html

Feature in use:
    https://github.com/sio/Makefile.venv/issues/13
    https://github.com/sio/Makefile.venv/pull/10
    https://github.com/sio/bash-complete-partial-path/blob/2be6ef1f1885d3cb1ec2547ae41d78aa66f4ab78/Makefile#L42-L48
'''

from tests.common import MakefileTestCase, slow_test

class TestMakefileRecipeOverride(MakefileTestCase):

    @slow_test
    def test_recipe_override(self):
        '''Check that default recipe for $(VENV) may be overwritten by user'''
        makefile = self.copy_data('recipe-override.mk', makefile=True)

        first = self.make('freeze', makefile=makefile)
        self.assertIn('dummy-test==0.1.3', first.stdout.splitlines())

        second = self.make('freeze', makefile=makefile)
        self.assertNotIn('pip install', second.stdout)
        self.assertIn('dummy-test==0.1.3', second.stdout.splitlines())
