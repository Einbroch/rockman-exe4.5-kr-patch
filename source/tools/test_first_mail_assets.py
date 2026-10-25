"""Source-bound selected mail inventory and guard regressions."""
import json,unittest
from build_visibility_poc import ROOT
from first_mail import prepare,scopes,SPECS,validate_selected

class MailTests(unittest.TestCase):
    def test_news_literal_and_identity_guards(self):
        import copy
        body=json.loads((ROOT/prepare('news')[0]).read_text(encoding='utf8'))
        for key,field,value in [('6DD9AC:9:7','translation','절대로 넷 배틀에\n도전하는 일이 없도록\n해 주세요!!'),('6DD9AC:10:0','id','6DD9AC:11:0')]:
            changed=copy.deepcopy(body)
            next(u for u in changed['units'] if u['id']==key)[field]=value
            with self.assertRaises(ValueError):validate_selected(changed)
    def test_news_scope_and_carry(self):
        from first_mail import selected_units,specifications
        paths=prepare('news')
        self.assertEqual(sum(len(json.loads((ROOT/p).read_text(encoding='utf8'))['units']) for p in paths),84)
        body=selected_units('6DD9AC','news')
        self.assertEqual([u for u in body if int(u['id'].split(':')[1])<8],selected_units('6DD9AC',True))
        self.assertEqual(specifications('news')['6DD9AC']['scripts'],[0,1,2,3,8,9,10])
        for p in paths:validate_selected(json.loads((ROOT/p).read_text(encoding='utf8')))
    def test_full_header_scope_and_extent(self):
        import copy
        from first_mail import FULL_HEADER_SCRIPTS,specifications
        paths=prepare('news',True);self.assertEqual(len(paths),3)
        header=json.loads((ROOT/paths[2]).read_text(encoding='utf8'))
        self.assertEqual(header['scope_variant'],'full-mail-header-v1')
        self.assertEqual([int(u['id'].split(':')[1]) for u in header['units']],FULL_HEADER_SCRIPTS)
        self.assertEqual(specifications('news',True)['6DD63C']['count'],22)
        self.assertLessEqual(max(len(u['translation'])*8 for u in header['units']),88)
        validate_selected(header)
        broken=copy.deepcopy(header);next(u for u in broken['units'] if u['id']=='6DD63C:7:0')['translation']='또 다른 1체의 다크로이드'
        with self.assertRaises(ValueError):validate_selected(broken)
    def test_official_scope_and_carry(self):
        from first_mail import selected_units,specifications
        paths=prepare(True)
        self.assertEqual(sum(len(json.loads((ROOT/p).read_text(encoding='utf8'))['units']) for p in paths),62)
        body=selected_units('6DD9AC',True)
        self.assertEqual([u for u in body if u['id'].split(':')[1]=='0'],selected_units('6DD9AC'))
        self.assertEqual(specifications(True)['6DD9AC']['scripts'],[0,1,2,3])
        for p in paths:validate_selected(json.loads((ROOT/p).read_text(encoding='utf8')))
    def test_exact_existing_drafts_and_inventory(self):
        paths=prepare();self.assertEqual(len(paths),3)
        self.assertEqual(sum(len(json.loads((ROOT/p).read_text(encoding='utf8'))['units']) for p in paths),30)
        source=(ROOT/'Rockman EXE 4.5 Real Operation (J)(Independent).gba').read_bytes()
        registered=scopes(source)
        for a,s in SPECS.items():
            self.assertLessEqual(s['destination']+s['cap'],s['next'])
            self.assertEqual(registered[a]['pointers'],s['pointers'])
    def test_changed_mail_destinations_rejected(self):
        source=bytearray((ROOT/'Rockman EXE 4.5 Real Operation (J)(Independent).gba').read_bytes())
        for at in [0xEC158,0x405F0,0x4066C,0x4119C,0x411C4,0x4057C,0x405F8,0x41140]:
            broken=source[:];broken[at]^=1
            with self.assertRaises(ValueError):scopes(broken)
    def test_last_page_layout_guard(self):
        paths=prepare();a=json.loads((ROOT/paths[0]).read_text(encoding='utf8'));validate_selected(a)
        a['units'][-1]['translation']='부디 주의하시며,\n쾌적한 넷 배틀러\n생활을 즐기시길 바랍니다'
        with self.assertRaises(ValueError):validate_selected(a)

if __name__=='__main__':unittest.main()
