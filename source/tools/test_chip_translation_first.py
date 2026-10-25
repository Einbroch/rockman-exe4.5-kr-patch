"""Translation-first source/control/layout checks, no emulator or ROM build."""
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from importlib import import_module
from build_visibility_poc import ROOT,require_hash
from report_chip_library_runtime import read
from tpl_literals import resolve_units,literals,skeleton,replace_literals
from build_development_patch import selected_scope,validate_literal_numerals,validate_characters
from chip_library_extension import compile_clone
from textpet_korean import prepare_plugins


class TranslationFirst(unittest.TestCase):
    def test_three_compositions_and_source_invariants(self):
        registry=read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')
        source=ROOT/read(ROOT/'project.json')['source_profile']['filename']
        require_hash(source,registry['source_sha256']);native=source.read_bytes()
        table={int(k,16):v for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines() if '=' in line for k,v in [line.split('=',1)] if len(k)==2}
        for batch,total,prior in ((5,150,120),(6,180,150),(7,194,180),(8,249,194)):
            composed=import_module(f'prepare_chip_batch{batch:02d}_assets').prepare()
            for key,stem in (('names','library_chip_names'),('descriptions','chip_descriptions')):
                asset=read(ROOT/f'translations/{stem}_batch{batch:02d}_ko.json')
                self.assertEqual(asset,composed[key])
                units=resolve_units(asset)
                self.assertEqual(len(units),total)
                self.assertEqual(units[:prior],resolve_units(read(ROOT/f'translations/{stem}_batch{batch-1:02d}_ko.json')))
                self.assertTrue(all(u['state']=='needs_review' for u in units))
                self.assertFalse(asset['review']['release_eligible'])
                original=(ROOT/f"analysis/tpl_baseline/{asset['archive']}.tpl").read_text(encoding='utf-8-sig')
                target=replace_literals(original,units,language='mmbn45s' if key=='names' else 'mmbn45')
                self.assertEqual(skeleton(original),skeleton(target))
                selected={u['id'] for u in units}
                before={u.key:u.text for u in literals(original)};after={u.key:u.text for u in literals(target)}
                self.assertTrue(all(before[k]==after[k] for k in before if k not in selected))
                if key=='descriptions':
                    scope=selected_scope(registry['archives']['76937C'],asset)
                    validate_literal_numerals(units,scope)
                    with TemporaryDirectory(prefix='exe45-translation-first-') as temp:
                        plugins=Path(temp)/'plugins';prepare_plugins(plugins)
                        layout=validate_characters(target,plugins/'exe45-utf8.tbl',scope,selected)
                    self.assertEqual(len(layout),total)
                else:
                    spec=read(ROOT/'tools/specs/exe45_chip_library_v1.json')
                    clone,record=compile_clone(native,spec,asset,table)
                    self.assertEqual(len(record['units']),total)
                    self.assertEqual(len(record['unselected_scripts']),256-total)
                    self.assertTrue(clone)


if __name__=='__main__':unittest.main()
