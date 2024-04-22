import unittest
from invoke import config, MockContext
from pathlib import Path
from unittest.mock import patch, MagicMock
from tasks.build import sync_targets
from tasks.buildtarget import BuildTarget

class SyncTargetsTest(unittest.TestCase):
    def setUp(self):
        self.c = MockContext({
            'src_path': Path('src'),
            'build_path': Path('build'),
            'pack_path': Path('pack'),
            'build': config.DataProxy.from_data({
                'targets': []
            })
        })

    def test_syncs_each_target(self):
        target1 = BuildTarget(self.c, 'foo')
        target1.sync = MagicMock()
        target1.up_to_date = True
        self.c.build.targets.append(target1)

        target2 = BuildTarget(self.c, 'bar')
        target2.sync = MagicMock()
        target2.up_to_date = False
        self.c.build.targets.append(target2)

        sync_targets(self.c)

        target1.sync.assert_called_once()
        target2.sync.assert_called_once()

        self.assertListEqual([target2], self.c.build.out_of_date)
        self.assertFalse(self.c.build.all_up_to_date)

    def test_sets_all_up_to_date(self):
        target1 = BuildTarget(self.c, 'foo')
        target1.sync = MagicMock()
        target1.up_to_date = True
        self.c.build.targets.append(target1)

        target2 = BuildTarget(self.c, 'bar')
        target2.sync = MagicMock()
        target2.up_to_date = True
        self.c.build.targets.append(target2)

        sync_targets(self.c)

        self.assertListEqual([], self.c.build.out_of_date)
        self.assertTrue(self.c.build.all_up_to_date)

if __name__ == '__main__':
    unittest.main()