import unittest
from report_roll_pet import ROOT,read
from calendar_types_model import validate,replace_types_literals
from tpl_literals import literals
from build_development_patch import selected_scope,literal_scope
class CalendarTypeTests(unittest.TestCase):
    def test_exact_scope_and_replacement(self):
        a=read(ROOT/'translations/calendar_types_ko.json');self.assertEqual(validate(a['units'])['cells'],27);old=read(ROOT/'translations/calendar_menu_ko.json');self.assertEqual(a['units'][0],old['units'][0]);tpl=(ROOT/'analysis/tpl_baseline/6368E8.tpl').read_text(encoding='utf-8');after=replace_types_literals(tpl,a['units']);self.assertEqual({x.key:x.text for x in literals(after)}['6368E8:60:0'],a['units'][1]['translation'])
    def test_segment_overflow_fails(self):
        a=read(ROOT/'translations/calendar_types_ko.json');a['units'][1]['translation']='TV 방송친구와 약속  식사 학원 기타 ?????'
        with self.assertRaises(ValueError):validate(a['units'])
    def test_native_mono_scope(self):
        a=read(ROOT/'translations/calendar_types_ko.json');scope=selected_scope(read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['6368E8'],a)
        self.assertEqual(literal_scope(scope,'6368E8:60:0')['consumer'],'fixed-cell-mono');self.assertEqual(literal_scope(scope,'6368E8:0:0')['consumer'],'fixed-cell-big')
if __name__=='__main__':unittest.main()
