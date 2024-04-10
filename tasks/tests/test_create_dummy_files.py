import unittest
import tasks.tests.util as testutil

class DummyFilesTest(unittest.TestCase):
    def tearDown(self):
        testutil.remove_dummy_files(self)

    def test_creates_directory_structure(self):
        self.root = testutil.create_dummy_files({
            'src': {
                'dir1': {
                    'dir2': {
                        'foo.txt': None
                    }
                },
                'bar.txt': None
            },
            'dst': {}
        })

        self.assertIsNotNone(self.root)
        self.assertTrue(self.root.is_dir())

        src = self.root / 'src'
        dst = self.root / 'dst'
        dir1 = src / 'dir1'
        dir2 = dir1 / 'dir2'
        foo_txt = dir2 / 'foo.txt'
        bar_txt = src / 'bar.txt'

        self.assertTrue(src.is_dir())
        self.assertTrue(dst.is_dir())
        self.assertTrue(dir1.is_dir())
        self.assertTrue(dir1.is_dir())
        self.assertTrue(dir2.is_dir())
        self.assertTrue(foo_txt.is_file())
        self.assertTrue(bar_txt.is_file())

    def test_creates_within_existing_structure(self):
        self.root = testutil.create_dummy_files({
            'dst': {}
        })

        testutil.create_dummy_files({
            'dst': {
                'dir1': {
                    'foo.txt': None
                },
                'bar.txt': None
            }
        })

        dst = self.root / 'dst'
        dir1 = dst / 'dir1'
        foo_txt = dir1 / 'foo.txt'
        bar_txt = dst / 'bar.txt'

        self.assertTrue(dst.is_dir())
        self.assertTrue(dir1.is_dir())
        self.assertTrue(foo_txt.is_file())
        self.assertTrue(bar_txt.is_file())

if __name__ == '__main__':
    unittest.main()
