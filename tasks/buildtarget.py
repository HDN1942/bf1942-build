import re
from pathlib import Path
from tasks.sync import sync_dirs

class BuildTarget:
    extension_re = re.compile('_\d{3}$')

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

        self.name = None
        '''Name of build target.

        Example:
        objects
        texture
        Guadalcanal'''

        self.extension = None
        '''Archive extension. Will be None if there is no extension.

        Example:
        _001
        _002'''

        match = self.extension_re.search(self.full_name)
        if match:
            self.extension = match.group(0)
            self.name = self.full_name.removesuffix(self.extension)
        else:
            self.name = self.full_name

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

    def __str__(self):
        return self.full_name
