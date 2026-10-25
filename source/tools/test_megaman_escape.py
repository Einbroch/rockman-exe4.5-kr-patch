"""Mixed-language archive guards, explicit denominator and draft provenance."""
import copy
import unittest
from build_visibility_poc import ROOT
from build_development_patch import read_json,selected_scope,literal_scope,translate_literal_scope,validate_characters
from prepare_megaman_escape import prepare
from tpl_literals import literals,resolve_units,skeleton

class MegamanEscape(unittest.TestCase):
    def setUp(self):
        self.asset=read_json(ROOT/'translations/megaman_tactics_escape_ko.json')
        self.scope=selected_scope(read_json(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['76C944'],self.asset)
        self.source=(ROOT/'analysis/tpl_baseline/76C944.tpl').read_text(encoding='utf-8-sig')

    def test_serialization_and_prior_wording(self):
        self.assertEqual(prepare(),self.asset)
        prior=resolve_units(read_json(ROOT/'translations/megaman_tactics_prompts_ko.json'))
        self.assertEqual(resolve_units(self.asset)[:2],prior)
        self.assertEqual(len(self.asset['units']),8)
        self.assertFalse(self.asset['review']['release_eligible'])

    def test_mixed_language_and_unselected_literals(self):
        units=resolve_units(self.asset);target=translate_literal_scope(self.source,units,self.scope)
        self.assertEqual(skeleton(target),skeleton(self.source))
        before={x.key:x for x in literals(self.source)};after={x.key:x for x in literals(target)}
        ids={u['id'] for u in units}
        for key,item in before.items():
            if key not in ids:self.assertEqual((item.text,item.language),(after[key].text,after[key].language))
        self.assertEqual(set(self.scope['literal_ids']),ids)
        self.assertEqual(literal_scope(self.scope,'76C944:0:0')['consumer'],'fixed-cell-mono')
        self.assertEqual(literal_scope(self.scope,'76C944:2:0')['consumer'],'normal-dialogue')
        self.assertEqual(after['76C944:2:1'].text,'예  ')

    def test_overlap_and_wrong_language_fail_closed(self):
        scope=copy.deepcopy(self.scope);scope['literal_profiles']*=2
        with self.assertRaises(ValueError):literal_scope(scope,'76C944:2:0')
        scope=copy.deepcopy(self.scope);scope['literal_profiles'][0]['literal_language']='mmbn45s'
        with self.assertRaises(ValueError):translate_literal_scope(self.source,resolve_units(self.asset),scope)
