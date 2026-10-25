"""Controlled same-wording layout and source-entry guard fixtures."""
import unittest
from fullbox_layout import place
from fullbox_capacity import validate
from test_fullbox_capacity import tpl
from nickname_capacity import advance

class Layout(unittest.TestCase):
    def test_unchanged(self):self.assertEqual(place('가 나\n다 라'),'가 나\n다 라')
    def test_reflow(self):
        text='가'*10+' '+'나'*10+'\n'+'다'*4;v=place(text)
        self.assertIsNotNone(v);self.assertEqual(v.replace('\n',' '),text.replace('\n',' '));self.assertEqual(v.count('\n'),1);self.assertLessEqual(max(map(advance,v.split('\n'))),180)
    def test_unbreakable(self):self.assertIsNone(place('가'*16))
    def test_rows_not_added(self):self.assertIsNone(place('가\n가\n가\n가'))
    def test_guarded_source(self):
        pre='\tstoreGlobal16\n\t\tglobal = 15\n\t\tvalue = 513\n\tflagSet\n\t\tflag = 5473\n'
        original=tpl('あ').replace('\tmugshotShow',pre+'\tmugshotShow',1);target=original.replace('"あ"','"가"');profile=dict(script=0,ids=['ABCDEF:0:0'],entry_guards=['storeGlobal16','flagSet'])
        self.assertTrue(validate(original,target,[profile],{'ABCDEF:0:0'}))
        profile['entry_guards']=['flagSet']
        with self.assertRaises(ValueError):validate(original,target,[profile],{'ABCDEF:0:0'})
    def test_guard_cannot_position_window(self):
        original=tpl('あ').replace('\tmugshotShow','\tpositionBox\n\t\tleft = 10\n\tmugshotShow',1)
        with self.assertRaises(ValueError):validate(original,original,[dict(script=0,ids=['ABCDEF:0:0'],entry_guards=['positionBox'])],{'ABCDEF:0:0'})

    def test_portrait_changes_explicit_only(self):
        tail='\tclearMsg\n\tmugshotShow\n\t\tmugshot = GutsMan\n\t"い"\n'
        original=tpl('あ',tail=tail);target=original.replace('"あ"','"가"').replace('"い"','"나"')
        ids=['ABCDEF:0:0','ABCDEF:0:1'];profile=dict(script=0,ids=ids)
        with self.assertRaises(ValueError):validate(original,target,[profile],set(ids))
        profile['portrait_changes']=True
        self.assertEqual(len(validate(original,target,[profile],set(ids))[0]['pages']),2)

    def test_portrait_change_needs_page_clear(self):
        original=tpl('あ',tail='\tmugshotShow\n\t\tmugshot = GutsMan\n\t"い"\n')
        ids=['ABCDEF:0:0','ABCDEF:0:1']
        with self.assertRaises(ValueError):validate(original,original,[dict(script=0,ids=ids,portrait_changes=True)],set(ids))

if __name__=='__main__':unittest.main()
