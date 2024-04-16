
from invoke import task
from pathlib import Path

@task
def prepare_config(c):
    if c.mod.name.lower() == 'bf1942':
        raise ValueError('mod.name cannot be BF1942')

    c.project_root = Path(c.project_root)
    if c.project_root.exists() is False:
        raise FileNotFoundError(f'project_root "{c.project_root}" does not exist')

    c.src_path = c.project_root / 'src'
    if c.src_path.exists() is False:
        raise FileNotFoundError(f'"{c.src_path}" does not exist under project_root')

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
