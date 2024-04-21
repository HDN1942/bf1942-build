import hashlib
import logging
import shutil
from invoke import task, config
from pathlib import Path

logger = logging.getLogger(__name__)

def compute_hash(file):
    contents = Path(file).read_bytes()

    sha256 = hashlib.sha256(contents, usedforsecurity=False)
    return sha256.hexdigest()

def copyfile_if_changed(src, dst):
    src_path = Path(src)
    dst_path = Path(dst)

    assert src_path.is_file()
    assert dst_path.parent.is_dir()
    assert not dst_path.exists() or dst_path.is_file()

    if not Path(dst).exists():
        shutil.copyfile(src, dst)
        return True

    src_hash = compute_hash(src)
    dst_hash = compute_hash(dst)

    if src_hash != dst_hash:
        shutil.copyfile(src, dst)
        return True

    return False

def sync_dirs(src, dst):
    '''Sync files from src to dst directory and return True if there were any changes.'''

    src_path = Path(src)
    dst_path = Path(dst)

    assert src_path.is_dir()

    changed = False

    for src_file in [f for f in src_path.rglob('*') if f.is_file()]:
        dst_file = dst_path / src_file.relative_to(src)

        dst_file.parent.mkdir(parents=True, exist_ok=True)
        if not dst_file.exists() or src_file.stat().st_mtime > dst_file.stat().st_mtime:
            logger.debug(f'copy {src_file} to {dst_file}')
            shutil.copyfile(src_file, dst_file)
            changed = True

    for dst_file in [f for f in dst_path.rglob('*') if f.is_file()]:
        src_file = src_path / dst_file.relative_to(dst)

        if not src_file.exists():
            logger.debug(f'{src_file} does not exist, delete "{dst_file}"')
            dst_file.unlink()
            changed = True

            # delete directory if empty and any empty parent directories
            parent = dst_file.parent
            while parent.is_dir() and len(list(parent.iterdir())) == 0:
                logger.debug(f'{parent} directory is empty, remove')
                parent.rmdir()
                parent = parent.parent

    if changed:
        logger.debug(f'"{src}" has changed')
    else:
        logger.debug(f'"{src}" has not changed')

    return changed

