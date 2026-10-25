"""Read-only native Roll mail-arrival pool, nickname and font observer."""
import json,sys
from pathlib import Path
import capture_roll_pet as pet
from capture_roll_return import PROBE
from build_visibility_poc import ROOT,sha,require_hash

def main():
    rp=Path(sys.argv[sys.argv.index('--rom')+1]);m=json.loads(rp.with_suffix('.json').read_text());require_hash(rp,m['output_sha256'])
    ar=next((a for a in m['archives'] if a['archive']=='661060'),None);pool=0x08000000+(ar['rom_offset'] if ar else 0x661060);size=ar['compiled_bytes'] if ar else 1351
    ef=m['extension'];font=0x08000000+ef['normal_font_offset'];code=pet.PROBE+PROBE.replace('RETURN_POOL',str(pool)).replace('dumpReturn','dumpMail').replace('_return_ram.json','_talk_ram.json')
    for key,value in [('PET_FONT_END',font+(ef['legacy_index_view']+11172+ef['extra_glyph_count'])*96),('PET_FONT',font),('PET_POOL',pool),('PET_END',pool+size)]:code=code.replace(key,str(value))
    marker='local function capture(name)\n'
    if pet.runner.LUA_TEMPLATE.count(marker)!=1:raise ValueError('mail arrival capture anchor')
    pet.runner.LUA_TEMPLATE=pet.runner.LUA_TEMPLATE.replace(marker,code+marker+' dumpRollPet(name)\n dumpMail(name)\n',1)
    rc=pet.runner.main();out=Path(sys.argv[sys.argv.index('--out')+1])
    (out/'mail_environment.json').write_text(json.dumps({'rom_sha256':m['output_sha256'],'observer_only':True,'tool_sha256':sha(Path(__file__).read_bytes()),'probe_sha256':sha(Path(pet.__file__).read_bytes()),'nickname_probe_sha256':sha((ROOT/'tools/capture_roll_return.py').read_bytes()),'pool':pool,'size':size},indent=2),encoding='utf-8');return rc

if __name__=='__main__':raise SystemExit(main())
