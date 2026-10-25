"""Fixed unit-count interface fixtures; not product-population verification."""
import unittest
from cumulative_batch500 import unit_count
class DenominatorTests(unittest.TestCase):
    def test_legacy(self):self.assertEqual(unit_count({}),500)
    def test_explicit(self):
        for n in (1,268,500):self.assertEqual(unit_count({'units':n}),n)
    def test_reject(self):
        for n in (True,False,0,501,-1,'268',268.0,None):
            with self.subTest(n=n),self.assertRaises(ValueError):unit_count({'units':n})
if __name__=='__main__':unittest.main()
