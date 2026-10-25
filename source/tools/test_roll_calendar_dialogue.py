import unittest
from report_roll_pet import ROOT,read,sha
from tpl_literals import literals
class CalendarDialogueTests(unittest.TestCase):
    def test_source_and_finite_scope(self):
        a=read(ROOT/'translations/roll_calendar_dialogue_ko.json');s=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes();self.assertEqual(sha(s),a['source_sha256']);self.assertEqual(sha(s[0x65F11C:0x65F11C+2190]),a['source_archive_sha256']);self.assertEqual(len(a['units']),9);self.assertFalse(a['review']['release_eligible'])
        rows={x.key:x.text for x in literals((ROOT/'analysis/tpl_baseline/65F11C.tpl').read_text(encoding='utf-8'))}
        for u in a['units']:self.assertEqual(u['source'],rows[u['id']]);self.assertEqual(u['source'].count('\n'),u['translation'].count('\n'));self.assertEqual(u['state'],'needs_review')
    def test_register_scope_not_date_or_user_string(self):
        a=read(ROOT/'translations/roll_calendar_dialogue_ko.json');r=read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['65F11C'];self.assertEqual(r['pointers'],[0x322E0]);self.assertEqual(r['literal_scripts'],[1,2,20,21,24]);self.assertEqual(r['literal_ids'],[u['id'] for u in a['units']]);self.assertEqual(r['script_count'],255)
    def test_choices_and_padding_preserved(self):
        a=read(ROOT/'translations/roll_calendar_dialogue_ko.json');d={u['id']:u for u in a['units']};self.assertEqual(d['65F11C:24:1']['translation'],'예  ');self.assertEqual(d['65F11C:24:2']['translation'],'아니오');self.assertEqual(d['65F11C:2:1']['translation'],'일정\n');self.assertEqual(d['65F11C:2:2']['translation'],'기념일')
if __name__=='__main__':unittest.main()
