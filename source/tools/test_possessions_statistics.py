import copy,json,unittest
from possessions_statistics import ROOT,CHILD,ADDED,validate,replace
from tpl_literals import literals,skeleton
class StatisticsTests(unittest.TestCase):
    def setUp(self):self.a=json.loads((ROOT/CHILD).read_text(encoding='utf8'))
    def test_parent12(self):self.assertEqual(len(validate(self.a)['units']),12)
    def test_parent_drift_rejected(self):
        self.a['units'][0]['translation']='변경'
        with self.assertRaises(ValueError):validate(self.a)
    def test_padding_rejected(self):
        self.a['units'][-1]['translation']=ADDED['translation'][:-1]
        with self.assertRaises(ValueError):validate(self.a)
    def test_source_rejected(self):
        self.a['units'][-1]['source']='wrong'
        with self.assertRaises(ValueError):validate(self.a)
    def test_replacement(self):
        src=(ROOT/'analysis/full_scope_v1/source_tpl/6368E8.tpl').read_text(encoding='utf-8-sig')
        dest=replace(src,self.a['units']);self.assertEqual(skeleton(src),skeleton(dest))
        self.assertEqual(next(x.text for x in literals(dest) if x.key==ADDED['id']),ADDED['translation'])
        project=lambda s:[(x.key,x.language,x.text) for x in literals(s) if ':81:' in x.key or ':82:' in x.key]
        self.assertEqual(project(src),project(dest))
if __name__=='__main__':unittest.main()
