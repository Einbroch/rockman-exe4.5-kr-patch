import copy,unittest
from report_roll_pet import ROOT,read,static,sha
from tpl_literals import resolve_units,literals,skeleton
from build_development_patch import selected_scope,translate_literal_scope,validate_nickname_suffix,validate_characters
from archive_scripts import script_spans
from report_roll_family import STEM,PREFIX,main

class RollFamilyTests(unittest.TestCase):
    def test_eight_source_units_95_protected_scripts_and_fonts(self):
        a=read(ROOT/'translations/roll_family_sister_ko.json');u=resolve_units(a);src=(ROOT/'analysis/tpl_baseline/661858.tpl').read_text(encoding='utf-8-sig');s=selected_scope(read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['661858'],a);target=translate_literal_scope(src,u,s)
        self.assertEqual(len(u),8);self.assertEqual({x['id'] for x in u},{x.key for x in literals(src) if int(x.key.split(':')[1]) in [7,8]});self.assertEqual(skeleton(src),skeleton(target));self.assertTrue(all(x['state']=='needs_review' and x['source'].count('\n')==x['translation'].count('\n') for x in u))
        m,rom,e,streams,c=static(STEM,'661858');self.assertEqual(m['translated_units'],974);self.assertEqual(len(streams),8);self.assertEqual(len(c['protected_nonliteral_scripts']),95);self.assertTrue(c['all_fonts_verified']);self.assertEqual(c['max_literal_width'],123)
        old={x['path']:x['sha256'] for x in read(ROOT/'poc/output/exe45_ko_development_roll_plugout_v1.json')['translation_assets']};now={x['path']:x['sha256'] for x in m['translation_assets']};self.assertTrue(all(now[k]==v for k,v in old.items()));self.assertEqual(sha((ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes()),a['source_sha256'])
    def test_particle_free_nickname_and_separate_choice_build_guards(self):
        a=read(ROOT/'translations/roll_family_sister_ko.json');u=resolve_units(a);s=selected_scope(read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['661858'],a);src=(ROOT/'analysis/tpl_baseline/661858.tpl').read_text(encoding='utf-8-sig');tbl=ROOT/'poc/work/roll_family_sister_v1_r2/plugins/exe45-utf8.tbl';validate_nickname_suffix(u,'661858',s)
        for first in ['는、','은、','は、',',']:
            bad=copy.deepcopy(u);bad[3]['translation']=first+'\n여동생 있어?'
            with self.assertRaisesRegex(ValueError,'nickname'):validate_nickname_suffix(bad,'661858',s)
        layout=validate_characters(translate_literal_scope(src,u,s),tbl,s,{x['id'] for x in u});yes=next(x for x in layout if x['id']=='661858:7:4');self.assertEqual(yes['choice_row_advance_pixels'],96);self.assertTrue(yes['choice_runtime_check_required'])
        bad=copy.deepcopy(u);bad[4]['translation']='가'*8+'  '
        with self.assertRaisesRegex(ValueError,'standalone choice row exceeds'):validate_characters(translate_literal_scope(src,bad,s),tbl,s,{x['id'] for x in bad})
    def test_unselected_leading_newline29_preserved_by_serialization(self):
        a=read(ROOT/'translations/roll_family_sister_ko.json');u=resolve_units(a);s=read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['661858'];src=(ROOT/'analysis/tpl_baseline/661858.tpl').read_text(encoding='utf-8-sig');target=translate_literal_scope(src,u,s);before=next(x for x in literals(src) if x.key=='661858:29:1');after=next(x for x in literals(target) if x.key==before.key)
        self.assertEqual(before.text,after.text);self.assertTrue(before.text.startswith('\n'));self.assertTrue(target[after.start:after.end].startswith('"\\n'));self.assertEqual(skeleton(src),skeleton(target))
        p=ROOT/'poc/work/roll_family_sister_v1_r2/661858';native=(p/'661858.msg').read_bytes();compiled=(p/'compiled/661858.msg').read_bytes();self.assertEqual(script_spans(native,97)[29],script_spans(compiled,97)[29]);self.assertEqual((p/'rebuilt.msg').read_bytes(),compiled)
        # Retain and identify the failed experiment; never bless its lost E8.
        failed=ROOT/'poc/work/roll_family_sister_v1/661858';self.assertNotEqual(script_spans((failed/'661858.msg').read_bytes(),97)[29],script_spans((failed/'compiled/661858.msg').read_bytes(),97)[29])
    def test_normal_eight_units_choice_branches_nickname_and_name_stop(self):
        r=main();self.assertTrue(r['passed']);self.assertFalse(r['release_eligible']);self.assertEqual(len(r['normal_runtime_units']),8);self.assertTrue(r['defaultYes_rightNo_leftYes']);self.assertTrue(r['name_question_stopped_before_input_init']);self.assertEqual(r['nickname_topic_suffix_pixels'],{'source':22,'translated':11});self.assertTrue(all(p['font_vram_screen_pixels_match'] and p['no_translated_ink_occluded'] and p['vacant_text_pixels_cleared']>0 for p in r['pages']));self.assertEqual(next(p['nickname'] for p in r['pages'] if p['nickname']),'ああくん')
    def test_current_rom_plugout_return_and_cumulative_regressions(self):
        import report_roll_plugout as plug
        import report_roll_return as ret
        for module,out in [(plug,'roll_family_sister_v1/plugout_regression'),(ret,'roll_family_sister_v1/return_regression')]:
            previous=module.STEM,module.PREFIX
            try:module.STEM,module.PREFIX=STEM,PREFIX;r=module.main(out)
            finally:module.STEM,module.PREFIX=previous
            self.assertTrue(r['passed']);self.assertEqual(r['translated_units'],974)
        from report_roll_intro import main as intro
        from report_roll_pet import main as pet
        from report_roll_fortune import main as fortune
        from report_attack_caption_runtime import main as caption
        reports=[intro(STEM,PREFIX+'roll-','roll_family_sister_v1/greeting_regression'),pet(STEM,PREFIX,'roll_family_sister_v1/pet_regression'),fortune(STEM,PREFIX,'roll_family_sister_v1',('sample-97','sample-211','sample-389')),caption(STEM,PREFIX+'rockman-','roll_family_sister_v1/rockman_regression'),caption(STEM,PREFIX+'roll-','roll_family_sister_v1/roll_caption',roll=True)]
        self.assertTrue(all(x['passed'] and x['rom_sha256']==r['rom_sha256'] for x in reports));self.assertEqual(reports[1]['translated_units'],974)

if __name__=='__main__':unittest.main()
