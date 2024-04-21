import unittest
import tasks.tests.util as testutil
from datetime import datetime, timedelta
from invoke import MockContext
from pathlib import Path
from unittest.mock import patch
from tasks.build import gen_mod_init

class GenModInitTest(unittest.TestCase):
    def setUp(self):
        testutil.remove_dummy_files(self)

        self.root = testutil.create_dummy_files({
            'build': {
                'pack': {}
            },
            'src': {},
            'bf1942': {
                'Mods': {
                    'bf1942': {
                        'init.con': None
                    }
                }
            }
        })

        self.c = MockContext({
            'project_root': self.root,
            'src_path': self.root / 'src',
            'build_path': self.root / 'build',
            'pack_path': self.root / 'build' / 'pack',
            'mod': {
                'name': 'Test',
                'version': '1.0.0',
                'url': 'https://example.net',
                'base_path': self.root / 'bf1942' / 'Mods' / 'bf1942'
            }
        })

    def tearDown(self):
        testutil.remove_dummy_files(self)

    def test_skips_gen_and_copies_existing_if_pack_init_does_not_exist(self):
        self.root = testutil.create_dummy_files({
            'src': {
                'init.con': None
            }
        })

        gen_mod_init(self.c)

        self.assertTrue((self.c.pack_path / 'init.con').exists())

    def test_skips_gen_and_copies_existing_if_out_of_date(self):
        self.root = testutil.create_dummy_files({
            'src': {
                'init.con': 'foo'
            },
            'build': {
                'pack': {
                    'init.con': 'bar'
                }
            }
        })

        gen_mod_init(self.c)

        self.assertEqual('foo\n', (self.c.pack_path / 'init.con').read_text())

    @patch('shutil.copyfile')
    def test_skips_gen_and_skips_copying_existing_if_up_to_date(self, copyfile_mock):
        self.root = testutil.create_dummy_files({
            'src': {
                'init.con': 'foo'
            },
            'build': {
                'pack': {
                    'init.con': 'foo'
                }
            }
        })

        gen_mod_init(self.c)

        copyfile_mock.assert_not_called()

    def test_copies_gen_if_pack_init_does_not_exist(self):
        gen_mod_init(self.c)

        self.assertTrue((self.c.pack_path / 'init.con').exists())

    def test_copies_gen_if_out_of_date(self):
        self.root = testutil.create_dummy_files({
            'build': {
                'pack': {
                    'init.con': 'foo'
                }
            }
        })

        gen_mod_init(self.c)

        self.assertNotEqual('foo\n', (self.c.pack_path / 'init.con').read_text())

    def test_skips_copying_gen_if_up_to_date(self, ):
        gen_mod_init(self.c)

        self.assertTrue((self.c.pack_path / 'init.con').exists())

        with patch('shutil.copyfile') as copyfile_mock:
            gen_mod_init(self.c)
            copyfile_mock.assert_not_called()

if __name__ == '__main__':
    unittest.main()