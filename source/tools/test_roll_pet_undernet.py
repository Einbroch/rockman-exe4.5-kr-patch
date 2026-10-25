import unittest
from report_roll_pet import ROOT,read,static
from tpl_literals import resolve_units,skeleton
from build_development_patch import selected_scope,translate_literal_scope,validate_nickname_suffix
from run_roll_pet_undernet import STEM

class RollPetUndernetTests(unittest.TestCase):
    def test_previous_units_controls_and_denominator(self):
        a=read(ROOT/'translations/roll_pet_undernet_ko.json');u=resolve_units(a);old=resolve_units(read(ROOT/'translations/roll_pet_mail_ko.json'));s=selected_scope(read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['664E28'],a);src=(ROOT/'analysis/tpl_baseline/664E28.tpl').read_text(encoding='utf-8-sig')
        self.assertEqual(u[:22],old);self.assertEqual([v['id'] for v in u[22:]],['664E28:27:0','664E28:27:1']);self.assertEqual(skeleton(src),skeleton(translate_literal_scope(src,u,s)));self.assertEqual(s['nickname_suffix_scripts'],[10,33]);validate_nickname_suffix(u,'664E28',s)
        m,rom,e,streams,c=static(STEM,'664E28');self.assertEqual(m['translated_units'],1031);self.assertEqual(len(c['protected_nonliteral_scripts']),234);self.assertEqual(len(streams),24)

    def test_two_page_renderer_and_clear(self):
        from report_roll_pet_undernet import main
        r=main();self.assertEqual(len(r),24);d=r[-1];self.assertEqual(d['diagnostic_renderer_units'],['664E28:27:0','664E28:27:1']);self.assertEqual(d['normal_runtime_units'],[]);self.assertFalse(d['release_eligible']);self.assertEqual([p['step'] for p in d['pages']],[2,4,5])
        self.assertTrue(all(p['font_vram_screen_pixels_match'] and p['no_translated_ink_occluded'] and p['vacant_text_pixels_cleared'] and p['nickname_width']==0 for p in d['pages']))

if __name__=='__main__':unittest.main()
