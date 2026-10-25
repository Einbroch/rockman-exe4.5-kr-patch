"""Compact mixed HOST contracts, not memory ownership or emitted CPU proof."""
import random
import struct
import unittest
from hangul_mixed_replay_state import MixedReplay, SIZE, KEYS, apply, editor_candidate
from hangul_mixed_editor import MixedEditor, Snapshot
from hangul_native_tokens import tag
from hangul_keyboard_model import INITIALS, MEDIALS, FINALS, FINAL_SPLIT


class MixedReplayTests(unittest.TestCase):
    def test_96byte_placement_preserves_all_ui_and_destination(self):
        for cap in range(1, 11):
            ui = bytes([0xA7] * 4 + [cap] + list(range(5, 16)))
            c = MixedReplay(cap); c.load([tag(b'\xE4\x00')] * cap); c.press('ㄱ')
            compact = c.serialize()
            for destination in (0x020010A6, 0x02026280):
                result = editor_candidate(ui, destination, compact)
                self.assertEqual(len(result), 96)
                self.assertEqual(result[:16], ui)
                self.assertEqual(struct.unpack_from('<I', result, 16)[0], destination)
                self.assertEqual(result[20:], compact)
                self.assertEqual(MixedReplay.restore(result[20:]).model.state, c.model.state)
            with self.assertRaises(ValueError): editor_candidate(ui[:15], 0, compact)
            with self.assertRaises(ValueError): editor_candidate(ui, True, compact)
            with self.assertRaises(ValueError): editor_candidate(ui, 0x100000000, compact)
            bad = bytearray(ui); bad[4] = 0
            with self.assertRaises(ValueError): editor_candidate(bytes(bad), 0, compact)

    def same(self, compact, reference):
        raw = compact.serialize()
        self.assertEqual(len(raw), SIZE)
        decoded = MixedReplay.restore(raw)
        self.assertEqual((decoded.model.state, decoded.model.history), (reference.state, reference.history))
        self.assertEqual(decoded.baseline, compact.baseline)
        self.assertEqual(decoded.keys, compact.keys)
        return raw

    def test_complete_repertoire_every_slot_and_undo(self):
        legacy = tuple(tag(bytes([0x9B + i])) for i in range(10))
        for slot in range(10):
            for li, l in enumerate(INITIALS):
                for vi, v in enumerate(MEDIALS):
                    for ti, t in enumerate(FINALS):
                        c = MixedReplay(10)
                        c.model.state = Snapshot(legacy, slot, None); c._rebase()
                        original = c.serialize()
                        for k in [l, v] + ([] if not t else list(FINAL_SPLIT.get(t, (t,)))):
                            self.assertTrue(c.press(k))
                        decoded = MixedReplay.restore(c.serialize())
                        expected = list(legacy); expected[slot] = li * 588 + vi * 28 + ti
                        self.assertEqual(decoded.candidate(), tuple(expected))
                        self.assertEqual(decoded.model.state.cursor, slot + 1)
                        while decoded.keys: self.assertTrue(decoded.backspace())
                        self.assertEqual(decoded.serialize(), original)

    def test_random_mixed_commands_preserve_reference(self):
        rng = random.Random(4545)
        for cap in range(1, 11):
            c, m = MixedReplay(cap), MixedEditor(cap)
            words = [tag(b'\xE4\x00')] * cap
            c.load(words); m.load(words)
            for _ in range(500):
                before = c.serialize()
                action = rng.randrange(4)
                if action == 0:
                    key = rng.choice(KEYS + ('invalid',))
                    self.assertEqual(c.press(key), m.press(key))
                elif action == 1:
                    delta = rng.choice((-1, 1, 0, 2))
                    self.assertEqual(c.move(delta), m.move(delta))
                elif action == 2:
                    token = rng.choice((b'\x9B', b'\xE4\x98', b'\xE4\xE5', b'\xFF'))
                    self.assertEqual(c.write_native(token), m.write_native(token))
                else:
                    self.assertEqual(c.backspace(), m.backspace())
                self.same(c, m)
                # Reject-invalid movement must preserve exact encoded baseline.
                self.assertEqual(apply(c.serialize(), 'move', 2), (False, c.serialize()))

    def test_sealed_partial_carry_and_max_history(self):
        for cap in range(1, 11):
            c = MixedReplay(cap); c.load([tag(b'\x9B')] * cap)
            original = c.serialize()
            for k in 'ㄱㅏㄴ': self.assertTrue(c.press(k))
            before = c.serialize()
            accepted = c.press('ㅏ')
            self.assertEqual(accepted, cap > 1)
            if accepted:
                c = MixedReplay.restore(c.serialize()); c.backspace()
            self.assertEqual(c.serialize(), before)
            while c.keys: c.backspace()
            self.assertEqual(c.serialize(), original)
        c = MixedReplay(2); c.press('ㄱ'); c.move(-1)
        raw = c.serialize(); c = MixedReplay.restore(raw)
        self.assertEqual(c.model.state.cells, (11172,))
        with self.assertRaises(ValueError): c.candidate()
        self.assertEqual(apply(raw, 'jamo', 'ㅏ'), (False, raw))
        c.backspace(); self.assertEqual(c.model.state.cells, ())
        c = MixedReplay(10)
        empty = c.serialize()
        for k in 'ㄱㄱㅗㅏㅣㄹㄱ' * 10: self.assertTrue(c.press(k))
        full = c.serialize(); self.assertEqual(full[2], 70)
        self.assertEqual(apply(full, 'jamo', 'ㄱ'), (False, full))
        c = MixedReplay.restore(full)
        for _ in range(70): self.assertTrue(c.backspace())
        self.assertEqual(c.serialize(), empty)

    def test_baseline_word_domain_and_malformed(self):
        c = MixedReplay(1); c.load([0]); base = c.serialize()
        for word in range(65536):
            raw = bytearray(base); struct.pack_into('<H', raw, 3, word)
            valid = word < 11191 or 0x8000 <= word <= 0x80E3 or 0x8100 <= word <= 0x81FF
            if valid: self.assertEqual(MixedReplay.restore(bytes(raw)).model.state.cells, (word,))
            else:
                with self.assertRaises(ValueError): MixedReplay.restore(bytes(raw))
        for length in range(SIZE):
            with self.assertRaises(ValueError): MixedReplay.restore(base[:length])
        for offset, value in ((0, 0x10), (0, 0x1B), (0, 0x21), (1, 0xF2),
                              (1, 0x10), (2, 71), (5, 0), (23, 1), (75, 0xA0), (75, 0xB1)):
            raw = bytearray(base); raw[offset] = value
            with self.assertRaises(ValueError): MixedReplay.restore(bytes(raw))
        c = MixedReplay(1); c.press('ㄱ'); valid = c.serialize()
        for key in range(40, 64):
            raw = bytearray(valid); raw[23] = key
            with self.assertRaises(ValueError): MixedReplay.restore(bytes(raw))
        raw = bytearray(valid); raw[23] = KEYS.index('ㅏ')
        with self.assertRaises(ValueError): MixedReplay.restore(bytes(raw))
        # A structurally valid key stream which attempts carry beyond cap1.
        raw = bytearray(MixedReplay(1).serialize()); raw[2] = 4
        bits = sum(KEYS.index(k) << (6 * i) for i, k in enumerate('ㄱㅏㄴㅏ'))
        raw[23:76] = (bits | (0xB << 420)).to_bytes(53, 'little')
        with self.assertRaises(ValueError): MixedReplay.restore(bytes(raw))
        before = c.serialize()
        with self.assertRaises(ValueError): c.load([11172])
        self.assertEqual(c.serialize(), before)


if __name__ == '__main__': unittest.main()
