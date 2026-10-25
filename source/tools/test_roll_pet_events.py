import unittest
from report_roll_pet import ROOT,read,static
from tpl_literals import resolve_units,skeleton
from build_development_patch import selected_scope,translate_literal_scope
from run_roll_pet_events import STEM
from archive_scripts import script_spans

class RollPetEventsTests(unittest.TestCase):
    def test_previous_units_flags_and_controls(self):
        a=read(ROOT/'translations/roll_pet_events_ko.json');u=resolve_units(a);old=resolve_units(read(ROOT/'translations/roll_pet_tournament_ko.json'));s=selected_scope(read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['664E28'],a);src=(ROOT/'analysis/tpl_baseline/664E28.tpl').read_text(encoding='utf-8-sig')
        self.assertEqual(u[:14],old);self.assertEqual(skeleton(src),skeleton(translate_literal_scope(src,u,s)));self.assertEqual(s['literal_scripts'],[10,11,12,14,15,16,17,18,19,20,21,22,23,24,25,30,31,34])
        m,rom,e,streams,c=static(STEM,'664E28');self.assertEqual(m['translated_units'],1027);self.assertEqual(len(c['protected_nonliteral_scripts']),237);self.assertEqual(len(streams),20)
        ar=next(a for a in m['archives'] if a['archive']=='664E28');source=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes();before=script_spans(source[0x664E28:0x664E28+2158],255);after=script_spans(rom[ar['rom_offset']:ar['rom_offset']+ar['compiled_bytes']],255)
        for script in [16,18,19,20,21,22]:self.assertEqual(before[script][:6],after[script][:6])

    def test_all_six_runtime_and_quarantine(self):
        from report_roll_pet_events import main
        r=main();self.assertEqual(len(r),21)
        self.assertEqual([d['diagnostic_renderer_units'] for d in r[-6:]],[[f'664E28:{s}:0'] for s in [16,18,19,20,21,22]])
        for d in r[-6:]:
            self.assertEqual(d['normal_runtime_units'],[]);self.assertTrue(all(p['diagnostic'] and p['font_vram_screen_pixels_match'] and p['no_translated_ink_occluded'] and p['vacant_text_pixels_cleared'] for p in d['pages']))

if __name__=='__main__':unittest.main()
