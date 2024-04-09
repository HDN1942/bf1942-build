from invoke import task
from .config import prepare_config
from .bf1942 import run_bf1942

def write_maplist(c, level, gpm, mod):
    maplist_path = c.bf1942.path / 'Mods' / 'bf1942' / 'Settings' / 'maplist.con'

    with open(maplist_path, 'w') as maplist:
        maplist.write(f'game.addLevel {level} {gpm} {mod}\n')
        maplist.write(f'game.setCurrentLevel {level} {gpm} {mod}\n')

# TODO possible to auto complete level param?
# TODO save last level launched to temp config instead of relying on BF's built-in
@task(prepare_config)
def launch(c, level=None, gpm='GPM_COOP', mod=None, debug=True):
    # TODO validate params

    if mod is None:
        mod = c.mod.name

    if level is not None:
        write_maplist(c, level, gpm, mod)

    run_bf1942(c, '+hostServer 1 +restart 1', debug)
