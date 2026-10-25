"""Compact reference replay contracts; does not exercise a native64-byte wrapper."""
import unittest
from hangul_keyboard_model import INITIALS,MEDIALS,FINALS,FINAL_SPLIT,syllable,Composer
from hangul_compact_state import CompactComposer

class CompactContracts(unittest.TestCase):
    def check(self,c):
        raw=c.serialize();self.assertEqual(len(raw),64)
        restored=CompactComposer.restore(raw,c.baseline)
        self.assertEqual(restored.model.state,c.model.state);self.assertEqual(restored.model.history,c.model.history)
    def test_all_syllable_input_undo_load_delete_roundtrips(self):
        for li,l in enumerate(INITIALS):
            for vi,v in enumerate(MEDIALS):
                for ti,t in enumerate(FINALS):
                    c=CompactComposer(1)
                    for key in [l,v]+([] if not t else list(FINAL_SPLIT.get(t,(t,)))):
                        self.assertTrue(c.press(key));self.check(c)
                    self.assertEqual(c.candidate(),syllable(li,vi,ti))
                    while c.backspace():self.check(c)
                    c=CompactComposer(1,syllable(li,vi,ti))
                    while c.backspace():self.check(c)
                    self.assertEqual(c.display,'')
    def test_capacity8_maximum_key_history_then_loaded_erase_retype(self):
        c=CompactComposer(8)
        for key in 'ㄱㄱㅗㅏㅣㄹㄱ'*8:self.assertTrue(c.press(key));self.check(c)
        self.assertEqual(len(c.keys),56);self.assertFalse(c.press('ㅏ'));self.check(c)
        while c.backspace():self.check(c)
        self.assertEqual(c.display,'')
        c=CompactComposer(8,syllable(1,10,9)*8)
        while c.backspace():self.check(c)
        self.assertEqual(c.deletions,56)
        for key in 'ㄱㄱㅗㅏㅣㄹㄱ'*8:self.assertTrue(c.press(key));self.check(c)
        self.assertEqual(c.deletions,56);self.assertEqual(len(c.keys),56)
    def test_cross_syllable_actions_and_rejections(self):
        for baseline,keys in [('', 'ㄷㅏㄹㄱㅏ'),('국어','ㄱㅏㄴㅏ'),('가나다라','ㅏㄱㅅㅏ')]:
            c=CompactComposer(4,baseline);reference=Composer(4);reference.load(baseline)
            for key in keys:
                self.assertEqual(c.press(key),reference.press(key));self.assertEqual(c.model.state,reference.state);self.check(c)
            while reference.backspace():self.assertTrue(c.backspace());self.assertEqual(c.model.state,reference.state);self.check(c)
            self.assertFalse(c.backspace())
    def test_reject_malformed_and_wrong_baseline(self):
        c=CompactComposer(4,'국');c.press('ㅓ');raw=c.serialize()
        for offset,value in [(0,9),(1,0),(2,57),(3,2),(4,255),(20,63),(61,255),(62,57),(63,1)]:
            bad=bytearray(raw);bad[offset]=value
            with self.assertRaises(ValueError):CompactComposer.restore(bytes(bad),'국')
        with self.assertRaises(ValueError):CompactComposer.restore(raw,'가')
        with self.assertRaises(ValueError):CompactComposer.restore(raw[:-1],'국')

if __name__=='__main__':unittest.main()
