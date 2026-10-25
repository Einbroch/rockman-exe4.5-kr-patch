import copy,struct,unittest
from report_roll_pet import ROOT,read
from build_visibility_poc import require_hash
from tpl_literals import literals,replace_literals,skeleton
from draft_gutsman_operations import PACKS
from build_development_patch import validate_literal_numerals,validate_nickname_suffix
from archive_scripts import script_spans

class GutsManOperations(unittest.TestCase):
    def test_all_sources_and_commands(self):
        counts=[]
        for ar,p in PACKS.items():
            a=read(ROOT/f"translations/{p['name']}.json");t=(ROOT/f'analysis/full_scope_v1/source_tpl/{ar}.tpl').read_text(encoding='utf-8-sig');counts.append(len(a['units']))
            self.assertEqual({x.key:x.text for x in literals(t)},{u['id']:u['source'] for u in a['units']});self.assertEqual(skeleton(t),skeleton(replace_literals(t,a['units'])));validate_literal_numerals(a['units'],dict(preserve_literal_numerals=True))
            for u in a['units']:
                _,s,i=u['id'].split(':');self.assertEqual(p['draft'][int(s)][int(i)],u['translation']);self.assertEqual(u['source'].count('\n'),u['translation'].count('\n'));self.assertEqual('needs_review',u['state'])
            self.assertFalse(a['review']['release_eligible'])
        self.assertEqual([2,1,28],counts)
    def test_geometry_names_and_timing(self):
        for p in PACKS.values():
            for rows in p['draft'].values():
                for text in rows:
                    for line in text.split('\n'):self.assertLessEqual(sum(12 if '\uac00'<=c<='\ud7a3' else 8 if c==' ' else 11 for c in line),132)
        a=read(ROOT/'translations/gutsman_mail_alert_ko.json');scope=read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['666820'];validate_nickname_suffix(a['units'],'666820',scope)
        for u in a['units']:
            if u['source']=='!!':self.assertEqual('!!',u['translation'])
        self.assertEqual(14,sum(u['source']=='!!' for u in a['units']))
        t=(ROOT/'analysis/full_scope_v1/source_tpl/6664D0.tpl').read_text(encoding='utf-8-sig');self.assertIn('frames = 30',t);self.assertIn('.EXE、',PACKS['6664D0']['draft'][1][0])
        self.assertIn('당해',PACKS['6663B8']['draft'][2][0]);self.assertIn('다녀왔',PACKS['6663B8']['draft'][1][0])
    def test_native_bindings_and_row_rejection(self):
        c=read(ROOT/'project.json');p=ROOT/c['source_profile']['filename'];require_hash(p,c['source_profile']['sha256']);b=p.read_bytes()
        for root,ar in [(0x38118,'6663B8'),(0x38120,'6664D0'),(0x38128,'666820')]:self.assertEqual(0x08000000+int(ar,16),struct.unpack_from('<I',b,root)[0])
        spans=script_spans(b[0x666820:0x666820+1337],255)
        anchor=bytes.fromhex('f604e18d8383fd009b00ed006000fd009b00ed006000f1')
        for script in [1,2,3,4,5,6,7,20,21,22,23,24,25,26]:
            self.assertEqual(2,spans[script].count(bytes.fromhex('8383')))
            self.assertEqual(1,spans[script].count(anchor))
        a=read(ROOT/'translations/gutsman_mail_alert_ko.json');bad=copy.deepcopy(a['units']);bad[1]['translation']='메일이거스!!'
        with self.assertRaises(ValueError):replace_literals((ROOT/'analysis/full_scope_v1/source_tpl/666820.tpl').read_text(encoding='utf-8-sig'),bad)

if __name__=='__main__':unittest.main()
