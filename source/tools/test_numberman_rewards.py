import copy,unittest
from report_roll_pet import ROOT,read
from tpl_literals import resolve_units,skeleton
from build_development_patch import selected_scope,translate_literal_scope
from numberman_reward_model import model,validate_layout

class RewardsTests(unittest.TestCase):
    def test_protected_scope(self):
        a=read(ROOT/'translations/numberman_training_rewards_ko.json');o=read(ROOT/'translations/numberman_training_results_ko.json');self.assertEqual(a['units'][:33],o['units']);self.assertEqual(a['wordings'][:24],o['wordings'])
        u=resolve_units(a);self.assertEqual(len(u),39);s=selected_scope(read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['687910'],a)
        src=(ROOT/'analysis/tpl_baseline/687910.tpl').read_text(encoding='utf-8');dst=translate_literal_scope(src,u,s);self.assertEqual(skeleton(src),skeleton(dst));self.assertFalse(a['review']['release_eligible'])
    def test_composed_maxima_and_overflow(self):
        src=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes();p=model(src);self.assertEqual(max(p['zenny_values']),800);self.assertEqual(max(p['bugfrag_values']),5)
        rows=[{'id':k,'line_advance_pixels':[30]} for k in ['687910:16:0','687910:18:0','687910:18:1','687910:52:2','687910:53:2','687910:53:3']]
        s={'reward_variable_profile':'numberman-minigame-buffer3-v1','max_line_advance':132};self.assertEqual(len(validate_layout(src,rows,s)['composed_lines']),4)
        rows[1]['line_advance_pixels']=[130]
        with self.assertRaisesRegex(ValueError,'overflow'):validate_layout(src,rows,s)
    def test_source_consumer_mutation_rejected(self):
        b=bytearray((ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes());b[0x363C2]^=1
        with self.assertRaises(ValueError):model(b)

if __name__=='__main__':unittest.main()
