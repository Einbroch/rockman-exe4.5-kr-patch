import unittest
from build_visibility_poc import ROOT
from build_development_patch import read_json,selected_scope,translate_literal_scope,literal_scope
from tpl_literals import resolve_units,literals,skeleton
from prepare_roll_tactics import prepare

class RollTactics(unittest.TestCase):
    def test_linked_wording_and_exact_source_scope(self):
        a=read_json(ROOT/'translations/rockman_roll_tactics_escape_ko.json');self.assertEqual(a,prepare());units=resolve_units(a)
        self.assertEqual(units[:14],resolve_units(read_json(ROOT/'translations/rockman_roll_escape_ko.json')))
        self.assertEqual(len(units),16);self.assertEqual(len(a['wordings']),14)
        self.assertEqual([u['wording_id'] for u in a['units'][-2:]],['tactics.target','tactics.distance'])
        scope=selected_scope(read_json(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['76C944'],a)
        source=(ROOT/'analysis/tpl_baseline/76C944.tpl').read_text(encoding='utf-8-sig');target=translate_literal_scope(source,units,scope)
        self.assertEqual(skeleton(source),skeleton(target));after={x.key:x for x in literals(target)};ids={u['id'] for u in units}
        self.assertEqual(ids,set(scope['literal_ids']))
        for x in literals(source):
            if x.key not in ids:self.assertEqual((x.text,x.language),(after[x.key].text,after[x.key].language))
        for key in ('76C944:6:0','76C944:7:0'):self.assertEqual(literal_scope(scope,key)['consumer'],'fixed-cell-mono')
        self.assertFalse(a['review']['release_eligible'])
