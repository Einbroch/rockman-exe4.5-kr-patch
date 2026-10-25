import copy,unittest
from report_roll_pet import ROOT,read,static,sha
from tpl_literals import resolve_units,literals,skeleton
from build_development_patch import selected_scope,translate_literal_scope,validate_nickname_suffix
from report_roll_return import STEM,PREFIX,main

class RollReturnTests(unittest.TestCase):
    def test_four_literals_controls_fonts_and_cumulative_inputs(self):
        asset=read(ROOT/'translations/roll_return_ko.json');u=resolve_units(asset);source=(ROOT/'analysis/tpl_baseline/65FEC0.tpl').read_text(encoding='utf-8-sig');scope=selected_scope(read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['65FEC0'],asset)
        self.assertEqual(len(u),4);self.assertEqual({x.key for x in literals(source)},{x['id'] for x in u});self.assertEqual(skeleton(source),skeleton(translate_literal_scope(source,u,scope)))
        self.assertTrue(all(x['state']=='needs_review' and x['source'].count('\n')==x['translation'].count('\n') for x in u))
        m,rom,e,streams,c=static(STEM,'65FEC0');self.assertEqual(m['translated_units'],962);self.assertEqual(len(streams),4);self.assertEqual(len(c['protected_nonliteral_scripts']),2);self.assertTrue(c['all_fonts_verified']);self.assertEqual(c['max_literal_width'],103)
        old={x['path']:x['sha256'] for x in read(ROOT/'poc/output/exe45_ko_development_roll_jackin_v1.json')['translation_assets']};now={x['path']:x['sha256'] for x in m['translation_assets']};self.assertTrue(all(now[k]==v for k,v in old.items()))
        self.assertEqual(sha((ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes()),asset['source_sha256'])
    def test_configurable_second_literal_nickname_guard(self):
        asset=read(ROOT/'translations/roll_return_ko.json');u=resolve_units(asset);scope=selected_scope(read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['65FEC0'],asset);validate_nickname_suffix(u,'65FEC0',scope)
        bad=copy.deepcopy(u);next(x for x in bad if x['id']=='65FEC0:1:1')['translation']='야、\n수고했어!'
        with self.assertRaisesRegex(ValueError,'nickname'):validate_nickname_suffix(bad,'65FEC0',scope)
        pet=read(ROOT/'translations/roll_pet_menu_ko.json');s=selected_scope(read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['65FA58'],pet);validate_nickname_suffix(resolve_units(pet),'65FA58',s)
    def test_normal_two_pages_native_nickname_and_defeat_quarantine(self):
        r=main();self.assertTrue(r['passed']);self.assertFalse(r['release_eligible']);self.assertEqual(r['normal_runtime_units'],['65FEC0:1:0','65FEC0:1:1']);self.assertEqual(r['diagnostic_renderer_units'],['65FEC0:2:0','65FEC0:2:1'])
        self.assertTrue(all(p['font_vram_screen_pixels_match'] and p['vacant_text_pixels_cleared']>0 for p in r['pages']));self.assertEqual(next(p['nickname'] for p in r['pages'] if p['unit']=='65FEC0:1:1'),'ああくん');self.assertTrue(r['return_draws_stopped_after_exit'])
        p=ROOT/'poc/runtime'/(PREFIX+'defeat-diagnostic');self.assertFalse(read(p/'result.json')['normal_play_checkpoint_eligible']);self.assertFalse((p/'checkpoint.mss').exists());self.assertTrue((p/'diagnostic_checkpoint.mss').exists())
    def test_current_rom_regressions(self):
        from report_roll_intro import main as intro
        from report_roll_pet import main as pet
        from report_roll_fortune import main as fortune
        from report_attack_caption_runtime import main as caption
        reports=[intro(STEM,PREFIX+'roll-','roll_return_v1/greeting_regression'),pet(STEM,PREFIX,'roll_return_v1/pet_regression'),fortune(STEM,PREFIX,'roll_return_v1',('sample-97','sample-211','sample-389')),caption(STEM,PREFIX+'rockman-','roll_return_v1/rockman_regression'),caption(STEM,PREFIX+'roll-','roll_return_v1/roll_caption',roll=True)]
        self.assertTrue(all(r['passed'] for r in reports));self.assertTrue(all(r['rom_sha256']==reports[0]['rom_sha256'] for r in reports));self.assertEqual(reports[1]['translated_units'],962)

if __name__=='__main__':unittest.main()
