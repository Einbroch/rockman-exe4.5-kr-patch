import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from build_visibility_poc import ROOT
from build_development_patch import selected_scope,validate_characters,validate_literal_numerals
from chip_library_extension import compile_clone
from prepare_chip_batch02_assets import prepare
from textpet_korean import prepare_plugins
from tpl_literals import resolve_units,replace_literals,skeleton


def read(path): return json.loads((ROOT/path).read_text(encoding='utf-8'))


class Batch02Tests(unittest.TestCase):
    def test_reproducible_composition(self):
        bundle=prepare()
        self.assertEqual(bundle['names'],read('translations/library_chip_names_batch02_ko.json'))
        self.assertEqual(bundle['descriptions'],read('translations/chip_descriptions_batch02_ko.json'))

    def test_prior_units_verbatim(self):
        for stem in ('library_chip_names','chip_descriptions'):
            old=resolve_units(read(f'translations/{stem}_batch01_ko.json'))
            new=resolve_units(read(f'translations/{stem}_batch02_ko.json'))
            self.assertEqual(new[:30],old);self.assertEqual(len(new),60)
            self.assertTrue(all(u['state']=='needs_review' for u in new))

    def test_description_controls_numbers_and_rows(self):
        asset=read('translations/chip_descriptions_batch02_ko.json');units=resolve_units(asset)
        base=read('tools/specs/exe45_dialogue_archives_v1.json')['archives']['76937C'];scope=selected_scope(base,asset)
        self.assertEqual(scope['literal_scripts'],list(range(1,61)))
        tpl=(ROOT/'analysis/tpl_baseline/76937C.tpl').read_text(encoding='utf-8-sig');translated=replace_literals(tpl,units)
        self.assertEqual(skeleton(tpl),skeleton(translated));validate_literal_numerals(units,scope)
        self.assertTrue(all(u['source'].count('\n')==u['translation'].count('\n') for u in units))
        with TemporaryDirectory(prefix='exe45-batch02-unit-') as temp:
            plugins=Path(temp)/'plugins';prepare_plugins(plugins)
            layout=validate_characters(translated,plugins/'exe45-utf8.tbl',scope,{u['id'] for u in units})
            self.assertEqual(len(layout),60);self.assertTrue(all(max(x['line_advance_pixels'])<=72 for x in layout))

    def test_name_clone_roundtrip_and196_preserved(self):
        project=read('project.json');source=(ROOT/project['source_profile']['filename']).read_bytes()
        table={int(k,16):v for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines() if '=' in line for k,v in [line.split('=',1)] if len(k)==2}
        clone,report=compile_clone(source,read('tools/specs/exe45_chip_library_v1.json'),read('translations/library_chip_names_batch02_ko.json'),table)
        self.assertEqual(len(report['units']),60);self.assertEqual(len(report['unselected_scripts']),196);self.assertGreater(len(clone),2437)


if __name__=='__main__': unittest.main()
