"""Source-bound applicability rejects changed native providers on current019."""
import unittest
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read
from nickname_capacity import CPU
from survey_batch500_020_variables import applicability

class Applicability(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);cls.source=sp.read_bytes();rp=ROOT/'poc/output/pending500_019_v1.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);cls.rom=rp.read_bytes();cls.cpu=read(CPU)
    def reject(self,offset):
        altered=bytearray(self.rom);altered[offset]^=1
        with self.assertRaises(ValueError):applicability(self.source,altered,self.cpu)
    def test_current_provider(self):self.assertEqual(applicability(self.source,self.rom,self.cpu),99)
    def test_changed_code(self):self.reject(self.cpu['native_code'][0]['offset'])
    def test_changed_literal(self):self.reject(0x38F84)
    def test_changed_descriptor(self):self.reject(0x526D8)
    def test_changed_width(self):self.reject(0x5290C+440*4)
    def test_changed_suffix_pointer(self):self.reject(0x63720C)
    def test_changed_suffix_body(self):
        import struct
        self.reject(0x63720C+struct.unpack_from('<H',self.source,0x63720C)[0])

if __name__=='__main__':unittest.main()
