"""Source-pinned finite alarm scope and previous-development selection tests."""
import unittest
from report_roll_pet import ROOT,read,sha
from tpl_literals import literals

class AlarmScopeTests(unittest.TestCase):
    def test_source_revision_and_exact_archive(self):
        asset=read(ROOT/'translations/roll_schedule_alarm_ko.json');source=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes()
        self.assertEqual(sha(source),asset['source_sha256']);self.assertEqual(sha(source[0x660D90:0x660D90+717]),asset['source_archive_sha256'])
    def test_registered_scope_and_source_literals(self):
        asset=read(ROOT/'translations/roll_schedule_alarm_ko.json');entry=read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['660D90']
        self.assertEqual(entry['literal_scripts'],[3,4,6]);self.assertEqual(entry['script_count'],28);self.assertEqual(entry['pointers'],[0x380E8]);self.assertEqual(entry['literal_ids'],[u['id'] for u in asset['units']])
        parsed={x.key:x.text for x in literals((ROOT/'analysis/tpl_baseline/660D90.tpl').read_text(encoding='utf-8'))}
        for u in asset['units']:self.assertEqual(u['source'],parsed[u['id']]);self.assertEqual(u['source'].count('\n'),u['translation'].count('\n'))
    def test_explicit_manual_drafts_not_release(self):
        asset=read(ROOT/'translations/roll_schedule_alarm_ko.json');self.assertFalse(asset['review']['release_eligible'])
        self.assertEqual([u['translation'] for u in asset['units']],['저기~!\n밥 먹을 시간이야!','학원 갈 시간이야\n얼른 준비하지 않으면\n지각하겠어!','음, 그리고・・・'])
        self.assertTrue(all(u['state']=='needs_review' for u in asset['units']))

if __name__=='__main__':unittest.main()
