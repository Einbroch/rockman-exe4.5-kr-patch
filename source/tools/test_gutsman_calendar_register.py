import copy,unittest
from gutsman_calendar_register import ROOT,CHILD,validate_parent
from report_roll_pet import read,sha
from inventory_full_scope import inherited_guts_input
from build_development_patch import selected_scope,translate_literal_scope,validate_characters
class CalendarRegister(unittest.TestCase):
    def test_parent_chain_and_one_writer(self):
        a=read(ROOT/CHILD);validate_parent(a);p10=dict(a['parent_asset'],archive='665698',scope='read-only inherited10 calendar units');home=read(ROOT/a['parent_asset']['path']);p7=dict(home['parent_asset'],archive='665698',scope='read-only inherited7 calendar units');confirmation=read(ROOT/home['parent_asset']['path']);p4=dict(confirmation['parent_asset'],archive='665698',scope='read-only inherited4 calendar units');content=read(ROOT/confirmation['parent_asset']['path']);p2=dict(content['parent_asset'],archive='665698',scope='read-only inherited2 calendar units');child=dict(path=CHILD,sha256=sha((ROOT/CHILD).read_bytes()),archive='665698');m=dict(translation_assets=[p10,p7,p4,p2,child])
        for p in [p10,p7,p4,p2]:self.assertTrue(inherited_guts_input(p,m))
        self.assertRaises(ValueError,inherited_guts_input,p10,dict(translation_assets=[p10,p7,p4,p2]))
        bad=copy.deepcopy(a);bad['units'][0]['translation']='변경';self.assertRaises(ValueError,validate_parent,bad)
    def test_register_structure_and_build_gate(self):
        a=read(ROOT/CHILD);base=read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['665698'];scope=selected_scope(base,a);self.assertEqual(scope['literal_scripts'],[0,1,2,20,21,22,23,24]);self.assertEqual(set(scope['literal_ids']),{u['id'] for u in a['units']})
        t=(ROOT/'analysis/full_scope_v1/source_tpl/665698.tpl').read_text(encoding='utf-8-sig');target=translate_literal_scope(t,a['units'],scope);tbl=ROOT/'poc/build/exe45_ko_development_gutsman_calendar_home_v1/plugins/exe45-utf8.tbl';measured=validate_characters(target,tbl,scope,{u['id'] for u in a['units']});rows={x['id']:x['line_advance_pixels'] for x in measured}
        self.assertLessEqual(max(max(v) for v in rows.values()),183);self.assertEqual(len(rows['665698:1:0']),2);self.assertEqual(len(rows['665698:2:0']),2)
        for i in range(-4,-1):
            bad=copy.deepcopy(a);bad['units'][i]['translation']=bad['units'][i]['translation'].replace('\n','');self.assertRaises(ValueError,validate_parent,bad)
        bad=copy.deepcopy(a);bad['units'][-1]['source']='잘못된 원문';self.assertRaises(ValueError,validate_parent,bad)
if __name__=='__main__':unittest.main()
