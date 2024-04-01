import shutil
from invoke import task
from tasks.build import build

# TODO allow specifying target bf1942 install
@task(build)
def deploy(c):
    deploy_path = c.bf1942.path / 'Mods' / c.mod.name

    if deploy_path.exists():
        shutil.rmtree(deploy_path)
    shutil.copytree(c.pack_path, deploy_path)

