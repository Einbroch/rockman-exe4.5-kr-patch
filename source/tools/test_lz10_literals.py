import unittest
from tools.lz10_literals import encode, decode
from tools.verify_tpi_index import lz77_decompress


class LZ10LiteralTests(unittest.TestCase):
    def test_boundaries_and_independent_decoder(self):
        for size in range(1, 161):
            with self.subTest(size=size):
                payload = bytes((i * 31 + size) % 256 for i in range(size))
                blob = encode(payload, limit=160)
                self.assertEqual(len(blob) % 4, 0)
                self.assertEqual(decode(blob, limit=160), payload)
                self.assertEqual(lz77_decompress(blob, 0)[0], payload)

    def test_invalid_size_and_truncation(self):
        for value in (b"", bytes(161)):
            with self.assertRaises(ValueError):
                encode(value, limit=160)
        blob = encode(bytes(range(17)), limit=160)
        for at in range(len(blob)):
            with self.assertRaises(ValueError):
                decode(blob[:at], limit=160)
        with self.assertRaises(ValueError):
            decode(blob, limit=16)

    def test_flags_type_padding_and_trailing_data_rejected(self):
        blob = encode(b"a", limit=160)
        for at, value in ((0, 0x11), (4, 0x80), (7, 1)):
            bad = bytearray(blob)
            bad[at] = value
            with self.assertRaises(ValueError):
                decode(bytes(bad), limit=160)
        with self.assertRaises(ValueError):
            decode(blob + bytes(4), limit=160)


if __name__ == "__main__":
    unittest.main()
