"""Candidate serialization contracts; no native marker/save adoption."""
import unittest
from hangul_record_candidate import pack,unpack,display_bytes

class CandidateContracts(unittest.TestCase):
    def test_all_modern_syllables_all_slot_positions(self):
        for limit in [4,8]:
            for slot in range(limit):
                for rank in range(11172):
                    text='가'*slot+chr(0xac00+rank)+'힣'*(limit-slot-1)
                    record=pack(text,limit);self.assertEqual(len(record),2*limit+2);self.assertEqual(unpack(record,limit),text)
    def test_complete_word_rank_domain(self):
        good=pack('가',4)
        for rank in range(65536):
            record=good[:1]+rank.to_bytes(2,'little')+good[3:]
            if rank<11172:self.assertEqual(unpack(record,4),chr(0xac00+rank))
            else:
                with self.assertRaises(ValueError):unpack(record,4)
    def test_marker_terminator_and_empty_word_domains(self):
        good=pack('가',4)
        for value in range(256):
            if value!=0x81:
                with self.assertRaises(ValueError):unpack(bytes([value])+good[1:],4)
            if value!=0xe5:
                with self.assertRaises(ValueError):unpack(good[:-1]+bytes([value]),4)
        for rank in range(65535):
            with self.assertRaises(ValueError):unpack(good[:3]+rank.to_bytes(2,'little')+good[5:],4)
    def test_reject_bad_width_domain_and_input(self):
        for limit in [None,True,0,9,-1]:
            with self.assertRaises(ValueError):pack('가',limit)
        for text in [None,'','ㄱ','A','가나다라마']:
            with self.assertRaises(ValueError):pack(text,4)
        good=pack('가',4)
        for record in [bytearray(good),good[:-1],good+b'\x00']:
            with self.assertRaises(ValueError):unpack(record,4)
    def test_every_capacity_occupancy_and_embedded_native_terminators(self):
        for limit in range(1,9):
            for count in range(1,limit+1):
                text=chr(0xac00+0xe5)*count;record=pack(text,limit)
                self.assertEqual(unpack(record,limit),text);self.assertEqual(len(display_bytes(record,limit)),4*count+1)
                self.assertEqual(display_bytes(record,limit),b'\xf9\xfc\xe5\x00'*count+b'\xe5')

if __name__=='__main__':unittest.main()
