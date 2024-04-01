import re
import shutil
from invoke import Collection, task
from pathlib import Path

@task
def check_config(c):
    c.project_root = Path(c.project_root)
    if c.project_root.exists() is False:
        raise FileNotFoundError(f'project_root "{c.project_root}" does not exist')

    c.bf1942.path = Path(c.bf1942.path)
    if c.bf1942.path.exists() is False:
        raise FileNotFoundError(f'bf1942.path "{c.bf1942.path}" does not exist')

    c.mod.base_path = c.bf1942.path / 'Mods' / c.mod.base
    if c.mod.base_path.exists() is False:
        raise FileNotFoundError(f'mod.base "{c.mod.base}" does not exist')

@task
def make_directories(c):
    c.build_path = c.project_root / c.build_dir
    c.build_path.mkdir(exist_ok=True)

    c.pack_path = c.build_path / 'pack'
    c.pack_path.mkdir(exist_ok=True)

@task
def gen_mod_init(c):
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

@task(check_config, make_directories, gen_mod_init)
def build(c):
    levels_path = c.project_root / 'src' / 'bf1942' / 'levels'

    for level_src in levels_path.iterdir():
        level_name = level_src.name
        level_work = c.build_path / 'src' / 'bf1942' / 'levels' / level_name
        level_pack = c.pack_path / 'Archives' / 'bf1942' / 'levels'

        # TODO copy changed files only and build only if changed
        if level_work.exists():
            shutil.rmtree(level_work)
        shutil.copytree(level_src, level_work)

        if level_pack.exists():
            shutil.rmtree(level_pack)
        level_pack.mkdir(parents=True, exist_ok=True)

        c.run(f'python3 ./bf1942-modding-scripts/pack.py {level_work} {level_pack} -b bf1942/levels/{level_name}')

ns = Collection()

ns.add_task(build)

ns.configure({
    'project_root': '..',
    'build_dir': 'build',
    'bf1942': {
        'path': 'c:\\Program Files (x86)\\EA Games\\Battlefield 1942'
    },
    'mod': {
        'name': 'MyMod',
        'base': 'BF1942',
        'version': '0.1.0',
        'url': 'https://example.net'
    }
})