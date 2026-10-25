import copy,struct,unittest
from draft_gutsman_pet_talk import DRAFT,TPL_SHA,PAYLOAD_SHA
from report_roll_pet import ROOT,read,sha
from tpl_literals import literals,replace_literals,skeleton
from build_development_patch import validate_literal_numerals,validate_nickname_suffix
class GutsTalk(unittest.TestCase):
    def test_source_scope_and_commands(self):
        p=ROOT/'analysis/full_scope_v1/source_tpl/66A844.tpl';self.assertEqual(TPL_SHA,sha(p.read_bytes()));t=p.read_text(encoding='utf-8-sig');items=literals(t);a=read(ROOT/'translations/gutsman_pet_talk_ko.json');u=a['units'];self.assertEqual(33,len(items));self.assertEqual(31,len(u));self.assertEqual({x.key:x.text for x in items if x.key.split(':')[1]!='13'},{x['id']:x['source'] for x in u});self.assertEqual(skeleton(t),skeleton(replace_literals(t,u)));self.assertFalse(a['review']['release_eligible'])
        for x in u:
            _,s,i=x['id'].split(':');self.assertEqual(DRAFT[int(s)][int(i)],x['translation']);self.assertEqual('needs_review',x['state']);self.assertEqual(x['source'].count('\n'),x['translation'].count('\n'))
    def test_source_root_and_geometry(self):
        c=read(ROOT/'project.json');b=(ROOT/c['source_profile']['filename']).read_bytes();self.assertEqual(c['source_profile']['sha256'],sha(b));self.assertEqual(PAYLOAD_SHA,sha(b[0x66a844:0x66a844+2191]));self.assertEqual(0x0866a844,struct.unpack_from('<I',b,0x38148)[0])
        for rows in DRAFT.values():
            for text in rows:
                self.assertLessEqual(text.count('\n')+1,3)
                for line in text.split('\n'):self.assertLessEqual(sum(12 if '\uac00'<=c<='\ud7a3' else 8 if c==' ' else 11 for c in line),132)
    def test_numerals_and_nickname_fail_closed(self):
        u=read(ROOT/'translations/gutsman_pet_talk_ko.json')['units'];scope=read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['66A844'];validate_literal_numerals(u,scope);validate_nickname_suffix(u,'66A844',scope)
        bad=copy.deepcopy(u);next(x for x in bad if x['id']=='66A844:24:0')['translation']=DRAFT[24][0].replace('1','2')
        with self.assertRaises(ValueError):validate_literal_numerals(bad,scope)
        bad=copy.deepcopy(u);next(x for x in bad if x['id']=='66A844:31:0')['translation']='이름은\n인터넷을'
        with self.assertRaises(ValueError):validate_nickname_suffix(bad,'66A844',scope)
if __name__=='__main__':unittest.main()
