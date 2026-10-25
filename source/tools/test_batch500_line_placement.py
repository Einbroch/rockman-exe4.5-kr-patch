"""Controlled fixtures for unchanged-wording, same-row132px placement."""
import unittest
from survey_batch500_017_layout import place,advance,protected_edges
class PlacementTests(unittest.TestCase):
    def test_unchanged_valid(self):
        self.assertEqual(place('한글\n대사'), '한글\n대사')
    def test_reposition_preserves_flat_words_and_rows(self):
        text='가나다라마바사아자차카 파\n하'
        result=place(text)
        self.assertIsNotNone(result)
        self.assertEqual(result.replace('\n',' '),text.replace('\n',' '))
        self.assertEqual(result.count('\n'),text.count('\n'))
        self.assertTrue(all(advance(line)<=132 for line in result.split('\n')))
    def test_no_capacity_or_extra_rows(self):
        self.assertIsNone(place('가'*12))
        self.assertIsNone(place('가\n나\n다\n라'))
    def test_no_split_inside_word(self):
        self.assertIsNone(place('가'*12+' 나\n다'))
    def test_protected_terminal_newline(self):
        self.assertFalse(protected_edges('원문\n','번역\n문구 '))
        self.assertTrue(protected_edges('원문\n','번역\n'))
    def test_protected_prefix_and_padding(self):
        self.assertFalse(protected_edges('\n원문','번역\n'))
        self.assertFalse(protected_edges('원문  ','번역 '))
        self.assertTrue(protected_edges('원문  ','번역  '))
if __name__=='__main__':unittest.main()
