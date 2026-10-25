"""Structural-template fixtures; not proof of live nickname capacity."""
import unittest
from dataclasses import replace
from tpl_literals import literals
from survey_batch500_019_variables import inspect_template,ARGS
class NicknameTemplates(unittest.TestCase):
    def inspect(self,text,targets=None,native_bound=None,invariant_suffixes=False):
        head='@archive 123456\n';items=[replace(i,start=i.start-len(head),end=i.end-len(head)) for i in literals(head+text)]
        units={i.key:dict(source=i.text,translation=(targets or {}).get(i.key,i.text),state='needs_review') for i in items}
        return inspect_template(text,items,units,native_bound,invariant_suffixes)
    def section(self,suffix='!\\n대사'):
        return 'script 1 mmbn45 {\n\tmsgOpen\n\tprintPlayerNickname\n'+ARGS+'\t"'+suffix+'"\n\tkeyWait\n\t\tany = false\n\tend\n}\n'
    def test_non_growing_punctuation(self):
        model,reason=self.inspect(self.section())
        self.assertIsNone(reason);self.assertEqual(model['target_static_advance'],11);self.assertEqual(model['aggregate_rows'],2)
    def test_one_pixel_comma_growth_rejected(self):
        model,reason=self.inspect(self.section('、\\n대사'),{'123456:1:0':',\n대사'})
        self.assertIsNone(model);self.assertEqual(reason,'suffix_row_or_static_growth')
    def test_particle_suffix_not_mechanically_approved(self):
        model,reason=self.inspect(self.section('님\\n대사'))
        self.assertIsNone(model);self.assertEqual(reason,'particle_or_word_suffix_requires_context')
    def test_extra_variable_not_admitted(self):
        text=self.section().replace('\tend','\tprintSchool\n\tend')
        self.assertEqual(self.inspect(text)[1],'other_or_multiple_variables')
    def test_nickname_arguments_protected(self):
        self.assertEqual(self.inspect(self.section().replace('capitalizeAll = false','capitalizeAll = true'))[1],'nickname_arguments')
    def test_conditional_comma_growth_fits(self):
        model,reason=self.inspect(self.section('、\\n대사'),{'123456:1:0':',\n대사'},99)
        self.assertIsNone(reason);self.assertEqual(model['conditional_first_row_advance'],111)
    def test_conditional_exact_boundary(self):
        model,reason=self.inspect(self.section('!!!\\n대사'),native_bound=99)
        self.assertIsNone(reason);self.assertEqual(model['conditional_first_row_advance'],132)
    def test_conditional_one_extra_glyph_overflow(self):
        model,reason=self.inspect(self.section('!!!!\\n대사'),native_bound=99)
        self.assertIsNone(model);self.assertEqual(reason,'nickname_aggregate_width')
    def test_explicit_invariant_suffix_has_no_name_dependent_particle(self):
        for suffix in ('의','도','님의','님은','님이','님께',' 님의',' 님은',' 님이',' 님께'):
            model,reason=self.inspect(self.section(suffix+'\\n대사'),native_bound=99,invariant_suffixes=True)
            self.assertIsNone(reason);self.assertFalse(model['semantic_approval']);self.assertLessEqual(model['conditional_first_row_advance'],132)
    def test_name_dependent_particle_still_rejected(self):
        for suffix in ('은','는','이','가','을','를','과','와','로','으로'):
            self.assertEqual(self.inspect(self.section(suffix+'\\n대사'),native_bound=99,invariant_suffixes=True)[1],'particle_or_word_suffix_requires_context')
    def test_invariant_needs_native_capacity_evidence(self):
        self.assertEqual(self.inspect(self.section('의\\n대사'),invariant_suffixes=True)[1],'particle_or_word_suffix_requires_context')
if __name__=='__main__':unittest.main()
