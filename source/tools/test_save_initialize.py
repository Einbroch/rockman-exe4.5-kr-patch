"""Initialization UI preserves existing55 and the erase-flow controls."""
import copy,json,unittest
import save_initialize as m
from build_visibility_poc import ROOT
from tpl_literals import literals,skeleton
from build_development_patch import selected_scope,translate_literal_scope

class SaveInitializeTests(unittest.TestCase):
    def setUp(self):
        old,self.d=m.inputs();self.source=(ROOT/m.SOURCE).read_text(encoding='utf-8-sig')
        self.a=dict(old,scope_variant='save-initialize-v1',parent_asset=dict(path=m.PARENT,sha256=m.PARENT_SHA,carry_units=55),units=old['units']+self.d['units'],context=self.d['context'])
    def test_selection(self):
        target=m.replace(self.source,self.a['units']);self.assertEqual(skeleton(target),skeleton(self.source))
        before={x.key:x.text for x in literals(self.source)};after={x.key:x.text for x in literals(target)};wanted={u['id']:u['translation'] for u in self.a['units']}
        self.assertEqual(after,{k:wanted.get(k,v) for k,v in before.items()})
    def test_parent_mutation(self):
        a=copy.deepcopy(self.a);a['units'][0]['translation']='changed'
        with self.assertRaises(ValueError):m.validate(a)
    def test_missing(self):
        with self.assertRaises(ValueError):m.validate(dict(self.a,units=self.a['units'][:-1]))
    def test_source_mismatch(self):
        a=copy.deepcopy(self.d);a['units'][0]['source']='wrong'
        with self.assertRaises(ValueError):m.validate_delta(a,self.source,set(range(0xAC00,0xD7A4)))
    def test_commands_changed(self):
        with self.assertRaises(ValueError):m.replace(self.source.replace('callSaveErase','callSave'),self.a['units'])
    def test_duplicate(self):
        a=copy.deepcopy(self.d);a['units'][-1]=a['units'][0]
        with self.assertRaises(ValueError):m.validate_delta(a,self.source,set(range(0xAC00,0xD7A4)))
    def test_prompt_rows(self):
        a=copy.deepcopy(self.d);a['units'][0]['translation']=a['units'][0]['translation'].rstrip('\n')
        with self.assertRaises(ValueError):m.validate_delta(a,self.source,set(range(0xAC00,0xD7A4)))
    def test_choice_overflow(self):
        a=copy.deepcopy(self.d);a['units'][1]['translation']='가'*7
        with self.assertRaises(ValueError):m.validate_delta(a,self.source,set(range(0xAC00,0xD7A4)))
    def test_missing_glyph(self):
        with self.assertRaises(ValueError):m.validate_delta(self.d,self.source,set())
    def test_scope(self):
        registry=json.loads((ROOT/'tools/specs/exe45_dialogue_archives_v1.json').read_text(encoding='utf8'))
        scope=selected_scope(registry['archives']['6368E8'],self.a)
        self.assertEqual(len(scope['literal_ids']),64);self.assertEqual(scope['literal_tokens'],{'6368E8:91:1':{'[z]':'99'}})
        self.assertEqual(translate_literal_scope(self.source,self.a['units'],scope),m.replace(self.source,self.a['units']))

if __name__=='__main__':unittest.main()
