import re
import shutil
from invoke import task
from pathlib import Path
from .config import prepare_config
from .process import process_files
from .sync import sync_targets

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

@task()
def pack_rfas(c):
    for target in [t for t in c.build.targets if not t.up_to_date]:
        target.pack_path.mkdir(parents=True, exist_ok=True)

        if target.rfa_path.exists():
            target.rfa_path.unlink()

        work_base = c.build_path / 'process' if target.processed else c.build_path / 'src'
        src_path = target.process_path if target.processed else target.work_path

        c.run(f'python3 {c.scripts.pack} {src_path} {target.pack_path} -b {work_base}')

# src -> build/src -> build/process -> build/pack
# 1. sync changes from src to build/src
# 2. for each processable type, if src has changed, sync and then process to build/process
# 3. for each rfa, if src has changed, pack from src or process

@task(prepare_config, make_directories, gen_mod_init, sync_targets, process_files, pack_rfas)
def build(c):
    return
    # TODO copy biks from parent mod where missing

@task(prepare_config)
def clean(c):
    c.build_path = c.project_root / c.build_dir
    if c.build_path.exists():
        shutil.rmtree(c.build_path)
