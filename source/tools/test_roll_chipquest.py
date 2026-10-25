import unittest
from report_roll_pet import ROOT,read,static
from tpl_literals import resolve_units,skeleton
from build_development_patch import selected_scope,translate_literal_scope
from roll_chipquest_model import validate_layout
from run_roll_chipquest import STEM

class RollChipQuestTests(unittest.TestCase):
    def inputs(self):
        a=read(ROOT/'translations/roll_pet_chipquest_ko.json');return resolve_units(a),selected_scope(read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['664E28'],a)
    def test_selected_denominator_and_original_controls(self):
        u,s=self.inputs();old=resolve_units(read(ROOT/'translations/roll_pet_weekday_ko.json'));self.assertEqual(u[:29],old);self.assertEqual(len(u),30);self.assertNotIn('664E28:13:0',{v['id'] for v in u});src=(ROOT/'analysis/tpl_baseline/664E28.tpl').read_text(encoding='utf-8-sig');self.assertEqual(skeleton(src),skeleton(translate_literal_scope(src,u,s)));m,rom,e,streams,c=static(STEM,'664E28');self.assertEqual(m['translated_units'],1051);self.assertEqual(len(c['protected_nonliteral_scripts']),230)
    def test_inserted_name_layout_guard(self):
        u,s=self.inputs();source=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes();layout=[{'id':'664E28:13:1','line_advance_pixels':[11,79]}];p=validate_layout(source,u,layout,s);self.assertEqual(p['combined_first_row'],110);bad=[dict(x) for x in u];bad[-1]['translation']='」 찾으러\n가자!'
        with self.assertRaises(ValueError):validate_layout(source,bad,layout,s)
        damaged=bytearray(source);damaged[0x765190+208]=0
        # Independent consumer boundary rejection does not depend on a glyph.
        badscope=dict(s,chipquest_variable_profile='unknown')
        with self.assertRaises(ValueError):validate_layout(source,u,layout,badscope)
    def test_native_chip_RAM_renderer_and_quarantine(self):
        from report_roll_chipquest import chip_report
        r=chip_report();self.assertEqual(r['normal_runtime_units'],[]);self.assertEqual(r['diagnostic_renderer_units'],['664E28:13:1']);self.assertTrue(all(p['native_chip_name']=='ビッグハンマー1' and p['font_vram_screen_pixels_match'] and p['vacant_text_pixels_cleared'] for p in r['pages']));self.assertFalse(r['release_eligible'])

if __name__=='__main__':unittest.main()
