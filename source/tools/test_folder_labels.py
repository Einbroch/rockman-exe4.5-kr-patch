import json,unittest
from build_visibility_poc import ROOT,sha
from folder_labels import title,validate_header_path,HEADER_ROOT,TITLE_BASE
from archive_scripts import script_spans
from verify_tpi_index import lz77_decompress

class FolderLabelsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source=(ROOT/json.loads((ROOT/'project.json').read_text())['source_profile']['filename']).read_bytes()
        cls.asset=json.loads((ROOT/'translations/pet_menu_graphics_ko.json').read_text(encoding='utf-8'))
    def test_native_scope_and_title_protection(self):
        scope=validate_header_path(self.source)
        self.assertEqual(len(scope['identical_native_header_sources']),23)
        self.assertEqual(scope['literal_read_sites'],[0x3E460])
        target,meta=title(self.source,self.asset)
        self.assertEqual(sha(target),'8fa932633528fccbc38c8daaecb6e9d0d0dd63287533996e779a705cf1f572c0')
        old=self.source[TITLE_BASE:TITLE_BASE+256]
        for y in range(8):
            for x in range(64):
                if 22<=x<45:continue
                at=x//8*32+y*4+x%8//2;shift=4*(x%2)
                self.assertEqual((old[at]>>shift)&15,(target[at]>>shift)&15)
        self.assertTrue(meta['unchanged_roundtrip'])
    def test_built_clone_preserves_original_navi_storage(self):
        p=ROOT/'poc/output/exe45_ko_development_folder_labels_v1.gba'
        rom=p.read_bytes();meta=json.loads(p.with_suffix('.json').read_text());h=meta['folder_labels']['header']
        self.assertEqual(sha(rom),meta['output_sha256'])
        self.assertEqual(rom[0x3C5BC:0x3C61C],self.source[0x3C5BC:0x3C61C])
        self.assertEqual(rom[0x6E2B9C:0x6E2B9C+634],self.source[0x6E2B9C:0x6E2B9C+634])
        self.assertEqual(rom[0x3E45C:HEADER_ROOT],self.source[0x3E45C:HEADER_ROOT])
        self.assertEqual(int.from_bytes(rom[HEADER_ROOT:HEADER_ROOT+4],'little'),0x08000000+h['rom_offset'])
        before=script_spans(lz77_decompress(self.source,0x6E2B9C)[0],76)
        after=script_spans(rom[h['rom_offset']:h['rom_offset']+h['compiled_bytes']],76)
        self.assertNotEqual(before[1],after[1])
        for i in range(76):
            if i!=1:self.assertEqual(before[i],after[i])
    def test_wrong_source_rejected(self):
        data=bytearray(self.source);data[HEADER_ROOT]^=1
        with self.assertRaises(ValueError):validate_header_path(bytes(data))
        with self.assertRaises(ValueError):title(bytes(data),self.asset)
    def test_exact_rom_runtime_receipts_and_pixels(self):
        from report_folder_labels_runtime import main
        main()
        report=json.loads((ROOT/'analysis/folder_labels_v1/runtime.json').read_text(encoding='utf-8'))
        self.assertTrue(report['passed']);self.assertFalse(report['release_eligible'])
        self.assertEqual(len(report['folder_screens']),4)
        self.assertEqual(len(report['pet_focus_screens']),7)
        self.assertEqual(report['protected_clone_scripts'],75)

if __name__=='__main__':unittest.main()
