import unittest
from tempfile import TemporaryDirectory
from pathlib import Path
from build_visibility_poc import ROOT
from report_chip_library_runtime import read
from tpl_literals import resolve_units,literals,replace_literals,skeleton
from prepare_chip_secondary_descriptions import prepare
from build_development_patch import validate_characters,validate_literal_numerals
from textpet_korean import prepare_plugins

class SecondaryDescriptions(unittest.TestCase):
    def test_source_controls_numbers_and_all75_layouts(self):
        a=read(ROOT/'translations/chip_secondary_descriptions_ko.json');self.assertEqual(a,prepare())
        units=resolve_units(a);self.assertEqual(len(units),75)
        self.assertTrue(all(x['state']=='needs_review' for x in units));self.assertFalse(a['review']['release_eligible'])
        scope=read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['76BC60']
        self.assertEqual(scope['literal_scripts'],[int(u['id'].split(':')[1]) for u in units]);validate_literal_numerals(units,scope)
        original=(ROOT/'analysis/tpl_baseline/76BC60.tpl').read_text(encoding='utf-8-sig')
        target=replace_literals(original,units);self.assertEqual(skeleton(original),skeleton(target))
        for u in units:self.assertEqual(u['source'].count('\n'),u['translation'].count('\n'))
        with TemporaryDirectory(prefix='exe45-secondary-descriptions-') as temp:
            plugins=Path(temp)/'plugins';prepare_plugins(plugins)
            layout=validate_characters(target,plugins/'exe45-utf8.tbl',scope,{u['id'] for u in units})
        self.assertEqual(len(layout),75)
