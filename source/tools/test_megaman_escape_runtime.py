"""Retained exact-ROM escaped-dialogue screens and bounded regressions."""
import unittest
from report_megaman_escape_runtime import prepare

class EscapeRuntime(unittest.TestCase):
    def test_native_forbidden_and_diagnostic_pages(self):
        r=prepare()
        self.assertEqual(r['translated_units'],750)
        self.assertEqual(r['new_escape_literals'],6)
        self.assertEqual(r['preserved_other_navi_scripts'],138)
        self.assertEqual(len(r['escape_pixels']),11)
        self.assertEqual(len(r['folder_regression']),4)
        self.assertEqual(len(r['clear_and_return']),8)
        self.assertEqual(set(r['tactics_regression']),{'target','distance'})
        self.assertFalse(r['routes']['l-target']['diagnostic'])
        for p in r['escape_pixels'].values():
            self.assertTrue(p['pixel_masks_match'])
            self.assertTrue(all(c['pixel_masks_match'] for c in p['normal_draws']))
            if p['script']==2:self.assertFalse(p['choice_cursor']['pixel_roles_verified'])
