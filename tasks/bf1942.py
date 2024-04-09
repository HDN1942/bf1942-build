import platform

def run_bf1942(c, args, debug=True):
    exe_path = 'BF1942_r.exe' if debug is True else 'BF1942.exe'
    cmd = f'{exe_path} {args}'
    env = {}

    if platform.system() == 'Linux':
        cmd = f'{c.linux.wine_path} {cmd}'

        if len(c.linux.wine_prefix) > 0:
            env['WINE_PREFIX'] = c.linux.wine_prefix

    with c.cd(c.bf1942.path):
        c.run(cmd)
