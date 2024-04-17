import logging
import shutil
from invoke import task
from .build import build
from .sync import sync_dirs

logger = logging.getLogger(__name__)

# TODO allow specifying target bf1942 install
@task(build)
def deploy(c, force=False):
    deploy_path = c.bf1942.path / 'Mods' / c.mod.name

    if force:
        if deploy_path.exists():
            logger.info(f'removing existing files from {deploy_path}')
            shutil.rmtree(deploy_path)

        deploy_path.mkdir(parents=True)

    sync_dirs(c.pack_path, deploy_path)
    logger.info(f'deployed {c.mod.name} to {deploy_path}')
