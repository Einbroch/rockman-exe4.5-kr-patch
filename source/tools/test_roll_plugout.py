import copy,unittest
from report_roll_pet import ROOT,read,static,sha
from tpl_literals import resolve_units,literals,skeleton
from build_development_patch import selected_scope,translate_literal_scope,validate_nickname_suffix,validate_characters
from report_roll_plugout import STEM,PREFIX,main

class RollPlugoutTests(unittest.TestCase):
    def test_four_source_literals_44_other_scripts_and_fonts(self):
        a=read(ROOT/'translations/roll_plugout_ko.json');u=resolve_units(a);src=(ROOT/'analysis/tpl_baseline/778338.tpl').read_text(encoding='utf-8-sig');s=selected_scope(read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['778338'],a);target=translate_literal_scope(src,u,s)
        self.assertEqual(len(u),4);self.assertEqual({x['id'] for x in u},{x.key for x in literals(src) if int(x.key.split(':')[1]) in [6,26]});self.assertEqual(skeleton(src),skeleton(target));self.assertTrue(all(x['state']=='needs_review' and x['source'].count('\n')==x['translation'].count('\n') for x in u))
        m,rom,e,streams,c=static(STEM,'778338');self.assertEqual(m['translated_units'],966);self.assertEqual(len(streams),4);self.assertEqual(len(c['protected_nonliteral_scripts']),44);self.assertTrue(c['all_fonts_verified']);self.assertLessEqual(c['max_literal_width'],132)
        self.assertEqual(sha((ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes()),a['source_sha256'])
        old={x['path']:x['sha256'] for x in read(ROOT/'poc/output/exe45_ko_development_roll_return_v1.json')['translation_assets']};now={x['path']:x['sha256'] for x in m['translation_assets']};self.assertTrue(all(now[k]==v for k,v in old.items()))
    def test_build_nickname_and_empty_selection_row_guards(self):
        a=read(ROOT/'translations/roll_plugout_ko.json');u=resolve_units(a);s=selected_scope(read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['778338'],a);src=(ROOT/'analysis/tpl_baseline/778338.tpl').read_text(encoding='utf-8-sig');tbl=ROOT/'poc/work/roll_plugout_v1/plugins/exe45-utf8.tbl'
        validate_nickname_suffix(u,'778338',s);layout=validate_characters(translate_literal_scope(src,u,s),tbl,s,{x['id'] for x in u});self.assertTrue(layout[0]['choice_runtime_check_required']);self.assertLessEqual(layout[0]['choice_row_advance_pixels'],132)
        bad=copy.deepcopy(u);bad[0]['translation']='야、\n플러그아웃할까?\n'
        with self.assertRaisesRegex(ValueError,'nickname'):validate_nickname_suffix(bad,'778338',s)
        bad=copy.deepcopy(u);bad[0]['translation']='、\n플러그아웃할까?'
        with self.assertRaisesRegex(ValueError,'line/choice-padding|selection row'):validate_characters(translate_literal_scope(src,bad,s),tbl,s,{x['id'] for x in bad})
    def test_normal_no_cancel_yes_response_and_nickname_pixels(self):
        r=main();self.assertTrue(r['passed']);self.assertFalse(r['release_eligible']);self.assertEqual(r['normal_runtime_units'],['778338:26:0','778338:6:0','778338:6:1','778338:6:2']);self.assertTrue(r['defaultNo_leftYes_rightNo'] and r['No_and_B_no_response_draw'] and r['Yes_response_to_normal_return']);self.assertTrue(all(p['font_vram_screen_pixels_match'] and p['no_translated_ink_occluded'] and p['vacant_text_pixels_cleared']>0 for p in r['pages']));self.assertTrue(all(p['nickname']=='ああくん' for p in r['pages'] if p['script']==6))
    def test_current_rom_return_and_cumulative_regressions(self):
        import report_roll_return as ret
        old=ret.STEM,ret.PREFIX
        try:
            ret.STEM,ret.PREFIX=STEM,PREFIX;r=ret.main('roll_plugout_v1/return_regression')
        finally:ret.STEM,ret.PREFIX=old
        self.assertTrue(r['passed'] and r['return_draws_stopped_after_exit']);self.assertEqual(len(r['normal_runtime_units']),2);self.assertEqual(len(r['diagnostic_renderer_units']),2)
        from report_roll_intro import main as intro
        from report_roll_pet import main as pet
        from report_roll_fortune import main as fortune
        from report_attack_caption_runtime import main as caption
        reports=[intro(STEM,PREFIX+'roll-','roll_plugout_v1/greeting_regression'),pet(STEM,PREFIX,'roll_plugout_v1/pet_regression'),fortune(STEM,PREFIX,'roll_plugout_v1',('sample-97','sample-211','sample-389')),caption(STEM,PREFIX+'rockman-','roll_plugout_v1/rockman_regression'),caption(STEM,PREFIX+'roll-','roll_plugout_v1/roll_caption',roll=True)]
        self.assertTrue(all(x['passed'] and x['rom_sha256']==r['rom_sha256'] for x in reports));self.assertEqual(reports[1]['translated_units'],966)

if __name__=='__main__':unittest.main()
