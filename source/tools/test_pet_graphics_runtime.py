import json,unittest
from build_visibility_poc import ROOT,sha,require_hash
from report_fixedcell_runtime import verify_route
from pet_graphics_font import construct
from report_pet_graphics_runtime import sample

class PetGraphicRuntimeTests(unittest.TestCase):
    def test_exact_rom_all_focus_and_prompt_masks(self):
        report=json.loads((ROOT/'analysis/pet_font_v2/runtime.json').read_text(encoding='utf-8'))
        rom=ROOT/'poc/output/exe45_ko_development_pet_graphics_v1.gba';require_hash(rom,report['rom_sha256'])
        asset=json.loads((ROOT/'translations/pet_menu_graphics_ko.json').read_text(encoding='utf-8'))
        source=ROOT/json.loads((ROOT/'project.json').read_text())['source_profile']['filename']
        block,prepared=construct(source.read_bytes(),asset);self.assertEqual(prepared,report['prepared_asset'])
        observed=[]
        for name in ('focus','prompts'):
            route=ROOT/('poc/runtime/pet-graphics-v1-'+name);r=verify_route(route,report['rom_sha256'],set())
            for step in r['capture_steps']:observed.append(sample(route,step,block,step-1 if name=='focus' else None))
        self.assertEqual(observed,report['visible_label_mask_samples'])
        self.assertEqual(len(observed),21);self.assertTrue(report['passed']);self.assertFalse(report['release_eligible'])

if __name__=='__main__':unittest.main()
