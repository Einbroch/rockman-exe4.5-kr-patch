#!/usr/bin/env python3

import tempfile
import unittest
from pathlib import Path

try:
    from tools.verify_tpi_index import parse_tpi
except ModuleNotFoundError:  # direct execution from the tools directory
    from verify_tpi_index import parse_tpi


class TextPetNumberSyntaxTests(unittest.TestCase):
    def test_prefixed_hex_and_unprefixed_decimal(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.tpi"
            path.write_text("0x6DD0B8:&1412=0x041140\n", encoding="utf-8")
            row = parse_tpi(path)[0]
        self.assertEqual(row["offset"], 0x6DD0B8)
        self.assertEqual(row["size"], 1412)
        self.assertEqual(row["pointers"], [0x041140])
        self.assertTrue(row["compressed"])


if __name__ == "__main__":
    unittest.main()
