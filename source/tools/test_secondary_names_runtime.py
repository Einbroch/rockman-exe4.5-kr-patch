"""Retained exact-ROM secondary name pages; bounded diagnostic evidence."""
import unittest
from report_secondary_names_runtime import prepare

class SecondaryNamesRuntime(unittest.TestCase):
    def test_retained_secondary_names_and_primary_scroll(self):
        r=prepare()
        self.assertEqual(r['translated_units'],744)
        self.assertEqual(r['secondary_name_units'],98)
        self.assertEqual(r['native_slots_preserved'],39)
        self.assertEqual(r['sample_scripts'],[0,1,7,16,22,29,88])
        self.assertEqual(len(r['name_pixels']),8)
        self.assertEqual(len(r['primary_name_regression']),4)
        self.assertEqual(r['cpu_vectors'],{'library':34054,'folder':34058})
        for pages in (r['name_pixels'],r['primary_name_regression']):
            for cells in pages.values():
                self.assertTrue(all(c['pixel_masks_match'] for c in cells))
        for page in r['secondary_description_pixels'].values():
            self.assertTrue(page['pixel_masks_match'])
            self.assertEqual(page['visible_cells'],27)
