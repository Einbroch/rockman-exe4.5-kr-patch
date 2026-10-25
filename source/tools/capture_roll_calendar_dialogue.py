"""Read-only calendar dialogue + fixed-cell observers; no state injection."""
import json,sys
from pathlib import Path
import capture_fixedcell_probe as fixed
import capture_roll_pet as pet
from build_visibility_poc import sha,require_hash
def main():
    rp=Path(sys.argv[sys.argv.index('--rom')+1]);m=json.loads(rp.with_suffix('.json').read_text());require_hash(rp,m['output_sha256']);ar=next(a for a in m['archives'] if a['archive']=='65F11C');pool=0x08000000+ar['rom_offset'];ef=m['extension'];font=0x08000000+ef['normal_font_offset'];code=pet.PROBE
    for k,v in [('PET_FONT_END',font+(ef['legacy_index_view']+11172+ef['extra_glyph_count'])*96),('PET_FONT',font),('PET_POOL',pool),('PET_END',pool+ar['compiled_bytes'])]:code=code.replace(k,str(v))
    marker='local function capture(name)\n'
    if fixed.runner.LUA_TEMPLATE.count(marker)!=1:raise ValueError('calendar observer anchor')
    fixed.runner.LUA_TEMPLATE=fixed.runner.LUA_TEMPLATE.replace(marker,code+marker+' dumpRollPet(name)\n',1)
    rc=fixed.main();out=Path(sys.argv[sys.argv.index('--out')+1]);(out/'calendar_dialogue_environment.json').write_text(json.dumps({'rom_sha256':m['output_sha256'],'observer_only':True,'pool':pool,'tool_sha256':sha(Path(__file__).read_bytes()),'pet_probe_sha256':sha(Path(pet.__file__).read_bytes()),'fixed_probe_sha256':sha(Path(fixed.__file__).read_bytes())},indent=2),encoding='utf-8');return rc
if __name__=='__main__':raise SystemExit(main())
