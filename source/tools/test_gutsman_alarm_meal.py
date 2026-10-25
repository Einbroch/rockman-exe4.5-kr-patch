import copy,unittest
from gutsman_alarm_meal import ROOT,CHILD,validate_parent,KEY
from report_roll_pet import read,sha
from inventory_full_scope import inherited_guts_input
from build_development_patch import selected_scope,validate_nickname_suffix
from tpl_literals import skeleton,replace_literals
class AlarmMeal(unittest.TestCase):
    def test_parent_dependency_and_rejection(self):
        a=read(ROOT/CHILD);validate_parent(a);item=dict(a['parent_asset'],archive='66651C',scope='read-only inherited5 alarm units');child=dict(path=CHILD,sha256=sha((ROOT/CHILD).read_bytes()),archive='66651C');m=dict(translation_assets=[item,child])
        self.assertTrue(inherited_guts_input(item,m));self.assertRaises(ValueError,inherited_guts_input,item,dict(translation_assets=[item]));self.assertRaises(ValueError,inherited_guts_input,dict(item,carry_units=6),m)
        bad=copy.deepcopy(a);bad['units'][0]['translation']='변경';self.assertRaises(ValueError,validate_parent,bad)
    def test_same_row_suffix_and_structure(self):
        a=read(ROOT/CHILD);scope=selected_scope(read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['66651C'],a);validate_nickname_suffix(a['units'],'66651C',scope)
        bad=copy.deepcopy(a);next(u for u in bad['units'] if u['id']==KEY)['translation']='님、\n밥 먹을 시간이거스!';self.assertRaises(ValueError,validate_nickname_suffix,bad['units'],'66651C',scope)
        t=(ROOT/'analysis/full_scope_v1/source_tpl/66651C.tpl').read_text(encoding='utf-8-sig');self.assertEqual(skeleton(t),skeleton(replace_literals(t,a['units'])))
        for u in a['units']:
            self.assertEqual(u['source'].count('\n'),u['translation'].count('\n'))
            for line in u['translation'].split('\n'):self.assertLessEqual(sum(12 if '\uac00'<=c<='\ud7a3' else 8 if c==' ' else 11 for c in line),132)
if __name__=='__main__':unittest.main()
