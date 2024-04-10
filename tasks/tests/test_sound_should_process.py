import unittest
import tasks.tests.util as testutil
from tasks.sound import should_process

class SoundShouldProcessTest(unittest.TestCase):
    def setUp(self):
        testutil.remove_dummy_files(self)

        self.root = testutil.create_dummy_files({
            'sound': {
                'dir1': {
                    'dir2': {
                        'foo.wav': None
                    }
                }
            },
            'sound': {
                '44khz': {
                    'bar.wav': None
                }
            },
        })

    def tearDown(self):
        testutil.remove_dummy_files(self)

    def test_sound_directory_with_unconverted_files_returns_true(self):
        self.root = testutil.create_dummy_files({
            'sound': {
                'dir1': {
                    'dir2': {
                        'foo.wav': None
                    }
                }
            }
        })

        result = should_process(self.root)

        self.assertTrue(result)

    def test_sound_directory_with_converted_files_returns_false(self):
        self.root = testutil.create_dummy_files({
            'sound': {
                '44khz': {
                    'foo.wav': None
                }
            }
        })

        result = should_process(self.root)

        self.assertFalse(result)

    def test_no_root_sound_directory_returns_false(self):
        self.root = testutil.create_dummy_files({
            'not_sound': {
                'sound': {
                    'baz.con': None
                }
            }
        })

        result = should_process(self.root)

        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()