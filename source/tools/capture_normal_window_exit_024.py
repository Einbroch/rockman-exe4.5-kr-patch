"""Observe transient native end before the original PET reopens, no writes."""
import sys
from pathlib import Path
from cumulative_batch500 import read
from build_visibility_poc import require_hash
import capture_normal_window_024 as normal


def main():
    rp=Path(sys.argv[sys.argv.index('--rom')+1]);m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256'])
    pool=0x08000000+next(r['rom_offset'] for r in m['archives'] if r['archive']=='71551C')
    code=f'''
local normalEndEntries={{}};local normalEndExits={{}}
local function normalRead32(a)
 local v=0;for j=0,3 do v=v+emu.read(a+j,emu.memType.gbaMemory)*2^(j*8) end;return v
end
emu.addMemoryCallback(function()
 local s=emu.getState()
 if s['cpu.r5']~=0x0200FA20 or normalRead32(0x0200FA50)~={pool} then return end
 normalEndEntries[#normalEndEntries+1]=string.format('{{"frame":%d,"stream":%d,"active":%d}}',frame,s['cpu.r4'],emu.read(0x0200FA20,emu.memType.gbaMemory))
end,emu.callbackType.exec,0x08050168,0x08050168)
emu.addMemoryCallback(function()
 local s=emu.getState()
 if s['cpu.r5']~=0x0200FA20 or normalRead32(0x0200FA50)~={pool} then return end
 normalEndExits[#normalEndExits+1]=string.format('{{"frame":%d,"stream":%d,"active":%d}}',frame,s['cpu.r4'],emu.read(0x0200FA20,emu.memType.gbaMemory))
end,emu.callbackType.exec,0x080501BC,0x080501BC)
local function dumpNormalEnd(name)
 write(name..'_normal_end.json','{{"entries":['..table.concat(normalEndEntries,',')..'],"exits":['..table.concat(normalEndExits,',')..']}}')
end
'''
    runner=normal.capture.pet.runner
    anchor='local function capture(name)\n'
    if runner.LUA_TEMPLATE.count(anchor)!=1:raise ValueError('Normal end observer anchor')
    runner.LUA_TEMPLATE=runner.LUA_TEMPLATE.replace(anchor,code+anchor+' dumpNormalEnd(name)\n',1)
    return normal.capture.main()


if __name__=='__main__':raise SystemExit(main())
