import re
import shutil
from invoke import task
from pathlib import Path
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
def prepare_config(c):
    if c.mod.name == 'BF1942':
        raise ValueError('mod.name cannot be BF1942')

    c.project_root = Path(c.project_root)
    if c.project_root.exists() is False:
        raise FileNotFoundError(f'project_root "{c.project_root}" does not exist')

    c.bf1942.path = Path(c.bf1942.path)
    if c.bf1942.path.exists() is False:
        raise FileNotFoundError(f'bf1942.path "{c.bf1942.path}" does not exist')

    c.mod.base_path = c.bf1942.path / 'Mods' / c.mod.base
    if c.mod.base_path.exists() is False:
        raise FileNotFoundError(f'mod.base "{c.mod.base}" does not exist')

    scripts_path = Path(__file__).parent / 'bf1942-modding-scripts'
    c.scripts = {
        'pack': scripts_path / 'pack.py'
    }

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
        init.write(f'game.customGameFlushArchives 0\n')
        init.write(f'game.setCustomGameUrl "{c.mod.url}"\n')
        init.write('\n')

        for line in biks:
            init.write(line + '\n')

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

@task(prepare_config, make_directories, gen_mod_init, pack_rfas)
def build(c):
    return
    # TODO copy biks from parent mod where missing

@task(prepare_config)
def clean(c):
    c.build_path = c.project_root / c.build_dir
    if c.build_path.exists():
        shutil.rmtree(c.build_path)
