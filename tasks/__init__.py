from invoke import Collection, task
from .build import build, clean
from .install import install, uninstall
from .launch import launch

ns = Collection()

ns.add_task(build)
ns.add_task(clean)
ns.add_task(install)
ns.add_task(uninstall)
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
    'logging': {
        'level': 'info'
    },
    'linux': {
        'wine_path': 'wine',
        'wine_prefix': ''
    },
    'processors': {
        'sound': {
            'generate_11khz': True,
            'generate_22khz': True
        }
    }
})