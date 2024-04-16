import unittest
import tasks.tests.util as testutil
from invoke import MockContext
from pathlib import Path
from unittest.mock import patch, call
from tasks.buildtarget import BuildTarget
from tasks.sound import RATE_11KHZ, RATE_22KHZ, RATE_44KHZ, process

class SoundProcessTest(unittest.TestCase):
    def setUp(self):
        testutil.remove_dummy_files(self)

        self.root = testutil.create_dummy_files({
            'src': {
                'sound': {},
                'notsound': {}
            },
            'build': {
                'src': {
                    'sound': {
                        'sound': {
                            'dir1': {
                                'dir2': {
                                    'foo.wav': None
                                }
                            },
                            '44khz': {
                                'bar.wav': None
                            }
                        },
                    },
                    'notsound': {
                        'notsound': {
                            'sound': {
                                'dir1': {
                                    'dir2': {
                                        'baz.wav': None
                                    }
                                },
                                '44khz': {
                                    'bat.wav': None
                                }
                            }
                        }
                    }
                },
                'process': {}
            }
        })

        self.c = MockContext({
            'project_root': self.root,
            'src_path': self.root / 'src',
            'build_path': self.root / 'build',
            'pack_path': self.root / 'pack',
            'processors': {
                'sound': {
                    'generate_11khz': True,
                    'generate_22khz': True
                }
            }
        })

        self.sound = BuildTarget(self.c, 'sound')
        self.notsound = BuildTarget(self.c, 'notsound')

    def tearDown(self):
        testutil.remove_dummy_files(self)

    @patch('tasks.sound.run_ffmpeg')
    def test_converts_unconverted_sound_files_in_sound(self, run_ffmpeg_mock):
        self.sound.setup_for_process()

        process(self.c, self.sound)

        self.assertEqual(run_ffmpeg_mock.call_count, 3)

        top = self.root / 'build' / 'process' / 'sound' / 'sound'
        rel = Path('dir1') / 'dir2' / 'foo.wav'
        original = top / rel

        calls = [
            call(
                original,
                top / '44kHz' / rel,
                RATE_44KHZ),
            call(
                original,
                top / '22khz' / rel,
                RATE_22KHZ),
            call(
                original,
                top / '11khz' / rel,
                RATE_11KHZ)
        ]
        run_ffmpeg_mock.assert_has_calls(calls)

        self.assertFalse(original.exists())

    @patch('tasks.sound.run_ffmpeg')
    def test_converts_unconverted_sound_files_in_sound_under_root(self, run_ffmpeg_mock):
        self.notsound.setup_for_process()

        process(self.c, self.notsound)

        self.assertEqual(run_ffmpeg_mock.call_count, 3)

        top = self.root / 'build' / 'process' / 'notsound' / 'notsound' / 'sound'
        rel = Path('dir1') / 'dir2' / 'baz.wav'
        original = top / rel

        calls = [
            call(
                original,
                top / '44kHz' / rel,
                RATE_44KHZ),
            call(
                original,
                top / '22khz' / rel,
                RATE_22KHZ),
            call(
                original,
                top / '11khz' / rel,
                RATE_11KHZ)
        ]
        run_ffmpeg_mock.assert_has_calls(calls)

        self.assertFalse(original.exists())

if __name__ == '__main__':
    unittest.main()