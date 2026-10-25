"""Read-only source preset reads and transient name-buffer writes; no aliases."""
import json,sys
from pathlib import Path
import capture_roll_schedule_native as native
from build_visibility_poc import sha

def main():
    marker='local function capture(name)\n'
    code=r'''
local presetRows={}
local function observePreset(address,value,kind)
 local s=emu.getState()
 if #presetRows>=20000 then error('preset observer overflow') end
 presetRows[#presetRows+1]=string.format('{"frame":%d,"kind":"%s","address":%d,"value":%d,"pc":%d,"r0":%d,"r1":%d,"r2":%d,"r3":%d,"lr":%d}',frame,kind,address,value or 0,s['cpu.r15'],s['cpu.r0'],s['cpu.r1'],s['cpu.r2'],s['cpu.r3'],s['cpu.r14'])
end
emu.addMemoryCallback(function(a,v) observePreset(a,v,'source-read') end,emu.callbackType.read,0x08636da1,0x08636da4)
emu.addMemoryCallback(function(a,v) observePreset(a,v,'name-write') end,emu.callbackType.write,0x02010c40,0x02010cbf)
local function dumpPreset(name)
 write(name..'_preset_source.json','{"observer_only":true,"events":['..table.concat(presetRows,',')..']}')
end
'''
    runner=native.pet.runner
    if runner.LUA_TEMPLATE.count(marker)!=1:raise ValueError('source observer anchor')
    runner.LUA_TEMPLATE=runner.LUA_TEMPLATE.replace(marker,code+marker+' dumpPreset(name)\n',1)
    rc=native.main()
    out=Path(sys.argv[sys.argv.index('--out')+1])
    (out/'preset_source_environment.json').write_text(json.dumps({'observer_only':True,'self_sha256':sha(Path(__file__).read_bytes()),'native_probe_sha256':sha(Path(native.__file__).read_bytes()),'pet_probe_sha256':sha(Path(native.pet.__file__).read_bytes()),'source_range':[0x08636da1,0x08636da4],'ram_write_range':[0x02010c40,0x02010cbf]},indent=2),encoding='utf-8')
    return rc

if __name__=='__main__':raise SystemExit(main())
