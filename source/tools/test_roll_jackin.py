import unittest
from report_roll_pet import ROOT,read,static,sha
from tpl_literals import resolve_units,literals,skeleton
from build_development_patch import selected_scope,translate_literal_scope
from report_roll_jackin import STEM,PREFIX,main

class RollJackinTests(unittest.TestCase):
    def test_five_source_literals_controls_roundtrip_fonts(self):
        a=read(ROOT/'translations/roll_jackin_ko.json');u=resolve_units(a);source=(ROOT/'analysis/tpl_baseline/660CA8.tpl').read_text(encoding='utf-8-sig');scope=selected_scope(read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['660CA8'],a);translated=translate_literal_scope(source,u,scope)
        self.assertEqual(len(u),5);self.assertEqual({x.key for x in literals(source)},{x['id'] for x in u});self.assertEqual(skeleton(source),skeleton(translated))
        self.assertTrue(all(x['state']=='needs_review' and x['source'].count('\n')==x['translation'].count('\n') for x in u))
        m,rom,e,streams,c=static(STEM,'660CA8');self.assertEqual(m['translated_units'],958);self.assertEqual(len(streams),5);self.assertEqual(len(c['protected_nonliteral_scripts']),2);self.assertTrue(c['all_fonts_verified'])
        self.assertEqual(sha((ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes()),a['source_sha256'])
        ar=next(x for x in m['archives'] if x['archive']=='660CA8');self.assertEqual(max(max(x['line_advance_pixels']) for x in ar['layout']),123)
        previous=read(ROOT/'poc/output/exe45_ko_development_roll_location_v3.json');old={x['path']:x['sha256'] for x in previous['translation_assets']};now={x['path']:x['sha256'] for x in m['translation_assets']};self.assertTrue(all(now[k]==v for k,v in old.items()))
    def test_normal_confirmation_page_order_transmission_and_pixels(self):
        r=main();self.assertTrue(r['passed']);self.assertFalse(r['release_eligible']);self.assertEqual(r['normal_runtime_units'],['660CA8:1:0','660CA8:2:0','660CA8:2:1']);self.assertEqual([c['script'] for c in r['native_entry_order']],[2,1]);self.assertTrue(r['draws_stopped_after_transmission'])
        self.assertTrue(all(x['font_vram_screen_pixels_match'] and x['vacant_text_pixels_cleared']>0 for x in r['pages']));self.assertTrue(r['native_wait30_source_controls_preserved']);self.assertTrue(r['wait_cursor_samples']);self.assertLess(max(r['wait_cursor_samples']),min(r['post_wait_cursor_samples']))
        deferred=r['in_flight_snapshots_not_credited'];self.assertEqual(len(deferred),1);self.assertFalse(deferred[0]['credited_as_complete_page']);self.assertEqual((deferred[0]['step'],deferred[0]['later_pass_step']),(13,14));self.assertEqual(deferred[0]['changing_pixels'],10)
    def test_upbeat_diagnostic_two_pages_quarantine(self):
        r=main();self.assertEqual(r['diagnostic_renderer_units'],['660CA8:3:0','660CA8:3:1']);path=ROOT/'poc/runtime'/(PREFIX+'upbeat-diagnostic');receipt=read(path/'result.json');env=read(path/'upbeat_environment.json');self.assertFalse(receipt['normal_play_checkpoint_eligible']);self.assertFalse((path/'checkpoint.mss').exists());self.assertTrue((path/'diagnostic_checkpoint.mss').exists());self.assertEqual((env['native_script'],env['displayed_entry'],env['aliases']),(2,3,1))
    def test_same_new_rom_cumulative_regressions(self):
        from report_roll_intro import main as intro
        from report_roll_pet import main as pet
        from report_roll_fortune import main as fortune
        from report_attack_caption_runtime import main as caption
        reports=[intro(STEM,PREFIX+'roll-','roll_jackin_v1/greeting_regression'),pet(STEM,PREFIX,'roll_jackin_v1/pet_regression'),fortune(STEM,PREFIX,'roll_jackin_v1',('sample-97','sample-211','sample-389')),caption(STEM,PREFIX+'rockman-','roll_jackin_v1/rockman_regression'),caption(STEM,PREFIX+'roll-','roll_jackin_v1/roll_caption',roll=True)]
        self.assertTrue(all(x['passed'] for x in reports));self.assertTrue(all(x['rom_sha256']==reports[0]['rom_sha256'] for x in reports));self.assertEqual(reports[1]['translated_units'],958)

if __name__=='__main__':unittest.main()
