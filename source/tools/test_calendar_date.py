import unittest
from report_roll_pet import ROOT,read
from tpl_literals import literals
from build_development_patch import selected_scope
class CalendarDateTests(unittest.TestCase):
    def test_prior11_unchanged_and_date_scope(self):
        old=read(ROOT/'translations/roll_calendar_content_ko.json');a=read(ROOT/'translations/roll_calendar_date_ko.json');d={u['id']:u for u in a['units']};self.assertEqual(len(d),14)
        for u in old['units']:self.assertEqual(d[u['id']],u)
        scope=selected_scope(read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['65F11C'],a);self.assertEqual(scope['literal_ids'],[u['id'] for u in a['units']]);self.assertFalse(a['review']['release_eligible'])
    def test_source_and_structural_padding(self):
        a=read(ROOT/'translations/roll_calendar_date_ko.json');s={x.key:x.text for x in literals((ROOT/'analysis/tpl_baseline/65F11C.tpl').read_text(encoding='utf-8'))}
        for u in a['units']:self.assertEqual(u['source'],s[u['id']]);self.assertEqual(u['state'],'needs_review');self.assertEqual(u['source'].count('\n'),u['translation'].count('\n'))
        self.assertEqual(a['units'][0]['translation'],'오늘은 ')
if __name__=='__main__':unittest.main()
