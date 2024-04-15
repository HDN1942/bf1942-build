import shutil
from invoke import task, config
from pathlib import Path

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

