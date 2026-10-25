import unittest

from tools.archive_scripts import script_spans, verify_untouched_scripts


def fixture(parts):
    offset = len(parts) * 2
    header = bytearray()
    for part in parts:
        header.extend(offset.to_bytes(2, "little"))
        offset += len(part)
    return bytes(header) + b"".join(parts)


class ScriptPreservationTests(unittest.TestCase):
    def test_growth_preserves_empty_and_other_scripts(self):
        before = fixture([b"old", b"", b"unchanged"])
        after = fixture([b"longer Korean bytes", b"", b"unchanged"])
        result = verify_untouched_scripts(before, after, 3, {0})
        self.assertEqual([(r["script"], r["bytes"]) for r in result], [(1, 0), (2, 9)])

    def test_unselected_change_rejected(self):
        with self.assertRaisesRegex(ValueError, "unselected script"):
            verify_untouched_scripts(fixture([b"x", b"original"]), fixture([b"y", b"damaged"]), 2, {0})

    def test_invalid_boundaries_rejected(self):
        for data, count in [(b"", 2), (b"\x00\x00", 1), (b"\x06\x00\x08\x00\x07\x00ABC", 3),
                            (b"\x04\x00\xff\xff", 2)]:
            with self.subTest(data=data), self.assertRaises(ValueError):
                script_spans(data, count)

    def test_unknown_script_rejected(self):
        with self.assertRaises(ValueError):
            verify_untouched_scripts(fixture([b"x"]), fixture([b"x"]), 1, {1})


if __name__ == "__main__":
    unittest.main()
