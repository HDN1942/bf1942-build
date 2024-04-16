import re
from ffmpeg import FFmpeg
from invoke import task
from pathlib import Path

RATE_11KHZ = 11025
RATE_22KHZ = 22050
RATE_44KHZ = 44100

def run_ffmpeg(src, dst, rate):
    '''Run ffmpeg to transcode a sound file into a BF1942 supported wave file at the specified sample rate.'''

    ffmpeg = (
        FFmpeg()
        .option('y')
        .input(src)
        .output(
            dst,
            {'fflags': '+bitexact', 'flags:a': '+bitexact'},
            acodec='pcm_s16le',
            ar=rate,
            map_metadata=-1
        )
    )
    ffmpeg.execute()

def get_sound_path(path):
    sound_path_re = re.compile('^sound(?:_\d{3})?$', re.IGNORECASE)

    if sound_path_re.match(path.name) is not None:
        sound_path = path
    else:
        sound_path = path / 'sound'

    if sound_path.exists() and sound_path.is_dir():
        return sound_path
    else:
        return None

def sounds_to_convert(path):
    for file in [f for f in path.rglob('*') if f.is_file()]:
        top = file.relative_to(path).parts[0]
        if str(top).lower() in ['11khz', '22khz', '44khz']:
            continue

        yield file

def should_process(target):
    '''Process sounds if target has a sound directory containing files/directories other than 11khz/22khz/44khz.'''

    sound_path = get_sound_path(target.work_path)
    if sound_path is None:
        return False

    for file in sounds_to_convert(sound_path):
        return True

    return False

# TODO async in threads?
@task
def process(c, target):
    '''Convert sounds to BF1942 supported wave format.'''

    sound_path = get_sound_path(target.work_path)
    sounds = []
    for file in sounds_to_convert(sound_path):
        parts = Path(*file.relative_to(sound_path).parent.parts)
        file_name = f'{file.stem}.wav'
        sounds.append((file, parts, file_name))

    d44_path = sound_path / '44kHz'
    d44_path.mkdir(parents=True, exist_ok=True)

    for file, parts, file_name in sounds:
        d44_file = d44_path / parts / file_name
        run_ffmpeg(file, d44_file, RATE_44KHZ)

    if c.processors.sound.generate_22khz:
        d22_path = sound_path / '22khz'
        d22_path.mkdir(parents=True, exist_ok=True)

        for file, parts, file_name in sounds:
            d22_file = d22_path / parts / file_name
            run_ffmpeg(file, d22_file, RATE_22KHZ)

    if c.processors.sound.generate_11khz:
        d11_path = sound_path / '11khz'
        d11_path.mkdir(parents=True, exist_ok=True)

        for file, parts, file_name in sounds:
            d11_file = d11_path / parts / file_name
            run_ffmpeg(file, d11_file, RATE_11KHZ)

    for file, parts, file_name in sounds:
        file.unlink()