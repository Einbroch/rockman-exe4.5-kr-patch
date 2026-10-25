"""Pinned aggregate consumer and inherited54 negative tests."""
import json,unittest
from gutsman_calendar_inventory import *
from tpl_literals import replace_literals,skeleton
class Inventory(unittest.TestCase):
    def asset(self):return json.loads((ROOT/CHILD).read_text(encoding='utf8'))
    def test_projection_controls(self):
        a=self.asset();self.assertEqual(len(validate(a)['units']),54)
        src=(ROOT/'analysis/full_scope_v1/source_tpl/665698.tpl').read_text(encoding='utf-8-sig');self.assertEqual(skeleton(src),skeleton(replace(src,a['units'])))
    def test_aggregate(self):
        a=self.asset();src=(ROOT/'analysis/full_scope_v1/source_tpl/665698.tpl').read_text(encoding='utf-8-sig');self.assertEqual(template(a['units'],PROFILE,src)['translated_static_advance'],44)
        self.assertGreater(advance('의'),advance('の'))
        with self.assertRaises(ValueError):template(a['units'],PROFILE,src.replace('capitalizeAll = false','capitalizeAll = true'))
        with self.assertRaises(ValueError):template(a['units'],dict(PROFILE,static_advance=45),src)
    def test_drift(self):
        for i,key in [(0,'translation'),(54,'source'),(55,'translation'),(56,'state')]:
            a=self.asset();a['units'][i][key]+='X'
            with self.assertRaises(ValueError):validate(a)
    def test_registry(self):
        a=self.asset();r=json.loads((ROOT/'tools/specs/exe45_dialogue_archives_v1.json').read_text(encoding='utf8'))['archives']['665698']['variants'][a['scope_variant']]
        self.assertEqual(r['nickname_aggregate_profiles'],[PROFILE]);self.assertEqual(set(r['literal_ids']),{u['id']for u in a['units']});self.assertEqual(r['nickname_suffix_scripts'],[25])
if __name__=='__main__':unittest.main()
