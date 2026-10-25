"""Controlled accept/reject fixtures for full-page variable aggregation."""
import unittest
from field_hint_capacity import validate


def tpl(body,guard='',opener='msgOpen'):
    return '@archive ABCDEF\nscript 0 mmbn45 {\n'+guard+'\tmugshotShow\n\t\tmugshot = MegaMan\n\t'+opener+'\n'+body+'\tkeyWait\n\t\tany = false\n\tend\n}\n'


def lit(s):return '\t"'+s.replace('\n','\\n')+'"\n'
NICK='\tprintPlayerNickname\n\t\tcapitalizeFirst = false\n\t\tcapitalizeAll = false\n\t\tprintN = false\n'
CHIP='\tprintChip\n\t\tbuffer = 0\n\t\tchip = 104\n'
GUARD='\tcheckTournament\n\t\tbitmask = 4\n\t\tjumpIfNone = continue\n\t\tjumpIfTrue = 29\n\t\tjumpIfFalse = continue\n'
DAY='\tcheckNetDateWeekday\n\t\tlower = 6\n\t\tupper = 6\n\t\tjumpIfInRange = 34\n\t\tjumpIfOutOfRange = continue\n'


class HintCapacity(unittest.TestCase):
    def check(self,t,original=None,ids=None,scripts=None):
        return validate(original or t,t,[0] if scripts is None else scripts,{'ABCDEF:0:0'} if ids is None else ids,99,88)
    def test_plain_limit(self):self.assertEqual(self.check(tpl(lit('가'*15)))[0]['pages'][0]['widths'],[180])
    def test_plain_overflow(self):
        with self.assertRaises(ValueError):self.check(tpl(lit('가'*16)))
    def test_arrow_boundary(self):self.check(tpl(lit('가\n가\n'+'가'*14)))
    def test_arrow_overflow(self):
        with self.assertRaises(ValueError):self.check(tpl(lit('가\n가\n'+'가'*15)))
    def test_nickname_combined(self):self.assertEqual(self.check(tpl(NICK+lit(',\n안녕')))[0]['pages'][0]['widths'],[111,24])
    def test_nickname_aggregate_overflow(self):
        with self.assertRaises(ValueError):self.check(tpl(NICK+lit('가'*7)))
    def test_chip_quote_composite(self):self.assertEqual(self.check(tpl(lit('「')+CHIP+lit('」\n찾자')))[0]['pages'][0]['widths'],[110,24])
    def test_two_variables_composite_overflow(self):
        with self.assertRaises(ValueError):self.check(tpl(NICK+CHIP+lit('가')))
    def test_tournament_guard(self):self.check(tpl(lit('가'),GUARD))
    def test_weekday_guard(self):self.check(tpl(lit('가'),DAY))
    def test_unproven_mask(self):
        with self.assertRaises(ValueError):self.check(tpl(lit('가'),GUARD.replace('bitmask = 4','bitmask = 8')))
    def test_unproven_date(self):
        with self.assertRaises(ValueError):self.check(tpl(lit('가'),DAY.replace('upper = 6','upper = 0')))
    def test_changed_guard_argument(self):
        with self.assertRaises(ValueError):self.check(tpl(lit('가'),GUARD.replace('29','30')),tpl(lit('あ'),GUARD))
    def test_changed_print_argument(self):
        with self.assertRaises(ValueError):self.check(tpl(NICK.replace('false','true',1)+lit('가')))
    def test_changed_chip(self):
        with self.assertRaises(ValueError):self.check(tpl(CHIP.replace('104','105')+lit('가')))
    def test_quick_window(self):
        with self.assertRaises(ValueError):self.check(tpl(lit('가'),opener='msgOpenQuick'))
    def test_new_window_after_open(self):
        with self.assertRaises(ValueError):self.check(tpl(lit('가')+'\tmsgOpen\n'))
    def test_unknown_command(self):
        with self.assertRaises(ValueError):self.check(tpl(lit('가')+'\tspacePx\n\t\tcount = 24\n'))
    def test_clear_before_wait(self):
        with self.assertRaises(ValueError):self.check(tpl(lit('가')+'\tclearMsg\n'+lit('나')))
    def test_clear_after_wait(self):
        body=lit('가')+'\tkeyWait\n\t\tany = false\n\tclearMsg\n'+lit('나')
        self.assertEqual(len(self.check(tpl(body))[0]['pages']),2)
    def test_missing_selected_literal(self):
        with self.assertRaises(ValueError):self.check(tpl(lit('가')),ids={'ABCDEF:1:0'})
    def test_duplicate_scripts(self):
        with self.assertRaises(ValueError):self.check(tpl(lit('가')),scripts=[0,0])


if __name__=='__main__':unittest.main()
