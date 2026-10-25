"""Frozen weekday-v1 artifact checks and nickname suffix rejection fixture."""
import unittest
from report_roll_pet import ROOT,read,static
from tpl_literals import resolve_units,skeleton
from build_development_patch import selected_scope,translate_literal_scope,validate_nickname_suffix
from run_roll_pet_weekday import STEM

class RollPetWeekdayTests(unittest.TestCase):
    def inputs(self):
        a=read(ROOT/'translations/roll_pet_weekday_ko.json');u=resolve_units(a);s=selected_scope(read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['664E28'],a);return u,s

    def test_frozen_source_controls_and_protected_slots(self):
        u,s=self.inputs();old=resolve_units(read(ROOT/'translations/roll_pet_undernet_ko.json'));src=(ROOT/'analysis/tpl_baseline/664E28.tpl').read_text(encoding='utf-8-sig')
        self.assertEqual(u[:24],old);self.assertEqual(skeleton(src),skeleton(translate_literal_scope(src,u,s)));self.assertEqual(s['nickname_suffix_scripts'],[10,28,33]);validate_nickname_suffix(u,'664E28',s)
        m,rom,e,streams,c=static(STEM,'664E28');self.assertEqual(m['translated_units'],1036);self.assertEqual(len(c['protected_nonliteral_scripts']),231);self.assertEqual(len(streams),29)

    def test_nickname_first_row_change_rejected(self):
        u,s=self.inputs();bad=[dict(v) for v in u];next(v for v in bad if v['id']=='664E28:28:0')['translation']='너는\n오피셜\n토너먼트에'
        with self.assertRaises(ValueError):validate_nickname_suffix(bad,'664E28',s)

    def test_weekday_native_nickname_then_clear(self):
        from report_roll_pet_weekday import main
        r=main();self.assertEqual(len(r),27);self.assertEqual([d['diagnostic_renderer_units'] for d in r[-3:]],[['664E28:26:0','664E28:26:1'],['664E28:28:0','664E28:28:1'],['664E28:29:0']])
        self.assertTrue(all(not d['release_eligible'] and d['normal_runtime_units']==[] and all(p['font_vram_screen_pixels_match'] and p['no_translated_ink_occluded'] and p['vacant_text_pixels_cleared'] for p in d['pages']) for d in r[-3:]))
        pages=r[-2]['pages'];self.assertEqual([p['nickname_width'] for p in pages],[44,0,0]);self.assertEqual(pages[0]['nickname'],'ああくん');self.assertTrue(all(p['nickname']=='' for p in pages[1:]));self.assertTrue(read(ROOT/'analysis/roll_pet_weekday_v1/weekday_route.json')['normal_controller_only'])

if __name__=='__main__':unittest.main()
