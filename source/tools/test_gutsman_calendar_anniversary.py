import copy,unittest
from report_roll_pet import ROOT,read,sha
from gutsman_calendar_anniversary import CHILD as DIALOGUE,validate_parent as validate_dialogue
from calendar_anniversary_labels import CHILD as LABELS,validate_parent as validate_labels,replace
from build_development_patch import selected_scope,translate_literal_scope,validate_characters
from tpl_literals import literals
class CalendarAnniversary(unittest.TestCase):
    def test_parent_projections(self):
        d=read(ROOT/DIALOGUE);validate_dialogue(d);l=read(ROOT/LABELS);validate_labels(l)
        bad=copy.deepcopy(d);bad['units'][0]['translation']='변경';self.assertRaises(ValueError,validate_dialogue,bad)
        bad=copy.deepcopy(l);bad['units'][-1]['translation']='내 생일';self.assertRaises(ValueError,validate_labels,bad)
    def test_dialogue_and_fixed_cells_build(self):
        registry=read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']
        for path,archive in [(DIALOGUE,'665698'),(LABELS,'6368E8')]:
            a=read(ROOT/path);scope=selected_scope(registry[archive],a);tpl=(ROOT/f'analysis/full_scope_v1/source_tpl/{archive}.tpl').read_text(encoding='utf-8-sig');target=translate_literal_scope(tpl,a['units'],scope);tbl=ROOT/'poc/build/exe45_ko_development_gutsman_calendar_home_v1/plugins/exe45-utf8.tbl';validate_characters(target,tbl,scope,{u['id'] for u in a['units']})
        before={x.key:x.text for x in literals((ROOT/'analysis/full_scope_v1/source_tpl/6368E8.tpl').read_text(encoding='utf-8-sig'))};after={x.key:x.text for x in literals(replace((ROOT/'analysis/full_scope_v1/source_tpl/6368E8.tpl').read_text(encoding='utf-8-sig'),read(ROOT/LABELS)['units']))}
        self.assertEqual(after['6368E8:73:0'],read(ROOT/LABELS)['units'][-1]['translation']);self.assertEqual([k for k in before if before[k]!=after[k]],['6368E8:0:0','6368E8:60:0','6368E8:62:0','6368E8:63:0','6368E8:73:0'])
if __name__=='__main__':unittest.main()
