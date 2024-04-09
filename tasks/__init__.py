from invoke import Collection, task
from .build import build, clean
from .deploy import deploy
from .launch import launch

ns = Collection()

ns.add_task(build)
ns.add_task(clean)
ns.add_task(deploy)
ns.add_task(launch)

ns.configure({
    'project_root': '',
    'build_dir': 'build',
    'bf1942': {
        # TODO what's the actual default install path on Windows?
        'path': 'C:\\Program Files (x86)\\EA Games\\Battlefield 1942'
    },
    'mod': {
        'name': 'MyMod',
        'base': 'bf1942',
        'version': '0.1.0',
        'url': 'https://example.net'
    },
    'linux': {
        'wine_path': 'wine',
        'wine_prefix': ''
    }
})