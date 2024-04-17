import logging
import shutil
from invoke import task
from .build import build
from .config import prepare_config
from .sync import sync_dirs

logger = logging.getLogger(__name__)

# TODO allow specifying target bf1942 install
@task(build, help={'force': 'Force installation even if up-to-date'})
def install(c, force=False):
    '''Install mod to Battlefield 1942 Mods directory.'''

    install_path = c.bf1942.path / 'Mods' / c.mod.name

    if force:
        if install_path.exists():
            logger.info(f'delete existing files from {install_path}')
            shutil.rmtree(install_path)

        install_path.mkdir(parents=True)

    if sync_dirs(c.pack_path, install_path):
        logger.info(f'installed {c.mod.name} to {install_path}')
    else:
        logger.info(f'{c.mod.name} is up-to-date under {install_path}')

@task(prepare_config)
def uninstall(c):
    '''Uninstall mod from Battlefield 1942 Mods directory.'''

    install_path = c.bf1942.path / 'Mods' / c.mod.name

    if install_path.exists():
        logger.info(f'delete installed {c.mod.name} mod from {install_path}')
        shutil.rmtree(install_path)
    else:
        logger.info(f'{c.mod.name} is not installed at {install_path}')
