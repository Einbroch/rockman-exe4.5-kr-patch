import copy,unittest
from report_roll_pet import ROOT,read,sha
from calendar_menu_model import validate
from tpl_literals import literals
class CalendarMenuTests(unittest.TestCase):
    def asset(self):return read(ROOT/'translations/calendar_menu_ko.json')
    def test_source_revision_and_scope(self):
        a=self.asset();s=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes();self.assertEqual(sha(s),a['source_sha256']);self.assertEqual(sha(s[0x6368E8:0x6368E8+2337]),a['source_archive_sha256'])
        x=next(x for x in literals((ROOT/'analysis/tpl_baseline/6368E8.tpl').read_text(encoding='utf-8')) if x.key=='6368E8:0:0');self.assertEqual(x.text,a['units'][0]['source']);self.assertFalse(a['review']['release_eligible'])
    def test_cell_stride_and_growth_rejected(self):
        a=self.asset();r=validate(a['units']);self.assertEqual(r['decoded_cells'],24);self.assertEqual(r['expected_stage_bytes'],1536)
        for text in ['등록 일정 보기 삭제',a['units'][0]['translation']+' ',a['units'][0]['translation'].replace('등록','등록함')]:
            bad=copy.deepcopy(a['units']);bad[0]['translation']=text
            with self.assertRaises(ValueError):validate(bad)
    def test_keyboard_or_name_scope_rejected(self):
        a=self.asset();bad=copy.deepcopy(a['units']);bad[0]['id']='6368E8:62:0'
        with self.assertRaises(ValueError):validate(bad)
    def test_replacement_preserves_every_other_literal_and_controls(self):
        from calendar_menu_model import replace_menu_literal
        from tpl_literals import skeleton
        a=self.asset();tpl=(ROOT/'analysis/tpl_baseline/6368E8.tpl').read_text(encoding='utf-8');out=replace_menu_literal(tpl,a['units'])
        self.assertEqual(skeleton(tpl),skeleton(out));before={x.key:x.text for x in literals(tpl)};after={x.key:x.text for x in literals(out)}
        for key in before:
            if key!='6368E8:0:0':self.assertEqual(before[key],after[key])
        bad=copy.deepcopy(a['units']);bad.append(bad[0])
        with self.assertRaises(ValueError):validate(bad)
if __name__=='__main__':unittest.main()
