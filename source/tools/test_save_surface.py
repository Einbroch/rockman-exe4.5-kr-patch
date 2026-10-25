import unittest,copy
from report_roll_pet import ROOT,read
from tpl_literals import resolve_units,literals,skeleton
from build_development_patch import selected_scope,literal_scope,translate_literal_scope
from save_title_graphics import construct,decode,encode,BASE

class SaveSurfaceTests(unittest.TestCase):
    def test_prior36_units_and_only_count_suffix(self):
        a=read(ROOT/'translations/rockman_roll_save_surface_ko.json');u=resolve_units(a)
        self.assertEqual(u[:36],resolve_units(read(ROOT/'translations/rockman_roll_save_labels_ko.json')))
        self.assertEqual(u[-1],{'id':'6DA21C:16:1','source':'コ','translation':'개','state':'needs_review'})
        s=selected_scope(read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['6DA21C'],a)
        self.assertNotIn('6DA21C:16:0',s['literal_ids']);self.assertEqual(literal_scope(s,'6DA21C:16:1')['max_line_advance'],40)
    def test_icons_and_printbuffer_preserved(self):
        a=read(ROOT/'translations/rockman_roll_save_surface_ko.json');s=selected_scope(read(ROOT/'tools/specs/exe45_dialogue_archives_v1.json')['archives']['6DA21C'],a)
        source=(ROOT/'analysis/tpl_baseline/6DA21C.tpl').read_text(encoding='utf-8');target=translate_literal_scope(source,resolve_units(a),s)
        self.assertEqual(skeleton(source),skeleton(target));t={x.key:x.text for x in literals(target)};self.assertEqual(t['6DA21C:16:0'],'fg');self.assertEqual(t['6DA21C:16:1'],'개')
    def test_title_roundtrip_and_protected_pixels(self):
        source=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes();asset=read(ROOT/'translations/save_title_graphics_ko.json');block,meta=construct(source,asset)
        old=decode(source[BASE:BASE+256]);new=decode(block);self.assertEqual(encode(old),source[BASE:BASE+256]);self.assertTrue(meta['protected_pixels_equal']);self.assertNotEqual(old,new)
        self.assertTrue(all(old[y][x]==new[y][x] for y in range(8) for x in range(64) if not 21<=x<44))
        self.assertTrue(any(v==15 for r in new for v in r))
    def test_wrong_title_scope_rejected(self):
        source=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes();asset=read(ROOT/'translations/save_title_graphics_ko.json')
        for key,value in [('translation','보존'),('edit_rect',[0,0,64,8]),('bytes',255),('release_eligible',True)]:
            bad=copy.deepcopy(asset);bad[key]=value
            with self.assertRaises(ValueError):construct(source,bad)

if __name__=='__main__':unittest.main()
