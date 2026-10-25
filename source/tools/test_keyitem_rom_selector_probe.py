"""Controlled selector-generation contract fixtures, not source/runtime QA."""
import struct,unittest
from keyitem_rom_selector_probe import construct,INSTALL,EXPECTED,CALL_SITES

class SelectorContract(unittest.TestCase):
    def setUp(self):
        self.source=bytearray(INSTALL+12);self.source[INSTALL:INSTALL+12]=EXPECTED
        for at,value in CALL_SITES.items():self.source[at:at+4]=bytes.fromhex(value)
        self.header=struct.pack('<8H',98,100,102,104,106,108,110,112)
    def make(self):return construct(bytes(self.source),self.header,0x08800000,0x08801000)
    def test_complete_verified_thumb(self):
        stub,hook,m=self.make();self.assertEqual(len(stub),12);self.assertTrue(hook);self.assertTrue(all(x['final_placement_roundtrip'] for x in m['machine_code']))
    def test_reader_drift(self):
        self.source[INSTALL]^=1
        with self.assertRaises(ValueError):self.make()
    def test_call_drift(self):
        self.source[next(iter(CALL_SITES))]^=1
        with self.assertRaises(ValueError):self.make()
    def test_wrong_archive_header(self):
        self.header=struct.pack('<H',90)+self.header[2:]
        with self.assertRaises(ValueError):self.make()
    def test_unaligned_clone(self):
        with self.assertRaises(ValueError):construct(bytes(self.source),self.header,0x08800001,0x08801000)
    def test_overlapping_hook(self):
        with self.assertRaises(ValueError):construct(bytes(self.source),self.header,0x08800000,0x08800400)
    def test_derived_payload_extent_not_old_draft_length(self):
        with self.assertRaises(ValueError):construct(bytes(self.source),self.header,0x08800000,0x08801000,5000)
        self.assertTrue(construct(bytes(self.source),self.header,0x08800000,0x08801000,3500)[1])
if __name__=='__main__':unittest.main()
