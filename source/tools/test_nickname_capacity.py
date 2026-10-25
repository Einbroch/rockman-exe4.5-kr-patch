import unittest
from nickname_capacity import validate_templates,ARGS
class Capacity(unittest.TestCase):
    def fixture(self,first=',',after=''):
        original='@archive 123456\n@size 2\nscript 1 mmbn45 {\n\tmsgOpen\n\tprintPlayerNickname\n'+ARGS+'\t"、\\n대사"\n'+after+'\tkeyWait\n\t\tany = false\n\tclearMsg\n\tend\n}\n'
        target=original.replace('、\\n',first+'\\n')
        profile=dict(script=1,suffix_id='123456:1:0',source_first_line='、',first_line=first)
        return original,target,[profile],99,{'123456:1:0'}
    def test_comma_growth_fits_real_capacity(self):self.assertEqual(validate_templates(*self.fixture())[0]['first_row_advance'],111)
    def test_exact_boundary(self):self.assertEqual(validate_templates(*self.fixture('!!!'))[0]['first_row_advance'],132)
    def test_overflow(self):
        with self.assertRaisesRegex(ValueError,'aggregate capacity'):validate_templates(*self.fixture('!!!!'))
    def test_extra_same_page_literal(self):
        with self.assertRaisesRegex(ValueError,'same-page'):validate_templates(*self.fixture(after='\t"추가"\n'))
    def test_particle_dependency(self):
        with self.assertRaisesRegex(ValueError,'dependent'):validate_templates(*self.fixture('는'))
    def test_command_arguments(self):
        args=list(self.fixture());args[1]=args[1].replace('capitalizeAll = false','capitalizeAll = true')
        with self.assertRaisesRegex(ValueError,'arguments'):validate_templates(*args)
    def test_source_first_line(self):
        args=list(self.fixture());args[2][0]['source_first_line']='!'
        with self.assertRaisesRegex(ValueError,'pinned'):validate_templates(*args)
if __name__=='__main__':unittest.main()
