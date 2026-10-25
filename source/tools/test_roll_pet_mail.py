import unittest
from report_roll_pet import ROOT,read,static
from tpl_literals import resolve_units,skeleton
from build_development_patch import selected_scope,translate_literal_scope,validate_nickname_suffix
from run_roll_pet_mail import STEM

class RollPetMailTests(unittest.TestCase):
    def test_previous_units_and_nickname_guards(self):
        a=read(ROOT/'translations/roll_pet_mail_ko.json');u=resolve_units(a);old=resolve_units(read(ROOT/'translations/roll_pet_events_ko.json'));s=selected_scope(read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['664E28'],a);src=(ROOT/'analysis/tpl_baseline/664E28.tpl').read_text(encoding='utf-8-sig')
        self.assertEqual(u[:20],old);self.assertEqual(skeleton(src),skeleton(translate_literal_scope(src,u,s)));self.assertEqual(s['nickname_suffix_scripts'],[10,33]);validate_nickname_suffix(u,'664E28',s)
        bad=[dict(v) for v in u];bad[-1]['translation']='너는'+bad[-1]['translation']
        with self.assertRaises(ValueError):validate_nickname_suffix(bad,'664E28',s)
        m,rom,e,streams,c=static(STEM,'664E28');self.assertEqual(m['translated_units'],1029);self.assertEqual(len(c['protected_nonliteral_scripts']),235);self.assertEqual(len(streams),22)

    def test_qualifier_and_nickname_runtime(self):
        from report_roll_pet_mail import main
        r=main();self.assertEqual(len(r),23);self.assertEqual([d['diagnostic_renderer_units'] for d in r[-2:]],[['664E28:32:0'],['664E28:33:0']])
        for d in r[-2:]:
            self.assertEqual(d['normal_runtime_units'],[]);self.assertTrue(all(p['font_vram_screen_pixels_match'] and p['no_translated_ink_occluded'] and p['vacant_text_pixels_cleared'] for p in d['pages']))
        self.assertTrue(all(p['nickname']=='ああくん' and p['nickname_width']==44 for p in r[-1]['pages']))

if __name__=='__main__':unittest.main()
