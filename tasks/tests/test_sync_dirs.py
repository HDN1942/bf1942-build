import unittest
import time
import tasks.tests.util as testutil
from tasks.sync import sync_dirs

class SyncDirsTest(unittest.TestCase):
    def setUp(self):
        testutil.remove_dummy_files(self)

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

        self.src = self.root / 'src'
        self.dst = self.root / 'dst'

    def tearDown(self):
        testutil.remove_dummy_files(self)

    def test_copies_new_files(self):
        changed = sync_dirs(self.src, self.dst)

        dir1 = self.dst / 'dir1'
        dir2 = dir1 / 'dir2'
        foo_txt = dir2 / 'foo.txt'
        bar_txt = self.dst / 'bar.txt'

        self.assertTrue(changed)
        self.assertTrue(dir1.is_dir())
        self.assertTrue(dir1.is_dir())
        self.assertTrue(dir2.is_dir())
        self.assertTrue(foo_txt.is_file())
        self.assertTrue(bar_txt.is_file())

    def test_copies_changed_files(self):
        sync_dirs(self.src, self.dst)

        src_bar_txt = self.src / 'bar.txt'
        dst_bar_txt = self.dst / 'bar.txt'

        # need a small amount of delay to ensure mtime changes
        time.sleep(0.005)

        with open(src_bar_txt, 'w') as file:
            print('changed', file=file)

        changed = sync_dirs(self.src, self.dst)
        contents = dst_bar_txt.read_text()

        self.assertTrue(changed)
        self.assertEqual('changed\n', contents)

    def test_deletes_removed_files(self):
        sync_dirs(self.src, self.dst)

        src_foo_txt = self.src / 'dir1' / 'dir2' / 'foo.txt'
        dst_dir1 = self.dst / 'dir1'
        dst_dir2 = dst_dir1 / 'dir2'
        dst_foo_txt = dst_dir2 / 'foo.txt'

        src_foo_txt.unlink()

        changed = sync_dirs(self.src, self.dst)

        self.assertTrue(changed)
        self.assertFalse(dst_foo_txt.exists())
        self.assertFalse(dst_dir2.exists())
        self.assertFalse(dst_dir1.exists())

    def test_returns_false_on_no_changes(self):
        sync_dirs(self.src, self.dst)
        changed = sync_dirs(self.src, self.dst)

        self.assertFalse(changed)

if __name__ == '__main__':
    unittest.main()