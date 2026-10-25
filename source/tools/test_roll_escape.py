import unittest
from build_visibility_poc import ROOT
from build_development_patch import read_json,selected_scope,translate_literal_scope,validate_characters
from tpl_literals import resolve_units,literals,skeleton
from prepare_roll_escape import prepare

class RollEscape(unittest.TestCase):
    def test_draft_and_protected_scope(self):
        a=read_json(ROOT/'translations/rockman_roll_escape_ko.json');self.assertEqual(a,prepare())
        self.assertEqual(resolve_units(a)[:8],resolve_units(read_json(ROOT/'translations/megaman_tactics_escape_ko.json')))
        scope=selected_scope(read_json(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['76C944'],a)
        source=(ROOT/'analysis/tpl_baseline/76C944.tpl').read_text(encoding='utf-8-sig')
        target=translate_literal_scope(source,resolve_units(a),scope);self.assertEqual(skeleton(source),skeleton(target))
        ids={u['id'] for u in resolve_units(a)};self.assertEqual(ids,set(scope['literal_ids']));self.assertEqual(len(ids),14)
        after={x.key:x for x in literals(target)}
        for x in literals(source):
            if x.key not in ids:self.assertEqual((x.text,x.language),(after[x.key].text,after[x.key].language))
        self.assertEqual(after['76C944:8:1'].text,'예  ');self.assertFalse(a['review']['release_eligible'])

    def test_only_roll_confirmation_adopts_wider_development_bound(self):
        import copy
        a=prepare();scope=selected_scope(read_json(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['76C944'],a)
        units=resolve_units(a);ids={u['id'] for u in units}
        source=(ROOT/'analysis/tpl_baseline/76C944.tpl').read_text(encoding='utf-8-sig')
        target=translate_literal_scope(source,units,scope);table=ROOT/'poc/build_roll_escape_v1_r2/plugins/exe45-utf8.tbl'
        layout=validate_characters(target,table,scope,ids)
        self.assertEqual(next(x for x in layout if x['id']=='76C944:8:0')['line_advance_pixels'],[156,0])
        previous=copy.deepcopy(scope);previous['literal_profiles'][1]['max_line_advance']=144
        with self.assertRaises(ValueError):validate_characters(target,table,previous,ids)
