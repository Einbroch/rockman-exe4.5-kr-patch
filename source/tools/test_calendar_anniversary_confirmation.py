"""Reject parent/source/control drift before a cumulative ROM is emitted."""
import copy,json,unittest
from pathlib import Path
from build_visibility_poc import ROOT
from calendar_anniversary_confirmation import DIALOGUE,LABELS,validate,replace
from tpl_literals import skeleton,literals
class AnniversaryConfirmation(unittest.TestCase):
    def test_parent_and_field_drift_rejected(self):
        for path in [DIALOGUE,LABELS]:
            a=json.loads((ROOT/path).read_text(encoding='utf8'));validate(a)
            for index in [0,len(a['units'])-1]:
                bad=copy.deepcopy(a);bad['units'][index]['translation']+='가';self.assertRaises(ValueError,validate,bad)
            bad=copy.deepcopy(a);bad['units'][-1]['source']='변경';self.assertRaises(ValueError,validate,bad)
    def test_only_declared_literals_and_controls(self):
        for path in [DIALOGUE,LABELS]:
            a=json.loads((ROOT/path).read_text(encoding='utf8'));t=(ROOT/f"analysis/full_scope_v1/source_tpl/{a['archive']}.tpl").read_text(encoding='utf-8-sig');out=replace(t,a)
            self.assertEqual(skeleton(t),skeleton(out));before={x.key:x.text for x in literals(t)};after={x.key:x.text for x in literals(out)}
            self.assertEqual({k for k in before if before[k]!=after[k]},{u['id'] for u in a['units']})
if __name__=='__main__':unittest.main()
