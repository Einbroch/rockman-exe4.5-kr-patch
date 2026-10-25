"""Controlled heading source/parent/single-line ten-cell contracts."""
import copy,unittest
from unittest.mock import patch
import input_heading as model
from report_roll_pet import ROOT,read
from tpl_literals import literals,skeleton

class HeadingContracts(unittest.TestCase):
    def setUp(self):
        self.asset=read(ROOT/model.CHILD)
        self.source=(ROOT/'analysis/full_scope_v1/source_tpl/6368E8.tpl').read_text(encoding='utf-8-sig')
    def test_valid_protects_control_and_unselected(self):
        target=model.replace(self.source,self.asset['units']);self.assertEqual(skeleton(target),skeleton(self.source))
        selected={u['id'] for u in self.asset['units']};before={x.key:x.text for x in literals(self.source)};after={x.key:x.text for x in literals(target)}
        self.assertTrue(all(after[k]==v for k,v in before.items() if k not in selected));self.assertEqual(after[model.ADDED['id']],model.ADDED['translation'])
    def test_parent_changed_rejected(self):
        self.asset['units'][13]['translation']='다른 문구\n'
        with self.assertRaises(ValueError):model.validate(self.asset)
    def test_parent_hash_rejected(self):
        self.asset['parent_asset']['sha256']='0'*64
        with self.assertRaises(ValueError):model.validate(self.asset)
    def test_extra_unit_rejected(self):
        self.asset['units'].append(copy.deepcopy(model.ADDED))
        with self.assertRaises(ValueError):model.validate(self.asset)
    def test_source_mismatch_rejected(self):
        altered=self.source.replace(model.ADDED['source'],'べつの なまえは?')
        with self.assertRaises(ValueError):model.replace(altered,self.asset['units'])
    def test_over_ten_cells_rejected(self):
        changed=dict(model.ADDED,translation='가'*11);self.asset['units'][16]=changed
        with patch.object(model,'ADDED',changed):
            with self.assertRaises(ValueError):model.validate(self.asset)
    def test_newline_rejected(self):
        changed=dict(model.ADDED,translation='가\n나');self.asset['units'][16]=changed
        with patch.object(model,'ADDED',changed):
            with self.assertRaises(ValueError):model.validate(self.asset)
if __name__=='__main__':unittest.main()
