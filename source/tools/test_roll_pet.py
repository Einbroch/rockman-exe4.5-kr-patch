import unittest
from copy import deepcopy
from build_development_patch import validate_nickname_suffix
from report_roll_pet import ROOT,read,static,main
from tpl_literals import resolve_units

class RollPetTests(unittest.TestCase):
    def test_complete44_literal_static_font_and_nonliteral_preservation(self):
        m,rom,expected,streams,r=static('exe45_ko_development_roll_pet_v2')
        self.assertEqual(m['translated_units'],845);self.assertEqual(len(streams),44);self.assertEqual(len(r['protected_nonliteral_scripts']),6)
        self.assertTrue(r['all_fonts_verified']);self.assertTrue(r['nickname_first_line_bytes_unchanged']);self.assertLessEqual(r['max_literal_width'],132)
    def test_product_build_rejects_nickname_suffix_change(self):
        units=resolve_units(read(ROOT/'translations/roll_pet_menu_ko.json'));scope=read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['65FA58']
        validate_nickname_suffix(units,'65FA58',scope)
        for text in [',\n뭘 할까?','아,\n뭘 할까?','는\n뭘 할까?']:
            bad=deepcopy(units);bad[0]['translation']=text
            with self.assertRaises(ValueError):validate_nickname_suffix(bad,'65FA58',scope)
    def test_normal_roll_pet_full_glyph_pixels_choice_behavior_and_open_partition(self):
        r=main();self.assertTrue(r['passed']);self.assertFalse(r['release_eligible']);self.assertEqual(len(r['runtime_observed_units']),22);self.assertEqual(len(r['runtime_open_units']),22)
        self.assertEqual(len(r['choice_behavior']),29);self.assertTrue(all(p['font_vram_screen_pixels_match'] and p['no_translated_ink_occluded'] for p in r['pages']))
    def test_exact_cumulative_rockman_roll_caption_guides_and_pet_graphics(self):
        from report_attack_caption_runtime import main as report
        rock=report('exe45_ko_development_roll_pet_v2','roll-pet-v2-rockman-','roll_pet_v2/rockman_regression')
        roll=report('exe45_ko_development_roll_pet_v2','roll-pet-v2-roll-','roll_pet_v2/roll_caption',roll=True)
        self.assertTrue(rock['passed'] and roll['passed']);self.assertEqual(roll['translated_text_units'],845)

if __name__=='__main__':unittest.main()
