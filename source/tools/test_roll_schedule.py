"""Source-pinned limited schedule scope and exact-ROM renderer evidence."""
import unittest
from report_roll_pet import ROOT,read,sha,static
from tpl_literals import literals
from archive_scripts import script_spans
from run_roll_schedule import STEM

class ScheduleTests(unittest.TestCase):
    def test_exact_five_literal_source_inventory(self):
        a=read(ROOT/'translations/roll_schedule_ko.json');source=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes();native=source[0x661754:0x661858]
        self.assertEqual(sha(native),a['source_archive_sha256']);inventory={x.key:x.text for x in literals((ROOT/'analysis/tpl_baseline/661754.tpl').read_text(encoding='utf-8'))}
        self.assertEqual(len(inventory),12);self.assertEqual({u['id'] for u in a['units']},{'661754:1:0','661754:3:0','661754:10:0','661754:10:1','661754:12:0'})
        for u in a['units']:self.assertEqual(u['source'],inventory[u['id']]);self.assertEqual(u['state'],'needs_review')
        self.assertFalse(a['review']['release_eligible'])

    def test_unselected_dynamic_scripts_byte_identical(self):
        m,rom,_,_,_=static(STEM,'661754');ar=next(a for a in m['archives'] if a['archive']=='661754');source=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes();old=script_spans(source[0x661754:0x661858],14);new=script_spans(rom[ar['rom_offset']:ar['rom_offset']+ar['compiled_bytes']],14)
        for script in set(range(14))-{1,3,10,12}:self.assertEqual(new[script],old[script])
        self.assertEqual(m['translated_units'],1070)

    def test_all_five_pages_quarantined_renderer_proof(self):
        from report_roll_schedule import main
        r=main();self.assertTrue(r['passed']);self.assertEqual(len(r['pages']),5);self.assertEqual(len(r['diagnostic_renderer_units']),5);self.assertEqual(r['normal_runtime_units'],[]);self.assertEqual(r['name_selector_cpu_vectors'],32)

if __name__=='__main__':unittest.main()
