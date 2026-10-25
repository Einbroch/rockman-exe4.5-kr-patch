"""Controlled parent/source/padding/command preservation regression fixtures."""
import copy,unittest
from report_roll_pet import ROOT,read
from input_confirmation import validate,replace,CHILD
from tpl_literals import literals,skeleton
class ConfirmationContracts(unittest.TestCase):
    def setUp(self):
        self.asset=read(ROOT/CHILD)
        self.source=(ROOT/'analysis/full_scope_v1/source_tpl/6368E8.tpl').read_text(encoding='utf-8-sig')
    def test_preserves_commands_and_unselected(self):
        validate(self.asset);target=replace(self.source,self.asset['units']);self.assertEqual(skeleton(self.source),skeleton(target))
        before={x.key:x.text for x in literals(self.source)};after={x.key:x.text for x in literals(target)};selected={u['id'] for u in self.asset['units']}
        self.assertTrue(all(after[k]==v for k,v in before.items() if k not in selected))
    def test_parent_wording_mutation_rejected(self):
        a=copy.deepcopy(self.asset);a['units'][0]['translation']='바뀐 문구'
        with self.assertRaises(ValueError):validate(a)
    def test_parent_digest_rejected(self):
        a=copy.deepcopy(self.asset);a['parent_asset']['sha256']='0'*64
        with self.assertRaises(ValueError):validate(a)
    def test_missing_option_rejected(self):
        a=copy.deepcopy(self.asset);a['units'].pop()
        with self.assertRaises(ValueError):validate(a)
    def test_protected_source_rejected(self):
        a=copy.deepcopy(self.asset);a['units'][13]['source']='다른 원문\n'
        with self.assertRaises(ValueError):replace(self.source,a['units'])
    def test_prompt_newline_rejected(self):
        a=copy.deepcopy(self.asset);a['units'][13]['translation']=a['units'][13]['translation'].rstrip('\n')
        with self.assertRaises(ValueError):replace(self.source,a['units'])
    def test_choice_padding_rejected(self):
        a=copy.deepcopy(self.asset);a['units'][14]['translation']='예'
        with self.assertRaises(ValueError):replace(self.source,a['units'])
    def test_option_slot_overflow_rejected(self):
        a=copy.deepcopy(self.asset);a['units'][15]['translation']='가'*7
        with self.assertRaises(ValueError):validate(a)
    def test_combined_choice_overflow_rejected(self):
        a=copy.deepcopy(self.asset);a['units'][14]['translation']='가가가  ';a['units'][15]['translation']='가가가'
        with self.assertRaises(ValueError):validate(a)
    def test_prompt_overflow_rejected(self):
        a=copy.deepcopy(self.asset);a['units'][13]['translation']='가'*16+'\n'
        with self.assertRaises(ValueError):validate(a)
if __name__=='__main__':unittest.main()
