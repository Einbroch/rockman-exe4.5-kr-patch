"""Bound source-read and destination-residency evidence, without ROM edits."""
import json,struct
from pathlib import Path
from build_visibility_poc import ROOT,sha,require_hash
from report_fixedcell_runtime import verify_route

def main():
    route=ROOT/'poc/runtime/pet-graphics-load-v1';m=json.loads((ROOT/'poc/output/exe45_ko_development_roll_tactics_v1.json').read_text())
    verify_route(route,m['output_sha256'],set())
    source=ROOT/json.loads((ROOT/'project.json').read_text())['source_profile']['filename'];require_hash(source,m['source_sha256'])
    rom=source.read_bytes();trace=json.loads((route/'step_040_pet_source_reads.json').read_text());reads=trace['first_reads']
    if len(reads)!=160 or trace['total']<160:raise ValueError('source trace population')
    for i,r in enumerate(reads):
        if r['address']!=0x086303B8+i*4 or r['value']!=struct.unpack_from('<I',rom,r['address']-0x08000000)[0]:raise ValueError('observed source read identity')
        if r['pc']!=0xC18 or r['r0']!=0x086303B8+(i//8+1)*32 or r['r1']!=0x06011000+(i//8)*32:raise ValueError('BIOS copy source/destination progression')
    v=(route/'step_040_gbaVideoRam.bin').read_bytes()
    if v[0x11000:0x12200]!=rom[0x6303B8:0x6315B8]:raise ValueError('resident graphics')
    result={'policy':'development-draft; NON-DISTRIBUTION','rom_sha256':m['output_sha256'],'source_sha256':m['source_sha256'],
        'tool_sha256':sha(Path(__file__).read_bytes()),'observer_sha256':sha((ROOT/'tools/capture_pet_graphics_load.py').read_bytes()),
        'receipt_sha256':sha((route/'result.json').read_bytes()),'passed':True,'source':[0x086303B8,0x086315B8],
        'destination':[0x06011000,0x06012200],'first_read_frame':reads[0]['frame'],'observed_read_events':trace['total'],
        'retained_first_events':len(reads),'source_value_checks':True,'observed_bios_copy_pc':'0x00000C18',
        'observed_pointer_progression':'r0 post-load increment32, r1 pre-store group base, each8-word group; first160 reads640bytes consecutive',
        'full_block_residency_equal':True,'scope':'Existing758 ROM native PET source reads and resident OBJ block, same-ROM pre-menu checkpoint. New graphic candidate/whole-loader control-flow/native caller not proven.',
        'release_eligible':False}
    out=ROOT/'analysis/pet_labels_v1/load_runtime.json';out.write_text(json.dumps(result,indent=2),encoding='utf-8');print(out)

if __name__=='__main__':main()
