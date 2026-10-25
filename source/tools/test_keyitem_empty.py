import unittest
from pathlib import Path
from capstone import Cs,CS_ARCH_ARM,CS_MODE_THUMB
from build_visibility_poc import ROOT
from verify_tpi_index import lz77_decompress
from keyitem_empty import compact,validate_source,resolved,READER

class KeyitemEmptyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rom=(ROOT/'Rockman EXE 4.5 Real Operation (J)(Independent).gba').read_bytes()
        cls.source,_=lz77_decompress(cls.rom,0x709408)
        cls.payload=(ROOT/'analysis/keyitem_translation_draft_v1/bench/empty-only/709408.msg').read_bytes()

    def test_compact_native_meaning(self):
        validate_source(self.rom,self.source)
        target,proof=compact(self.source,self.payload)
        self.assertEqual(len(target),1273)
        self.assertTrue(proof['no_destination_growth'])
        self.assertEqual(resolved(target),resolved(self.payload))
        self.assertEqual(resolved(target)[10],resolved(target)[11])

    def test_reader_independent_indexing(self):
        ins=list(Cs(CS_ARCH_ARM,CS_MODE_THUMB).disasm(READER,0x0804fb74))
        self.assertEqual([(i.mnemonic,i.op_str)for i in ins],
            [('lsls','r1, r1, #1'),('ldrh','r1, [r0, r1]'),('adds','r0, r0, r1'),
             ('str','r0, [r5, #0x2c]'),('str','r0, [r5, #0x34]')])

    def test_duplicate_drift_rejected(self):
        target=bytearray(self.payload);target[497]^=1
        with self.assertRaisesRegex(ValueError,'duplicate changed'):compact(self.source,bytes(target))

    def test_other_script_drift_rejected(self):
        target=bytearray(self.payload);target[100]^=1
        with self.assertRaisesRegex(ValueError,'unselected native'):compact(self.source,bytes(target))

    def test_full_draft_capacity_rejected(self):
        target=(ROOT/'analysis/keyitem_translation_draft_v1/bench/full-draft/709408.msg').read_bytes()
        with self.assertRaises(ValueError):compact(self.source,target)

if __name__=='__main__':unittest.main()
