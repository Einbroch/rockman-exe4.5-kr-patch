import copy,unittest
from report_roll_pet import ROOT,read
from tpl_literals import literals,resolve_units,skeleton
from build_development_patch import selected_scope,translate_literal_scope,validate_nickname_suffix

class ResultsTests(unittest.TestCase):
    def test_scope_and_protected_readouts(self):
        a=read(ROOT/'translations/numberman_training_results_ko.json');old=read(ROOT/'translations/numberman_training_intro_ko.json')
        self.assertEqual(a['units'][:16],old['units']);self.assertEqual(a['wordings'][:15],old['wordings']);self.assertFalse(a['review']['release_eligible'])
        u=resolve_units(a);self.assertEqual(len(u),33);s=selected_scope(read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['687910'],a)
        self.assertEqual(s['literal_ids'],[x['id'] for x in u]);self.assertEqual(s['nickname_suffix_scripts'],[13])
        t=(ROOT/'analysis/tpl_baseline/687910.tpl').read_text(encoding='utf-8');v=translate_literal_scope(t,u,s)
        self.assertEqual(skeleton(t),skeleton(v));chosen={x['id'] for x in u}
        self.assertEqual({x.key:x.text for x in literals(t) if x.key not in chosen},{x.key:x.text for x in literals(v) if x.key not in chosen})
        self.assertTrue({'687910:16:0','687910:18:0','687910:18:1','687910:52:2','687910:53:2','687910:53:3'}.isdisjoint(chosen))
        for x in u:self.assertEqual(x['source'].count('\n'),x['translation'].count('\n'))
        validate_nickname_suffix(u,'687910',s)
        self.assertEqual(next(x for x in u if x['id']=='687910:13:0')['translation'].split('\n')[0],'、')
    def test_nickname_suffix_growth_rejected(self):
        a=read(ROOT/'translations/numberman_training_results_ko.json');u=copy.deepcopy(resolve_units(a));s=selected_scope(read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['687910'],a)
        next(x for x in u if x['id']=='687910:13:0')['translation']='님、\n이런 계산도\n못하시다니・・・'
        with self.assertRaisesRegex(ValueError,'nickname'):validate_nickname_suffix(u,'687910',s)
    def test_identical_praise_wordings_reused(self):
        a=read(ROOT/'translations/numberman_training_results_ko.json');u={x['id']:x for x in a['units']}
        for i in range(3):self.assertEqual(u[f'687910:14:{i}']['wording_id'],u[f'687910:51:{i}']['wording_id'])

if __name__=='__main__':unittest.main()
