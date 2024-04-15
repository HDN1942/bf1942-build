import unittest
import tasks.tests.util as testutil
from invoke import MockContext
from pathlib import Path
from unittest.mock import patch, call
from tasks.build import BuildTarget
from tasks.sound import RATE_11KHZ, RATE_22KHZ, RATE_44KHZ, process

class SoundProcessTest(unittest.TestCase):
    def setUp(self):
        testutil.remove_dummy_files(self)

        self.root = testutil.create_dummy_files({
            'build': {
                'process': {
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
                    'not_sound': {
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
            }
        })

        self.c = MockContext({
            'processors': {
                'sound': {
                    'generate_11khz': True,
                    'generate_22khz': True
                }
            }
        })
        self.sound = BuildTarget(self.root / 'build', self.root / 'pack', self.root / 'src' / 'sound', 'sound')
        self.not_sound = BuildTarget(self.root / 'build', self.root / 'pack', self.root / 'src' / 'not_sound', 'not_sound')

    def tearDown(self):
        testutil.remove_dummy_files(self)

    @patch('tasks.sound.run_ffmpeg')
    def test_converts_unconverted_sound_files_in_sound(self, run_ffmpeg_mock):
        process(self.c, self.sound)

        self.assertEqual(run_ffmpeg_mock.call_count, 3)

        top = self.root / 'build' / 'process' / 'sound'
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
        process(self.c, self.not_sound)

        self.assertEqual(run_ffmpeg_mock.call_count, 3)

        top = self.root / 'build' / 'process' / 'not_sound' / 'sound'
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