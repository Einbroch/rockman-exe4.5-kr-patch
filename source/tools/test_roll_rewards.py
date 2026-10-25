import unittest
from copy import deepcopy
from report_roll_pet import ROOT,read,static
from tpl_literals import literals,resolve_units,skeleton
from build_development_patch import selected_scope,translate_literal_scope
from roll_reward_model import model,validate_layout
from report_roll_rewards import main,STEM,PREFIX

class RollRewardTests(unittest.TestCase):
    def inputs(self):
        a=read(ROOT/'translations/roll_minigame_rewards_ko.json');s=selected_scope(read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['65FF3C'],a)
        return a,s,(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes()
    def test_102_source_scope_prior88_and_roundtrips(self):
        a,s,source=self.inputs();u=resolve_units(a);base=resolve_units(read(ROOT/'translations/roll_minigame_results_ko.json'));self.assertEqual(u[:88],base);self.assertEqual(len(u),102)
        src=(ROOT/'analysis/tpl_baseline/65FF3C.tpl').read_text(encoding='utf-8-sig');dst=translate_literal_scope(src,u,s);self.assertEqual(skeleton(src),skeleton(dst));before={x.key:x.text for x in literals(src)};after={x.key:x.text for x in literals(dst)};ids={x['id'] for x in u}
        self.assertEqual(len(before),109);self.assertEqual({k for k in before if k not in ids},{'65FF3C:23:0','65FF3C:0:4','65FF3C:0:5','65FF3C:0:6','65FF3C:1:3','65FF3C:1:4','65FF3C:1:5'});self.assertTrue(all(before[k]==after[k] for k in before if k not in ids))
        m,rom,e,streams,c=static(STEM,'65FF3C');self.assertEqual(m['translated_units'],952);self.assertEqual(len(streams),102);self.assertEqual(len(c['protected_unselected_scripts']),36);self.assertTrue(c['all_fonts_verified'])
    def test_bonus_bound_and_composed_overflow_fail_closed(self):
        a,s,source=self.inputs();proof=model(source);self.assertEqual(max(proof['zenny_values']),800);self.assertEqual(max(proof['bugfrag_values']),5)
        m=read(ROOT/f'poc/output/{STEM}.json');ar=next(a for a in m['archives'] if a['archive']=='65FF3C');p=validate_layout(source,deepcopy(ar['layout']),s)
        self.assertEqual([x['composed_line_advance'] for x in p['composed_lines']],[69,91,69,91])
        bad=deepcopy(ar['layout']);next(x for x in bad if x['id']=='65FF3C:53:2')['line_advance_pixels']=[120]
        with self.assertRaises(ValueError):validate_layout(source,bad,s)
        bad=bytearray(source);bad[0x362C4]^=1
        with self.assertRaises(ValueError):model(bytes(bad))
    def test_all14_diagnostic_number_pixels_and_partition(self):
        r=main();n=set(r['normal_runtime_observed_units']);d=set(r['diagnostic_renderer_observed_units']);s=set(r['static_only_units'])
        self.assertTrue(r['passed']);self.assertFalse(r['release_eligible']);self.assertEqual((len(n),len(d),len(s)),(23,14,65));self.assertFalse(n&d or n&s or d&s);self.assertEqual(len(n|d|s),102)
        numeric=[p for p in r['pages'] if p['numeric']];self.assertEqual(len({p['route'] for p in numeric}),4);self.assertEqual({p['numeric']['value'] for p in numeric},{800,5});self.assertTrue(all(p['font_vram_screen_pixels_match'] and p['numeric']['native_ram_codes_verified'] for p in numeric))
    def test_cumulative_exact_rom_regressions(self):
        from report_roll_intro import main as intro
        from report_roll_pet import main as pet
        from report_attack_caption_runtime import main as caption
        reports=[intro(STEM,PREFIX+'roll-','roll_rewards_v2/greeting_regression'),pet(STEM,PREFIX,'roll_rewards_v2/pet_regression'),caption(STEM,PREFIX+'rockman-','roll_rewards_v2/rockman_regression'),caption(STEM,PREFIX+'roll-','roll_rewards_v2/roll_caption',roll=True)]
        self.assertTrue(all(r['passed'] for r in reports));self.assertEqual(reports[1]['translated_units'],952)

if __name__=='__main__':unittest.main()
