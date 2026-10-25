import json,unittest
from build_visibility_poc import ROOT,sha
from equipment_guides import construct,INSTALL
from archive_scripts import verify_untouched_scripts
from verify_tpi_index import lz77_decompress
from report_equipment_guides_runtime import main

def read(p):return json.loads(p.read_text(encoding='utf-8'))

class RollEquipmentGuidesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.stem='exe45_ko_development_roll_equipment_guides_v1'
        cls.path=ROOT/f'poc/output/{cls.stem}.gba';cls.rom=cls.path.read_bytes();cls.meta=read(cls.path.with_suffix('.json'))
        cls.source=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes()
    def test_clone_identity_protected_source_and_rebuild(self):
        m=self.meta;rom=self.rom;guides=m['equipment_guides'];ar=guides['roll_archive'];h=guides['selector']
        self.assertEqual(sha(rom),m['output_sha256']);self.assertEqual(rom,(ROOT/f'poc/output/{self.stem}_repro.gba').read_bytes());self.assertEqual(m['translated_units'],801)
        payload=rom[ar['rom_offset']:ar['rom_offset']+ar['compiled_bytes']]
        self.assertEqual(sha(payload),ar['compiled_sha256']);self.assertEqual(len(verify_untouched_scripts(lz77_decompress(self.source,0x6E12DC)[0],payload,76,{60,61,62})),73)
        appended,patches,record=construct(self.source,rom[len(self.source):h['hook_offset']],guides['archive']['rom_offset'],ar['rom_offset'])
        self.assertEqual(appended,rom[len(self.source):]);self.assertEqual(record,h);self.assertEqual(rom[INSTALL:INSTALL+12],patches[0][1])
        for a,b in [(0x3C5BC,0x3C61C),(0x3C484,0x3C48C),(0x6E12DC,0x6E12DC+631)]:self.assertEqual(rom[a:b],self.source[a:b])
    def test_roll_selector_source_guard(self):
        guides=self.meta['equipment_guides'];bad=bytearray(self.source);bad[0x3C5C0]^=1
        with self.assertRaises(ValueError):construct(bytes(bad),b'',guides['archive']['rom_offset'],guides['roll_archive']['rom_offset'])
        with self.assertRaises(ValueError):construct(self.source,b'',guides['archive']['rom_offset'],guides['roll_archive']['rom_offset']+1)
    def test_roll_normal_runtime_full_glyph_pixels(self):
        r=main(self.stem,'roll-equipment-v1-roll-','roll_equipment_guides_v1/roll_runtime',roll=True)
        self.assertTrue(r['passed']);self.assertFalse(r['release_eligible']);self.assertEqual(r['protected_clone_scripts'],73)
        self.assertEqual([a['navi'] for a in r['native_abi']],[1]*4);self.assertEqual([p['script'] for p in r['guide_pages']],[60,61,62,60])
        self.assertTrue(all(p['all_glyph_pixels_match'] for p in r['guide_pages']));self.assertTrue(r['exit_check']['guide_replaced'])
    def test_current_cumulative_graphics_and_rockman_regression(self):
        from report_attack_caption_runtime import main as report
        report(self.stem,'roll-equipment-v1-rockman-','roll_equipment_guides_v1/rockman_regression')
        r=read(ROOT/'analysis/roll_equipment_guides_v1/rockman_regression/runtime.json')
        self.assertTrue(r['passed']);self.assertTrue(r['weapons_guides_folder_pet_regression']);self.assertEqual(r['translated_text_units'],801)
    def test_roll_caption_native_decompression_residency_and_pixels(self):
        from report_attack_caption_runtime import main as report
        r=report(self.stem,'roll-equipment-v1-roll-','roll_equipment_guides_v1/roll_caption',roll=True)
        self.assertTrue(r['passed']);self.assertTrue(r['roll_guides_regression']);self.assertEqual(len(r['native_decompressions']),2)
        self.assertTrue(all(p['caption_vram_objects_pixels_match'] and p['attack_number_unchanged'] for p in r['pages']))

if __name__=='__main__':unittest.main()
