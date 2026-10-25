import unittest
from report_roll_pet import ROOT,read,static
from tpl_literals import resolve_units,skeleton
from build_development_patch import selected_scope,translate_literal_scope
from run_roll_pet_tournament import STEM

class RollPetTournamentTests(unittest.TestCase):
    def test_previous_scope_and_controls(self):
        a=read(ROOT/'translations/roll_pet_tournament_ko.json');u=resolve_units(a);old=resolve_units(read(ROOT/'translations/roll_pet_keyquest_ko.json'));s=selected_scope(read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['664E28'],a);src=(ROOT/'analysis/tpl_baseline/664E28.tpl').read_text(encoding='utf-8-sig')
        self.assertEqual(u[:11],old);self.assertEqual(skeleton(src),skeleton(translate_literal_scope(src,u,s)));self.assertEqual(s['literal_scripts'],[10,11,12,14,15,17,23,24,25,30,31,34])
        m,rom,e,streams,c=static(STEM,'664E28');self.assertEqual(m['translated_units'],1021);self.assertEqual(len(c['protected_nonliteral_scripts']),243);self.assertEqual(len(streams),14);self.assertLessEqual(c['max_literal_width'],132)
        from report_roll_pet_license import literal_end
        first=streams['664E28:34:0'];self.assertEqual(literal_end(rom,first,e),max(first)+4)
        ascii_last=streams['664E28:30:0'];self.assertEqual(literal_end(rom,ascii_last,e),max(ascii_last)+1)

    def test_page_transition_and_quarantine(self):
        from report_roll_pet_tournament import main
        r=main();self.assertEqual(len(r),15);self.assertEqual(r[12]['diagnostic_renderer_units'],['664E28:30:0']);self.assertEqual(r[-1]['diagnostic_renderer_units'],['664E28:34:0','664E28:34:1']);self.assertEqual([p['step'] for p in r[-1]['pages']],[2,4,5])
        for d in [r[12],r[-1]]:
            self.assertEqual(d['normal_runtime_units'],[]);self.assertTrue(all(p['diagnostic'] and p['font_vram_screen_pixels_match'] and p['no_translated_ink_occluded'] and p['vacant_text_pixels_cleared'] for p in d['pages']))

if __name__=='__main__':unittest.main()
