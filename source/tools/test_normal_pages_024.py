import unittest
from normal_page_capacity_024 import validate
from pet_flag_page_capacity_024 import validate as flag_validate
from test_pet_quick_capacity_024 import fixture as quick_fixture


def normal(body,entry='\tmsgOpen\n\tmugshotShow\n\t\tmugshot = MegaMan\n',terminal='\tend\n'):
    return '@archive TEST\n@size 1\nscript 0 mmbn45 {\n'+entry+body+terminal+'}\n'


class NormalPages(unittest.TestCase):
    def check(self,src,ids=None):
        return validate(src,src,[0],ids or {'TEST:0:0'},99,88)[0]

    def test_reverse_portrait_order(self):
        p=self.check(normal('\t"말"\n\tkeyWait\n\t\tany = false\n'))
        self.assertEqual(p['pages'][0]['widths'],[12])

    def test_composite_width_guard(self):
        src=normal('\t"'+'가'*8+'"\n\twait\n\t\tframes = 18\n\t"'+'나'*8+'"\n\tkeyWait\n\t\tany = false\n')
        with self.assertRaisesRegex(ValueError,'extent'):self.check(src,{'TEST:0:0','TEST:0:1'})

    def test_repeated_terminal_bytes(self):
        p=self.check(normal('\t"말"\n\tkeyWait\n\t\tany = false\n',terminal='\tend\n\tend\n'))
        self.assertEqual(p['source_trailing_ends'],1)

    def test_no_text_after_end(self):
        with self.assertRaisesRegex(ValueError,'after terminal'):
            self.check(normal('\t"말"\n\tkeyWait\n\t\tany = false\n',terminal='\tend\n\t"추가"\n'))

    def test_clear_then_jump(self):
        p=self.check(normal('\t"말"\n\tkeyWait\n\t\tany = false\n\tclearMsg\n',terminal='\tjump\n\t\ttarget = 2\n'))
        self.assertEqual(p['terminal'],'jump')

    def test_jump_must_clear(self):
        with self.assertRaisesRegex(ValueError,'jump after'):
            self.check(normal('\t"말"\n\tkeyWait\n\t\tany = false\n',terminal='\tjump\n\t\ttarget = 2\n'))

    def test_no_quick_window(self):
        with self.assertRaisesRegex(ValueError,'msgOpen'):
            self.check(normal('\t"말"\n\tkeyWait\n\t\tany = false\n',entry='\tmsgOpenQuick\n'))

    def test_no_position_change(self):
        with self.assertRaisesRegex(ValueError,'unmodeled body'):
            self.check(normal('\tpositionText\n\t\tleft = 92\n\t\ttop = 110\n\t\tarrowDistance = 3\n\t"말"\n\tkeyWait\n\t\tany = false\n'))

    def test_no_unbounded_provider(self):
        with self.assertRaisesRegex(ValueError,'unmodeled body'):
            self.check(normal('\tprintCurrentNavi\n\t"말"\n\tkeyWait\n\t\tany = false\n'))

    def test_no_unknown_entry(self):
        with self.assertRaisesRegex(ValueError,'unmodeled entry'):
            self.check(normal('\t"말"\n\tkeyWait\n\t\tany = false\n',entry='\tcallUnknown\n\tmsgOpen\n'))

    def test_source_change_rejected(self):
        src=normal('\t"말"\n\tkeyWait\n\t\tany = false\n')
        with self.assertRaisesRegex(ValueError,'protected'):
            validate(src,src.replace('msgOpen','msgOpenQuick'),[0],{'TEST:0:0'},99,88)

    def test_fixed_flag_at_cleared_pet_boundary(self):
        src=quick_fixture().replace('\twaitHold\n','\tflagClear\n\t\tflag = 3585\n\twaitHold\n')
        p=flag_validate(src,src,[0],{'TEST:0:0'})[0]
        self.assertEqual(p['preserved_zero_width_flags'][0]['command'],'flagClear')

    def test_flag_after_terminal_rejected(self):
        src=quick_fixture()+ '\tflagClear\n\t\tflag = 3585\n'
        with self.assertRaisesRegex(ValueError,'outside empty-page'):
            flag_validate(src,src,[0],{'TEST:0:0'})

    def test_flag_mid_text_rejected(self):
        src=quick_fixture().replace('\tkeyWait\n','\tflagSet\n\t\tflag = 3585\n\tkeyWait\n')
        with self.assertRaisesRegex(ValueError,'outside empty-page'):
            flag_validate(src,src,[0],{'TEST:0:0'})


if __name__=='__main__':unittest.main()
