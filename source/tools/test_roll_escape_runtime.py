import unittest
import json
from report_roll_escape_runtime import prepare
from report_chip_library_runtime import read
from build_visibility_poc import ROOT

class RollEscapeRuntime(unittest.TestCase):
    def test_retained_exact_rom_pixels_and_native_obj_flash(self):
        r=json.loads(json.dumps(prepare()));self.assertEqual(r,read(ROOT/'analysis/exe45_roll_escape_runtime_v1.json'))
        self.assertEqual(r['translated_units'],756);self.assertEqual(r['preserved_other_navi_scripts'],134)
        self.assertEqual(len(r['escape_pixels']),22);self.assertEqual(len(r['clear_and_return']),16)
        for name in ['roll-confirm-sample','roll-success-sample','roll-failure-sample','roll-forbidden-sample']:
            self.assertTrue(r['routes'][name]['diagnostic'])
        delta=r['clear_and_return']['roll-confirm-sample:8']['native_obj_animation_delta']
        self.assertFalse(delta['full_mask_match']);self.assertTrue(delta['outside_native_obj_mask_matches'])
        self.assertEqual(delta['native_obj_delta_pixels'],130)
        self.assertEqual(delta['outside_dialogue_roi_calibration_pixels'],65)
        self.assertEqual(delta['frontmost_obj_owners'],{'14':125,'16':5})
