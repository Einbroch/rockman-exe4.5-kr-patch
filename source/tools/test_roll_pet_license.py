import copy,unittest
from report_roll_pet import ROOT,read,static
from tpl_literals import resolve_units,skeleton
from build_development_patch import selected_scope,translate_literal_scope,validate_nickname_suffix
from run_roll_pet_license import STEM

class RollPetLicenseTests(unittest.TestCase):
    def test_source_scope_prior_unit_and_suffix_guard(self):
        a=read(ROOT/'translations/roll_pet_license_ko.json');u=resolve_units(a);s=selected_scope(read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['664E28'],a);src=(ROOT/'analysis/tpl_baseline/664E28.tpl').read_text(encoding='utf-8-sig');self.assertEqual(skeleton(src),skeleton(translate_literal_scope(src,u,s)));self.assertEqual(u[:1],resolve_units(read(ROOT/'translations/roll_pet_talk_ko.json')));self.assertEqual(s['literal_scripts'],[10,11,12,14,15]);validate_nickname_suffix(u,'664E28',s)
        bad=copy.deepcopy(u);bad[0]['translation']='은'+bad[0]['translation'][1:]
        with self.assertRaisesRegex(ValueError,'nickname'):validate_nickname_suffix(bad,'664E28',s)
        m,rom,e,streams,c=static(STEM,'664E28');self.assertEqual(m['translated_units'],1012);self.assertEqual(len(c['protected_nonliteral_scripts']),250);self.assertEqual(c['max_literal_width'],123);self.assertEqual(len(streams),5)

    def test_focused_runtime_and_diagnostic_quarantine(self):
        from report_roll_pet_license import main
        r=main();self.assertEqual(len(r),8)
        for d in r[-4:]:
            self.assertEqual(d['normal_runtime_units'],[]);self.assertEqual(len(d['diagnostic_renderer_units']),1);self.assertTrue(all(p['diagnostic'] and p['font_vram_screen_pixels_match'] and p['no_translated_ink_occluded'] for p in d['pages']))

if __name__=='__main__':unittest.main()
