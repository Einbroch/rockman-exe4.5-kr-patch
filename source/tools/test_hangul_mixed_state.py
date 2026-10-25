"""Serialized HOST contracts; no CPU, game allocation or ROM evidence."""
import unittest
from hangul_mixed_state import pack, unpack, apply, SIZE, HEADER
from hangul_mixed_editor import MixedEditor
from hangul_native_tokens import tag
from hangul_mixed_editor import validate_word
from hangul_keyboard_model import INITIALS, MEDIALS, FINALS, FINAL_SPLIT


class MixedStateTests(unittest.TestCase):
    def test_occupied_uint16_domain_and_every_truncation(self):
        m = MixedEditor(1); m.load([0])
        valid = pack(m)
        for word in range(65536):
            bad = bytearray(valid); bad[8:10] = word.to_bytes(2, 'little')
            try:
                validate_word(word)
            except ValueError:
                with self.assertRaises(ValueError): unpack(bytes(bad))
            else:
                self.assertEqual(unpack(bytes(bad)).state.cells, (word,))
        for length in range(SIZE):
            with self.assertRaises(ValueError): unpack(valid[:length])

    def test_repertoire_roundtrip_native_overwrite_and_undo(self):
        old = tag(b'\xE4\x00')
        for li, l in enumerate(INITIALS):
            for vi, v in enumerate(MEDIALS):
                for ti, t in enumerate(FINALS):
                    m = MixedEditor(2); m.load([old, tag(b'\x9B')])
                    original = m.state
                    for k in [l, v] + ([] if not t else list(FINAL_SPLIT.get(t, (t,)))):
                        self.assertTrue(m.press(k))
                    decoded = unpack(pack(m))
                    self.assertEqual(decoded.state.cells[0], li * 588 + vi * 28 + ti)
                    self.assertEqual((decoded.state, decoded.history), (m.state, m.history))
                    while decoded.history:
                        self.assertTrue(decoded.backspace())
                    self.assertEqual(decoded.state, original)

    def test_carry_last_slot_and_sealed_partial(self):
        for slot in range(10):
            m = MixedEditor(10); m.load([tag(bytes([0x9B + i])) for i in range(10)])
            for _ in range(slot): m.move(1)
            original = pack(m)
            for k in 'ㄱㅏㄴ': m.press(k)
            b = pack(m)
            ok, carried = apply(b, 'jamo', 'ㅏ')
            self.assertEqual(ok, slot < 9)
            if ok:
                self.assertEqual(apply(carried, 'backspace'), (True, b))
            else:
                self.assertEqual(carried, b)
            for _ in range(3): _, b = apply(b, 'backspace')
            self.assertEqual(b, original)
        m = MixedEditor(2); m.press('ㄱ'); m.move(-1)
        b = pack(m)
        with self.assertRaises(ValueError): unpack(b).candidate()
        self.assertEqual(apply(b, 'move', -1), (False, b))
        self.assertEqual(apply(b, 'jamo', 'ㅏ'), (False, b))

    def test_max_history_serialized_undo_and_malformed(self):
        m = MixedEditor(10)
        for k in 'ㄱㄱㅗㅏㅣㄹㄱ' * 10: self.assertTrue(m.press(k))
        b = pack(m)
        self.assertEqual(len(b), SIZE)
        self.assertEqual(b[5], 70)
        self.assertEqual(apply(b, 'jamo', 'ㄱ'), (False, b))
        decoded = unpack(b)
        for _ in range(70): decoded.backspace()
        self.assertEqual(pack(decoded), pack(MixedEditor(10)))
        empty = pack(MixedEditor(1))
        for bad in (empty[:-1], empty + b'\x00', bytearray(empty)):
            with self.assertRaises(ValueError): unpack(bad)
        for offset, value in ((0, 0), (1, 0), (1, 11), (2, 2), (3, 1), (4, 0),
                              (5, 71), (6, 1), (7, 1), (8, 0), (HEADER, 1), (SIZE - 1, 1)):
            bad = bytearray(empty); bad[offset] = value
            with self.assertRaises(ValueError): unpack(bytes(bad))
        m = MixedEditor(2); m.load([tag(b'\x9B')]); m.press('ㄱ')
        valid = pack(m)
        for offset, value in ((HEADER + 3, 1), (HEADER, 0), (HEADER + 4, 0xFF),
                              (HEADER + 6, 0), (4, 0xFF)):
            bad = bytearray(valid); bad[offset] = value
            with self.assertRaises(ValueError): unpack(bytes(bad))
        # Structurally valid history must still be a real jamo transition:
        # changing the resulting partial to complete 가 after one initial is invalid.
        bad = bytearray(valid); bad[8:10] = b'\x00\x00'
        with self.assertRaises(ValueError): unpack(bytes(bad))


if __name__ == '__main__': unittest.main()
