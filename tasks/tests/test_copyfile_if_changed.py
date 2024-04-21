import unittest
import tasks.tests.util as testutil
from pathlib import Path
from tasks.sync import copyfile_if_changed

class CopyfileIfChangedTest(unittest.TestCase):
    def setUp(self):
        testutil.remove_dummy_files(self)

        self.root = testutil.create_dummy_files({
            'src': {
                'foo.txt': 'foo'
            },
            'dst': {}
        })

        self.src_file = self.root / 'src' / 'foo.txt'
        self.dst_file = self.root / 'dst' / 'foo.txt'

    def tearDown(self):
        testutil.remove_dummy_files(self)

    def test_copies_file_if_dst_file_does_not_exist(self):
        result = copyfile_if_changed(self.src_file, self.dst_file)

        self.assertTrue(result)
        self.assertTrue(self.dst_file.exists())

    def test_copies_file_if_contents_differ(self):
        self.root = testutil.create_dummy_files({
            'dst': {
                'foo.txt': 'bar'
            }
        })

        result = copyfile_if_changed(self.src_file, self.dst_file)

        self.assertTrue(result)
        self.assertTrue(self.dst_file.exists())
        self.assertEqual('foo\n', self.dst_file.read_text())

    def test_does_not_copy_file_if_contents_are_the_same(self):
        self.root = testutil.create_dummy_files({
            'dst': {
                'foo.txt': 'foo'
            }
        })

        result = copyfile_if_changed(self.src_file, self.dst_file)

        self.assertFalse(result)
        self.assertTrue(self.dst_file.exists())
        self.assertEqual('foo\n', self.dst_file.read_text())

if __name__ == '__main__':
    unittest.main()