import logging
from invoke import task
from .config import prepare_config
from .bf1942 import run_bf1942

logger = logging.getLogger(__name__)

def write_maplist(c, level, gpm, mod):
    maplist_path = c.bf1942.path / 'Mods' / 'bf1942' / 'Settings' / 'maplist.con'

    logger.debug(f'update maplist.con with {level} {gpm} {mod}')
    logger.debug(f'write {maplist_path}')
    with open(maplist_path, 'w') as maplist:
        maplist.write(f'game.addLevel {level} {gpm} {mod}\n')
        maplist.write(f'game.setCurrentLevel {level} {gpm} {mod}\n')

# TODO should depend on deploy?
# TODO possible to auto complete level param?
# TODO save last level launched to temp config instead of relying on BF's built-in
@task(prepare_config)
def launch(c, level=None, gpm='GPM_COOP', mod=None, debug=True):
    # TODO validate params

    if mod is None:
        logger.debug(f'using default mod {c.mod.name}')
        mod = c.mod.name
    else:
        logger.debug(f'default mod overridden with {mod}')

    if level is not None:
        logger.debug(f'level set to {level}, update maplist.con')
        write_maplist(c, level, gpm, mod)
    else:
        logger.warn(f'level not specified, relying on existing values in Mods\\bf1942\\Settings\\maplist.con which may not be what you expect')

    logger.info('run Battlefield 1942')
    run_bf1942(c, '+hostServer 1 +restart 1', debug)
