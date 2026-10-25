import unittest
from report_roll_pet import ROOT,read,static
from tpl_literals import resolve_units,skeleton
from build_development_patch import selected_scope,translate_literal_scope
from run_roll_pet_incident import STEM

class RollPetIncidentTests(unittest.TestCase):
    def test_source_scope_previous_units_and_controls(self):
        a=read(ROOT/'translations/roll_pet_incident_ko.json');u=resolve_units(a);old=resolve_units(read(ROOT/'translations/roll_pet_license_ko.json'));s=selected_scope(read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['664E28'],a);src=(ROOT/'analysis/tpl_baseline/664E28.tpl').read_text(encoding='utf-8-sig');self.assertEqual(u[:5],old);self.assertEqual(skeleton(src),skeleton(translate_literal_scope(src,u,s)));self.assertEqual(s['literal_scripts'],[10,11,12,14,15,17,31])
        m,rom,e,streams,c=static(STEM,'664E28');self.assertEqual(m['translated_units'],1015);self.assertEqual(len(c['protected_nonliteral_scripts']),248);self.assertEqual(c['max_literal_width'],124);self.assertEqual(len(streams),8)

    def test_two_page_runtime_and_diagnostic_quarantine(self):
        from report_roll_pet_incident import main
        r=main();self.assertEqual(len(r),10);self.assertEqual(r[-2]['diagnostic_renderer_units'],['664E28:17:0','664E28:17:1']);self.assertEqual([p['step'] for p in r[-2]['pages']],[2,4,5]);self.assertEqual(r[-1]['diagnostic_renderer_units'],['664E28:31:0'])
        for d in r[-2:]:
            self.assertEqual(d['normal_runtime_units'],[]);self.assertTrue(all(p['diagnostic'] and p['font_vram_screen_pixels_match'] and p['no_translated_ink_occluded'] and p['vacant_text_pixels_cleared'] for p in d['pages']))

if __name__=='__main__':unittest.main()
