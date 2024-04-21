import unittest
import tasks.tests.util as testutil
from invoke import MockContext
from pathlib import Path
from unittest.mock import patch
from tasks.install import install

class InstallTest(unittest.TestCase):
    def setUp(self):
        testutil.remove_dummy_files(self)

        self.root = testutil.create_dummy_files({
            'build': {
                'pack': {
                    'init.con': None
                }
            },
            'bf1942': {
                'Mods': {}
            }
        })

        self.c = MockContext({
            'project_root': self.root,
            'pack_path': self.root / 'build' / 'pack',
            'bf1942': {
                'path': self.root / 'bf1942'
            },
            'mod': {
                'name': 'Test'
            }
        })

    def tearDown(self):
        testutil.remove_dummy_files(self)

    def test_installs_mod(self):
        install(self.c)

        self.assertTrue((self.c.bf1942.path / 'Mods' / 'Test' / 'init.con').exists())

    @patch('shutil.rmtree')
    def test_force_deletes_existing_files_before_install(self, rmtree_mock):
        self.root = testutil.create_dummy_files({
            'bf1942': {
                'Mods': {
                    'Test': {
                        'init.con': None
                    }
                }
            }
        })

        install(self.c, force=True)

        rmtree_mock.assert_called()

    @patch('shutil.rmtree')
    def test_force_does_nothing_if_there_is_no_existing_install(self, rmtree_mock):
        install(self.c, force=True)

        rmtree_mock.assert_not_called()

if __name__ == '__main__':
    unittest.main()