import unittest
from copy import deepcopy
from report_roll_pet import ROOT,read,static
from tpl_literals import resolve_units,literals,skeleton
from build_development_patch import translate_literal_scope,selected_scope,validate_literal_numerals
from report_roll_fortune import main

STEM='exe45_ko_development_roll_fortune_v2'
PREFIX='roll-fortune-v2-'
SAMPLES=('sample-97','sample-211','sample-389')

class RollFortuneResultsTests(unittest.TestCase):
    def inputs(self):
        a=read(ROOT/'translations/roll_fortune_results_ko.json');u=resolve_units(a)
        return u,selected_scope(read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['65FF3C'],a)
    def test_all80_fonts_and44_protected_scripts(self):
        m,rom,expected,streams,r=static(STEM,'65FF3C')
        self.assertEqual(m['translated_units'],930);self.assertEqual(len(streams),80)
        self.assertEqual(len(r['protected_unselected_scripts']),44)
        self.assertTrue(r['all_fonts_verified']);self.assertLessEqual(r['max_literal_width'],132)
        u,s=self.inputs();base=resolve_units(read(ROOT/'translations/roll_fortune_intro_blue_ko.json'));byid={x['id']:x for x in u}
        self.assertTrue(all(byid[x['id']]==x for x in base));self.assertEqual(len(u)-len(base),67)
    def test_source_lines_controls_dots_and_deferred23(self):
        src=(ROOT/'analysis/tpl_baseline/65FF3C.tpl').read_text(encoding='utf-8-sig');u,s=self.inputs();dst=translate_literal_scope(src,u,s)
        self.assertEqual(skeleton(src),skeleton(dst));ids={x['id'] for x in u}
        before={x.key:x.text for x in literals(src)};after={x.key:x.text for x in literals(dst)}
        self.assertTrue(all(before[k]==after[k] for k in before if k not in ids))
        self.assertEqual(before['65FF3C:23:0'],after['65FF3C:23:0'])
        bad=deepcopy(u);bad[0]['source']='wrong source'
        with self.assertRaises(ValueError):translate_literal_scope(src,bad,s)
        bad=deepcopy(u);bad[-1]['translation']+='\nextra'
        with self.assertRaises(ValueError):translate_literal_scope(src,bad,s)
    def test_hint_numerals_and_range_notation_fail_closed(self):
        u,s=self.inputs();validate_literal_numerals(u,s)
        for source,target in [('1~4','1~5'),('1~4','1,4'),('1~4','4~1')]:
            bad=deepcopy(u);x=next(x for x in bad if x['id']=='65FF3C:20:0');x['translation']=x['translation'].replace(source,target)
            with self.assertRaises(ValueError):validate_literal_numerals(bad,s)
    def test_exact_rom_normal_pages_and_open_partition(self):
        r=main(STEM,PREFIX,'roll_fortune_v2',SAMPLES)
        self.assertTrue(r['passed']);self.assertFalse(r['release_eligible'])
        observed=set(r['runtime_observed_units']);opened=set(r['runtime_open_units'])
        self.assertIn('65FF3C:20:0',observed);self.assertFalse(observed&opened);self.assertEqual(len(observed|opened),80)
        self.assertTrue(r['page_vacancies_cleared']);self.assertTrue(all(p['font_vram_screen_pixels_match'] for p in r['pages']))
    def test_cumulative_greeting_pet_communication_and_equipment(self):
        from report_roll_intro import main as intro
        from report_roll_pet import main as pet
        from report_attack_caption_runtime import main as caption
        i=intro(STEM,PREFIX+'roll-','roll_fortune_v2/greeting_regression');p=pet(STEM,PREFIX,'roll_fortune_v2/pet_regression')
        rock=caption(STEM,PREFIX+'rockman-','roll_fortune_v2/rockman_regression');roll=caption(STEM,PREFIX+'roll-','roll_fortune_v2/roll_caption',roll=True)
        self.assertTrue(i['passed'] and p['passed'] and rock['passed'] and roll['passed'])
        self.assertEqual(p['translated_units'],930)

if __name__=='__main__':unittest.main()
