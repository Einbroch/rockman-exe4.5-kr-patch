"""Controlled fixtures for the isolated development full-box contract."""
import unittest
from fullbox_capacity import validate

def tpl(text,opener='msgOpen',tail=''):
    return '@archive ABCDEF\nscript 0 mmbn45 {\n\tmugshotShow\n\t\tmugshot = NormalNaviBrown\n\t'+opener+'\n\t"'+text.replace('\n','\\n')+'"\n'+tail+'\tkeyWait\n\t\tany = false\n\tend\n}\n'

class FullBox(unittest.TestCase):
    def check(self,target,original=None):return validate(original or tpl('あ'),target,[dict(script=0,ids=['ABCDEF:0:0'])],{'ABCDEF:0:0'})
    def test_first_row180(self):self.assertEqual(self.check(tpl('가'*15))[0]['pages'][0]['widths'],[180])
    def test_third_row168(self):self.check(tpl('가\n가\n'+'가'*14))
    def test_overflow(self):
        with self.assertRaises(ValueError):self.check(tpl('가'*16))
    def test_arrow_region(self):
        with self.assertRaises(ValueError):self.check(tpl('가\n가\n'+'가'*15))
    def test_quick_window(self):
        with self.assertRaises(ValueError):self.check(tpl('가'),tpl('あ','msgOpenQuick'))
    def test_dynamic_variable(self):
        with self.assertRaises(ValueError):self.check(tpl('가'),tpl('あ',tail='\tprintPlayerNickname\n'))
    def test_composite_page(self):
        with self.assertRaises(ValueError):self.check(tpl('가'),tpl('あ',tail='\t"い"\n'))
    def test_unselected_scope(self):
        with self.assertRaises(ValueError):validate(tpl('あ'),tpl('가'),[dict(script=0,ids=['ABCDEF:0:0'])],set())

if __name__=='__main__':unittest.main()
