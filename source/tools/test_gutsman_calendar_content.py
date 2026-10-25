import copy,unittest
from gutsman_calendar_content import ROOT,CHILD,PARENT,PARENT_SHA,validate_parent
from report_roll_pet import read,sha
from inventory_full_scope import inherited_guts_input
from build_development_patch import selected_scope
class CalendarContent(unittest.TestCase):
    def test_parent_and_child_identity(self):
        a=read(ROOT/CHILD);validate_parent(a)
        item=dict(a['parent_asset'],archive='665698',scope='read-only inherited2 calendar units');child=dict(path=CHILD,sha256=sha((ROOT/CHILD).read_bytes()),archive='665698');m=dict(translation_assets=[item,child])
        self.assertTrue(inherited_guts_input(item,m))
        for bad in [dict(translation_assets=[item]),dict(translation_assets=[item,child,child])]:self.assertRaises(ValueError,inherited_guts_input,item,bad)
        self.assertRaises(ValueError,inherited_guts_input,dict(item,carry_units=3),m)
        bad=copy.deepcopy(a);bad['units'][0]['translation']='변경';self.assertRaises(ValueError,validate_parent,bad)
    def test_exact_scope_and_rejections(self):
        a=read(ROOT/CHILD);s=selected_scope(read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['665698'],a)
        self.assertEqual(s['literal_scripts'],[20,21,22,23]);self.assertEqual(s['literal_ids'],[u['id'] for u in a['units']])
        for field,value in [('source','잘못된 원문'),('translation','줄\n변경'),('state','approved')]:
            bad=copy.deepcopy(a);bad['units'][-1][field]=value;self.assertRaises(ValueError,validate_parent,bad)
        bad=copy.deepcopy(a);bad['units'].append(bad['units'][-1]);self.assertRaises(ValueError,validate_parent,bad)
if __name__=='__main__':unittest.main()
