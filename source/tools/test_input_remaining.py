"""Parent immutability, selection and source/control contracts."""
import copy,json,unittest
from unittest.mock import patch
import input_remaining as m
from build_development_patch import selected_scope,translate_literal_scope
from build_visibility_poc import ROOT
from tpl_literals import literals,skeleton

class InputRemainingTests(unittest.TestCase):
    def setUp(self):
        old,delta=m.inputs();self.a=dict(old,parent_asset=delta['parent_asset'],units=old['units']+delta['units'],scope_variant='input-remaining-v1')
        self.source=(ROOT/'analysis/full_scope_v1/source_tpl/6368E8.tpl').read_text(encoding='utf-8-sig')
    def test_selected_and_unselected(self):
        target=m.replace(self.source,self.a['units']);self.assertEqual(skeleton(target),skeleton(self.source))
        before={x.key:x.text for x in literals(self.source)};after={x.key:x.text for x in literals(target)};wanted={u['id']:u['translation'] for u in self.a['units']}
        self.assertEqual(after,{k:wanted.get(k,v) for k,v in before.items()})
    def test_parent_mutation(self):
        self.a=copy.deepcopy(self.a);self.a['units'][0]['translation']='changed'
        with self.assertRaises(ValueError):m.validate(self.a)
    def test_omission(self):
        self.a['units']=self.a['units'][:-1]
        with self.assertRaises(ValueError):m.validate(self.a)
    def test_source_mismatch(self):
        with self.assertRaises(ValueError):m.replace(self.source.replace('しゅみは?','しゅみ?'),self.a['units'])
    def test_scope_mixed_consumers(self):
        registry=json.loads((ROOT/'tools/specs/exe45_dialogue_archives_v1.json').read_text(encoding='utf8'))
        scope=selected_scope(registry['archives']['6368E8'],self.a)
        self.assertEqual(translate_literal_scope(self.source,self.a['units'],scope),m.replace(self.source,self.a['units']))
        self.assertEqual(len(scope['literal_ids']),38)
        self.assertNotIn(20,scope['literal_scripts']);self.assertNotIn(22,scope['literal_scripts'])

if __name__=='__main__':unittest.main()
