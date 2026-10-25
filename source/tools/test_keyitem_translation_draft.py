import unittest
from unittest.mock import patch
import prepare_keyitem_translation_draft as draft
from tpl_literals import literals

class KeyitemDraftTests(unittest.TestCase):
    def test_full_inventory_and_controls(self):
        asset,tpl=draft.prepare()
        self.assertEqual(len(asset['units']),39)
        self.assertEqual(len(literals(tpl)),39)
        self.assertFalse(asset['rom_applied'])
        self.assertFalse(asset['release_eligible'])
        self.assertTrue(all(u['state']=='needs_review' for u in asset['units']))

    def test_quantity_boundaries(self):
        asset,_=draft.prepare()
        for script in [6,7,16,17,18]:
            units=[u for u in asset['units'] if u['id'].startswith(f'709408:{script}:')]
            self.assertTrue(units[0]['translation'].endswith('(×'))
            self.assertEqual(units[1]['translation'],'개)')

    def test_row_drift_rejected(self):
        with patch.dict(draft.TEXT,{32:['키 아이템이 없다']}):
            with self.assertRaisesRegex(ValueError,'row structure'):
                draft.prepare()

    def test_missing_literal_rejected(self):
        with patch.dict(draft.TEXT,{6:['씨앗']}):
            with self.assertRaisesRegex(ValueError,'inventory changed'):
                draft.prepare()

if __name__=='__main__':unittest.main()
