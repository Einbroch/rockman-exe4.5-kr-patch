import copy,unittest
from gutsman_calendar_confirmation import ROOT,CHILD,validate_parent
from report_roll_pet import read,sha
from inventory_full_scope import inherited_guts_input
from build_development_patch import selected_scope,translate_literal_scope,validate_characters
class CalendarConfirmation(unittest.TestCase):
    def test_parent_chain_and_one_writer(self):
        a=read(ROOT/CHILD);validate_parent(a);p4=dict(a['parent_asset'],archive='665698',scope='read-only inherited4 calendar units');content=read(ROOT/a['parent_asset']['path']);p2=dict(content['parent_asset'],archive='665698',scope='read-only inherited2 calendar units');child=dict(path=CHILD,sha256=sha((ROOT/CHILD).read_bytes()),archive='665698');m=dict(translation_assets=[p4,p2,child])
        self.assertTrue(inherited_guts_input(p4,m));self.assertTrue(inherited_guts_input(p2,m))
        self.assertRaises(ValueError,inherited_guts_input,p4,dict(translation_assets=[p4,p2]))
        bad=copy.deepcopy(a);bad['units'][0]['translation']='변경';self.assertRaises(ValueError,validate_parent,bad)
    def test_choice_structure_padding_and_build_gate(self):
        a=read(ROOT/CHILD);base=read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['665698'];scope=selected_scope(base,a);self.assertEqual(scope['literal_scripts'],[20,21,22,23,24]);self.assertEqual(scope['literal_ids'],[u['id'] for u in a['units']])
        t=(ROOT/'analysis/full_scope_v1/source_tpl/665698.tpl').read_text(encoding='utf-8-sig');target=translate_literal_scope(t,a['units'],scope);tbl=ROOT/'poc/build/exe45_ko_development_gutsman_calendar_content_v1/plugins/exe45-utf8.tbl';measured=validate_characters(target,tbl,scope,{u['id'] for u in a['units']});yes=next(x for x in measured if x['id']=='665698:24:1');self.assertEqual(yes['choice_row_advance_pixels'],104);self.assertTrue(yes['choice_runtime_check_required'])
        for field,value in [('translation','예 '),('translation','예   '),('source','잘못된 원문')]:
            bad=copy.deepcopy(a);bad['units'][-2][field]=value;self.assertRaises(ValueError,validate_parent,bad)
        bad=copy.deepcopy(a);bad['units'][-3]['translation']='이렇게 하면 되거스?\n';self.assertRaises(ValueError,validate_parent,bad)
if __name__=='__main__':unittest.main()
