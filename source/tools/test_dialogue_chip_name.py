import copy,unittest
from report_roll_pet import ROOT,read
from dialogue_chip_name import construct
from archive_scripts import script_spans

class DialogueChipNameTests(unittest.TestCase):
    def inputs(self):
        source=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes();a=read(ROOT/'translations/library_chip_names_batch08_ko.json');span=script_spans(source[0x664E28:0x664E28+2158],255)[13];return source,a,{'rom_offset':0x800000,'script13_offset':925,'script13_prefix_hex':span[:21].hex()}
    def test_declared_source_and_stream_reject(self):
        s,a,ar=self.inputs();bad=bytearray(s);bad[0x5162C]^=1
        with self.assertRaises(ValueError):construct(bytes(bad),b'',ar,a)
        badar=dict(ar,script13_prefix_hex='00')
        with self.assertRaises(ValueError):construct(s,b'',badar,a)
    def test_guarded_asset_and_machine_code(self):
        s,a,ar=self.inputs();out,w,h=construct(s,b'',ar,a);self.assertEqual(h['copy_extent'],128);self.assertEqual(h['wording_count_increment'],0);self.assertEqual(len(w[0][1]),12);self.assertTrue(all(r['final_placement_roundtrip'] for r in h['machine_code']));bad=copy.deepcopy(a);next(v for v in bad['wordings'] if v['id']=='library.chip.batch04.104')['translation']='다른 이름'
        with self.assertRaises(ValueError):construct(s,b'',ar,bad)
    def test_cpu_guard_fallback_and_native_effects(self):
        from bench_dialogue_chip_name import main
        r=main('exe45_ko_development_dialogue_chip_name_v1','dialogue_chip_name_v1');self.assertTrue(r['passed']);self.assertEqual(r['vectors'],32)

if __name__=='__main__':unittest.main()
