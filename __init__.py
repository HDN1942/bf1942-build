import shutil
from invoke import Collection, task
from pathlib import Path

@task
def build(c):
    build_path = Path(c.project_root) / c.build_path
    build_path.mkdir(exist_ok=True)

    pack_path = build_path / 'pack'
    pack_path.mkdir(exist_ok=True)

    levels_path = Path(c.project_root) / 'src' / 'bf1942' / 'levels'

    for level_src in levels_path.iterdir():
        level_name = level_src.name
        level_work = build_path / 'src' / 'bf1942' / 'levels' / level_name
        level_pack = pack_path / 'Archives' / 'bf1942' / 'levels'

        # TODO copy changed files only and build only if changed
        if level_work.exists():
            shutil.rmtree(level_work)
        shutil.copytree(level_src, level_work)

        # TODO convert pathmaps from png to raw

        if level_pack.exists():
            shutil.rmtree(level_pack)
        level_pack.mkdir(parents=True, exist_ok=True)

        c.run(f'python3 ./bf1942-modding-scripts/pack.py {level_work} {level_pack} -b bf1942/levels/{level_name}')

ns = Collection()
ns.add_task(build)

ns.configure({
    'project_root': '..',
    'build_path': 'build'
})