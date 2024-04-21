import unittest
import tasks.tests.util as testutil
from invoke import MockContext
from pathlib import Path
from unittest.mock import patch
from tasks.install import uninstall

class UninstallTest(unittest.TestCase):
    def setUp(self):
        testutil.remove_dummy_files(self)

        self.root = testutil.create_dummy_files({
            'bf1942': {
                'Mods': {}
            }
        })

        self.c = MockContext({
            'project_root': self.root,
            'bf1942': {
                'path': self.root / 'bf1942'
            },
            'mod': {
                'name': 'Test'
            }
        })

    def tearDown(self):
        testutil.remove_dummy_files(self)

    def test_uninstalls_mod(self):
        self.root = testutil.create_dummy_files({
            'bf1942': {
                'Mods': {
                    'Test': {
                        'init.con': None
                    }
                }
            }
        })

        uninstall(self.c)

        self.assertFalse((self.c.bf1942.path / 'Mods' / 'Test').exists())

    @patch('shutil.rmtree')
    def test_does_nothing_if_mod_is_not_installed(self, rmtree_mock):
        uninstall(self.c)

        rmtree_mock.assert_not_called()

if __name__ == '__main__':
    unittest.main()