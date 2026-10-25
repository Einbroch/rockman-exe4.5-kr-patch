"""Controlled rejection fixtures for inherited wording, nickname and choices."""
import copy,unittest
from report_roll_pet import ROOT,read
from build_development_patch import selected_scope,translate_literal_scope,validate_nickname_suffix,validate_characters

class PlugoutGuards(unittest.TestCase):
    def setUp(self):
        self.asset=read(ROOT/'translations/roll_gutsman_plugout_ko.json')
        self.registry=read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['778338']
        self.source=(ROOT/'analysis/full_scope_v1/source_tpl/778338.tpl').read_text(encoding='utf-8-sig')
    def test_parent_accept_and_mutation_reject(self):
        selected_scope(self.registry,self.asset)
        bad=copy.deepcopy(self.asset);bad['units'][0]['translation']='다른 대사'
        with self.assertRaisesRegex(ValueError,'parent'):selected_scope(self.registry,bad)
    def test_gutsman_nickname_suffix_growth_reject(self):
        scope=selected_scope(self.registry,self.asset);units=copy.deepcopy(self.asset['units'])
        validate_nickname_suffix(units,'778338',scope)
        units[4]['translation']='야、\n플러그아웃하거스?\n'
        with self.assertRaisesRegex(ValueError,'nickname'):validate_nickname_suffix(units,'778338',scope)
    def test_protected_source_and_selection_padding_reject(self):
        scope=selected_scope(self.registry,self.asset)
        for field,value in [('source','잘못된 원문'),('translation','예')]:
            units=copy.deepcopy(self.asset['units']);units[5][field]=value
            with self.assertRaises(ValueError):translate_literal_scope(self.source,units,scope)
    def test_choice_row_empty_and_width_guard(self):
        scope=selected_scope(self.registry,self.asset);units=copy.deepcopy(self.asset['units'])
        table=ROOT/'poc/build/exe45_ko_development_gutsman_plugout_v1/plugins/exe45-utf8.tbl'
        target=translate_literal_scope(self.source,units,scope)
        validate_characters(target,table,scope,{u['id'] for u in units})
        units[4]['translation']='、\n플러그아웃하거스?\n가'
        # Geometry validator independently rejects an occupied selection row.
        from tpl_literals import literals,serialize
        item=next(x for x in literals(target) if x.key==units[4]['id'])
        target=target[:item.start]+serialize(units[4]['translation'])+target[item.end:]
        with self.assertRaisesRegex(ValueError,'selection row'):validate_characters(target,table,scope,{u['id'] for u in units})

if __name__=='__main__':unittest.main()
