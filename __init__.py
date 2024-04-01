from invoke import Collection, task
from tasks.build import build
from tasks.deploy import deploy

ns = Collection()

ns.add_task(build)
ns.add_task(deploy)

ns.configure({
    'project_root': '..',
    'build_dir': 'build',
    'bf1942': {
        'path': 'C:\\Program Files (x86)\\EA Games\\Battlefield 1942'
    },
    'mod': {
        'name': 'MyMod',
        'base': 'BF1942',
        'version': '0.1.0',
        'url': 'https://example.net'
    }
})