import copy,struct,unittest
from draft_gutsman_competition import DRAFT,TPL_SHA,PAYLOAD_SHA
from report_roll_pet import ROOT,read,sha
from tpl_literals import literals,replace_literals,skeleton
from build_development_patch import validate_literal_numerals,validate_nickname_suffix
class GutsCompetition(unittest.TestCase):
    def test_complete_source_and_commands(self):
        p=ROOT/'analysis/full_scope_v1/source_tpl/666D5C.tpl';self.assertEqual(TPL_SHA,sha(p.read_bytes()));t=p.read_text(encoding='utf-8-sig');a=read(ROOT/'translations/gutsman_competition_ko.json');u=a['units'];self.assertEqual(10,len(u));self.assertEqual({x.key:x.text for x in literals(t)},{x['id']:x['source'] for x in u});self.assertEqual(skeleton(t),skeleton(replace_literals(t,u)))
        for x in u:
            _,s,i=x['id'].split(':');self.assertEqual(DRAFT[int(s)][int(i)],x['translation']);self.assertEqual('needs_review',x['state'])
        self.assertFalse(a['review']['release_eligible']);validate_literal_numerals(u,dict(preserve_literal_numerals=True))
    def test_native_scope_and_nickname_constraints(self):
        c=read(ROOT/'project.json');b=(ROOT/c['source_profile']['filename']).read_bytes();self.assertEqual(c['source_profile']['sha256'],sha(b));self.assertEqual(PAYLOAD_SHA,sha(b[0x666D5C:0x666D5C+473]));self.assertEqual(0x08666D5C,struct.unpack_from('<I',b,0x3812c)[0]);a=read(ROOT/'translations/gutsman_competition_ko.json');scope=read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['666D5C'];validate_nickname_suffix(a['units'],'666D5C',scope)
        bad=copy.deepcopy(a['units']);bad[3]['translation']='와\n2명이 함께 이룬\n영광이거스!!'
        with self.assertRaises(ValueError):validate_nickname_suffix(bad,'666D5C',scope)
        bad=copy.deepcopy(a['units']);bad[3]['translation']=bad[3]['translation'].replace('2','둘')
        with self.assertRaises(ValueError):validate_literal_numerals(bad,dict(preserve_literal_numerals=True))
    def test_prose_geometry_and_context(self):
        for rows in DRAFT.values():
            for text in rows:
                self.assertLessEqual(len(text.split('\n')),3)
                for line in text.split('\n'):self.assertLessEqual(sum(12 if '\uac00'<=c<='\ud7a3' else 8 if c==' ' else 11 for c in line),132)
        self.assertIn('분하',DRAFT[1][0]);self.assertIn('다음',DRAFT[1][1]);self.assertIn('함께',DRAFT[2][1]);self.assertIn('등록',DRAFT[10][0]);self.assertEqual('!',DRAFT[10][0].split('\n')[0])
if __name__=='__main__':unittest.main()
