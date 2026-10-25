import copy,unittest
from pathlib import Path
from report_roll_pet import ROOT,read,static
from tpl_literals import resolve_units,literals,skeleton
from build_development_patch import selected_scope,translate_literal_scope,validate_nickname_suffix,validate_characters
from run_roll_food import STEM,food_recipe

class RollFoodTests(unittest.TestCase):
    def test_source_fonts_previous_wording_and_suffix_guards(self):
        a=read(ROOT/'translations/roll_food_ko.json');u=resolve_units(a);old=resolve_units(read(ROOT/'translations/roll_family_siblings_ko.json'));s=selected_scope(read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['661858'],a)
        src=(ROOT/'analysis/tpl_baseline/661858.tpl').read_text(encoding='utf-8-sig');target=translate_literal_scope(src,u,s)
        self.assertEqual(u[:32],old);self.assertEqual(len(u),36);self.assertEqual(skeleton(src),skeleton(target));self.assertEqual({x['id'] for x in u},{x.key for x in literals(src) if int(x.key.split(':')[1]) in [1,2,3,4,5,6,7,8,11]})
        original={x.key:x.text for x in literals(src)}
        for x in u:self.assertEqual(x['source'],original[x['id']])
        self.assertTrue(u[33]['source'].endswith('\n'));self.assertTrue(u[33]['translation'].endswith('\n'));validate_nickname_suffix(u,'661858',s)
        for suffix in ['은','는','は',',','、가']:
            bad=copy.deepcopy(u);bad[34]['translation']=suffix
            with self.assertRaisesRegex(ValueError,'nickname'):validate_nickname_suffix(bad,'661858',s)
        bad=copy.deepcopy(u);bad[34]['source']='は、'
        with self.assertRaisesRegex(ValueError,'nickname'):validate_nickname_suffix(bad,'661858',s)
        tbl=ROOT/'poc/work/roll_food_v1/plugins/exe45-utf8.tbl';layout=validate_characters(target,tbl,s,{x['id'] for x in u});self.assertEqual(max(max(x['line_advance_pixels']) for x in layout),123)
        m,rom,e,streams,c=static(STEM,'661858');self.assertEqual(m['translated_units'],1002);self.assertEqual(len(streams),36);self.assertEqual(len(c['protected_nonliteral_scripts']),88)
        before={x['path']:x['sha256'] for x in read(ROOT/'poc/output/exe45_ko_development_roll_family_siblings_v1.json')['translation_assets'] if Path(x['path']).name!='roll_family_siblings_ko.json'};now={x['path']:x['sha256'] for x in m['translation_assets']};self.assertTrue(all(now[k]==v for k,v in before.items()));self.assertEqual(len(food_recipe().split(',')),13)

    def test_native_food_and_cumulative_runtime(self):
        from report_roll_food import cumulative
        reports=cumulative();self.assertEqual(len(reports),12);r=reports[-1];self.assertEqual(r['normal_runtime_units'],[f'661858:11:{i}' for i in range(4)]);self.assertTrue(r['food_question_stopped_before_input_init'])
        self.assertTrue(all(p['font_vram_screen_pixels_match'] and p['no_translated_ink_occluded'] for p in r['pages']));p=r['pages'][1];self.assertEqual(p['nickname_row'],1);self.assertEqual(p['nickname'],'ああくん');self.assertEqual(p['nickname_width'],44)

if __name__=='__main__':unittest.main()
