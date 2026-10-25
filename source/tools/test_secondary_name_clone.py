import unittest
from build_visibility_poc import ROOT
from report_chip_library_runtime import read
from chip_library_extension import compile_clone

class SecondaryClone(unittest.TestCase):
    def test_pinned_clone_preserves_all39_native_slots(self):
        source=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes()
        a=read(ROOT/'translations/chip_secondary_names_ko.json');spec=read(ROOT/'tools/specs/exe45_secondary_name_clone_v1.json')
        table={int(k,16):v for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines() if '=' in line for k,v in [line.split('=',1)] if len(k)==2}
        clone,record=compile_clone(source,spec,a,table)
        self.assertEqual(len(record['units']),98);self.assertEqual(len(record['unselected_scripts']),39)
        self.assertTrue(clone)
        wrong=dict(a,consumer='normal-dialogue')
        with self.assertRaises(ValueError):compile_clone(source,spec,wrong,table)
