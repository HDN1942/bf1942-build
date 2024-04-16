import unittest
import tasks.tests.util as testutil
from invoke import MockContext
from tasks.buildtarget import BuildTarget
from tasks.sound import should_process

class SoundShouldProcessTest(unittest.TestCase):
    def setUp(self):
        testutil.remove_dummy_files(self)

        self.root = testutil.create_dummy_files({
            'src': {
                'sound': {},
                'notsound': {}
            },
            'build': {
                'src': {
                    'sound': {},
                    'notsound': {}
                }
            }
        })

        self.c = MockContext({
            'project_root': self.root,
            'src_path': self.root / 'src',
            'build_path': self.root / 'build',
            'pack_path': self.root / 'pack'
        })

        self.sound = BuildTarget(self.c, 'sound')
        self.notsound = BuildTarget(self.c, 'notsound')

    def tearDown(self):
        testutil.remove_dummy_files(self)

    def test_sound_directory_with_unconverted_files_returns_true(self):
        self.root = testutil.create_dummy_files({
            'build': {
                'src': {
                    'sound': {
                        'sound': {
                            'dir1': {
                                'dir2': {
                                    'foo.wav': None
                                }
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

        result = should_process(self.sound)

        self.assertFalse(result)

    def test_top_sound_directory_with_unconverted_files_returns_true(self):
        self.root = testutil.create_dummy_files({
            'build': {
                'src': {
                    'notsound': {
                        'notsound': {
                            'sound': {
                                'baz.con': None
                            }
                        }
                    }
                }
            }
        })

        result = should_process(self.notsound)

        self.assertTrue(result)

    def test_top_sound_directory_with_converted_files_returns_false(self):
        self.root = testutil.create_dummy_files({
            'build': {
                'src': {
                    'notsound': {
                        'notsound': {
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
            }
        })

        result = should_process(self.notsound)

        self.assertFalse(result)

    def test_no_root_or_top_sound_directory_returns_false(self):
        self.root = testutil.create_dummy_files({
            'build': {
                'src': {
                    'notsound': {
                        'notsound': {
                            'also_notsound': {
                                'sound': {
                                    'baz.con': None
                                }
                            }
                        }
                    }
                }
            }
        })

        result = should_process(self.notsound)

        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()