"""Controlled defects in date/save translation boundaries."""
import copy,json,unittest
from build_visibility_poc import ROOT
from verify_calendar_date_save_draft import ASSET,validate

class DateSaveDraft(unittest.TestCase):
    def setUp(self):
        self.asset=json.loads((ROOT/ASSET).read_text(encoding='utf8'))
        self.source=(ROOT/'analysis/full_scope_v1/source_tpl/6368E8.tpl').read_text(encoding='utf-8-sig')
        self.glyphs=set(range(0xAC00,0xD7A4))
    def unit(self,key):return next(u for u in self.asset['units'] if u['id']==key)
    def test_valid(self):self.assertEqual(len(validate(self.asset,self.source,self.glyphs)),17)
    def test_credit_value(self):
        u=self.unit('6368E8:91:1');u['translation']=u['translation'].replace('0','1')
        with self.assertRaises(ValueError):validate(self.asset,self.source,self.glyphs)
    def test_currency_token(self):
        u=self.unit('6368E8:91:1');u['translation']=u['translation'].replace('[z]','')
        with self.assertRaises(ValueError):validate(self.asset,self.source,self.glyphs)
    def test_source_mismatch(self):
        with self.assertRaises(ValueError):validate(self.asset,self.source.replace('よろしいですか?','よろしい?'),self.glyphs)
    def test_prompt_rows(self):
        self.unit('6368E8:91:2')['translation']='괜찮으신가요?'
        with self.assertRaises(ValueError):validate(self.asset,self.source,self.glyphs)
    def test_choice_width(self):
        self.unit('6368E8:91:3')['translation']='가'*7
        with self.assertRaises(ValueError):validate(self.asset,self.source,self.glyphs)
    def test_missing_glyph(self):
        with self.assertRaises(ValueError):validate(self.asset,self.source,set())
    def test_duplicate_or_missing(self):
        self.asset['units'][-1]=copy.deepcopy(self.asset['units'][0])
        with self.assertRaises(ValueError):validate(self.asset,self.source,self.glyphs)

if __name__=='__main__':unittest.main()
