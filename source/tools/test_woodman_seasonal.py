import copy,unittest
from build_visibility_poc import ROOT
from report_roll_pet import read
from tpl_literals import literals,replace_literals,skeleton
from build_development_patch import validate_literal_numerals,validate_nickname_suffix
from draft_woodman_seasonal import DRAFT

class WoodSeasonal(unittest.TestCase):
    def test_complete_source_controls_and_manual_draft(self):
        a=read(ROOT/'translations/woodman_seasonal_ko.json');t=(ROOT/'analysis/full_scope_v1/source_tpl/6A2184.tpl').read_text(encoding='utf-8-sig')
        self.assertEqual(41,len(a['units']));self.assertEqual({x.key:x.text for x in literals(t)},{u['id']:u['source'] for u in a['units']})
        self.assertEqual(skeleton(t),skeleton(replace_literals(t,a['units'])));validate_literal_numerals(a['units'],dict(preserve_literal_numerals=True))
        for u in a['units']:
            _,s,i=u['id'].split(':');self.assertEqual(DRAFT[int(s)][int(i)],u['translation'])
        from archive_scripts import script_spans
        source=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes()
        span=script_spans(source[0x6A2184:0x6A2184+1348],21)[1]
        clap=bytes.fromhex('4f3a4f3a83');boundary=bytes.fromhex('e600f1')
        self.assertEqual(2,span.count(clap))
        self.assertEqual(1,span.count(clap+boundary+bytes.fromhex('e46a9cafc3d59cabc0')))
        self.assertEqual(1,span.count(clap+boundary+bytes.fromhex('f90c0187e8')))
    def test_geometry_and_development_policy(self):
        a=read(ROOT/'translations/woodman_seasonal_ko.json')
        for u in a['units']:
            self.assertEqual('needs_review',u['state']);self.assertLessEqual(len(u['translation'].split('\n')),3)
            for line in u['translation'].split('\n'):self.assertLessEqual(sum(12 if '\uac00'<=c<='\ud7a3' else 8 if c==' ' else 11 for c in line),132,(u['id'],line))
            if ':18:' in u['id']:self.assertEqual(u['source'],u['translation'])
        self.assertFalse(a['review']['release_eligible']);self.assertIn('NON-DISTRIBUTION',a['policy'])
        self.assertEqual(['짝짝!','짝짝!'],[DRAFT[1][1],DRAFT[1][3]])
    def test_nickname_and_numeral_rejections(self):
        a=read(ROOT/'translations/woodman_seasonal_ko.json');scope=read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['6A2184'];validate_nickname_suffix(a['units'],'6A2184',scope)
        bad=copy.deepcopy(a['units']);u=next(u for u in bad if u['id']=='6A2184:1:4');u['translation']='은'+u['translation'][1:]
        with self.assertRaises(ValueError):validate_nickname_suffix(bad,'6A2184',scope)
        bad=copy.deepcopy(a['units']);next(u for u in bad if u['id']=='6A2184:7:0')['translation']='오늘은 7월8일,\n칠석이구나・・・'
        with self.assertRaises(ValueError):validate_literal_numerals(bad,scope)

if __name__=='__main__':unittest.main()
