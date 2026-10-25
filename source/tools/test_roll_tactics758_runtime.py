import json,unittest
from report_roll_tactics758_runtime import prepare
from report_chip_library_runtime import read
from build_visibility_poc import ROOT

class RollTactics758Runtime(unittest.TestCase):
    def test_current_product_and_quarantined_roll_question_streams(self):
        r=json.loads(json.dumps(prepare()));self.assertEqual(r,read(ROOT/'analysis/exe45_roll_tactics758_runtime_v1.json'))
        self.assertEqual(r['translated_units'],758);self.assertEqual(r['new_roll_tactics_literals'],2)
        self.assertEqual(r['preserved_other_navi_scripts'],132)
        self.assertEqual(len(r['escape_pixels']),22);self.assertEqual(len(r['clear_and_return']),16)
        d=r['roll_prompt_diagnostic'];self.assertTrue(d['other_save_files_preserved'])
        self.assertEqual([(c['native_script'],c['displayed_script']) for c in d['aliases']],[(1,7),(0,6)])
        self.assertEqual([u['wording_id'] for u in d['wording_links']],['tactics.target','tactics.distance','tactics.target','tactics.distance'])
        for name,script in [('target',6),('distance',7)]:
            self.assertEqual(len(d['reports'][name]['screens']),2)
            self.assertTrue(all(s['pixels_verified'] and s['script']==script for s in d['reports'][name]['screens']))
