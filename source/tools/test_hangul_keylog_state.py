"""Host key-log contract, especially 10-character/70-key closure boundaries."""
import unittest
from hangul_keylog_state import KeylogComposer, KEYS
from hangul_keyboard_model import INITIALS, MEDIALS, FINALS, FINAL_SPLIT
from hangul_compact_state import CompactComposer


class KeylogTests(unittest.TestCase):
    def roundtrip(self, c):
        raw = c.serialize()
        self.assertEqual(len(raw), 64)
        restored = KeylogComposer.restore(raw, c.baseline)
        self.assertEqual((restored.display, restored.model.state, restored.model.history),
                         (c.display, c.model.state, c.model.history))
        return restored

    def test_full_repertoire_at_tenth_cell(self):
        for l in INITIALS:
            for v in MEDIALS:
                for t in FINALS:
                    c = KeylogComposer(10, '가' * 9)
                    # Erase the loaded baseline, then build all ten cells.
                    while c.backspace():
                        pass
                    for key in 'ㄱㅏ' * 9 + l + v + ''.join(FINAL_SPLIT.get(t, (t,))):
                        self.assertTrue(c.press(key))
                    self.assertEqual(len(c.candidate()), 10)
                    self.roundtrip(c)

    def test_70_keys_and_70_loaded_deletions(self):
        text = chr(0xAC00 + 588 + 10 * 28 + 9) * 10
        c = KeylogComposer(10, text)
        count = 0
        while c.backspace():
            count += 1
            self.roundtrip(c)
        self.assertEqual(count, 70)
        for key in 'ㄱㄱㅗㅏㅣㄹㄱ' * 10:
            self.assertTrue(c.press(key))
            self.roundtrip(c)
        self.assertEqual(len(c.keys), 70)
        self.assertEqual(c.candidate(), text)
        before = c.serialize()
        self.assertFalse(c.press('ㄱ'))
        self.assertEqual(c.serialize(), before)
        while c.backspace():
            self.roundtrip(c)

    def test_existing_capacities_keep_edit_semantics(self):
        for limit in range(1, 9):
            for text in ['', '국' * limit, '괙' * limit]:
                a, b = KeylogComposer(limit, text), CompactComposer(limit, text)
                for key in KEYS:
                    self.assertEqual(a.press(key), b.press(key))
                    self.assertEqual(a.model.state, b.model.state)
                    self.roundtrip(a)
                for _ in range(120):
                    self.assertEqual(a.backspace(), b.backspace())
                    self.assertEqual(a.model.state, b.model.state)
                    self.roundtrip(a)

    def test_malformed_keys_padding_and_header(self):
        raw = KeylogComposer(10).serialize()
        for offset, values in [(0, [0, 0xA0, 0xA2]), (1, [0, 11]),
                               (2, [71]), (3, [1, 71]), (56, [0x10]), (63, [1])]:
            for value in values:
                bad = bytearray(raw)
                bad[offset] = value
                with self.assertRaises(ValueError):
                    KeylogComposer.restore(bytes(bad), '')
        for slot in range(70):
            for value in [1, 40, 63]:
                bad = raw[:4] + (value << (slot * 6)).to_bytes(53, 'little') + bytes(7)
                with self.assertRaises(ValueError):
                    KeylogComposer.restore(bad, '')
        c = KeylogComposer(10)
        self.assertFalse(c.press('ㅏ'))
        self.assertFalse(c.press('x'))
        with self.assertRaises(ValueError):
            c.candidate()


if __name__ == '__main__':
    unittest.main()
