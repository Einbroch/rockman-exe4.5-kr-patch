"""Positive/refusal fixtures for025 analysis contracts, not GBA runtime."""
import json
import re
import unittest
from pathlib import Path
from normal_choice_capacity_025_v3 import validate as choice
from normal_timing_capacity_025 import validate as normal
from pet_nickname_capacity_025 import validate as quick, PREFIX
from pet_nickname_flags_capacity_025_v2 import validate as flags
from nickname_capacity import ARGS
from survey_layout500_025_v7 import place
from build_visibility_poc import ROOT,sha
from cumulative_batch500 import frozen_write

HEADER='@archive 123456\n@size 1\nscript 0 mmbn45 {\n'
END='}\n'
WAIT='\tkeyWait\n\t\tany = false\n'
SELECT=('\tselect\n\t\tdefault = 0\n\t\tlastCancelSFX = false\n'
        '\t\tnoDelay = false\n\t\tBSeparate = false\n\t\tdisableB = false\n'
        '\t\tclear = true\n\t\ttargets = [\n\t\t\tjump = continue,\n'
        '\t\t\tjump = 2,\n\t\t\tjump = 2\n\t\t]\n')
OPTION=('\toption\n\t\tbrackets = false\n\t\tleft = 1\n\t\tright = 1\n'
        '\t\tup = 0\n\t\tdown = 0\n\tspace\n\t\tcount = 1\n')
def choice_tpl(prompt=''):
    return HEADER+'\tmsgOpen\n'+prompt+'\tpositionOptionHorizontal\n\t\twidth = 8\n'+OPTION+'\t"예"\n'+OPTION+'\t"아니요"\n'+SELECT+'\tclearMsg\n\tend\n'+END
def quick_tpl(body):
    return HEADER+''.join('\t'+n+'\n'+a for n,a in PREFIX)+body+END
def keys(tpl):
    from tpl_literals import literals
    return {i.key for i in literals(tpl)}

