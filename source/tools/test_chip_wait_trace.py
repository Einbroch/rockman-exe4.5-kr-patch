import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from report_chip_wait_trace import summarize


class WaitTraceTests(unittest.TestCase):
    def fixture(self):
        return [dict(pc=pc, group=2, clock=t, frame=10, scanline=160) for pc, t in
                [(0x08000374, 100), (0x08000380, 121), (0x08000344, 141), (0x08000360, 200)]]

    def test_durations(self):
        r = summarize(self.fixture())
        self.assertEqual((r['wait_non_vblank_clocks'], r['wait_vblank_clocks']), (21, 59))

    def test_missing_boundary(self):
        with self.assertRaises(ValueError):
            summarize(self.fixture()[:-1])

    def test_clock_reversal(self):
        d = self.fixture()
        d[-1]['clock'] = 50
        with self.assertRaises(ValueError):
            summarize(d)
