"""Reject drift in cumulative calendar management and dynamic-name boundary."""
import copy,json,unittest
from build_visibility_poc import ROOT
from gutsman_calendar_management import CHILD,validate,CHANGED
from tpl_literals import literals,skeleton,replace_literals
from build_development_patch import selected_scope
class Management(unittest.TestCase):
    def asset(self):return json.loads((ROOT/CHILD).read_text(encoding='utf8'))
    def test_source_parent_wording_state_rejected(self):
        a=self.asset();validate(a)
        for index in [0,21,22,40,41,42,43,44]:
            for field in ['source','translation','state']:
                b=copy.deepcopy(a);b['units'][index][field]+='가';self.assertRaises(ValueError,validate,b)
    def test_exact_delta_and_controls(self):
        a=self.asset();t=(ROOT/'analysis/full_scope_v1/source_tpl/665698.tpl').read_text(encoding='utf-8-sig');out=replace_literals(t,a['units']);self.assertEqual(skeleton(t),skeleton(out));before={x.key:x.text for x in literals(t)};after={x.key:x.text for x in literals(out)}
        self.assertEqual({k for k in before if before[k]!=after[k]},{u['id'] for u in a['units']})
        self.assertTrue(all(before[f'665698:52:{i}']==after[f'665698:52:{i}'] for i in range(3)))
        self.assertEqual(before['665698:52:3'].split('\n')[0],after['665698:52:3'].split('\n')[0])
    def test_registry_scope_and_choice_geometry(self):
        a=self.asset();r=json.loads((ROOT/'tools/specs/exe45_dialogue_archives_v1.json').read_text(encoding='utf8'));s=selected_scope(r['archives']['665698'],a)
        self.assertEqual(set(s['literal_ids']),{u['id'] for u in a['units']});self.assertEqual(len(a['units']),45)
        self.assertEqual({int(u['id'].split(':')[1])for u in a['units'][22:]},CHANGED)
        self.assertIn(dict(script=52,literals=[5,6],prefix_pixels=24),s['standalone_choice_rows'])
if __name__=='__main__':unittest.main()
