"""Controlled host contracts, not CPU/ROM keyboard evidence."""
import unittest
from hangul_mixed_editor import MixedEditor, Snapshot
from hangul_native_tokens import tag
from hangul_keyboard_model import INITIALS, MEDIALS, FINALS, FINAL_SPLIT


class MixedEditorTests(unittest.TestCase):
    def test_complete_repertoire_every_slot_and_exact_undo(self):
        legacy = [tag(bytes([0x9B + i])) for i in range(10)]
        for slot in range(10):
            for li, l in enumerate(INITIALS):
                for vi, v in enumerate(MEDIALS):
                    for ti, t in enumerate(FINALS):
                        m = MixedEditor(10); m.load(legacy)
                        for _ in range(slot):
                            self.assertTrue(m.move(1))
                        original = m.state
                        for key in [l, v] + ([] if not t else list(FINAL_SPLIT.get(t, (t,)))):
                            self.assertTrue(m.press(key))
                        wanted = legacy.copy(); wanted[slot] = li * 588 + vi * 28 + ti
                        self.assertEqual(m.candidate(), tuple(wanted))
                        self.assertEqual(m.state.cursor, slot + 1)
                        while m.history:
                            self.assertTrue(m.backspace())
                        self.assertEqual(m.state, original)

    def test_native_cursor_delete_and_overwrite(self):
        # Compare directly to the original bounded-block effects, not to a
        # second invocation of this editor implementation.
        words = [tag(b'\x9B'), tag(b'\xE4\x00'), tag(b'\x5E')]
        for cursor in range(4):
            m = MixedEditor(4); m.load(words)
            for _ in range(cursor):
                self.assertTrue(m.move(1))
            before = m.state
            self.assertTrue(m.backspace())
            removed = max(0, cursor - 1)
            self.assertEqual(m.state, Snapshot(tuple(words[:removed] + words[removed + 1:]), max(0, cursor - 1), None))
            m.load(words)
            for _ in range(cursor):
                m.move(1)
            self.assertTrue(m.write_native(b'\xE4\x01'))
            wanted = words.copy()
            if cursor == 3:
                wanted.append(tag(b'\xE4\x01'))
            else:
                wanted[cursor] = tag(b'\xE4\x01')
            self.assertEqual(m.state, Snapshot(tuple(wanted), cursor + 1, None))

    def test_carry_preserves_unrelated_cells_and_undo(self):
        a, b, c = (tag(t) for t in (b'\x9B', b'\xE4\x00', b'\x5E'))
        m = MixedEditor(3); m.load([a, b, c])
        for key in 'ㄱㅏㄴ':
            self.assertTrue(m.press(key))
        before = m.state
        self.assertTrue(m.press('ㅏ'))
        self.assertEqual(m.candidate(), (0, ord('나') - 0xAC00, c))
        self.assertTrue(m.backspace()); self.assertEqual(m.state, before)
        self.assertTrue(m.move(1))
        self.assertIsNone(m.state.active)
        self.assertFalse(m.history)

    def test_partial_navigation_and_atomic_boundaries(self):
        m = MixedEditor(2); m.load([tag(b'\x9B'), tag(b'\x5E')])
        self.assertTrue(m.press('ㄱ'))
        self.assertTrue(m.move(-1))
        before = m.state
        with self.assertRaises(ValueError):
            m.candidate()
        self.assertEqual(m.state, before)
        self.assertFalse(m.move(-1)); self.assertEqual(m.state, before)
        self.assertFalse(m.press('ㅏ')); self.assertEqual(m.state, before)
        self.assertTrue(m.backspace())  # partial at cursor0 removed
        self.assertEqual(m.state.cells, (tag(b'\x5E'),))
        m = MixedEditor(1)
        for key in 'ㄱㅏㄴ':
            self.assertTrue(m.press(key))
        before, history = m.state, m.history.copy()
        self.assertFalse(m.press('ㅏ'))
        self.assertEqual((m.state, m.history), (before, history))
        self.assertFalse(m.write_native(b'\x5E'))
        self.assertEqual((m.state, m.history), (before, history))
        self.assertFalse(m.move(1))
        self.assertEqual((m.state, m.history), (before, history))

    def test_loaded_hangul_canonical_delete_and_invalid_import(self):
        native = tag(b'\xE4\x00')
        m = MixedEditor(2); m.load([ord('괙') - 0xAC00, native]); m.move(1)
        for expected in ['괘', '과', '고', 'ㄱ', '']:
            self.assertTrue(m.backspace())
            rank = 11172 if expected == 'ㄱ' else ord(expected) - 0xAC00 if expected else None
            self.assertEqual(m.state.cells, ((rank, native) if rank is not None else (native,)))
        before = m.state
        for words in ([11172], [0xFFFF], [True], [0, 0, 0]):
            with self.assertRaises(ValueError):
                m.load(words)
            self.assertEqual(m.state, before)
        for token in (b'', b'\xE4', b'\xF9', b'\x00\x00'):
            self.assertFalse(m.write_native(token)); self.assertEqual(m.state, before)

    def test_capacity_history_and_all_native_structural_tokens(self):
        tokens = [bytes([i]) for i in range(0xE4)] + [bytes([0xE4, i]) for i in range(256)]
        for cap in range(1, 11):
            for token in tokens:
                words = [tag(token)] * cap
                m = MixedEditor(cap); m.load(words)
                for _ in range(cap):
                    self.assertTrue(m.move(1))
                before = m.state
                self.assertFalse(m.write_native(token)); self.assertEqual(m.state, before)
                self.assertTrue(m.backspace())
                self.assertEqual(m.state, Snapshot(tuple(words[:-1]), cap - 1, None))
                self.assertTrue(m.write_native(token))
                self.assertEqual(m.candidate(), tuple(words))
        m = MixedEditor(10)
        for key in 'ㄱㄱㅗㅏㅣㄹㄱ' * 10:
            self.assertTrue(m.press(key))
        self.assertEqual(len(m.history), 70)
        self.assertEqual(len(m.candidate()), 10)
        before = m.state
        self.assertFalse(m.press('ㄱ')); self.assertEqual(m.state, before)
        for _ in range(70):
            self.assertTrue(m.backspace())
        self.assertEqual(m.state, Snapshot((), 0, None))
        self.assertFalse(m.backspace())


if __name__ == '__main__':
    unittest.main()
