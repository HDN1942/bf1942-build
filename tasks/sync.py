import shutil
from invoke import task, config
from pathlib import Path

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

def sync_dirs(src, dst):
    '''Sync files from src to dst directory and return True if there were any changes.'''

    src_path = Path(src)
    dst_path = Path(dst)

    changed = False

    for src_file in [f for f in src_path.rglob('*') if f.is_file()]:
        dst_file = dst_path / src_file.relative_to(src)

        dst_file.parent.mkdir(parents=True, exist_ok=True)
        if not dst_file.exists() or src_file.stat().st_mtime > dst_file.stat().st_mtime:
            shutil.copyfile(src_file, dst_file)
            changed = True

    for dst_file in [f for f in dst_path.rglob('*') if f.is_file()]:
        src_file = src_path / dst_file.relative_to(dst)

        if not src_file.exists():
            dst_file.unlink()
            changed = True

            # delete directory if empty and any empty parent directories
            parent = dst_file.parent
            while parent.is_dir() and len(list(parent.iterdir())) == 0:
                parent.rmdir()
                parent = parent.parent

    return changed

def sync_target(c, src, base):
    src_path = Path(src)
    name = src_path.name

    target = config.DataProxy.from_data({
        'name': name,
        'src_path': src_path
    })

    target.base_path = Path(base)
    target.work_path = c.build_path / 'src' / target.base_path
    target.process_path = c.build_path / 'process' / target.base_path
    target.pack_path = c.pack_path / 'Archives' / target.base_path.parent
    target.rfa_path = target.pack_path / f'{target.name}.rfa'
    target.up_to_date = not sync_dirs(target.src_path, target.work_path)
    target.processed = False

    return target

@task
def sync_targets(c):
    targets = []

    src_path = c.project_root / 'src'
    top_rfas = [d for d in src_path.iterdir() if d.is_dir() and d.name in TOP_LEVEL_RFAS]
    for src in top_rfas:
        targets.append(sync_target(c, src, src.name))

    bf1942_path = src_path / 'bf1942'
    bf1942_rfas = [d for d in bf1942_path.iterdir() if d.is_dir() and d.name in BF1942_LEVEL_RFAS]
    for src in bf1942_rfas:
        targets.append(sync_target(c, src, Path('bf1942', src.name)))

    levels_path = bf1942_path / 'levels'
    for src in [d for d in levels_path.iterdir() if d.is_dir()]:
        targets.append(sync_target(c, src, Path('bf1942', 'levels', src.name)))

    c.build = { 'targets': targets }
