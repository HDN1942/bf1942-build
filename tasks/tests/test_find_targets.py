import unittest
import tasks.tests.util as testutil
from invoke import MockContext
from pathlib import Path
from tasks.build import find_targets

class FindTargetsTest(unittest.TestCase):
    def setUp(self):
        testutil.remove_dummy_files(self)

        self.root = testutil.create_dummy_files({
            'src': {
                'ai': {},
                'aiMeshes': {},
                'animations': {},
                'font': {},
                'menu': {},
                'menu_001': {},
                'objects': {},
                'shaders': {},
                'sound': {},
                'sound_001': {},
                'standardMesh': {},
                'standardMesh_001': {},
                'texture': {},
                'texture_001': {},
                'treeMesh': {},
                'bf1942': {
                    'game': {},
                    'levels': {
                        'level1': {},
                        'level2': {}
                    }
                },
                'foo': {},
                'bar': {},
                'baz': {}
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

    def test_finds_targets(self):
        find_targets(self.c)

        self.assertEqual(18, len(self.c.build.targets))

        self.assert_target('ai')
        self.assert_target('aiMeshes')
        self.assert_target('animations')
        self.assert_target('font')
        self.assert_target('menu')
        self.assert_target('menu', extension='_001')
        self.assert_target('objects')
        self.assert_target('shaders')
        self.assert_target('sound')
        self.assert_target('sound', extension='_001')
        self.assert_target('standardMesh')
        self.assert_target('standardMesh', extension='_001')
        self.assert_target('texture')
        self.assert_target('texture', extension='_001')
        self.assert_target('treeMesh')
        self.assert_target('game', base_path=Path('bf1942', 'game'))
        self.assert_target('level1', base_path=Path('bf1942', 'levels', 'level1'))
        self.assert_target('level2', base_path=Path('bf1942', 'levels', 'level2'))

    def assert_target(self, name, base_path=None, extension=None):
        full_name = name
        if extension is not None:
            full_name += extension

        if base_path is None:
            base_path = Path(name)

        found = [t for t in self.c.build.targets if t.full_name == full_name]
        target = next(iter(found), None)

        self.assertIsNotNone(target, f'Target {full_name} not found')
        self.assertEqual(target.name, name)
        self.assertEqual(target.extension, extension)
        self.assertEqual(target.base_path, base_path)

if __name__ == '__main__':
    unittest.main()