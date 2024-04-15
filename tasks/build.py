import re
import shutil
from invoke import task
from pathlib import Path
from tasks.config import prepare_config
from tasks.process import process_files
from tasks.sync import sync_dirs

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

BF1942_EXTENDABLE_RFAS = set([
    'menu',
    'sound',
    'standardMesh',
    'texture'
])

class BuildTarget:
    def __init__(self, build_path, pack_path, src, base):
        self.src_path = Path(src)
        self.name = self.src_path.name
        self.base_path = Path(base)
        self.work_path = build_path / 'src' / self.base_path
        self.process_path = build_path / 'process' / self.base_path
        self.pack_path = pack_path / 'Archives' / self.base_path.parent
        self.rfa_path = self.pack_path / f'{self.name}.rfa'
        self.up_to_date = None
        self.processed = False

    def sync(self):
        self.up_to_date = not sync_dirs(self.src_path, self.work_path)

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
        init.write(f'game.setCustomGameUrl "{c.mod.url}"\n')
        init.write('\n')

        for line in biks:
            init.write(line + '\n')

def top_level_rfas(path):
    name_re = re.compile('^([^_]+)(_\d{3})?$', re.IGNORECASE)

    for directory in [d for d in path.iterdir() if d.is_dir()]:
        match = name_re.match(directory.name)
        if match:
            name = match.group(1)
            extension = match.group(2)
            if name in TOP_LEVEL_RFAS and (extension is None or name in BF1942_EXTENDABLE_RFAS):
                yield directory

@task
def find_targets(c):
    targets = []

    src_path = c.project_root / 'src'
    top_rfas = top_level_rfas(src_path)
    for src in top_rfas:
        targets.append(BuildTarget(c.build_path, c.pack_path, src, src.name))

    bf1942_path = src_path / 'bf1942'
    bf1942_rfas = [d for d in bf1942_path.iterdir() if d.is_dir() and d.name in BF1942_LEVEL_RFAS]
    for src in bf1942_rfas:
        targets.append(BuildTarget(c.build_path, c.pack_path, src, Path('bf1942', src.name)))

    levels_path = bf1942_path / 'levels'
    for src in [d for d in levels_path.iterdir() if d.is_dir()]:
        targets.append(BuildTarget(c.build_path, c.pack_path, src, Path('bf1942', 'levels', src.name)))

    c.build = { 'targets': targets }

@task()
def sync_targets(c):
    for target in c.build.targets:
        target.sync()

@task()
def pack_rfas(c):
    for target in [t for t in c.build.targets if not t.up_to_date]:
        target.pack_path.mkdir(parents=True, exist_ok=True)

        if target.rfa_path.exists():
            target.rfa_path.unlink()

        work_base = c.build_path / 'process' if target.processed else c.build_path / 'src'
        src_path = target.process_path if target.processed else target.work_path

        c.run(f'python3 {c.scripts.pack} {src_path} {target.pack_path} -b {work_base}')

# src -> build/src -> build/process (optional) -> build/pack
# 1. sync changes from src to build/src
# 2. for each processable type, if src has changed, sync to build/process and then process
# 3. for each rfa, if src has changed, pack from build/src or build/process
@task(prepare_config, make_directories, gen_mod_init, find_targets, sync_targets, process_files, pack_rfas)
def build(c):
    return
    # TODO copy biks from parent mod where missing

@task(prepare_config)
def clean(c):
    c.build_path = c.project_root / c.build_dir
    if c.build_path.exists():
        shutil.rmtree(c.build_path)
