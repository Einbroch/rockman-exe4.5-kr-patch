import unittest
from report_roll_pet import ROOT,read,static
from tpl_literals import resolve_units,literals,skeleton
from build_development_patch import translate_literal_scope,selected_scope
from report_roll_minigame import main,STEM,PREFIX

class RollMinigameTests(unittest.TestCase):
    def test_88_scope_prior80_unchanged_and_source_commands(self):
        a=read(ROOT/'translations/roll_minigame_results_ko.json');u=resolve_units(a);base=resolve_units(read(ROOT/'translations/roll_fortune_results_ko.json'))
        self.assertEqual(u[:80],base);self.assertEqual(len(u),88)
        self.assertEqual({x['id'] for x in u[80:]},{'65FF3C:50:0','65FF3C:51:0','65FF3C:51:1','65FF3C:60:0','65FF3C:60:1','65FF3C:60:2','65FF3C:61:0','65FF3C:61:1'})
        scope=selected_scope(read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['65FF3C'],a)
        src=(ROOT/'analysis/tpl_baseline/65FF3C.tpl').read_text(encoding='utf-8-sig');dst=translate_literal_scope(src,u,scope)
        self.assertEqual(skeleton(src),skeleton(dst));ids={x['id'] for x in u};before={x.key:x.text for x in literals(src)};after={x.key:x.text for x in literals(dst)}
        self.assertEqual(len(before),109);self.assertTrue(all(before[k]==after[k] for k in before if k not in ids))
        m,rom,e,streams,c=static(STEM,'65FF3C');self.assertEqual(m['translated_units'],938);self.assertEqual(len(streams),88);self.assertEqual(len(c['protected_unselected_scripts']),40);self.assertTrue(c['all_fonts_verified'])
    def test_diagnostic_pixels_quarantined_and_coverage_partition(self):
        r=main();normal=set(r['normal_runtime_observed_units']);diagnostic=set(r['diagnostic_renderer_observed_units']);remaining=set(r['static_only_units'])
        self.assertTrue(r['passed']);self.assertFalse(r['release_eligible']);self.assertEqual(len(normal),23)
        self.assertEqual(diagnostic,{'65FF3C:50:0','65FF3C:60:0','65FF3C:60:1','65FF3C:60:2'});self.assertEqual(len(remaining),61)
        self.assertFalse(normal&diagnostic or normal&remaining or diagnostic&remaining);self.assertEqual(len(normal|diagnostic|remaining),88)
        self.assertTrue(all(p['font_vram_screen_pixels_match'] for p in r['pages']))
    def test_cumulative_exact_rom_regressions(self):
        from report_roll_intro import main as intro
        from report_roll_pet import main as pet
        from report_attack_caption_runtime import main as caption
        results=[intro(STEM,PREFIX+'roll-','roll_minigame_v1/greeting_regression'),pet(STEM,PREFIX,'roll_minigame_v1/pet_regression'),caption(STEM,PREFIX+'rockman-','roll_minigame_v1/rockman_regression'),caption(STEM,PREFIX+'roll-','roll_minigame_v1/roll_caption',roll=True)]
        self.assertTrue(all(r['passed'] for r in results));self.assertEqual(results[1]['translated_units'],938)

if __name__=='__main__':unittest.main()
