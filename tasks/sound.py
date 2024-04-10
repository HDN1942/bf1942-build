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

def should_process(target):
    '''Process sounds if target has a sound directory containing files/directories other than 11khz/22khz/44khz.'''

    sound_path = target.src_path / 'sound'
    if sound_path.exists() and sound_path.is_dir():
        # TODO sound_path contains something other than the BF1942 sound dirs
        return True

    return False

@task
def process(c, target):
    '''Convert sounds to BF1942 supported wave format.'''

    # TODO config to disable generating 11/22 khz sounds
    d11_path = target.process_path / '11khz'
    d22_path = target.process_path / '22khz'
    d44_path = target.process_path / '44kHz'

    d11_path.mkdir(parents=True, exist_ok=True)
    d22_path.mkdir(parents=True, exist_ok=True)
    d44_path.mkdir(parents=True, exist_ok=True)

    # TODO async in threads?
    # TODO skip converted files (under 11/22/44khz dirs)
    for src_file in [f for f in target.process_path.rglob('*') if f.is_file()]:
        parts = Path(*src_file.relative_to(target.process_path).parents)
        file_name = f'{src_file.stem}.wav'

        d11_file = d11_path / parts / file_name
        d22_file = d22_path / parts / file_name
        d44_file = d44_path / parts / file_name

        run_ffmpeg(src_file, d11_file, RATE_11KHZ)
        run_ffmpeg(src_file, d22_file, RATE_22KHZ)
        run_ffmpeg(src_file, d44_file, RATE_44KHZ)

        src_file.unlink()