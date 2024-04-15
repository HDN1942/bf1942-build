import unittest
import tasks.tests.util as testutil
from invoke import MockContext
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
            'build_path': self.root / 'build',
            'pack_path': self.root / 'pack'
        })

    def tearDown(self):
        testutil.remove_dummy_files(self)

    def test_finds_targets(self):
        find_targets(self.c)

        self.assertEqual(18, len(self.c.build.targets))

if __name__ == '__main__':
    unittest.main()