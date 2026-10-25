"""Refusal tests of the024 input gate using exact selected source fixtures."""
import unittest
from copy import deepcopy
from build_visibility_poc import ROOT
from cumulative_batch500 import read
from survey_pet_quick_reflow_024 import replace_for_analysis
from layout500_inputs_024 import validate_group, load_inputs
from archive_scripts import verify_untouched_scripts


class Inputs024(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        selection = read('analysis/pending_insertion_500_024_selection_v1/selection.json')
        compiled = read('analysis/pending_insertion_500_024_compile500_v1/verification.json')
        by = {r['archive']:r['units'] for r in compiled['archives']}
        cls.fixtures = {}
        for group in selection['groups']:
            if group['profile'] in cls.fixtures:
                continue
            original = (ROOT/group['source_tpl']['path']).read_text(encoding='utf-8-sig')
            units = [u for u in by[group['archive']] if u['id'] in group['ids']]
            cls.fixtures[group['profile']] = (original, replace_for_analysis(original,units), group, units)

    def fixture(self):
        return deepcopy(self.fixtures['normal-pages'])

    def test_all_five_profiles(self):
        self.assertEqual(len(self.fixtures),5)
        for args in self.fixtures.values():
            self.assertTrue(validate_group(*args))

    def test_duplicate_id(self):
        a,b,g,u=self.fixture();u.append(deepcopy(u[0]))
        with self.assertRaisesRegex(ValueError,'ID denominator'):validate_group(a,b,g,u)

    def test_missing_unit(self):
        a,b,g,u=self.fixture();u.pop()
        with self.assertRaisesRegex(ValueError,'ID denominator'):validate_group(a,b,g,u)

    def test_wrong_script(self):
        a,b,g,u=self.fixture();g['script']+=1
        with self.assertRaisesRegex(ValueError,'script identity'):validate_group(a,b,g,u)

    def test_changed_wording(self):
        a,b,g,u=self.fixture();u[0]['translation']+='가'
        with self.assertRaisesRegex(ValueError,'wording/state'):validate_group(a,b,g,u)

    def test_changed_review_state(self):
        a,b,g,u=self.fixture();u[0]['state']='approved'
        with self.assertRaisesRegex(ValueError,'wording/state'):validate_group(a,b,g,u)

    def test_unapproved_prose_rule(self):
        a,b,g,u=self.fixture();g['explicit_layouts'][u[0]['id']]=u[0]['translation']+'가'
        with self.assertRaisesRegex(ValueError,'prose changed'):validate_group(a,b,g,u)

    def test_wrong_target(self):
        a,b,g,u=self.fixture()
        with self.assertRaisesRegex(ValueError,'merged target'):validate_group(a,a,g,u)

    def test_unknown_profile(self):
        a,b,g,u=self.fixture();g['profile']='accept-everything'
        with self.assertRaisesRegex(ValueError,'unknown consumer'):validate_group(a,b,g,u)

    def test_frozen_geometry_corruption(self):
        a,b,g,u=self.fixture();g['geometry']=[]
        with self.assertRaisesRegex(ValueError,'geometry differs'):validate_group(a,b,g,u)

    def test_wrong_source_rom(self):
        with self.assertRaisesRegex(ValueError,'immutable source'):load_inputs(b'not the supported ROM')

    def test_carry_script_byte_corruption(self):
        record=read('analysis/pending_insertion_500_024_carry_v1/preflight.json')['archives'][0]
        carry=(ROOT/record['carry_compiled']['path']).read_bytes()
        payload=bytearray((ROOT/record['compiled']['path']).read_bytes())
        kept=record['unselected_parent_scripts']
        chosen=next(r for r in kept if r['bytes'])['script']
        at=int.from_bytes(payload[chosen*2:chosen*2+2],'little')
        payload[at]^=1
        with self.assertRaisesRegex(ValueError,'unselected script bytes'):
            verify_untouched_scripts(carry,bytes(payload),record['script_count'],set(record['new_scripts']))


if __name__=='__main__':unittest.main()
