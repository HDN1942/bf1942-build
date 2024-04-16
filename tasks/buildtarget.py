import re
from pathlib import Path
from tasks.sync import sync_dirs

class BuildTarget:
    full_name_re = re.compile('^([^_]+)(_\d{3})?$', re.IGNORECASE)

    def __init__(self, c, path):
        '''Creates a BuildTarget instance.

        Args:
            c: The invoke context.
            path: The non-rooted path under the project root src directory.
                ie. objects, texture_001, bf1942/levels/Guadalcanal
        '''

        path = Path(path)

        self.full_name = path.name
        '''Full name of archive.

        Example:
        objects
        texture_001
        Guadalcanal
        '''

        match = self.full_name_re.match(self.full_name)
        if not match:
            raise ValueError(f'invalid path "{path}"')

        self.name = match.group(1)
        '''Name of build target.

        Example:
        objects
        texture
        Guadalcanal'''

        self.extension = match.group(2)
        '''Archive extension. Will be None if there is no extension.

        Example:
        _001
        _002'''

        self.base_path = path.parent / self.name
        '''Base path within RFA.

        Example:
        objects
        texture
        bf1942/levels/Guadalcanal'''

        self._src_path = c.src_path / path
        self._c_build_path = c.build_path
        self._build_src_path = self._c_build_path / 'src' / self.full_name / self.base_path
        self._build_process_path = self._c_build_path / 'process' / self.full_name / self.base_path

        self.work_path = self._build_src_path
        '''Working directory under build path.'''

        self.work_base_path = self._c_build_path / 'src' / self.full_name
        '''Base path of working directory under build path.'''

        self.rfa_file = c.pack_path / 'Archives' / path.parent / f'{self.full_name}.rfa'
        '''Path to archive under pack directory.

        Example:
        [project_root]/build/pack/Archives/objects.rfa
        [project_root]/build/pack/Archives/texture_001.rfa
        [project_root]/build/pack/Archives/bf1942/levels/Guadalcanal.rfa'''

        self.up_to_date = None
        '''Whether build target is up-to-date.'''

        self.processed = False
        ''' Whether build target has been processed.'''

    def sync(self):
        self.up_to_date = not sync_dirs(self._src_path, self._build_src_path)

    def setup_for_process(self):
        sync_dirs(self._build_src_path, self._build_process_path)

        self.work_path = self._build_process_path
        self.work_base_path = self._c_build_path / 'process' / self.full_name
        self.processed = True
