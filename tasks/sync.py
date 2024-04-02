import shutil
from pathlib import Path

def sync_dirs(src, dst):
    src_path = Path(src)
    dst_path = Path(dst)

    changed = False

    for src_file in [f for f in src_path.rglob('*') if f.is_file()]:
        dst_file = dst_path / src_file.relative_to(src)

        dst_file.parent.mkdir(parents=True, exist_ok=True)
        if not dst_file.exists() or src_file.stat().st_mtime > dst_file.stat().st_mtime:
            shutil.copyfile(src_file, dst_file)
            changed = True

    return changed