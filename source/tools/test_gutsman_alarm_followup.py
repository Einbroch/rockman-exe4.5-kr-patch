import copy,unittest
from gutsman_alarm_followup import ROOT,CHILD,validate_parent,DRAFT
from report_roll_pet import read
from inventory_full_scope import inherited_guts_input
from tpl_literals import skeleton,replace_literals
class AlarmFollowup(unittest.TestCase):
    def test_inherited_input_not_second_writer(self):
        a=read(ROOT/CHILD);validate_parent(a)
        bad=copy.deepcopy(a);bad['units'][-1]['translation']='변경';self.assertRaises(ValueError,validate_parent,bad)
        from build_visibility_poc import sha
        item=dict(a['parent_asset'],archive='66651C',scope='read-only inherited3 alarm units')
        child=dict(path=CHILD,sha256=sha((ROOT/CHILD).read_bytes()),archive='66651C')
        self.assertTrue(inherited_guts_input(item,dict(translation_assets=[item,child])))
        self.assertRaises(ValueError,inherited_guts_input,item,dict(translation_assets=[item]))
        bad=dict(item,carry_units=4);self.assertRaises(ValueError,inherited_guts_input,bad,dict(translation_assets=[bad,child]))
    def test_preserved_structure_and_finite_scope(self):
        a=read(ROOT/CHILD);t=(ROOT/'analysis/full_scope_v1/source_tpl/66651C.tpl').read_text(encoding='utf-8-sig')
        self.assertEqual(skeleton(t),skeleton(replace_literals(t,a['units'])))
        self.assertEqual(set(DRAFT),{u['id'] for u in a['units'] if u['id'].split(':')[1] in ('1','2')})
        for u in a['units']:
            self.assertEqual(u['source'].count('\n'),u['translation'].count('\n'))
            for line in u['translation'].split('\n'):self.assertLessEqual(sum(12 if '\uac00'<=c<='\ud7a3' else 8 if c==' ' else 11 for c in line),132)
if __name__=='__main__':unittest.main()