class Contracts(unittest.TestCase):
    def accept(self,fn,tpl,*args):
        return fn(tpl,tpl,[0],keys(tpl),*args)
    def refuse(self,fn,tpl,*args):
        with self.assertRaises(ValueError):self.accept(fn,tpl,*args)
    def test_choice_empty(self):
        p=self.accept(choice,choice_tpl(),99,88)
        self.assertEqual(p[0]['pages'][0]['target_advance'],64)
    def test_choice_inline_prompt(self):
        p=self.accept(choice,choice_tpl('\t"확인할까요?\\n"\n'),99,88)
        self.assertEqual(p[0]['pages'][0]['prompt_widths'][-1],0)
    def test_choice_requires_blank_row(self):
        self.refuse(choice,choice_tpl('\t"확인"\n'),99,88)
    def test_choice_width12(self):
        self.refuse(choice,choice_tpl().replace('width = 8','width = 12'),99,88)
    def test_choice_width0(self):
        self.refuse(choice,choice_tpl().replace('width = 8','width = 0'),99,88)
    def test_choice_allocation_overflow(self):
        self.refuse(choice,choice_tpl().replace('"아니요"','"'+'가'*12+'"'),99,88)
    def test_choice_navigation_node2(self):
        self.refuse(choice,choice_tpl().replace('left = 1','left = 2'),99,88)
    def test_choice_pad2(self):
        self.refuse(choice,choice_tpl().replace('count = 1','count = 2'),99,88)
    def test_choice_multiline_label(self):
        self.refuse(choice,choice_tpl().replace('"예"','"예\\n예"'),99,88)
    def test_choice_incomplete_options(self):
        self.refuse(choice,choice_tpl().replace(OPTION+'\t"아니요"\n',''),99,88)
    def test_choice_changed_cancel(self):
        t=choice_tpl()
        with self.assertRaises(ValueError):choice(t,t.replace('jump = 2','jump = 3'),[0],keys(t),99,88)
    def test_choice_no_clear(self):
        self.refuse(choice,choice_tpl().replace('clear = true','clear = false'),99,88)
    def test_choice_invalid_default(self):
        self.refuse(choice,choice_tpl().replace('default = 0','default = 2'),99,88)
    def test_normal_zero_timing(self):
        self.accept(normal,HEADER+'\tmsgOpen\n\ttextSpeed\n\t\tdelay = 0\n\t"확인"\n'+WAIT+'\tend\n'+END,99,88)
    def test_normal_nonzero_timing(self):
        self.refuse(normal,HEADER+'\tmsgOpen\n\ttextSpeed\n\t\tdelay = 1\n\t"확인"\n'+WAIT+'\tend\n'+END,99,88)
    def test_quick_nickname_aggregate(self):
        self.accept(quick,quick_tpl('\tprintPlayerNickname\n'+ARGS+'\t"님"\n'+WAIT+'\tend\n'),99)
    def test_quick_nickname_overflow(self):
        self.refuse(quick,quick_tpl('\tprintPlayerNickname\n'+ARGS+'\t"가가가"\n'+WAIT+'\tend\n'),99)
    def test_quick_bound100(self):
        self.refuse(quick,quick_tpl('\t"가"\n'+WAIT+'\tend\n'),100)
    def test_quick_unknown_provider(self):
        self.refuse(quick,quick_tpl('\tprintSchool\n'+ARGS+'\t"님"\n'+WAIT+'\tend\n'),99)
    def test_quick_wrong_provider_args(self):
        self.refuse(quick,quick_tpl('\tprintPlayerNickname\n\t\tbuffer = 0\n\t"님"\n'+WAIT+'\tend\n'),99)
    def test_quick_rows4(self):
        self.refuse(quick,quick_tpl('\t"가\\n나\\n다\\n라"\n'+WAIT+'\tend\n'),99)
    def test_flags_empty_boundary(self):
        self.accept(flags,quick_tpl('\tflagSet\n\t\tflag = 12\n\t"가"\n'+WAIT+'\tclearMsg\n\tflagClear\n\t\tflag = 12\n\t"나"\n'+WAIT+'\tend\n'),99)
    def test_flags_after_literal(self):
        self.refuse(flags,quick_tpl('\t"가"\n\tflagSet\n\t\tflag = 12\n'+WAIT+'\tend\n'),99)
    def test_flags_after_provider(self):
        self.refuse(flags,quick_tpl('\tprintPlayerNickname\n'+ARGS+'\tflagSet\n\t\tflag = 12\n\t"님"\n'+WAIT+'\tend\n'),99)
    def test_flags_changed(self):
        t=quick_tpl('\tflagSet\n\t\tflag = 12\n\t"가"\n'+WAIT+'\tend\n')
        with self.assertRaises(ValueError):flags(t,t.replace('flag = 12','flag = 13'),[0],keys(t),99)
    def test_layout_words(self):
        t='가나다라마바사 아자차카타파하 가나다라마';v=place(t,(132,132,132))
        self.assertIsNotNone(v);self.assertEqual(v.replace('\n',' '),t)
    def test_layout_edge_padding(self):
        self.assertIsNone(place(' '+'가'*20,(132,132,132)))
    def test_layout_four_rows(self):
        self.assertIsNone(place('가\n나\n다\n'+'라'*20,(132,132,132)))

def main():
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(Contracts)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():raise SystemExit(1)
    deps=['tools/test_layout500_025.py','tools/normal_choice_capacity_025_v3.py','tools/normal_timing_capacity_025.py','tools/pet_nickname_capacity_025.py','tools/pet_nickname_flags_capacity_025_v2.py','tools/survey_layout500_025_v7.py']
    frozen_write(ROOT/'analysis/pending_insertion_500_025_models_test_v1/result.json',dict(passed=True,tests=result.testsRun,dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},rom_written=False,runtime_tested=False,limits='Analysis-model contracts only, not product admission, source/prose review or GBA choice interaction.'))

if __name__=='__main__':main()
