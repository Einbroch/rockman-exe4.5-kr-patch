"""Source/control and immutable parent rejection tests for nine literals."""
import copy,json,unittest
from gutsman_calendar_schedule_delete import *
from tpl_literals import replace_literals,skeleton
class ScheduleDelete(unittest.TestCase):
    def asset(self):return json.loads((ROOT/CHILD).read_text(encoding='utf8'))
    def test_source_projection(self):
        a=self.asset();self.assertEqual(len(validate(a)['units']),45)
        source=(ROOT/'analysis/full_scope_v1/source_tpl/665698.tpl').read_text(encoding='utf-8-sig')
        target=replace_literals(source,a['units']);self.assertEqual(skeleton(source),skeleton(target))
    def test_drift_rejected(self):
        for index,key in [(0,'translation'),(45,'source'),(46,'translation'),(53,'state')]:
            a=self.asset();a['units'][index][key]+='X'
            with self.assertRaises(ValueError):validate(a)
    def test_variant(self):
        a=self.asset();r=json.loads((ROOT/'tools/specs/exe45_dialogue_archives_v1.json').read_text(encoding='utf8'))['archives']['665698']['variants'][a['scope_variant']]
        self.assertEqual(set(r['literal_ids']),{u['id']for u in a['units']})
        self.assertEqual(len(r['literal_scripts']),28)
        self.assertIn(25,r['nickname_suffix_scripts'])
if __name__=='__main__':unittest.main()
