import unittest
from report_roll_pet import ROOT,read,static,sha
from tpl_literals import resolve_units,literals,skeleton
from build_development_patch import selected_scope,translate_literal_scope
from report_roll_location_hint import STEM,PREFIX,main as hint

class RollLocationTests(unittest.TestCase):
    def test_103_scope_prior102_source_controls_and_dots(self):
        a=read(ROOT/'translations/roll_fortune_complete_ko.json');u=resolve_units(a);base=resolve_units(read(ROOT/'translations/roll_minigame_rewards_ko.json'))
        self.assertEqual(u[:102],base);self.assertEqual(len(u),103);self.assertEqual(u[-1]['id'],'65FF3C:23:0')
        src=(ROOT/'analysis/tpl_baseline/65FF3C.tpl').read_text(encoding='utf-8-sig');scope=selected_scope(read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['65FF3C'],a);dst=translate_literal_scope(src,u,scope)
        self.assertEqual(skeleton(src),skeleton(dst));remaining={x.key:x.text for x in literals(src) if x.key not in {v['id'] for v in u}}
        self.assertEqual(len(remaining),6);self.assertEqual(set(remaining.values()),{'・'})
        m,rom,e,s,c=static(STEM,'65FF3C');self.assertEqual(m['translated_units'],953);self.assertEqual(len(s),103);self.assertEqual(len(c['protected_unselected_scripts']),35)
        ar=next(a for a in m['archives'] if a['archive']=='65FF3C');self.assertEqual(next(x for x in ar['layout'] if x['id']=='65FF3C:23:0')['line_advance_pixels'],[92,132,79])
        source=ROOT/read(ROOT/'project.json')['source_profile']['filename'];self.assertEqual(sha(source.read_bytes()),a['source_sha256'])
    def test_native_jump_clear_pixels_and_quarantine(self):
        r=hint();self.assertTrue(r['passed']);self.assertFalse(r['release_eligible']);self.assertEqual(r['diagnostic_units'],['65FF3C:23:0'])
        self.assertTrue(all(p['font_vram_screen_pixels_match'] and p['vacant_text_pixels_cleared']>0 for p in r['pages']))
        e=r['native_clear'];self.assertEqual((e['aliases'],e['jumps']),(1,1));self.assertEqual(len(e['clears']),1);self.assertEqual(e['clears'][0]['checked_bytes'],7680);self.assertEqual(e['clears'][0]['nonzero_bytes'],0)
    def test_exact_new_rom_normal_and_bonus_partition(self):
        from report_roll_fortune import main as fortune
        from report_roll_rewards import main as reward
        n=fortune(STEM,PREFIX,'roll_location_v3',('sample-97','sample-211','sample-389'));b=reward(STEM,PREFIX,'roll_location_v3');h=hint()
        normal=set(n['runtime_observed_units']);diagnostic=set(b['diagnostic_renderer_observed_units'])|set(h['diagnostic_units']);static_only=set(b['static_only_units'])-diagnostic
        self.assertEqual((len(normal),len(diagnostic),len(static_only)),(23,15,65));self.assertFalse(normal&diagnostic or normal&static_only or diagnostic&static_only);self.assertEqual(len(normal|diagnostic|static_only),103)
        self.assertEqual(len({x['numeric']['value'] for x in b['pages'] if x['numeric']}),2)
    def test_exact_new_rom_cumulative_regressions(self):
        from report_roll_intro import main as intro
        from report_roll_pet import main as pet
        from report_attack_caption_runtime import main as caption
        reports=[intro(STEM,PREFIX+'roll-','roll_location_v3/greeting_regression'),pet(STEM,PREFIX,'roll_location_v3/pet_regression'),caption(STEM,PREFIX+'rockman-','roll_location_v3/rockman_regression'),caption(STEM,PREFIX+'roll-','roll_location_v3/roll_caption',roll=True)]
        self.assertTrue(all(x['passed'] for x in reports));self.assertTrue(all(x['rom_sha256']==reports[0]['rom_sha256'] for x in reports));self.assertEqual(reports[1]['translated_units'],953)

if __name__=='__main__':unittest.main()
