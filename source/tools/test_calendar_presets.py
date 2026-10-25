import copy,unittest
from report_roll_pet import ROOT,read
from calendar_presets import validate,replace
from tpl_literals import literals
from build_development_patch import selected_scope,literal_scope

class CalendarPresetTests(unittest.TestCase):
    def test_four_literal_scope_preserves_prior_two(self):
        a=read(ROOT/'translations/calendar_presets_ko.json');old=read(ROOT/'translations/calendar_types_ko.json')
        self.assertEqual(a['units'][:2],old['units']);self.assertEqual(validate(a['units'])['name_field_bytes'],22)
        tpl=(ROOT/'analysis/tpl_baseline/6368E8.tpl').read_text(encoding='utf-8');before={x.key:x.text for x in literals(tpl)};after={x.key:x.text for x in literals(replace(tpl,a['units']))}
        chosen={u['id'] for u in a['units']}
        self.assertEqual({k:v for k,v in before.items() if k not in chosen},{k:v for k,v in after.items() if k not in chosen})
    def test_wrong_name_state_and_scope_fail(self):
        a=read(ROOT/'translations/calendar_presets_ko.json')
        for field,value in [('translation','식사 시간'),('source','ごはん!'),('state','approved')]:
            b=copy.deepcopy(a['units']);b[2][field]=value
            with self.assertRaises(ValueError):validate(b)
        with self.assertRaises(ValueError):validate(a['units'][:-1])
    def test_consumer_profiles_do_not_change_keyboard(self):
        a=read(ROOT/'translations/calendar_presets_ko.json');s=selected_scope(read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['6368E8'],a)
        self.assertEqual(s['literal_scripts'],[0,60,62,63]);self.assertEqual(literal_scope(s,'6368E8:62:0')['consumer'],'fixed-cell-mono');self.assertEqual(literal_scope(s,'6368E8:63:0')['consumer'],'fixed-cell-mono')

if __name__=='__main__':unittest.main()
