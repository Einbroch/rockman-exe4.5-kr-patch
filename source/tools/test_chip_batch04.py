"""Independent source/layout/serialization checks at120 units."""
import unittest
from build_visibility_poc import ROOT
from report_chip_library_runtime import read
from tpl_literals import resolve_units,literals,skeleton,replace_literals
from prepare_chip_batch04_assets import prepare
from build_development_patch import validate_literal_numerals,selected_scope


class Batch04Tests(unittest.TestCase):
    def test_composition_and_prior90(self):
        composed=prepare()
        for key,stem in [('names','library_chip_names'),('descriptions','chip_descriptions')]:
            asset=read(ROOT/f'translations/{stem}_batch04_ko.json')
            self.assertEqual(asset,composed[key])
            units=resolve_units(asset)
            self.assertEqual(len(units),120)
            self.assertEqual(units[:90],resolve_units(read(ROOT/f'translations/{stem}_batch03_ko.json')))
            for unit in units:
                self.assertEqual(unit['state'],'needs_review')
                self.assertTrue(all(len(line)<=(8 if key=='names' else 9) for line in unit['translation'].split('\n')))
            self.assertFalse(asset['review']['release_eligible'])

    def test_scope_controls_numbers(self):
        asset=read(ROOT/'translations/chip_descriptions_batch04_ko.json')
        registry=read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')
        scope=selected_scope(registry['archives']['76937C'],asset)
        units=resolve_units(asset)
        self.assertEqual(scope['literal_scripts'],list(range(1,121)))
        validate_literal_numerals(units,scope)
        source=(ROOT/'analysis/tpl_baseline/76937C.tpl').read_text(encoding='utf-8-sig')
        target=replace_literals(source,units)
        self.assertEqual(skeleton(source),skeleton(target))
        wanted={u['id'] for u in units}
        before={u.key:u.text for u in literals(source)}
        after={u.key:u.text for u in literals(target)}
        self.assertTrue(all(before[k]==after[k] for k in before if k not in wanted))


if __name__=='__main__':unittest.main()
