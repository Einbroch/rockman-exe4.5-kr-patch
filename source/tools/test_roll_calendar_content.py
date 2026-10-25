import unittest
from report_roll_pet import ROOT,read
from tpl_literals import literals
from build_development_patch import selected_scope
class CalendarContentTests(unittest.TestCase):
    def test_prior_nine_unchanged(self):
        before=read(ROOT/'translations/roll_calendar_dialogue_ko.json');after=read(ROOT/'translations/roll_calendar_content_ko.json');d={u['id']:u for u in after['units']}
        self.assertEqual(len(d),11)
        for u in before['units']:self.assertEqual(d[u['id']],u)
    def test_source_and_registered_scope(self):
        a=read(ROOT/'translations/roll_calendar_content_ko.json');scope=selected_scope(read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['65F11C'],a);source={x.key:x.text for x in literals((ROOT/'analysis/tpl_baseline/65F11C.tpl').read_text(encoding='utf-8'))}
        self.assertEqual(scope['literal_ids'],[u['id'] for u in a['units']]);self.assertEqual(scope['literal_scripts'],[1,2,20,21,22,23,24]);self.assertFalse(a['review']['release_eligible'])
        for u in a['units']:self.assertEqual(u['source'],source[u['id']]);self.assertEqual(u['state'],'needs_review')
if __name__=='__main__':unittest.main()
