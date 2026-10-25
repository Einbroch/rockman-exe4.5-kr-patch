import unittest
from copy import deepcopy
from report_roll_pet import ROOT,read,static
from tpl_literals import resolve_units,skeleton
from build_development_patch import translate_literal_scope
from report_roll_intro import main

class RollIntroTests(unittest.TestCase):
    def test_all5_literals_font_and_two_nonliteral_slots(self):
        m,rom,expected,streams,r=static('exe45_ko_development_roll_intro_v1','65F9AC')
        self.assertEqual(m['translated_units'],850);self.assertEqual(len(streams),5);self.assertEqual(len(r['protected_nonliteral_scripts']),2)
        self.assertTrue(r['all_fonts_verified']);self.assertLessEqual(r['max_literal_width'],132)
    def test_source_and_line_controls_fail_closed(self):
        original=(ROOT/'analysis/tpl_baseline/65F9AC.tpl').read_text(encoding='utf-8-sig');units=resolve_units(read(ROOT/'translations/roll_intro_ko.json'));scope=read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['65F9AC']
        self.assertEqual(skeleton(original),skeleton(translate_literal_scope(original,units,scope)))
        bad=deepcopy(units);bad[0]['source']='wrong source'
        with self.assertRaises(ValueError):translate_literal_scope(original,bad,scope)
        bad=deepcopy(units);bad[0]['translation']+='\nextra'
        with self.assertRaises(ValueError):translate_literal_scope(original,bad,scope)
    def test_normal_first_meeting_pixels_clearing_and_unverified_branch_partition(self):
        r=main();self.assertTrue(r['passed']);self.assertFalse(r['release_eligible']);self.assertTrue(r['previous_page_cleared'])
        self.assertEqual(len(r['runtime_observed_units']),2);self.assertEqual(len(r['runtime_open_units']),3)
        self.assertTrue(all(p['font_vram_screen_pixels_match'] for p in r['pages']))
    def test_exact_rom_cumulative_pet_graphics_weapons_and_guides(self):
        from report_roll_pet import main as pet
        from report_attack_caption_runtime import main as caption
        p=pet('exe45_ko_development_roll_intro_v1','roll-intro-v1-','roll_intro_v1/pet_regression')
        rock=caption('exe45_ko_development_roll_intro_v1','roll-intro-v1-rockman-','roll_intro_v1/rockman_regression')
        roll=caption('exe45_ko_development_roll_intro_v1','roll-intro-v1-roll-','roll_intro_v1/roll_caption',roll=True)
        self.assertTrue(p['passed'] and rock['passed'] and roll['passed']);self.assertEqual(p['translated_units'],850)

if __name__=='__main__':unittest.main()
