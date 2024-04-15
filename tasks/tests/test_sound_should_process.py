import unittest
import tasks.tests.util as testutil
from tasks.build import BuildTarget
from tasks.sound import should_process

class SoundShouldProcessTest(unittest.TestCase):
    def setUp(self):
        testutil.remove_dummy_files(self)

        self.root = testutil.create_dummy_files({
            'build': {
                'src': {
                    'sound': {}
                }
            },
            'src': {
                'sound': {}
            }
        })

        self.sound = BuildTarget(self.root / 'build', self.root / 'pack', self.root / 'src' / 'sound', 'sound')
        self.not_sound = BuildTarget(self.root / 'build', self.root / 'pack', self.root / 'src' / 'not_sound', 'not_sound')

    def tearDown(self):
        testutil.remove_dummy_files(self)

    def test_sound_directory_with_unconverted_files_returns_true(self):
        self.root = testutil.create_dummy_files({
            'build': {
                'src': {
                    'sound': {
                        'dir1': {
                            'dir2': {
                                'foo.wav': None
                            }
                        }
                    }
                }
            }
        })

        result = should_process(self.sound)

        self.assertTrue(result)

    def test_sound_directory_with_converted_files_returns_false(self):
        self.root = testutil.create_dummy_files({
            'build': {
                'src': {
                    'sound': {
                        '44khz': {
                            'foo.wav': None,
                            'dir1': {
                                'bar.wav': None
                            }
                        }
                    }
                }
            }
        })

        result = should_process(self.sound)

        self.assertFalse(result)

    def test_top_sound_directory_with_unconverted_files_returns_true(self):
        self.root = testutil.create_dummy_files({
            'build': {
                'src': {
                    'not_sound': {
                        'sound': {
                            'baz.con': None
                        }
                    }
                }
            }
        })

        result = should_process(self.not_sound)

        self.assertTrue(result)

    def test_top_sound_directory_with_converted_files_returns_false(self):
        self.root = testutil.create_dummy_files({
            'build': {
                'src': {
                    'not_sound': {
                        'sound': {
                            '44khz': {
                                'foo.wav': None,
                                'dir1': {
                                    'bar.wav': None
                                }
                            }
                        }
                    }
                }
            }
        })

        result = should_process(self.not_sound)

        self.assertFalse(result)

    def test_no_root_or_top_sound_directory_returns_false(self):
        self.root = testutil.create_dummy_files({
            'build': {
                'src': {
                    'not_sound': {
                        'also_not_sound': {
                            'sound': {
                                'baz.con': None
                            }
                        }
                    }
                }
            }
        })

        result = should_process(self.not_sound)

        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()