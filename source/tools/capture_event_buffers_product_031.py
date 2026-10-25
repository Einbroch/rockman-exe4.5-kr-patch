"""Read-only actual030 calendar producers, string-copy residency and RAM draws."""
import sys
from pathlib import Path
import run_mesen_segment as runner
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read
from bench_event_buffers_product_031 import BASE,OUT as CPU

PROBE=r'''
local events={};local draws={};local fonts={}
local function word(a)
 local v=0;for i=0,3 do v=v+emu.read(a+i,emu.memType.gbaMemory)*2^(8*i) end;return v
end
local function hex(a,n)
 local t={};for i=0,n-1 do t[#t+1]=string.format('%02X',emu.read(a+i,emu.memType.gbaMemory)) end;return table.concat(t)
end
local function log(kind)
 if #events>=20000 then error('031 event log overflow') end
 local s=emu.getState();local record=word(0x02014DFC)
 local body='';if record>=0x02000000 and record+32<=0x02040000 then body=hex(record,32) end
 events[#events+1]=string.format('{"frame":%d,"kind":"%s","pc":%d,"r0":%d,"r1":%d,"r2":%d,"r3":%d,"r4":%d,"r5":%d,"lr":%d,"root":%d,"record":%d,"record_hex":"%s","buffer_hex":"%s"}',frame,kind,s['cpu.pipeline.execute.address'],s['cpu.r0'],s['cpu.r1'],s['cpu.r2'],s['cpu.r3'],s['cpu.r4'],s['cpu.r5'],s['cpu.r14'],word(0x0200FA50),record,body,hex(0x02014E54,32))
end
for _,v in ipairs({{0x08032AC6,'copy'},{0x08034122,'name-entry'},{0x08034130,'name-return'}}) do
 local pc,kind=v[1],v[2];emu.addMemoryCallback(function() log(kind) end,emu.callbackType.exec,pc,pc)
end
emu.addMemoryCallback(function()
 local s=emu.getState();local p=s['cpu.r4'];if emu.read(p+2,emu.memType.gbaMemory)==67 then log('F90C-entry') end
end,emu.callbackType.exec,0x080517D0,0x080517D0)
emu.addMemoryCallback(function()
 local s=emu.getState();local p=s['cpu.r4'];if ((p>=0x02000000 and p<0x02040000) or (p>=0x08000000 and p<0x0A000000)) and s['cpu.r5']==0x0200FA20 then
 draws[#draws+1]=string.format('{"frame":%d,"stream":%d,"glyph_index":%d,"offset":%d,"context":%d,"color":%d}',frame,p,s['cpu.r1'],s['cpu.r6'],s['cpu.r5'],emu.read(s['cpu.r5']+0x9c,emu.memType.gbaMemory)) end
end,emu.callbackType.exec,0x03006AE0,0x03006AE0)
emu.addMemoryCallback(function(a)
 local i=math.floor((a-EVENTFONT)/96);fonts[i]=(fonts[i] or 0)+1
end,emu.callbackType.read,EVENTFONT,EVENTFONTEND-1)
local function dumpEvents(name)
 local t={};for i,n in pairs(fonts) do t[#t+1]=string.format('{"index":%d,"reads":%d}',i,n) end
 write(name..'_event_buffers.json','{"events":['..table.concat(events,',')..'],"draws":['..table.concat(draws,',')..'],"font_reads":['..table.concat(t,',')..']}')
end
'''


def main():
    def value(k):return sys.argv[sys.argv.index(k)+1]
    rp=Path(value('--rom'));m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);cpu=read(CPU)
    if m['output_sha256']!=cpu['baseline_sha256'] or cpu['cases']!=3024 or not cpu['passed']:raise ValueError('031 exact event CPU baseline')
    for p,h in cpu['dependencies'].items():require_hash(ROOT/p,h)
    cfg=read('project.json');source=(ROOT/cfg['source_profile']['filename']).read_bytes();rom=rp.read_bytes()
    if sha(source)!=cpu['source_sha256']:raise ValueError('031 source identity')
    for r in cpu['native_ranges']:
        a,n=r['offset'],r['bytes']
        if sha(source[a:a+n])!=r['sha256'] or rom[a:a+n]!=source[a:a+n]:raise ValueError('031 event native range')
    font=0x08000000+m['extension']['normal_font_offset'];end=font+(m['extension']['legacy_index_view']+11172+m['extension']['extra_glyph_count'])*96
    code=PROBE.replace('EVENTFONTEND',str(end)).replace('EVENTFONT',str(font));anchor='local function capture(name)\n'
    if runner.LUA_TEMPLATE.count(anchor)!=1:raise ValueError('031 event capture anchor')
    runner.LUA_TEMPLATE=runner.LUA_TEMPLATE.replace(anchor,code+anchor+' dumpEvents(name)\n',1)
    return runner.main()


if __name__=='__main__':raise SystemExit(main())
