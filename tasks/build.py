import logging
import re
import shutil
from invoke import task
from pathlib import Path
from tasks.buildtarget import BuildTarget
from tasks.config import prepare_config
from tasks.process import process_files

logger = logging.getLogger(__name__)

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

@task
def make_directories(c):
    c.build_path = c.project_root / c.build_dir
    c.pack_path = c.build_path / 'pack'

    if not c.build_path.exists():
        logger.debug(f'create build directory {c.build_path}')
        c.build_path.mkdir()

    if not c.pack_path.exists():
        logger.debug(f'create pack directory {c.pack_path}')
        c.pack_path.mkdir()

@task
def gen_mod_init(c):
    # TODO don't generate if src/init.con exists

    logger.info(f'generate mod init.con')

    mod_path_re = re.compile('^game\.addModPath', re.IGNORECASE)
    bik_re = re.compile("^game\.\w+Filename.+\.bik", re.IGNORECASE)

    base_init_path = c.mod.base_path / 'init.con'
    paths = []
    biks = []
    for line in base_init_path.read_text().split('\n'):
        if mod_path_re.match(line) is not None:
            logger.debug(f'found base mod {line}')
            paths.append(line)
        if bik_re.match(line) is not None:
            logger.debug(f'found bik {line}')
            biks.append(line)

    init_path = c.pack_path / 'init.con'
    logger.debug(f'write {init_path}')

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

    top_rfas = top_level_rfas(c.src_path)
    for directory in top_rfas:
        target = BuildTarget(c, directory.relative_to(c.src_path))
        targets.append(target)

    bf1942_path = c.src_path / 'bf1942'
    bf1942_rfas = [d for d in bf1942_path.iterdir() if d.is_dir() and d.name in BF1942_LEVEL_RFAS]
    for directory in bf1942_rfas:
        target = BuildTarget(c, directory.relative_to(c.src_path))
        targets.append(target)

    levels_path = bf1942_path / 'levels'
    for directory in [d for d in levels_path.iterdir() if d.is_dir()]:
        target = BuildTarget(c, directory.relative_to(c.src_path))
        targets.append(target)

    for target in targets:
        logger.info(f'found build target: {target}')

    c.build = {
        'targets': targets,
        'out_of_date': None,
        'all_up_to_date': None
    }

@task()
def sync_targets(c):
    logger.info('sync build targets')
    logger.debug('start build targets sync')

    for target in c.build.targets:
        logger.info(f'sync {target}')
        target.sync()

        if target.up_to_date:
            logger.info(f'{target} is up-to-date')
        else:
            logger.info(f'{target} is out-of-date')

    logger.debug('end build targets sync')

    c.build.out_of_date = [t for t in c.build.targets if not t.up_to_date]
    c.build.all_up_to_date = len(c.build.out_of_date) == 0

    if c.build.all_up_to_date:
        logger.info('all build targets are up-to-date')

@task()
def pack_rfas(c):
    if c.build.all_up_to_date:
        return

    logger.info('pack build targets')
    logger.debug('start build targets pack')

    for target in [t for t in c.build.targets if not t.up_to_date]:
        logger.debug(f'create RFA destination directory {target.rfa_file.parent}')
        target.rfa_file.parent.mkdir(parents=True, exist_ok=True)

        if target.rfa_file.exists():
            logger.debug(f'delete existing RFA {target.rfa_file}')
            target.rfa_file.unlink()

        logger.debug(f'run pack script for {target}')
        c.run(f'python3 {c.scripts.pack} {target.work_path} {target.rfa_file} -b {target.work_base_path}')

    logger.debug('end build targets pack')

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
    logger.info('clean existing build files')

    c.build_path = c.project_root / c.build_dir
    if c.build_path.exists():
        logger.debug(f'remove tree {c.build_path}')
        shutil.rmtree(c.build_path)
    else:
        logger.debug(f'{c.build_path} does not exist, nothing to do')
