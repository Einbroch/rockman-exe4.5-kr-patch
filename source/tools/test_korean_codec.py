import unittest

try:
    from tools.korean_codec import decode_syllable, encode_hangul, find_escapes
except ModuleNotFoundError:
    from korean_codec import decode_syllable, encode_hangul, find_escapes


class KoreanCodecTests(unittest.TestCase):
    def test_explicit_middle_dot_extension(self):
        from tools.korean_codec import encode_character,decode_character
        self.assertEqual(encode_character('·').hex(),'f9fca52b')
        self.assertEqual(decode_character(encode_character('·')),('·',4))
        with self.assertRaises(ValueError):decode_syllable(encode_character('·'))
        with self.assertRaises(ValueError):decode_character(bytes.fromhex('f9fca62b'))
    def test_explicit_comma_extension(self):
        from tools.korean_codec import encode_character, decode_character
        self.assertEqual(encode_character(",").hex(), "f9fca42b")
        self.assertEqual(decode_character(encode_character(",")), (",", 4))
        with self.assertRaises(ValueError):
            encode_character("A")
    def test_known_wording(self):
        encoded = encode_hangul("한글")
        self.assertEqual(encoded.hex(), "f9fc5c29f9fc0002")
        first, offset = decode_syllable(encoded)
        second, offset = decode_syllable(encoded, offset)
        self.assertEqual((first + second, offset), ("한글", 8))
        self.assertEqual([x["character"] for x in find_escapes(encoded)], ["한", "글"])

    def test_reject_non_hangul(self):
        with self.assertRaises(ValueError):
            encode_hangul("A")

    def test_entire_repertoire(self):
        for cp in range(0xAC00, 0xD7A4):
            self.assertEqual(decode_syllable(encode_hangul(chr(cp))), (chr(cp), 4))

    def test_reject_bad_offsets_and_truncated_escapes(self):
        for blob, offset in ((b"\xF9\xFC\x00", 0), (b"\xF9\xFC\xA4\x2B", 0),
                             (b"\xF9\xFC\x00\x00", -4), (b"\xF9\xFC\x00\x00", 4)):
            with self.assertRaises(ValueError):
                decode_syllable(blob, offset)


if __name__ == "__main__":
    unittest.main()
