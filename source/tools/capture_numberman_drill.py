"""Read-only NumberMan calculation-drill observer, native or relocated."""
import json,sys
from pathlib import Path
import capture_roll_pet as pet
from build_visibility_poc import require_hash

def main():
    a=sys.argv;rp=Path(a[a.index('--rom')+1]);m=json.loads(rp.with_suffix('.json').read_text());require_hash(rp,m['output_sha256'])
    ar=next((x for x in m['archives'] if x['archive']=='715064'),None)
    pool=0x08000000+(ar['rom_offset'] if ar else 0x715064);end=pool+(ar['compiled_bytes'] if ar else 1207)
    ef=m['extension'];font=0x08000000+ef['normal_font_offset'];code=pet.PROBE
    for key,value in [('PET_FONT_END',font+(ef['legacy_index_view']+11172+ef['extra_glyph_count'])*96),('PET_FONT',font),('PET_POOL',pool),('PET_END',end)]:code=code.replace(key,str(value))
    marker='local function capture(name)\n'
    if pet.runner.LUA_TEMPLATE.count(marker)!=1:raise ValueError('drill capture anchor')
    pet.runner.LUA_TEMPLATE=pet.runner.LUA_TEMPLATE.replace(marker,code+marker+' dumpRollPet(name)\n',1)
    return pet.runner.main()

if __name__=='__main__':raise SystemExit(main())
