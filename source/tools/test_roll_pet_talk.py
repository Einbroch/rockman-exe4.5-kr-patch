import copy,unittest
from report_roll_pet import ROOT,read,static
from tpl_literals import resolve_units,skeleton
from build_development_patch import translate_literal_scope,validate_nickname_suffix
from run_roll_pet_talk import STEM

class RollPetTalkTests(unittest.TestCase):
    def test_source_scope_and_native_suffix_guard(self):
        a=read(ROOT/'translations/roll_pet_talk_ko.json');u=resolve_units(a);s=read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['664E28'];src=(ROOT/'analysis/tpl_baseline/664E28.tpl').read_text(encoding='utf-8-sig');target=translate_literal_scope(src,u,s)
        self.assertEqual(skeleton(src),skeleton(target));self.assertEqual(len(u),1);validate_nickname_suffix(u,'664E28',s)
        bad=copy.deepcopy(u);bad[0]['translation']='은'+bad[0]['translation'][1:]
        with self.assertRaisesRegex(ValueError,'nickname'):validate_nickname_suffix(bad,'664E28',s)
        m,rom,e,streams,c=static(STEM,'664E28');self.assertEqual(m['translated_units'],1008);self.assertEqual(len(c['protected_nonliteral_scripts']),254);self.assertEqual(c['max_literal_width'],79)
        previous=read(ROOT/'poc/output/exe45_ko_development_roll_subjects_v1.json');current={a['path']:a['sha256'] for a in m['translation_assets']}
        self.assertTrue(all(current[a['path']]==a['sha256'] for a in previous['translation_assets']))

    def test_normal_runtime_and_cumulative_reports(self):
        from report_roll_pet_talk import main
        r=main();self.assertEqual(len(r),15);self.assertEqual(r[-1]['normal_runtime_units'],['664E28:10:0'])
        for p in r[-1]['pages']:
            self.assertEqual(p['nickname'],'ああくん');self.assertEqual(p['nickname_width'],44);self.assertTrue(p['font_vram_screen_pixels_match']);self.assertTrue(p['no_translated_ink_occluded'])

if __name__=='__main__':unittest.main()
