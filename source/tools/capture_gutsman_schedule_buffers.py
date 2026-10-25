"""Native GutsMan L-query RAM producer/consumer observation; no aliases or writes."""
import json,sys
from pathlib import Path
import capture_roll_pet as pet
from build_visibility_poc import ROOT,require_hash,sha

def main():
    rp=Path(sys.argv[sys.argv.index('--rom')+1]);m=json.loads(rp.with_suffix('.json').read_text());require_hash(rp,m['output_sha256'])
    rom=rp.read_bytes();cfg=json.loads((ROOT/'project.json').read_text());source=ROOT/cfg['source_profile']['filename'];require_hash(source,m['source_sha256']);native=source.read_bytes()
    guards=[]
    for a,b in [(0x4f88a,0x4f88c),(0x4f7b6,0x4f7d0),(0x4fb4c,0x4fc20)]:
        if rom[a:b]!=native[a:b]:raise ValueError('native schedule consumer changed')
        guards.append(dict(start=a,end=b,sha256=sha(native[a:b])))
    ar=next(a for a in m['archives'] if a['archive']=='666F38');pool=0x08000000+ar['rom_offset']
    code=f'''
local bufferReads={{}};local bufferWrites={{}};local variableDraws={{}}
local function currentRoot()
 local v=0;for i=0,3 do v=v+emu.read(0x0200FA50+i,emu.memType.gbaMemory)*2^(8*i) end;return v
end
emu.addMemoryCallback(function(a,v)
 local s=emu.getState()
 if #bufferWrites>=10000 then error('buffer write overflow') end
 bufferWrites[#bufferWrites+1]=string.format('{{"frame":%d,"address":%d,"value":%d,"pc":%d,"root":%d}}',frame,a,v,s['cpu.pipeline.execute.address'],currentRoot())
end,emu.callbackType.write,0x02010AC0,0x02010AE0)
emu.addMemoryCallback(function()
 local s=emu.getState();local stream=s['cpu.r4'];if s['cpu.r5']~=0x0200FA20 or stream<0x02000000 or stream>=0x02040000 or currentRoot()~={pool} then return end
 if #bufferReads>=10000 then error('buffer read overflow') end
 bufferReads[#bufferReads+1]=string.format('{{"frame":%d,"stream":%d,"byte":%d}}',frame,stream,emu.read(stream,emu.memType.gbaMemory))
end,emu.callbackType.exec,0x0804F88A,0x0804F88A)
emu.addMemoryCallback(function()
 local s=emu.getState();local stream=s['cpu.r4'];if s['cpu.r5']~=0x0200FA20 or stream<0x02000000 or stream>=0x02040000 or currentRoot()~={pool} then return end
 variableDraws[#variableDraws+1]=string.format('{{"frame":%d,"stream":%d,"byte":%d,"glyph_index":%d,"offset":%d}}',frame,stream,emu.read(stream,emu.memType.gbaMemory),s['cpu.r1'],s['cpu.r6'])
end,emu.callbackType.exec,0x03006AE0,0x03006AE0)
local function dumpScheduleBuffers(name)
 write(name..'_schedule_buffers.json','{{"reads":['..table.concat(bufferReads,',')..'],"writes":['..table.concat(bufferWrites,',')..'],"draws":['..table.concat(variableDraws,',')..']}}')
end
'''
    anchor='local function capture(name)\n'
    if pet.runner.LUA_TEMPLATE.count(anchor)!=1:raise ValueError('buffer capture anchor')
    pet.runner.LUA_TEMPLATE=pet.runner.LUA_TEMPLATE.replace(anchor,code+anchor+' dumpScheduleBuffers(name)\n',1);pet.ARCHIVE='666F38'
    rc=pet.main();out=Path(sys.argv[sys.argv.index('--out')+1])
    (out/'schedule_buffers_environment.json').write_text(json.dumps(dict(observer_only=True,no_aliases=True,rom_sha256=m['output_sha256'],pool=pool,self_sha256=sha(Path(__file__).read_bytes()),pet_probe_sha256=sha(Path(pet.__file__).read_bytes()),native_guards=guards),indent=2),encoding='utf8');return rc

if __name__=='__main__':raise SystemExit(main())
