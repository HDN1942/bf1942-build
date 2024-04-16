import unittest
import tasks.tests.util as testutil
from invoke import MockContext
from pathlib import Path
from tasks.buildtarget import BuildTarget

class BuildTargetTest(unittest.TestCase):
    def setUp(self):
        self.root = testutil.create_dummy_files({
            'src': {},
            'build': {
                'src': {},
                'process': {},
                'pack': {
                    'Archives': {}
                }
            }
        })

        self.c = MockContext({
            'project_root': self.root,
            'src_path': self.root / 'src',
            'build_path': self.root / 'build',
            'pack_path': self.root / 'pack'
        })

    def tearDown(self):
        testutil.remove_dummy_files(self)

    def test_sets_data_attributes_objects(self):
        target = BuildTarget(self.c, 'objects')

        self.assertEqual('objects', target.full_name)
        self.assertEqual('objects', target.name)
        self.assertIsNone(target.extension)
        self.assertEqual(Path('objects'), target.base_path)
        self.assertEqual(self.c.src_path / 'objects', target._src_path)
        self.assertEqual(self.c.build_path / 'src' / 'objects' / 'objects', target._build_src_path)
        self.assertEqual(self.c.build_path / 'process' / 'objects' / 'objects', target._build_process_path)
        self.assertEqual(target._build_src_path, target.work_path)
        self.assertEqual(self.c.build_path / 'src' / 'objects', target.work_base_path)
        self.assertEqual(self.c.pack_path / 'Archives' / 'objects.rfa', target.rfa_file)
        self.assertIsNone(target.up_to_date)
        self.assertFalse(target.processed)

    def test_sets_data_attributes_objects_001(self):
        target = BuildTarget(self.c, 'objects_001')

        self.assertEqual('objects_001', target.full_name)
        self.assertEqual('objects', target.name)
        self.assertEqual('_001', target.extension)
        self.assertEqual(Path('objects'), target.base_path)
        self.assertEqual(self.c.src_path / 'objects_001', target._src_path)
        self.assertEqual(self.c.build_path / 'src' / 'objects_001' / 'objects', target._build_src_path)
        self.assertEqual(self.c.build_path / 'process' / 'objects_001' / 'objects', target._build_process_path)
        self.assertEqual(target._build_src_path, target.work_path)
        self.assertEqual(self.c.build_path / 'src' / 'objects_001', target.work_base_path)
        self.assertEqual(self.c.pack_path / 'Archives' / 'objects_001.rfa', target.rfa_file)
        self.assertIsNone(target.up_to_date)
        self.assertFalse(target.processed)

    def test_sets_data_attributes_game(self):
        target = BuildTarget(self.c, 'bf1942/game')

        self.assertEqual('game', target.full_name)
        self.assertEqual('game', target.name)
        self.assertIsNone(target.extension)
        self.assertEqual(Path('bf1942/game'), target.base_path)
        self.assertEqual(self.c.src_path / 'bf1942' / 'game', target._src_path)
        self.assertEqual(self.c.build_path / 'src' / 'game' / 'bf1942' / 'game', target._build_src_path)
        self.assertEqual(self.c.build_path / 'process' / 'game' / 'bf1942' / 'game', target._build_process_path)
        self.assertEqual(target._build_src_path, target.work_path)
        self.assertEqual(self.c.build_path / 'src' / 'game', target.work_base_path)
        self.assertEqual(self.c.pack_path / 'Archives' / 'bf1942' / 'game.rfa', target.rfa_file)
        self.assertIsNone(target.up_to_date)
        self.assertFalse(target.processed)

    def test_sets_data_attributes_guadalcanal(self):
        target = BuildTarget(self.c, 'bf1942/levels/Guadalcanal')

        self.assertEqual('Guadalcanal', target.full_name)
        self.assertEqual('Guadalcanal', target.name)
        self.assertIsNone(target.extension)
        self.assertEqual(Path('bf1942/levels/Guadalcanal'), target.base_path)
        self.assertEqual(self.c.src_path / 'bf1942' / 'levels' / 'Guadalcanal', target._src_path)
        self.assertEqual(self.c.build_path / 'src' / 'Guadalcanal' / 'bf1942' / 'levels' / 'Guadalcanal', target._build_src_path)
        self.assertEqual(self.c.build_path / 'process' / 'Guadalcanal' / 'bf1942' / 'levels' / 'Guadalcanal', target._build_process_path)
        self.assertEqual(target._build_src_path, target.work_path)
        self.assertEqual(self.c.build_path / 'src' / 'Guadalcanal', target.work_base_path)
        self.assertEqual(self.c.pack_path / 'Archives' / 'bf1942' / 'levels' / 'Guadalcanal.rfa', target.rfa_file)
        self.assertIsNone(target.up_to_date)
        self.assertFalse(target.processed)

    # TODO test_sync
    # TODO test_setup_for_process

if __name__ == '__main__':
    unittest.main()