import json,struct,unittest
from build_visibility_poc import ROOT,sha
from equipment_guides import validate,construct,INSTALL
from archive_scripts import verify_untouched_scripts
from verify_tpi_index import lz77_decompress
from report_equipment_guides_runtime import verify_pet_exit,main

def read(path):return json.loads(path.read_text(encoding='utf-8'))

class EquipmentGuidesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes()
        cls.path=ROOT/'poc/output/exe45_ko_development_equipment_guides_v1.gba'
        cls.rom=cls.path.read_bytes();cls.meta=read(cls.path.with_suffix('.json'))
    def test_source_identity_and_pool_guard(self):
        self.assertEqual(validate(self.source),[0,13,14])
        for at in [INSTALL,0xCEC,0x3C5BC,0x3C5F0,0x3C5F4]:
            bad=bytearray(self.source);bad[at]^=1
            with self.assertRaises(ValueError):validate(bytes(bad))
    def test_private_clone_and_generated_hook_exact_identity(self):
        m=self.meta;rom=self.rom;ar=m['equipment_guides']['archive'];h=m['equipment_guides']['selector']
        self.assertEqual(sha(rom),m['output_sha256'])
        self.assertEqual(rom,(ROOT/'poc/output/exe45_ko_development_equipment_guides_v1_repro.gba').read_bytes())
        clone=rom[ar['rom_offset']:ar['rom_offset']+ar['compiled_bytes']]
        self.assertEqual(len(verify_untouched_scripts(lz77_decompress(self.source,0x6E1068)[0],clone,76,{60,61,62})),73)
        appended,patches,rebuilt=construct(self.source,rom[len(self.source):h['hook_offset']],ar['rom_offset'])
        self.assertEqual(rom[len(self.source):],appended);self.assertEqual(h,rebuilt)
        self.assertEqual(rom[INSTALL:INSTALL+12],patches[0][1])
        for a,b in [(0x6E1068,0x6E1068+625),(0x3C5BC,0x3C61C),(0x3C484,0x3C48C)]:self.assertEqual(rom[a:b],self.source[a:b])
    def test_exit_accepts_pet_speech_but_rejects_stale_guide(self):
        p=ROOT/'poc/runtime/equipment-guides-v1-equipment';ram=(p/'step_012_gbaExtWorkRam.bin').read_bytes();previous=read(p/'step_011_guides.json');current=read(p/'step_012_guides.json')
        r=verify_pet_exit(self.source,self.rom,self.meta,ram,previous,current)
        self.assertTrue(r['guide_replaced']);self.assertTrue(r['normal_context_active'])
        bad=bytearray(ram);struct.pack_into('<I',bad,0xFA50,0x08000000+self.meta['equipment_guides']['archive']['rom_offset'])
        with self.assertRaises(ValueError):verify_pet_exit(self.source,self.rom,self.meta,bad,previous,current)
        bad_observation={**current,'draws':current['draws']+[current['draws'][-1]]}
        with self.assertRaises(ValueError):verify_pet_exit(self.source,self.rom,self.meta,ram,previous,bad_observation)
    def test_exact_rom_runtime_pixels_and_bench_boundaries(self):
        main();r=read(ROOT/'analysis/equipment_guides_v1/runtime.json')
        self.assertTrue(r['passed']);self.assertFalse(r['release_eligible'])
        self.assertEqual(r['rom_sha256'],self.meta['output_sha256']);self.assertEqual(r['translated_units'],765)
        self.assertEqual(r['protected_clone_scripts'],73);self.assertEqual(r['selector_cpu_fixture_vectors'],72)
        self.assertEqual([p['script'] for p in r['guide_pages']],[60,61,62,60])
        self.assertTrue(all(p['all_glyph_pixels_match'] for p in r['guide_pages']))
        self.assertTrue(r['equipment_folder_pet_regression_passed'])

if __name__=='__main__':unittest.main()
