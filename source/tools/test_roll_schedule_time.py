import unittest
from report_roll_pet import ROOT,read,static
class ScheduleTimeTests(unittest.TestCase):
    def test_prior_five_wordings_preserved(self):
        old=read(ROOT/'translations/roll_schedule_ko.json');new=read(ROOT/'translations/roll_schedule_time_ko.json');d={u['id']:u for u in new['units']}
        for u in old['units']:self.assertEqual(d[u['id']],u)
        self.assertEqual(len(d),6)
    def test_native_runtime_and_static_guard(self):
        from report_roll_schedule_time import main
        from roll_schedule_time_model import validate
        from run_roll_schedule_time import STEM
        r=main();self.assertTrue(r['passed']);m,_,_,_,_=static(STEM,'661754');self.assertEqual(m['translated_units'],1071)
        with self.assertRaises(ValueError):validate([],{'schedule_variable_profile':'unknown'},'','',[])
if __name__=='__main__':unittest.main()
