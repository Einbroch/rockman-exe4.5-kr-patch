import json,unittest
from copy import deepcopy
from build_visibility_poc import ROOT,sha
from equipment_weapons import merge,SCOPE,SCRIPTS
from tpl_literals import resolve_units
from archive_scripts import verify_untouched_scripts
from verify_tpi_index import lz77_decompress

def read(p):return json.loads(p.read_text(encoding='utf-8'))

class EquipmentWeaponsTests(unittest.TestCase):
    def setUp(self):
        self.base=read(ROOT/'translations/equipment_labels_ko.json');self.additional=read(ROOT/'translations/equipment_weapons_ko.json')
    def test_exact_scope_carry_and_abbreviation_guards(self):
        merged=merge(self.base,self.additional);units=resolve_units(merged)
        self.assertEqual(units[:4],resolve_units(self.base));self.assertEqual(len(units),37)
        self.assertEqual(SCOPE['literal_scripts'],list(range(1,38)));self.assertEqual(SCRIPTS,list(range(5,38)))
        for kind in ['population','source','abbreviation','release']:
            bad=deepcopy(self.additional)
            if kind=='population':bad['units'].pop()
            elif kind=='source':bad['source_sha256']='0'*64
            elif kind=='abbreviation':next(w for w in bad['wordings'] if w['id']=='weapon.kingdom_c')['translation']='킹덤'
            else:bad['review']['release_eligible']=True
            with self.assertRaises(ValueError):merge(self.base,bad)
    def test_integrated_clone_original_and_rebuild_identity(self):
        p=ROOT/'poc/output/exe45_ko_development_equipment_weapons_v1.gba';rom=p.read_bytes();m=read(p.with_suffix('.json'));h=m['folder_labels']['header']
        source=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes()
        self.assertEqual(sha(rom),m['output_sha256']);self.assertEqual(m['translated_units'],798)
        self.assertEqual(rom,(ROOT/'poc/output/exe45_ko_development_equipment_weapons_v1_repro.gba').read_bytes())
        clone=rom[h['rom_offset']:h['rom_offset']+h['compiled_bytes']]
        self.assertEqual(len(verify_untouched_scripts(lz77_decompress(source,0x6E2B9C)[0],clone,76,set(range(1,38)))),39)
        for a,b in [(0x6E2B9C,0x6E2B9C+634),(0x3C5BC,0x3C61C),(0xD389C,0xD3958)]:self.assertEqual(rom[a:b],source[a:b])
    def test_native_transition_pixels_and_full_static_population(self):
        from report_equipment_weapons_runtime import main
        r=main();self.assertTrue(r['passed']);self.assertFalse(r['release_eligible'])
        self.assertEqual(r['new_units'],33);self.assertEqual(len(r['finite_weapon_scope']),33)
        self.assertEqual(set(r['observed_scripts']),{3,4,5});self.assertEqual(r['observed_scripts'][-1],5)
        self.assertTrue(all(s['font_stage_vram_objects_pixels_match'] and s['trailing_cells_blank'] for s in r['normal_play_screens']))
        self.assertTrue(all(s['cells']<=9 and s['selector_navis'] for s in r['finite_weapon_scope']))

if __name__=='__main__':unittest.main()
