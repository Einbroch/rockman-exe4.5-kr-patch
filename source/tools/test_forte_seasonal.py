import copy,unittest
from build_visibility_poc import ROOT
from report_roll_pet import read
from tpl_literals import literals,replace_literals,skeleton
from build_development_patch import validate_literal_numerals
from draft_forte_seasonal import DRAFT

class ForteSeasonal(unittest.TestCase):
    def test_complete_source_controls_and_manual_draft(self):
        a=read(ROOT/'translations/forte_seasonal_ko.json');t=(ROOT/'analysis/full_scope_v1/source_tpl/6D5A9C.tpl').read_text(encoding='utf-8-sig')
        self.assertEqual(33,len(a['units']));self.assertEqual({x.key:x.text for x in literals(t)},{u['id']:u['source'] for u in a['units']})
        self.assertEqual(skeleton(t),skeleton(replace_literals(t,a['units'])));validate_literal_numerals(a['units'],dict(preserve_literal_numerals=True))
        for u in a['units']:
            _,s,i=u['id'].split(':');self.assertEqual(DRAFT[int(s)][int(i)],u['translation'])
    def test_geometry_meaning_and_development_policy(self):
        a=read(ROOT/'translations/forte_seasonal_ko.json')
        for u in a['units']:
            self.assertEqual('needs_review',u['state']);self.assertLessEqual(len(u['translation'].split('\n')),3)
            for line in u['translation'].split('\n'):self.assertLessEqual(sum(12 if '\uac00'<=c<='\ud7a3' else 8 if c==' ' else 11 for c in line),132,(u['id'],line))
            if ':18:' in u['id'] or u['id']=='6D5A9C:1:2':self.assertEqual(u['source'],u['translation'])
        self.assertFalse(a['review']['release_eligible']);self.assertIn('NON-DISTRIBUTION',a['policy']);self.assertEqual('・・・・・・',DRAFT[1][2])
        self.assertIn('빼앗는',DRAFT[3][2]);self.assertIn('힘으로라도',DRAFT[4][2]);self.assertIn('빌지 않는다',DRAFT[7][2]);self.assertNotIn('축하',DRAFT[11][0])
    def test_rows_rejected_and_source_navi_binding(self):
        import struct
        from build_visibility_poc import require_hash
        a=read(ROOT/'translations/forte_seasonal_ko.json');bad=copy.deepcopy(a['units']);next(u for u in bad if u['id']=='6D5A9C:8:0')['translation']='크리스마스\n이브다・・・'
        with self.assertRaises(ValueError):replace_literals((ROOT/'analysis/full_scope_v1/source_tpl/6D5A9C.tpl').read_text(encoding='utf-8-sig'),bad)
        c=read(ROOT/'project.json');p=ROOT/c['source_profile']['filename'];require_hash(p,c['source_profile']['sha256']);b=p.read_bytes()
        for x,y in [(0x382ac,0x868bbb4),(0x38548,0x86d2180),(0x38558,0x86d27a0),(0x3857c,0x86d5a9c)]:self.assertEqual(y,struct.unpack_from('<I',b,x)[0])
        self.assertIn('フォルテ.EXE',(ROOT/'analysis/full_scope_v1/source_tpl/6D27A0.tpl').read_text(encoding='utf-8-sig'))

if __name__=='__main__':unittest.main()
