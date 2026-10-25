"""Calendar navigation source, parent, finite delta and controls regressions."""
import copy,json,unittest
from build_visibility_poc import ROOT
from gutsman_calendar_navigation import CHILD,validate
from tpl_literals import literals,replace_literals,skeleton
class Navigation(unittest.TestCase):
    def test_drift_rejected(self):
        a=json.loads((ROOT/CHILD).read_text(encoding='utf8'));validate(a)
        for index in [0,18,19,20,21]:
            for field in ['source','translation','state']:
                bad=copy.deepcopy(a);bad['units'][index][field]+='가';self.assertRaises(ValueError,validate,bad)
        bad=copy.deepcopy(a);bad['units'].reverse();self.assertRaises(ValueError,validate,bad)
    def test_only_selected_literals(self):
        a=json.loads((ROOT/CHILD).read_text(encoding='utf8'));t=(ROOT/'analysis/full_scope_v1/source_tpl/665698.tpl').read_text(encoding='utf-8-sig');out=replace_literals(t,a['units'])
        self.assertEqual(skeleton(t),skeleton(out));old={x.key:x.text for x in literals(t)};new={x.key:x.text for x in literals(out)}
        self.assertEqual({k for k in old if old[k]!=new[k]},{u['id'] for u in a['units']})
    def test_registry_finite_scope(self):
        from build_development_patch import selected_scope
        a=json.loads((ROOT/CHILD).read_text(encoding='utf8'));r=json.loads((ROOT/'tools/specs/exe45_dialogue_archives_v1.json').read_text(encoding='utf8'));s=selected_scope(r['archives']['665698'],a)
        self.assertEqual(set(s['literal_ids']),{u['id'] for u in a['units']})
        self.assertEqual(set(s['literal_scripts']),{int(u['id'].split(':')[1]) for u in a['units']})
        self.assertEqual(s['standalone_choice_rows'],r['archives']['665698']['variants']['calendar-anniversary-confirmation-v1']['standalone_choice_rows'])
if __name__=='__main__':unittest.main()
