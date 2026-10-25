import json,struct,unittest
from build_visibility_poc import ROOT,sha
from equipment_labels import validate,ROOTS,HEADER_WIDTH
from archive_scripts import verify_untouched_scripts
from verify_tpi_index import lz77_decompress

class EquipmentLabelsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source=(ROOT/json.loads((ROOT/'project.json').read_text())['source_profile']['filename']).read_bytes()
    def test_shared_population_and_clear_extent(self):
        s=validate(self.source)
        self.assertEqual(s['common_scripts'],list(range(60)))
        self.assertEqual(s['native_navi_pools'],23)
        self.assertEqual(s['header_clear']['target_width'],12)
        for at in ROOTS+[HEADER_WIDTH]:
            bad=bytearray(self.source);bad[at]^=1
            with self.assertRaises(ValueError):validate(bytes(bad))
    def test_integrated_clone_and_native_preservation(self):
        p=ROOT/'poc/output/exe45_ko_development_equipment_labels_v2.gba';rom=p.read_bytes();m=json.loads(p.with_suffix('.json').read_text());h=m['folder_labels']['header']
        self.assertEqual(sha(rom),m['output_sha256']);self.assertEqual(rom[HEADER_WIDTH:HEADER_WIDTH+3],bytes([12,3,3]))
        for at in ROOTS:self.assertEqual(struct.unpack_from('<I',rom,at)[0],0x08000000+h['rom_offset'])
        before=lz77_decompress(self.source,0x6E2B9C)[0];clone=rom[h['rom_offset']:h['rom_offset']+h['compiled_bytes']]
        self.assertEqual(len(verify_untouched_scripts(before,clone,76,{1,2,3,4})),72)
        for f in validate(self.source)['functions']:self.assertEqual(rom[f['start']:f['end']],self.source[f['start']:f['end']])
    def test_runtime_boundaries_and_stale_title_regression(self):
        from report_equipment_labels_runtime import main
        main()
        r=json.loads((ROOT/'analysis/equipment_labels_v2/runtime.json').read_text(encoding='utf-8'))
        self.assertTrue(r['passed']);self.assertFalse(r['release_eligible'])
        self.assertEqual(len(r['equipment_screens']),4)
        self.assertTrue(all(s['title_tail_is_blank_background'] for s in r['equipment_screens']))
    def test_clear_repair_is_only_one_data_byte(self):
        a=(ROOT/'poc/output/exe45_ko_development_equipment_labels_v1.gba').read_bytes()
        b=(ROOT/'poc/output/exe45_ko_development_equipment_labels_v2.gba').read_bytes()
        self.assertEqual(len(a),len(b))
        self.assertEqual([i for i,(x,y) in enumerate(zip(a,b)) if x!=y],[HEADER_WIDTH])
        self.assertEqual(a[HEADER_WIDTH],10);self.assertEqual(b[HEADER_WIDTH],12)

if __name__=='__main__':unittest.main()
