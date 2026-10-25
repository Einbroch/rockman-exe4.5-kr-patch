import unittest
from report_roll_pet import ROOT,read,static
from tpl_literals import resolve_units,skeleton,literals
from build_development_patch import translate_literal_scope,validate_nickname_suffix
from run_roll_mail_alert import STEM

class RollMailAlertTests(unittest.TestCase):
    def inputs(self):
        a=read(ROOT/'translations/roll_mail_alert_ko.json');return resolve_units(a),read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['661060']

    def test_protected_controls_and_initial_literals(self):
        u,s=self.inputs();src=(ROOT/'analysis/tpl_baseline/661060.tpl').read_text(encoding='utf-8-sig');target=translate_literal_scope(src,u,s)
        self.assertEqual(skeleton(src),skeleton(target));self.assertEqual(len(u),14);validate_nickname_suffix(u,'661060',s)
        m,rom,e,streams,c=static(STEM,'661060');self.assertEqual(m['translated_units'],1050);self.assertEqual(len(c['protected_nonliteral_scripts']),241);self.assertEqual(len(streams),14)

    def test_nickname_growth_rejected(self):
        u,s=self.inputs();u=[dict(x) for x in u];u[0]['translation']='너는\n메일이 왔어!!'
        with self.assertRaises(ValueError):validate_nickname_suffix(u,'661060',s)

    def test_normal_mail_arrival(self):
        from report_roll_mail_alert import arrival_report
        r=arrival_report();self.assertEqual(r['normal_runtime_units'],['661060:1:1']);self.assertEqual(len(r['runtime_open_units']),13);self.assertEqual([p['nickname_width'] for p in r['pages']],[0,0,44,44]);self.assertTrue(all(p['font_vram_screen_pixels_match'] and p['vacant_text_pixels_cleared'] for p in r['pages']));self.assertFalse(r['release_eligible'])

if __name__=='__main__':unittest.main()
