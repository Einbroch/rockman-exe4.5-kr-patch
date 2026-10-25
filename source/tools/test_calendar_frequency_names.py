"""Frequency source/copy extent and independent parent rejection tests."""
import json,unittest
from calendar_frequency_names import *
class FrequencyNames(unittest.TestCase):
    def asset(self):return json.loads((ROOT/CHILD).read_text(encoding='utf8'))
    def test_source_controls(self):
        a=self.asset();self.assertEqual(len(validate(a)['units']),7);source=(ROOT/'analysis/full_scope_v1/source_tpl/6368E8.tpl').read_text(encoding='utf-8-sig');self.assertEqual(skeleton(source),skeleton(replace(source,a['units'])))
    def test_drift(self):
        for n,key in [(0,'translation'),(7,'source'),(8,'translation'),(11,'state')]:
            a=self.asset();a['units'][n][key]+='X'
            with self.assertRaises(ValueError):validate(a)
    def test_raw_limits_and_numeral(self):
        self.assertEqual([len(raw(u['translation']))for u in ADDED],[10,9,9,9,9]);self.assertEqual(raw('1회만')[0],2)
        self.assertTrue(all(b'\xe5'not in raw(u['translation'])[:-1]for u in ADDED))
        a=self.asset();r=json.loads((ROOT/'tools/specs/exe45_dialogue_archives_v1.json').read_text(encoding='utf8'))['archives']['6368E8']['variants'][a['scope_variant']]
        self.assertEqual(set(r['literal_ids']),{u['id']for u in a['units']});self.assertEqual(r['literal_profiles'][-1]['consumer'],'normal-dialogue')
if __name__=='__main__':unittest.main()
