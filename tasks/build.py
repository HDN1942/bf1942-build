import re
import shutil
from ffmpeg import FFmpeg
from invoke import task
from pathlib import Path
from .config import prepare_config
from .sync import sync_dirs

TOP_LEVEL_RFAS = set([
    'ai',
    'aiMeshes',
    'animations',
    'font',
    'menu',
    'objects',
    'shaders',
    'sound',
    'standardMesh',
    'texture',
    'treeMesh'
])

BF1942_LEVEL_RFAS = set([
    'game'
])

@task
def make_directories(c):
    c.build_path = c.project_root / c.build_dir
    c.build_path.mkdir(exist_ok=True)

    c.pack_path = c.build_path / 'pack'
    c.pack_path.mkdir(exist_ok=True)

@task
def gen_mod_init(c):
    # TODO don't generate if src/init.con exists
    mod_path_re = re.compile('^game\.addModPath', re.IGNORECASE)
    bik_re = re.compile("^game\.\w+Filename.+\.bik", re.IGNORECASE)

    base_init_path = c.mod.base_path / 'init.con'
    paths = []
    biks = []
    for line in base_init_path.read_text().split('\n'):
        if mod_path_re.match(line) is not None:
            paths.append(line)
        if bik_re.match(line) is not None:
            biks.append(line)

    init_path = c.pack_path / 'init.con'
    with open(init_path, 'w') as init:
        init.write(f'game.CustomGameName {c.mod.name}\n')
        init.write(f'game.addModPath Mods/{c.mod.name}/\n')

        for line in paths:
            init.write(line + '\n')

        init.write(f'game.setCustomGameVersion {c.mod.version}\n')
        # TODO this always causes an error in the logs, is it needed?
        # maybe only in retail build? can confirm? check bins?
        init.write(f'game.customGameFlushArchives 0\n')
        init.write(f'game.setCustomGameUrl "{c.mod.url}"\n')
        init.write('\n')

        for line in biks:
            init.write(line + '\n')

@task
def convert_files(c):
    sound_path = c.project_root / 'src' / 'sound'
    dst_path = c.build_path / 'src' / 'sound'
    d11_path = dst_path / '11khz'
    d22_path = dst_path / '22khz'
    d44_path = dst_path / '44kHz'

    d11_path.mkdir(parents=True, exist_ok=True)
    d22_path.mkdir(parents=True, exist_ok=True)
    d44_path.mkdir(parents=True, exist_ok=True)

    for src_file in [f for f in sound_path.rglob('*') if f.is_file()]:
        parts = Path(*src_file.relative_to(sound_path))
        file_name = f'{src_file.stem}.wav'

        d11_file = d11_path / parts / '11khz' / file_name
        d22_file = d22_path / parts / '22khz' / file_name
        d44_file = d44_path / parts / '44kHz' / file_name

        ffmpeg = (
            FFmpeg()
            .option('y')
            .input('input.mp4')
            .output(
                d11_file,
                acodec='pcm_s16le',
                ar=11025
            )
        )
        # 44100
        # 22050
        # 11025

        # ffmpeg -i sample.mp3 -acodec pcm_s16le -ar 44100 sample.wav

    ffmpeg.execute()


def pack_rfa(c, src, rfa):
    src_path = Path(src)
    rfa_path = Path(rfa)

    base_path = c.build_path / 'src'
    work_path = base_path / rfa_path

    if sync_dirs(src_path, work_path):
        pack_path = c.pack_path / 'Archives' / rfa_path.parent
        pack_path.mkdir(parents=True, exist_ok=True)

        rfa_file_path = pack_path / f'{rfa_path.name}.rfa'
        if rfa_file_path.exists():
            rfa_file_path.unlink()

        c.run(f'python3 {c.scripts.pack} {work_path} {pack_path} -b {base_path}')

@task()
def pack_rfas(c):
    src_path = c.project_root / 'src'
    top_rfas = [d for d in src_path.iterdir() if d.is_dir() and d.name in TOP_LEVEL_RFAS]
    for src in top_rfas:
        pack_rfa(c, src, Path(src.name))

    bf1942_path = src_path / 'bf1942'
    bf1942_rfas = [d for d in bf1942_path.iterdir() if d.is_dir() and d.name in BF1942_LEVEL_RFAS]
    for src in bf1942_rfas:
        pack_rfa(c, src, Path('bf1942', src.name))

    levels_path = bf1942_path / 'levels'
    for src in [d for d in levels_path.iterdir() if d.is_dir()]:
        pack_rfa(c, src, Path('bf1942', 'levels', src.name))

@task(prepare_config, make_directories, gen_mod_init, convert_files, pack_rfas)
def build(c):
    return
    # TODO copy biks from parent mod where missing

@task(prepare_config)
def clean(c):
    c.build_path = c.project_root / c.build_dir
    if c.build_path.exists():
        shutil.rmtree(c.build_path)
