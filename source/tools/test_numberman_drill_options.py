import copy,unittest,tempfile
from pathlib import Path
from textpet_korean import prepare_plugins
from korean_codec import EXTRA_CHARACTER_INDICES
from report_roll_pet import ROOT,read
from tpl_literals import resolve_units,skeleton,literals,serialize
from build_development_patch import selected_scope,translate_literal_scope,validate_literal_numerals,validate_characters

class OptionsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory(prefix='exe45-options-tests-');cls.plugins=Path(cls.temp.name)/'plugins';prepare_plugins(cls.plugins,set(EXTRA_CHARACTER_INDICES))
    @classmethod
    def tearDownClass(cls):cls.temp.cleanup()
    def test_scope_and_controls(self):
        a=read(ROOT/'translations/numberman_drill_options_ko.json');b=read(ROOT/'translations/numberman_drill_bubbles_ko.json')
        self.assertEqual(a['units'][:32],b['units']);self.assertEqual(a['wordings'][:32],b['wordings']);self.assertFalse(a['review']['release_eligible'])
        u=resolve_units(a);self.assertEqual(len(u),42);s=selected_scope(read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['715064'],a)
        t=(ROOT/'analysis/tpl_baseline/715064.tpl').read_text(encoding='utf-8');v=translate_literal_scope(t,u,s)
        self.assertEqual(skeleton(t),skeleton(v));validate_literal_numerals(u,s)
        validate_characters(v,self.plugins/'exe45-utf8.tbl',s,{x['id'] for x in u})
    def test_level_numeral_rejected(self):
        a=read(ROOT/'translations/numberman_drill_options_ko.json');u=copy.deepcopy(resolve_units(a));s=selected_scope(read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['715064'],a)
        next(x for x in u if x['id']=='715064:13:2')['translation']='레벨3\n'
        with self.assertRaisesRegex(ValueError,'numeral'):validate_literal_numerals(u,s)
    def test_exam_vertical_overflow_rejected(self):
        a=read(ROOT/'translations/numberman_drill_options_ko.json');u=copy.deepcopy(resolve_units(a));s=selected_scope(read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['715064'],a)
        next(x for x in u if x['id']=='715064:15:3')['translation']='훈련을 지금 시작하기\n'
        v=translate_literal_scope((ROOT/'analysis/tpl_baseline/715064.tpl').read_text(encoding='utf-8'),u,s)
        with self.assertRaisesRegex(ValueError,'vertical'):validate_characters(v,self.plugins/'exe45-utf8.tbl',s,{x['id'] for x in u})
    def test_padded_lineage_and_required_spacing(self):
        a=read(ROOT/'translations/numberman_drill_options_padded_ko.json');b=read(ROOT/'translations/numberman_drill_options_ko.json')
        self.assertEqual([(x['id'],x['source']) for x in a['units']],[(x['id'],x['source']) for x in b['units']])
        u=resolve_units(a);s=selected_scope(read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['715064'],a)
        t=(ROOT/'analysis/tpl_baseline/715064.tpl').read_text(encoding='utf-8');v=translate_literal_scope(t,u,s)
        self.assertEqual(skeleton(t),skeleton(v));layout=validate_characters(v,self.plugins/'exe45-utf8.tbl',s,{x['id'] for x in u})
        self.assertEqual(next(x['grid_choice_row_pixels'] for x in layout if x['id']=='715064:13:1'),102)
        next(x for x in u if x['id']=='715064:13:1')['translation']='레벨1'
        v=translate_literal_scope(t,u,s)
        with self.assertRaisesRegex(ValueError,'padding'):validate_characters(v,self.plugins/'exe45-utf8.tbl',s,{x['id'] for x in u})
    def test_leading_literal_space_roundtrip(self):
        for value in [' 레벨1',' 레벨2\n',' 레벨4\n']:
            tpl='@archive 715064\n@size 16\nscript 13 mmbn45 {\n'+serialize(value)+'\n}\n'
            self.assertEqual(literals(tpl)[0].text,value)
    def test_column_spacing_is_narrow_and_required(self):
        a=read(ROOT/'translations/numberman_drill_options_spaced_ko.json');u=resolve_units(a);s=selected_scope(read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['715064'],a)
        t=(ROOT/'analysis/tpl_baseline/715064.tpl').read_text(encoding='utf-8');v=translate_literal_scope(t,u,s)
        self.assertEqual(skeleton(t),skeleton(v))
        layout=validate_characters(v,self.plugins/'exe45-utf8.tbl',s,{x['id'] for x in u})
        self.assertEqual(next(x['grid_choice_row_pixels'] for x in layout if x['id']=='715064:13:1'),110)
        next(x for x in u if x['id']=='715064:13:1')['translation']=' 레벨1'
        with self.assertRaisesRegex(ValueError,'padding'):translate_literal_scope(t,u,s)
        next(x for x in u if x['id']=='715064:13:1')['translation']=' 레벨1 '
        next(x for x in u if x['id']=='715064:15:1')['translation']+=' '
        with self.assertRaisesRegex(ValueError,'padding'):translate_literal_scope(t,u,s)

if __name__=='__main__':unittest.main()
