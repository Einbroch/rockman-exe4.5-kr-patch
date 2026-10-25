import copy,unittest
from pathlib import Path
from report_roll_pet import ROOT,read,static
from tpl_literals import resolve_units,literals,skeleton
from build_development_patch import selected_scope,translate_literal_scope,validate_nickname_suffix,validate_characters
from run_roll_family_sisters import STEM

class RollFamilySistersTests(unittest.TestCase):
    def test_source_scope_previous_wording_and_build_guards(self):
        a=read(ROOT/'translations/roll_family_sisters_ko.json');u=resolve_units(a);old=resolve_units(read(ROOT/'translations/roll_family_sister_ko.json'));s=selected_scope(read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['661858'],a);src=(ROOT/'analysis/tpl_baseline/661858.tpl').read_text(encoding='utf-8-sig');target=translate_literal_scope(src,u,s)
        self.assertEqual(u[8:],old);self.assertEqual(len(u),16);self.assertEqual(skeleton(src),skeleton(target));self.assertEqual({x['id'] for x in u},{x.key for x in literals(src) if int(x.key.split(':')[1]) in [5,6,7,8]});validate_nickname_suffix(u,'661858',s)
        for index in [3,11]:
            bad=copy.deepcopy(u);bad[index]['translation']='는、\n있어?'
            with self.assertRaisesRegex(ValueError,'nickname'):validate_nickname_suffix(bad,'661858',s)
        layout=validate_characters(target,ROOT/'poc/work/roll_family_sisters_v1/plugins/exe45-utf8.tbl',s,{x['id'] for x in u});self.assertEqual([x['choice_row_advance_pixels'] for x in layout if 'choice_row_advance_pixels' in x],[96,96])
        bad=copy.deepcopy(u);bad[4]['translation']='가'*8+'  '
        with self.assertRaisesRegex(ValueError,'standalone choice row exceeds'):validate_characters(translate_literal_scope(src,bad,s),ROOT/'poc/work/roll_family_sisters_v1/plugins/exe45-utf8.tbl',s,{x['id'] for x in bad})
        m,rom,e,streams,c=static(STEM,'661858');self.assertEqual(m['translated_units'],982);self.assertEqual(len(streams),16);self.assertEqual(len(c['protected_nonliteral_scripts']),93);self.assertTrue(c['all_fonts_verified']);self.assertEqual(c['max_literal_width'],123)
        before={x['path']:x['sha256'] for x in read(ROOT/'poc/output/exe45_ko_development_roll_family_sister_v1.json')['translation_assets'] if Path(x['path']).name!='roll_family_sister_ko.json'};now={x['path']:x['sha256'] for x in m['translation_assets']};self.assertTrue(all(now[k]==v for k,v in before.items()))
    def test_normal_both_sister_scenes_and_cumulative_runtime(self):
        from report_roll_family_sisters import main
        reports=main();self.assertEqual(len(reports),9)
        for r in reports[:2]:
            self.assertEqual(len(r['normal_runtime_units']),8);self.assertTrue(r['defaultYes_rightNo_leftYes']);self.assertTrue(r['name_question_stopped_before_input_init']);self.assertTrue(all(p['font_vram_screen_pixels_match'] and p['no_translated_ink_occluded'] for p in r['pages']))

if __name__=='__main__':unittest.main()
