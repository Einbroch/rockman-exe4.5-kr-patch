"""Read-only source/relocated frequency strings plus fixed-cell observations."""
import json,sys,struct
from pathlib import Path
import capture_fixedcell_probe as fixed
from build_visibility_poc import ROOT,sha,require_hash
from archive_scripts import script_spans
def main():
    rp=Path(fixed.value('--rom'));m=json.loads(rp.with_suffix('.json').read_text());require_hash(rp,m['output_sha256']);rom=rp.read_bytes();source=(ROOT/json.loads((ROOT/'project.json').read_text())['source_profile']['filename']).read_bytes();ar=next(a for a in m['archives'] if a['archive']=='6368E8');payload=rom[ar['rom_offset']:ar['rom_offset']+ar['compiled_bytes']];ranges=[]
    for kind,data,base in [('source',source[0x6368E8:0x6368E8+2337],0x086368E8),('relocated',payload,0x08000000+ar['rom_offset'])]:
        spans=script_spans(data,255)
        for script in range(119,124):
            start=base+struct.unpack_from('<H',data,script*2)[0];ranges.append({'kind':kind,'script':script,'start':start,'end':start+len(spans[script])-1})
    code=r'''
local freqRows={}
local function observeFreq(a,v,kind,script)
 local s=emu.getState()
 if #freqRows>=10000 then error('frequency observer overflow') end
 freqRows[#freqRows+1]=string.format('{"frame":%d,"kind":"%s","script":%d,"address":%d,"value":%d,"pc":%d,"r0":%d,"r1":%d,"r2":%d,"r3":%d,"lr":%d}',frame,kind,script,a,v or 0,s['cpu.r15'],s['cpu.r0'],s['cpu.r1'],s['cpu.r2'],s['cpu.r3'],s['cpu.r14'])
end
local function dumpFreq(name)
 write(name..'_frequency_reads.json','{"observer_only":true,"events":['..table.concat(freqRows,',')..']}')
end
'''
    for r in ranges:code+=f"\nemu.addMemoryCallback(function(a,v) observeFreq(a,v,'{r['kind']}',{r['script']}) end,emu.callbackType.read,{r['start']},{r['end']})\n"
    marker='local function capture(name)\n'
    if fixed.runner.LUA_TEMPLATE.count(marker)!=1:raise ValueError('frequency observer anchor')
    fixed.runner.LUA_TEMPLATE=fixed.runner.LUA_TEMPLATE.replace(marker,code+marker+' dumpFreq(name)\n',1);rc=fixed.main();out=Path(fixed.value('--out'));(out/'frequency_environment.json').write_text(json.dumps({'observer_only':True,'rom_sha256':m['output_sha256'],'ranges':ranges,'self_sha256':sha(Path(__file__).read_bytes()),'fixed_probe_sha256':sha(Path(fixed.__file__).read_bytes())},indent=2),encoding='utf-8');return rc
if __name__=='__main__':raise SystemExit(main())
