import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fixedcell_font import pack_pixels, unpack_pixels, rasterize

PROFILE = dict(baseline=14, background=0, ink=1, shadow=2)


class FixedCellTests(unittest.TestCase):
    def test_tile_order_and_nibbles(self):
        grid = [[(x + y) % 16 for x in range(8)] for y in range(16)]
        result = pack_pixels(grid)
        self.assertEqual(result[:4], bytes.fromhex("10325476"))
        self.assertEqual(result[32:36], bytes.fromhex("98BADCFE"))
        self.assertEqual(unpack_pixels(result), grid)

    def test_ink_over_shadow_and_baseline(self):
        pixels = unpack_pixels(rasterize(2, 2, 0, 0, [0x80, 0x40], **PROFILE))
        self.assertEqual(pixels[12][0], 1)
        self.assertEqual(pixels[13][1], 1)
        self.assertEqual(pixels[14][2], 2)
        self.assertEqual(sum(n == 1 for row in pixels for n in row), 2)

    def test_clipping_and_empty_rejected(self):
        for args in ((8, 1, 0, 0, [128]), (1, 16, 0, 0, [128] * 16), (1, 1, 0, 0, [0])):
            with self.subTest(args=args), self.assertRaises(ValueError):
                rasterize(*args, **PROFILE)

    def test_invalid_representation_rejected(self):
        with self.assertRaises(ValueError):
            unpack_pixels(bytes(63))
        with self.assertRaises(ValueError):
            pack_pixels([[16] * 8 for _ in range(16)])
        with self.assertRaises(ValueError):
            rasterize(1, 1, 0, 0, [129], **PROFILE)


if __name__ == "__main__":
    unittest.main()
