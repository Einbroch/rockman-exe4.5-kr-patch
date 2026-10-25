import unittest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from report_chip_library_matrix import ROOT, read, validate


class MatrixChecks(unittest.TestCase):
    def setUp(self):
        p = ROOT / 'poc/runtime/chip-matrix-h56-i7'
        self.d = read(p / 'final_timing.json')
        self.s = read(p / 'final_stress.json')

    def test_observed_gap(self):
        self.assertEqual(validate(self.d, self.s, 56, 7)['gap_after_group_1based'], [2])

    def test_missing_copy_rejected(self):
        self.d['copies'].pop()
        with self.assertRaises(ValueError):
            validate(self.d, self.s, 56, 7)

    def test_wrong_factor_rejected(self):
        with self.assertRaises(ValueError):
            validate(self.d, self.s, 0, 7)

    def test_clock_corruption_rejected(self):
        self.d['groups'][0]['cycles'] += 1
        with self.assertRaises(ValueError):
            validate(self.d, self.s, 56, 7)

    def test_descriptor_mutation_rejected(self):
        self.s['descriptors'][0]['after'] = '00'
        with self.assertRaises(ValueError):
            validate(self.d, self.s, 56, 7)
