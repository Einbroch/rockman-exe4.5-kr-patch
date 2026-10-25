import unittest
from copy import deepcopy
from report_roll_pet import ROOT,read,static
from tpl_literals import resolve_units,literals,skeleton
from build_development_patch import translate_literal_scope
from report_roll_fortune import main,STEM,PREFIX

class RollFortuneTests(unittest.TestCase):
    def test_13_literals_fonts_62_unselected_scripts(self):
        m,rom,expected,streams,r=static(STEM,'65FF3C')
        self.assertEqual(m['translated_units'],863);self.assertEqual(len(streams),13)
        self.assertEqual(len(r['protected_unselected_scripts']),62)
        self.assertTrue(r['all_fonts_verified']);self.assertLessEqual(r['max_literal_width'],132)
    def test_source_controls_and_all_six_dots_preserved(self):
        src=(ROOT/'analysis/tpl_baseline/65FF3C.tpl').read_text(encoding='utf-8-sig');units=resolve_units(read(ROOT/'translations/roll_fortune_intro_blue_ko.json'));scope=read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['65FF3C']
        dst=translate_literal_scope(src,units,scope);self.assertEqual(skeleton(src),skeleton(dst))
        dots=[x for x in literals(src) if x.text=='・'];self.assertEqual(len(dots),6)
        self.assertTrue(all(x.text==next(y.text for y in literals(dst) if y.key==x.key) for x in dots))
        bad=deepcopy(units);bad[0]['source']='wrong source'
        with self.assertRaises(ValueError):translate_literal_scope(src,bad,scope)
        bad=deepcopy(units);bad[0]['translation']+='\nextra'
        with self.assertRaises(ValueError):translate_literal_scope(src,bad,scope)
    def test_normal_9_pages_and_repeat_4_static_only(self):
        r=main();self.assertTrue(r['passed']);self.assertFalse(r['release_eligible'])
        self.assertEqual(len(r['runtime_observed_units']),9);self.assertEqual(len(r['runtime_open_units']),4)
        self.assertTrue(r['timed_dot_pacing']);self.assertTrue(r['page_vacancies_cleared'])
        self.assertTrue(all(p['font_vram_screen_pixels_match'] for p in r['pages']))
    def test_exact_rom_cumulative_regressions(self):
        from report_roll_intro import main as intro
        from report_roll_pet import main as pet
        from report_attack_caption_runtime import main as caption
        i=intro(STEM,PREFIX+'roll-','roll_fortune_v1/greeting_regression');p=pet(STEM,PREFIX,'roll_fortune_v1/pet_regression')
        rock=caption(STEM,PREFIX+'rockman-','roll_fortune_v1/rockman_regression');roll=caption(STEM,PREFIX+'roll-','roll_fortune_v1/roll_caption',roll=True)
        self.assertTrue(i['passed'] and p['passed'] and rock['passed'] and roll['passed'])
        self.assertTrue(i['exit']['next_dialogue_partially_translated']);self.assertEqual(p['translated_units'],863)

if __name__=='__main__':unittest.main()
