import unittest
from report_roll_pet import ROOT,read,static
from tpl_literals import resolve_units,skeleton
from build_development_patch import selected_scope,translate_literal_scope
from run_roll_pet_keyquest import STEM

class RollPetKeyquestTests(unittest.TestCase):
    def test_scope_previous_units_and_controls(self):
        a=read(ROOT/'translations/roll_pet_keyquest_ko.json');u=resolve_units(a);old=resolve_units(read(ROOT/'translations/roll_pet_incident_ko.json'));s=selected_scope(read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['664E28'],a);src=(ROOT/'analysis/tpl_baseline/664E28.tpl').read_text(encoding='utf-8-sig')
        self.assertEqual(u[:8],old);self.assertEqual(skeleton(src),skeleton(translate_literal_scope(src,u,s)));self.assertEqual(s['literal_scripts'],[10,11,12,14,15,17,23,24,25,31])
        m,rom,e,streams,c=static(STEM,'664E28');self.assertEqual(m['translated_units'],1018);self.assertEqual(len(c['protected_nonliteral_scripts']),245);self.assertEqual(len(streams),11);self.assertLessEqual(c['max_literal_width'],132)

    def test_runtime_and_quarantine(self):
        from report_roll_pet_keyquest import main
        r=main();self.assertEqual(len(r),13)
        for d in r[9:12]:
            self.assertEqual(d['normal_runtime_units'],[]);self.assertTrue(all(p['diagnostic'] and p['font_vram_screen_pixels_match'] and p['no_translated_ink_occluded'] and p['vacant_text_pixels_cleared'] for p in d['pages']))
        self.assertEqual([d['diagnostic_renderer_units'] for d in r[9:12]],[['664E28:23:0'],['664E28:24:0'],['664E28:25:0']])

if __name__=='__main__':unittest.main()
