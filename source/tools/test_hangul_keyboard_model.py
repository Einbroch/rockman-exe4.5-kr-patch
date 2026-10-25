"""Full syllable construction and automatic-composition contract fixtures."""
import unittest
from hangul_keyboard_model import *

class CompositionContracts(unittest.TestCase):
    def compose(self,keys,limit=4):
        c=Composer(limit)
        for key in keys:self.assertTrue(c.press(key),(keys,key,c.display))
        return c
    def test_all_modern_syllables_and_delete_roundtrip(self):
        for li,l in enumerate(INITIALS):
            for vi,v in enumerate(MEDIALS):
                for ti,t in enumerate(FINALS):
                    keys=[l,v]+([] if not t else list(FINAL_SPLIT.get(t,(t,))))
                    c=self.compose(keys,1);self.assertEqual(c.candidate(),chr(0xac00+li*588+vi*28+ti))
                    for _ in keys:self.assertTrue(c.backspace())
                    self.assertEqual(c.display,'');self.assertFalse(c.backspace())
    def test_next_vowel_moves_final(self):
        c=self.compose('ㄱㅜㄱㅇㅓ');self.assertEqual(c.candidate(),'국어')
        c=self.compose('ㄱㅏㄴㅏ');self.assertEqual(c.candidate(),'가나')
        c=self.compose('ㄷㅏㄹㄱㅏ');self.assertEqual(c.candidate(),'달가')
    def test_compound_medials(self):
        for (first,second),combined in MEDIAL_MERGE.items():
            c=self.compose(['ㄱ',first,second]);self.assertEqual(c.candidate(),syllable(0,MEDIALS.index(combined)))
            self.assertTrue(c.backspace());self.assertEqual(c.candidate(),syllable(0,MEDIALS.index(first)))
    def test_undo_across_resyllabification(self):
        c=self.compose('ㄷㅏㄹㄱㅏ');c.backspace();self.assertEqual(c.display,'닭');c.backspace();self.assertEqual(c.display,'달');c.backspace();self.assertEqual(c.display,'다');c.backspace();self.assertEqual(c.display,'ㄷ')
        with self.assertRaises(ValueError):c.candidate()
    def test_four_logical_slots_boundary(self):
        c=self.compose('ㄱㅏㄴㅏㄷㅏㄹㅏ');self.assertEqual(c.candidate(),'가나다라')
        self.assertTrue(c.press('ㄱ'));self.assertEqual(c.candidate(),'가나다락')
        before=c.state;h=list(c.history);self.assertFalse(c.press('ㅏ'));self.assertEqual(c.state,before);self.assertEqual(c.history,h)
        self.assertFalse(c.press('ㄸ'));self.assertEqual(c.state,before)
    def test_reject_unknown_or_out_of_order_without_mutation(self):
        c=Composer(4)
        for key in ['ㅏ','ㄳ','A','가','',None]:self.assertFalse(c.press(key));self.assertEqual(c.state,State());self.assertEqual(c.history,[])
        c.press('ㄱ');self.assertFalse(c.press('ㄴ'));self.assertEqual(c.display,'ㄱ')
        with self.assertRaises(ValueError):c.candidate()
    def test_confirmation_does_not_mutate_edit(self):
        c=self.compose('ㄱㅜㄱㅇㅓ');before=c.state;h=list(c.history);self.assertEqual(c.candidate(),'국어');self.assertEqual(c.state,before);self.assertEqual(c.history,h)
    def test_malformed_states_rejected(self):
        for s in [State(('A',)),State(v=1),State(l=19),State(l=0,v=21),State(l=0,v=0,t=28),State(l=0,t=1),State(('가',),0,0,0),State(l=True)]:
            with self.assertRaises(ValueError):transition(s,'ㄱ',1)
    def test_all_loaded_syllables_erase_and_retype(self):
        for index in range(11172):
            text=chr(0xac00+index);c=Composer(1);c.load(text)
            self.assertEqual(c.candidate(),text)
            steps=0
            while c.backspace():
                steps+=1;self.assertLessEqual(steps,7)
            self.assertEqual(c.display,'');self.assertTrue(c.press('ㄱ'));self.assertTrue(c.press('ㅏ'));self.assertEqual(c.candidate(),'가')
    def test_loaded_reentry_resyllabification_and_no_cancel_mutation(self):
        c=Composer(4);c.load('국');self.assertTrue(c.press('ㅓ'));self.assertEqual(c.candidate(),'구거')
        before=c.state;history=list(c.history);self.assertEqual(c.candidate(),'구거');self.assertEqual(c.state,before);self.assertEqual(c.history,history)
        self.assertTrue(c.backspace());self.assertEqual(c.candidate(),'국');self.assertTrue(c.backspace());self.assertEqual(c.candidate(),'구')
        c.load('국어');expected=['국ㅇ','국','구','ㄱ','']
        for text in expected:self.assertTrue(c.backspace());self.assertEqual(c.display,text)
        c.load('괙');expected=['괘','과','고','ㄱ','']
        for text in expected:self.assertTrue(c.backspace());self.assertEqual(c.display,text)
    def test_loaded_rejection_is_atomic(self):
        c=self.compose('ㄱㅏ');before=c.state;history=list(c.history)
        for text in [None,['가'],'A','ㄱ','가나다라마']:
            with self.assertRaises(ValueError):c.load(text)
            self.assertEqual(c.state,before);self.assertEqual(c.history,history)
        c.load('');self.assertEqual(c.display,'');self.assertFalse(c.backspace())
if __name__=='__main__':unittest.main()
