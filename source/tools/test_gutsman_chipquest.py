import copy,unittest
from report_roll_pet import ROOT,read
from build_development_patch import selected_scope,validate_characters
from gutsman_chipquest_model import validate_parent,validate_layout,encoded_prefix
from tpl_literals import replace_literals,skeleton
from dialogue_chip_name import construct
import test_dialogue_chip_name as prior
from inventory_full_scope import inherited_guts_input
from report_roll_pet import sha

class GutsChip(unittest.TestCase):
    def test_parent_and_controls(self):
        a=read(ROOT/'translations/gutsman_pet_chipquest_ko.json');validate_parent(a);t=(ROOT/'analysis/full_scope_v1/source_tpl/66A844.tpl').read_text(encoding='utf-8-sig');self.assertEqual(skeleton(t),skeleton(replace_literals(t,a['units'])));bad=copy.deepcopy(a);bad['units'][0]['translation']='변경'
        with self.assertRaises(ValueError):validate_parent(bad)
    def test_layout_rejects_variable_overflow_anchor(self):
        a=read(ROOT/'translations/gutsman_pet_chipquest_ko.json');scope=selected_scope(read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['66A844'],a);s=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes();layout=[dict(id='66A844:13:0',line_advance_pixels=[81,11]),dict(id='66A844:13:1',line_advance_pixels=[23,59])];validate_layout(s,a['units'],layout,scope);bad=copy.deepcopy(layout);bad[1]['line_advance_pixels'][0]=60
        with self.assertRaises(ValueError):validate_layout(s,a['units'],bad,scope)
        self.assertTrue(encoded_prefix().endswith(b'\xe8\x92'))
    def test_additional_exact_guard_and_range(self):
        s,a,ar=prior.DialogueChipNameTests().inputs();out,w,h=construct(s,b'',ar,a,guts_command=0x08801234);self.assertEqual(h['gutsman_command_stream'],0x08801234);self.assertEqual(h['machine_code'][0]['literal_values']['guts_command_stream'],0x08801234);self.assertTrue(all(r['final_placement_roundtrip'] for r in h['machine_code']))
        for bad in [0,0x08001234,h['command_stream']]:
            with self.assertRaises(ValueError):construct(s,b'',ar,a,guts_command=bad)
    def test_read_only_parent_not_a_duplicate_selected_writer(self):
        from gutsman_chipquest_model import PARENT_SHA
        p=ROOT/'translations/gutsman_pet_chipquest_ko.json';child=dict(path='translations/gutsman_pet_chipquest_ko.json',archive='66A844',sha256=sha(p.read_bytes()));item=dict(path='translations/gutsman_pet_talk_ko.json',archive='66A844',sha256=PARENT_SHA,carry_units=31,scope='read-only inherited31 units');m=dict(translation_assets=[child,item]);self.assertTrue(inherited_guts_input(item,m));self.assertFalse(inherited_guts_input(child,m))
        with self.assertRaises(ValueError):inherited_guts_input(dict(item,carry_units=30),m)
        with self.assertRaises(ValueError):inherited_guts_input(item,dict(translation_assets=[item]))

if __name__=='__main__':unittest.main()
