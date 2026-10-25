import json
import re
import unittest
from tempfile import TemporaryDirectory
from pathlib import Path
from build_visibility_poc import ROOT
from build_development_patch import validate_characters
from fixedcell_font import bdf_cells,unpack_pixels
from tpl_literals import literals,replace_literals,resolve_units,skeleton
from textpet_korean import prepare_plugins


class MonoDescriptionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary=TemporaryDirectory(prefix='exe45-mono-unit-')
        cls.plugins=Path(cls.temporary.name)/'plugins'
        prepare_plugins(cls.plugins)

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def setUp(self):
        self.asset=json.loads((ROOT/'translations/chip_descriptions_cannon_poc_ko.json').read_text(encoding='utf-8'))
        self.tpl=(ROOT/'analysis/tpl_baseline/76937C.tpl').read_text(encoding='utf-8-sig')
        self.units=resolve_units(self.asset)
        self.scope={'consumer':'fixed-cell-mono','max_literal_rows':3,'max_line_advance':72}

    def test_source_and_control_skeleton(self):
        translated=replace_literals(self.tpl,self.units)
        self.assertEqual(skeleton(self.tpl),skeleton(translated))
        self.assertEqual({u['id'] for u in self.units},{f'76937C:{i}:0' for i in (1,2,3)})
        for u in self.units:
            self.assertEqual(re.findall(r'\d+',u['source']),re.findall(r'\d+',u['translation']))
            self.assertEqual(u['translation'].count('\n'),2)

    def test_three_rows_nine_visible_cells(self):
        t=replace_literals(self.tpl,self.units)
        layout=validate_characters(t,self.plugins/'exe45-utf8.tbl',self.scope,{u['id'] for u in self.units})
        self.assertEqual([l['line_advance_pixels'] for l in layout],[[72,64,24]]*3)

    def test_tenth_cell_rejected_despite_staging_width(self):
        units=[dict(u,translation='앞쪽의 적 1체를가\n공격할 수 있는\n캐논포') for u in self.units]
        t=replace_literals(self.tpl,units)
        with self.assertRaises(ValueError):
            validate_characters(t,self.plugins/'exe45-utf8.tbl',self.scope,{u['id'] for u in units})

    def test_line_break_change_rejected(self):
        units=[dict(u,translation=u['translation'].replace('\n',' ',1)) for u in self.units]
        with self.assertRaises(ValueError): replace_literals(self.tpl,units)

    def test_mono_roles_preserve_ink_geometry(self):
        profile=json.loads((ROOT/'tools/specs/exe45_fixedcell_visibility_v1.json').read_text())
        font=ROOT/profile['font']['path'];wanted=set('앞쪽적공격캐논포')
        big=bdf_cells(font,wanted,profile['raster'])
        mono=bdf_cells(font,wanted,dict(profile['raster'],background=1,ink=3,shadow=4))
        mapping={0:1,1:3,2:4}
        for ch in wanted:
            self.assertEqual(unpack_pixels(mono[ch]),[[mapping[p] for p in row] for row in unpack_pixels(big[ch])])


if __name__=='__main__': unittest.main()
