"""Read-only native RAM variable glyph/parser observations on PET alarm aliases."""
import json,sys,struct
from pathlib import Path
import capture_gutsman_schedule_alarm as base
import capture_roll_pet as pet
from capture_roll_return import PROBE
from build_visibility_poc import ROOT,sha,require_hash
def main():
    rp=Path(sys.argv[sys.argv.index('--rom')+1]);m=json.loads(rp.with_suffix('.json').read_text());require_hash(rp,m['output_sha256']);rom=rp.read_bytes()
    source=ROOT/json.loads((ROOT/'project.json').read_text())['source_profile']['filename'];require_hash(source,m['source_sha256']);native=source.read_bytes()
    if native[0x4f88a:0x4f88c]!=bytes.fromhex('2178') or rom[0x4f88a:0x4f88c]!=native[0x4f88a:0x4f88c]:raise ValueError('native parser byte-read boundary')
    pool=0x08000000+next(a['rom_offset'] for a in m['archives'] if a['archive']=='66651C')
    code=PROBE.replace('RETURN_POOL',str(pool))+f'''
local variableReads={{}}
emu.addMemoryCallback(function()
 local s=emu.getState();local ctx=s['cpu.r5'];local stream=s['cpu.r4']
 if ctx~=0x0200FA20 or stream<0x02000000 or stream>=0x02040000 then return end
 local root=0;for i=0,3 do root=root+emu.read(ctx+0x30+i,emu.memType.gbaMemory)*2^(8*i) end
 if root~={pool} then return end
 variableReads[#variableReads+1]=string.format('{{"frame":%d,"stream":%d,"byte":%d,"context":%d}}',frame,stream,emu.read(stream,emu.memType.gbaMemory),ctx)
end,emu.callbackType.exec,0x0804F88A,0x0804F88A)
local function dumpVariableReads(name)
 write(name..'_variable_reads.json','{{"reads":['..table.concat(variableReads,',')..']}}')
end
'''
    marker='local function capture(name)\n'
    if pet.runner.LUA_TEMPLATE.count(marker)!=1:raise ValueError('RAM observer capture anchor')
    pet.runner.LUA_TEMPLATE=pet.runner.LUA_TEMPLATE.replace(marker,code+marker+' dumpReturn(name)\n dumpVariableReads(name)\n',1)
    rc=base.main(scripts=(1,2,3,4,5,6),relocated_talk=True)
    p=Path(sys.argv[sys.argv.index('--out')+1])/'alarm_environment.json';env=json.loads(p.read_text())
    env.update(wrapper_sha256=sha(Path(__file__).read_bytes()),ram_probe_sha256=sha((ROOT/'tools/capture_roll_return.py').read_bytes()),parser_guard=dict(start=0x4f88a,end=0x4f88c,sha256=sha(native[0x4f88a:0x4f88c])))
    p.write_text(json.dumps(env,indent=2),encoding='utf8');return rc
if __name__=='__main__':raise SystemExit(main())
