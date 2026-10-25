import copy,struct,unittest
from build_visibility_poc import ROOT,require_hash
from report_roll_pet import read
from tpl_literals import literals,replace_literals,skeleton
from draft_gutsman_pet import DRAFT
from build_development_patch import validate_literal_numerals

class GutsManPET(unittest.TestCase):
    def test_source_and_all_controls(self):
        a=read(ROOT/'translations/gutsman_pet_menu_ko.json');t=(ROOT/'analysis/full_scope_v1/source_tpl/665F3C.tpl').read_text(encoding='utf-8-sig');self.assertEqual(44,len(a['units']))
        self.assertEqual({x.key:x.text for x in literals(t)},{u['id']:u['source'] for u in a['units']});self.assertEqual(skeleton(t),skeleton(replace_literals(t,a['units'])));validate_literal_numerals(a['units'],dict(preserve_literal_numerals=True))
        for u in a['units']:
            _,s,i=u['id'].split(':');self.assertEqual(DRAFT[int(s)][int(i)],u['translation'])
            self.assertEqual(u['source'].count('\n'),u['translation'].count('\n'))
    def test_options_geometry_and_meaning(self):
        a=read(ROOT/'translations/gutsman_pet_menu_ko.json');sp=read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['665F3C'];self.assertEqual(14,len(sp['choice_scripts']));self.assertFalse(a['review']['release_eligible'])
        for u in a['units']:
            self.assertEqual('needs_review',u['state'])
            for line in u['translation'].split('\n'):self.assertLessEqual(sum(12 if '\uac00'<=c<='\ud7a3' else 8 if c==' ' else 11 for c in line),132)
        for s in sp['choice_scripts']:
            self.assertEqual(2,DRAFT[s][0].count('\n'));self.assertTrue(DRAFT[s][0].endswith('\n'));self.assertEqual(['예  ','아니요'],DRAFT[s][1:]);self.assertLessEqual(24+8+12+16+8+36,132)
        self.assertIn('화면',DRAFT[8][0]);self.assertIn('데이터',DRAFT[16][0]);self.assertIn('안 끝났',DRAFT[20][0])
    def test_binding_and_reject_row_change(self):
        c=read(ROOT/'project.json');p=ROOT/c['source_profile']['filename'];require_hash(p,c['source_profile']['sha256']);b=p.read_bytes();self.assertEqual(0x8665F3C,struct.unpack_from('<I',b,0x38114)[0]);self.assertEqual(0x8665EB8,struct.unpack_from('<I',b,0x38110)[0])
        a=read(ROOT/'translations/gutsman_pet_menu_ko.json');bad=copy.deepcopy(a['units']);bad[1]['translation']=bad[1]['translation'].rstrip('\n')
        with self.assertRaises(ValueError):replace_literals((ROOT/'analysis/full_scope_v1/source_tpl/665F3C.tpl').read_text(encoding='utf-8-sig'),bad)

if __name__=='__main__':unittest.main()
