"""Controlled composed-selector source/input rejection fixtures."""
import struct,unittest
from keyitem_rom_selector import construct,INSTALL,EXPECTED,CALL_SITES

class MailSelectorTests(unittest.TestCase):
    def setUp(self):
        self.source=bytearray(0x50000);self.source[INSTALL:INSTALL+12]=EXPECTED
        for at,raw in CALL_SITES.items():self.source[at:at+4]=bytes.fromhex(raw)
        self.source[0x4F7B8:0x4F7BC]=bytes.fromhex('00f0c8f9')
        self.header=struct.pack('<8H',98,100,102,104,106,108,110,112)
        self.mail=dict(clone_address=0x08091000,payload_bytes=128,guard_header_hex=struct.pack('<8H',64,70,80,90,100,110,120,124).hex())
    def build(self,mail=None):return construct(self.source,self.header,0x08090000,0x08092000,128,self.mail if mail is None else mail)
    def test_valid_composition(self):
        stub,code,meta=self.build();self.assertEqual(len(stub),12);self.assertTrue(code);self.assertEqual(meta['mail_guard'],self.mail)
    def test_wrong_native_caller_rejected(self):
        self.source[0x4F7B8]^=1
        with self.assertRaises(ValueError):self.build()
    def test_foreign_table_and_overlap_rejected(self):
        for update in [dict(guard_header_hex=struct.pack('<8H',66,70,80,90,100,110,120,124).hex()),dict(clone_address=0x08090040),dict(clone_address=0x08092000),dict(payload_bytes=0x10000)]:
            with self.assertRaises(ValueError):self.build(dict(self.mail,**update))
    def test_unknown_inputs_rejected(self):
        with self.assertRaises(ValueError):self.build(dict(self.mail,unknown=1))

if __name__=='__main__':unittest.main()
