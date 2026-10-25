"""Read-only first-mail nickname/font observer on the actual cumulative ROM."""
import json, sys
from pathlib import Path
import capture_roll_pet as pet
from capture_roll_return import PROBE
from build_visibility_poc import ROOT, require_hash, sha

def main():
    def value(key): return sys.argv[sys.argv.index(key)+1]
    rp=Path(value('--rom')); m=json.loads(rp.with_suffix('.json').read_text(encoding='utf8'))
    require_hash(rp,m['output_sha256'])
    ar=next(a for a in m['archives'] if a['archive']=='65B220')
    pool=0x08000000+ar['rom_offset']; ef=m['extension']; font=0x08000000+ef['normal_font_offset']
    code=pet.PROBE+PROBE.replace('RETURN_POOL',str(pool))
    for k,v in [('PET_FONT_END',font+(ef['legacy_index_view']+11172+ef['extra_glyph_count'])*96),('PET_FONT',font),('PET_POOL',pool),('PET_END',pool+ar['compiled_bytes'])]: code=code.replace(k,str(v))
    code+='''
local nicknameEvents={}
local function readHex(address,size)
 local b={};for n=0,size-1 do b[#b+1]=string.format('%02x',emu.read(address+n,emu.memType.gbaMemory)) end
 return table.concat(b)
end
for _,pc in ipairs({0x08038F60,0x08038F82,0x080517D0,0x0805181A}) do
 emu.addMemoryCallback(function()
  local s=emu.getState()
  nicknameEvents[#nicknameEvents+1]=string.format('{"pc":%d,"frame":%d,"r4":%d,"r5":%d,"gender":%d,"owner":"%s","nickname":"%s"}',pc,frame,s['cpu.r4'],s['cpu.r5'],emu.read(0x02000952,emu.memType.gbaMemory),readHex(0x02000E50,14),readHex(0x02000E5F,21))
 end,emu.callbackType.exec,pc,pc)
end
local function dumpNickname(name)
 write(name..'_nickname_events.json','{"events":['..table.concat(nicknameEvents,',')..']}')
end
'''
    for anchor,replacement in [('local function capture(name)\n',code+'local function capture(name)\n dumpRollPet(name)\n dumpReturn(name)\n dumpNickname(name)\n'),('local function finish()\n',"local function finish()\n dumpNickname('final')\n")]:
        if pet.runner.LUA_TEMPLATE.count(anchor)!=1: raise ValueError('observer anchor')
        pet.runner.LUA_TEMPLATE=pet.runner.LUA_TEMPLATE.replace(anchor,replacement,1)
    rc=pet.runner.main(); out=Path(value('--out'))
    (out/'nickname_environment.json').write_text(json.dumps(dict(schema=1,observer_only=True,aliases=False,rom_sha256=m['output_sha256'],pool=pool,tool_sha256=sha(Path(__file__).read_bytes()),pet_probe_sha256=sha(Path(pet.__file__).read_bytes()),ram_probe_sha256=sha((ROOT/'tools/capture_roll_return.py').read_bytes())),indent=2)+'\n',encoding='utf8')
    return rc

if __name__=='__main__': raise SystemExit(main())
