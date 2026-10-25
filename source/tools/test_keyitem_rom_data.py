"""Controlled layout/install fixtures; no current-ROM validity claim."""
import struct,unittest
from keyitem_rom_data import install,verify_final
from keyitem_rom_selector import INSTALL,EXPECTED,CALL_SITES

class InstallationContract(unittest.TestCase):
    def setUp(self):
        b=bytearray(INSTALL+12);b[INSTALL:INSTALL+12]=EXPECTED
        for at,v in CALL_SITES.items():b[at:at+4]=bytes.fromhex(v)
        self.source=bytes(b);self.header=struct.pack('<8H',98,100,102,104,106,108,110,112)
        self.payload=self.header+bytes(2477-16)
    def build(self):
        tail,patches,meta=install(self.source,b'\xa7'*7,self.payload,self.header,{})
        target=bytearray(self.source+tail)
        for at,value,_ in patches:target[at:at+len(value)]=value
        return target,meta
    def test_complete_final_bytes(self):
        target,m=self.build();self.assertTrue(verify_final(self.source,target,m));self.assertEqual(target[len(self.source):len(self.source)+7],b'\xa7'*7)
        self.assertEqual(m['clone_address']%4,0);self.assertEqual(m['hook_address']%4,0)
    def test_payload_corruption_rejected(self):
        target,m=self.build();target[m['rom_offset']+20]^=1
        with self.assertRaises(ValueError):verify_final(self.source,target,m)
    def test_entry_corruption_rejected(self):
        target,m=self.build();target[INSTALL]^=1
        with self.assertRaises(ValueError):verify_final(self.source,target,m)
    def test_hook_corruption_rejected(self):
        target,m=self.build();target[m['hook_address']-0x08000000]^=1
        with self.assertRaises(ValueError):verify_final(self.source,target,m)
if __name__=='__main__':unittest.main()
