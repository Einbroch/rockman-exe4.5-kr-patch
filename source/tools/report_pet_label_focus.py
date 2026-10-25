"""Verify native menu focus cycling and graphics block against original ROM."""
import json,struct
from pathlib import Path
from build_visibility_poc import ROOT,sha,require_hash
from report_fixedcell_runtime import verify_route
from extract_pet_label_reference import ROWS

def main():
    route=ROOT/'poc/runtime/pet-labels-v1-focus'
    rom=ROOT/'poc/output/exe45_ko_development_roll_tactics_v1.gba'
    m=json.loads(rom.with_suffix('.json').read_text());require_hash(rom,m['output_sha256'])
    verify_route(route,m['output_sha256'],set())
    source=ROOT/json.loads((ROOT/'project.json').read_text())['source_profile']['filename'];require_hash(source,m['source_sha256'])
    native=source.read_bytes();block=native[0x6303B8:0x6315B8];samples=[]
    inventory=json.loads((ROOT/'analysis/pet_labels_v1/inventory.json').read_text())
    if rom.read_bytes()[0x6303B8:0x6315B8]!=block:raise ValueError('development graphics differ')
    for step in range(1,8):
        o=(route/f'step_{step:03}_gbaSpriteRam.bin').read_bytes()
        v=(route/f'step_{step:03}_gbaVideoRam.bin').read_bytes()
        rows=[]
        for row,unit in enumerate(inventory['units']):
            tile=unit['objects'][1]['tile'];found=[]
            for index in range(128):
                a,b,c=struct.unpack_from('<HHH',o,index*8)
                if a&0x2300 or a>>14!=1 or b>>14!=2:continue
                if c&1023==tile and c>>12 in (8,9) and a&255==16+row*12:
                    found.append({'id':ROWS[row][0],'oam_index':index,'left_obj_x':b&511,'y':a&255,'tile':tile,'palette':c>>12})
            if len(found)!=1:raise ValueError('unique native label OBJ required')
            rows.extend(found)
        focused=[r['id'] for r in rows if r['left_obj_x']==137 and r['palette']==8]
        expected=ROWS[step-1][0]
        passed=focused==[expected] and block==v[0x11000:0x12200]
        if not passed:raise ValueError(f'focus/source mismatch step {step}: {focused}')
        samples.append({'step':step,'focus':expected,'source_graphics_equal':True,'rows':rows,
            'screenshot_sha256':sha((route/f'step_{step:03}.png').read_bytes())})
    report={'policy':'development-draft; NON-DISTRIBUTION','rom_sha256':m['output_sha256'],
        'source_sha256':m['source_sha256'],'tool_sha256':sha(Path(__file__).read_bytes()),
        'receipt_sha256':sha((route/'result.json').read_bytes()),'passed':True,
        'scope':'Seven native PET menu focus states, controller input only from validated same-ROM cold chain; original Japanese OBJ graphics remain, no Korean image injection',
        'not_proven':['graphics loader instruction/source upload trace','full-game image inventory','Korean graphic native-size legibility','full-game playthrough','audio or hardware'],
        'source_block_sha256':sha(block),'samples':samples,'release_eligible':False}
    out=ROOT/'analysis/pet_labels_v1/focus_runtime.json';out.write_text(json.dumps(report,indent=2),encoding='utf-8');print(out)

if __name__=='__main__':main()
