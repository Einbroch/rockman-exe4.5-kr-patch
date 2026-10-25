import copy,unittest
from pathlib import Path
from report_roll_pet import ROOT,read,static
from tpl_literals import resolve_units,literals,skeleton
from build_development_patch import selected_scope,translate_literal_scope,validate_nickname_suffix,validate_characters
from run_roll_subjects import STEM,SCENES,subject_recipe

class RollSubjectsTests(unittest.TestCase):
    def test_source_fonts_previous_units_newline_and_particle_guards(self):
        a=read(ROOT/'translations/roll_subjects_ko.json');u=resolve_units(a);old=resolve_units(read(ROOT/'translations/roll_food_ko.json'));s=selected_scope(read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['661858'],a);src=(ROOT/'analysis/tpl_baseline/661858.tpl').read_text(encoding='utf-8-sig');target=translate_literal_scope(src,u,s)
        self.assertEqual(u[:36],old);self.assertEqual(len(u),41);self.assertEqual(skeleton(src),skeleton(target));self.assertEqual({x['id'] for x in u},{x.key for x in literals(src) if int(x.key.split(':')[1]) in [1,2,3,4,5,6,7,8,11,27,29]})
        original={x.key:x.text for x in literals(src)}
        for x in u:self.assertEqual(x['source'],original[x['id']])
        self.assertEqual(u[39]['source'].count('\n'),2);self.assertTrue(u[39]['source'].startswith('\n'));self.assertTrue(u[39]['translation'].startswith('\n'));validate_nickname_suffix(u,'661858',s)
        for index in [37,40]:
            for suffix in ['의','은','는','の',',']:
                bad=copy.deepcopy(u);bad[index]['translation']=suffix+'\n'+bad[index]['translation'].split('\n')[1]
                with self.assertRaisesRegex(ValueError,'nickname'):validate_nickname_suffix(bad,'661858',s)
        bad=copy.deepcopy(u);bad[39]['translation']=bad[39]['translation'].lstrip('\n')
        with self.assertRaisesRegex(ValueError,'line/choice-padding'):translate_literal_scope(src,bad,s)
        tbl=ROOT/'poc/work/roll_subjects_v1/plugins/exe45-utf8.tbl';layout=validate_characters(target,tbl,s,{x['id'] for x in u});self.assertEqual(max(max(x['line_advance_pixels']) for x in layout),123)
        m,rom,e,streams,c=static(STEM,'661858');self.assertEqual(m['translated_units'],1007);self.assertEqual(len(streams),41);self.assertEqual(len(c['protected_nonliteral_scripts']),86)
        before={x['path']:x['sha256'] for x in read(ROOT/'poc/output/exe45_ko_development_roll_food_v1.json')['translation_assets'] if Path(x['path']).name!='roll_food_ko.json'};now={x['path']:x['sha256'] for x in m['translation_assets']};self.assertTrue(all(now[k]==v for k,v in before.items()))
        self.assertEqual([len(subject_recipe(s).split(',')) for s in SCENES],[12,13])

    def test_native_subjects_and_cumulative_runtime(self):
        from report_roll_subjects import main
        reports=main();self.assertEqual(len(reports),14);r=reports[-2:];self.assertEqual(set().union(*(set(x['normal_runtime_units']) for x in r)),{f'661858:{s}:{i}' for s,n in [(27,2),(29,3)] for i in range(n)})
        for scene in r:
            self.assertTrue(scene['subject_question_stopped_before_input_init']);self.assertTrue(all(p['font_vram_screen_pixels_match'] and p['no_translated_ink_occluded'] for p in scene['pages']))
            for p in scene['pages'][1:]:self.assertEqual(p['nickname_row'],0);self.assertEqual(p['nickname'],'ああくん');self.assertEqual(p['nickname_width'],44)
        self.assertTrue(r[1]['pages'][1]['source_leading_newline_preserved'])

if __name__=='__main__':unittest.main()
