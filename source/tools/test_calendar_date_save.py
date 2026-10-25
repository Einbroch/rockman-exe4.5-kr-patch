"""Calendar17 integration must retain common38 and all control commands."""
import copy,json,unittest,tempfile
from pathlib import Path
import calendar_date_save as m
from build_visibility_poc import ROOT
from build_development_patch import selected_scope,translate_literal_scope,validate_characters
from korean_codec import encode_character
from tpl_literals import literals,skeleton

class CalendarDateSaveTests(unittest.TestCase):
    def setUp(self):
        old,delta=m.inputs()
        self.a=dict(old,parent_asset=dict(path=m.PARENT,sha256=m.PARENT_SHA,carry_units=38),units=old['units']+delta['units'],scope_variant='calendar-date-save-v1',context=delta['context'])
        self.source=(ROOT/'analysis/full_scope_v1/source_tpl/6368E8.tpl').read_text(encoding='utf-8-sig')
    def test_selection_controls(self):
        target=m.replace(self.source,self.a['units'])
        self.assertEqual(skeleton(target),skeleton(self.source))
        before={x.key:x.text for x in literals(self.source)};after={x.key:x.text for x in literals(target)}
        wanted={u['id']:u['translation'] for u in self.a['units']}
        self.assertEqual(after,{k:wanted.get(k,v) for k,v in before.items()})
    def test_parent_mutation(self):
        a=copy.deepcopy(self.a);a['units'][0]['translation']='changed'
        with self.assertRaises(ValueError):m.validate(a)
    def test_missing(self):
        a=dict(self.a,units=self.a['units'][:-1])
        with self.assertRaises(ValueError):m.validate(a)
    def test_source_mismatch(self):
        with self.assertRaises(ValueError):m.replace(self.source.replace('しゅみは?','しゅみ?'),self.a['units'])
    def test_scope(self):
        registry=json.loads((ROOT/'tools/specs/exe45_dialogue_archives_v1.json').read_text(encoding='utf8'))
        scope=selected_scope(registry['archives']['6368E8'],self.a)
        self.assertEqual(len(scope['literal_ids']),55)
        self.assertTrue(set(m.SCRIPTS)<=set(scope['literal_scripts']))
        self.assertIn('6368E8:91:1',scope['protected_numeral_ids'])
        self.assertEqual(translate_literal_scope(self.source,self.a['units'],scope),m.replace(self.source,self.a['units']))
    def test_currency_mapping_width(self):
        registry=json.loads((ROOT/'tools/specs/exe45_dialogue_archives_v1.json').read_text(encoding='utf8'))
        scope=selected_scope(registry['archives']['6368E8'],self.a)
        target=m.replace(self.source,self.a['units']);text=next(x.text for x in literals(target) if x.key=='6368E8:91:1')
        chars=set(text.replace('[z]','').replace('\n',''))
        table='\n'.join((encode_character(c).hex() if '\uac00'<=c<='\ud7a3' else '00')+'='+c for c in chars)+'\n99=[z]\n'
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'test.tbl';p.write_text(table,encoding='utf8')
            rows=validate_characters(target,p,scope,{'6368E8:91:1'})
            self.assertEqual(rows[0]['line_advance_pixels'],[122,112,60])
            p.write_text(table.replace('99=[z]','98=[z]'),encoding='utf8')
            with self.assertRaises(ValueError):validate_characters(target,p,scope,{'6368E8:91:1'})

if __name__=='__main__':unittest.main()
