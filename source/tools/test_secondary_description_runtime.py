"""Retained exact-ROM secondary screenshot regression; not whole-game QA."""
import unittest
from report_secondary_chip_descriptions import prepare

class SecondaryRuntime(unittest.TestCase):
    def test_retained_native_secondary_pages_and_primary_regression(self):
        report=prepare()
        self.assertEqual(report['translated_units'],646)
        self.assertEqual(report['secondary_scripts_with_screenshot_pixels'],[0,1,7,16,22,29,88])
        self.assertEqual(len(report['normal_primary_description_regression']),4)
        self.assertEqual(report['cpu_vectors'],150)
        for page in report['secondary_pixels'].values():
            self.assertTrue(page['pixel_masks_match'])
            self.assertEqual(page['visible_cells'],27)
            colors=page['observed_role_colors']
            self.assertEqual(set(colors),{'1','3','4'})
            self.assertNotEqual(colors['1']['rgb'],colors['3']['rgb'])
