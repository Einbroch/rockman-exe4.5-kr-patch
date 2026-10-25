"""Read-only stage/pool/canonical calendar name writer and lifetime observer.

Normal controller inputs / exact same-ROM checkpoint only. No RAM/script/save
injection, no keyboard hooks. Observe original paths before assigning ownership.
"""
import json,sys
from pathlib import Path
import run_mesen_segment as runner
from build_visibility_poc import ROOT,sha,require_hash

EXTRA=r'''
local nameAccess={};local nameEvents={};local nameWrites={}
local function nameHex(a,n)
 local t={};for i=0,n-1 do t[#t+1]=string.format('%02X',emu.read(a+i,emu.memType.gbaMemory)) end
 return table.concat(t)
end
local function nameWrite(a,v)
 if #nameWrites>=20000 then error('name writes overflow') end
 local s=emu.getState()
 nameWrites[#nameWrites+1]=string.format('{"frame":%d,"pc":%d,"address":%d,"before":%d,"value":%d,"lr":%d}',frame,s['cpu.pipeline.execute.address'],a,emu.read(a,emu.memType.gbaMemory),v,s['cpu.r14'])
end
emu.addMemoryCallback(nameWrite,emu.callbackType.write,0x02026280,0x02026295)
local function nameAccessAt(kind,a,v)
 local s=emu.getState();local pc=s['cpu.pipeline.execute.address'];local key=string.format('%s:%08X',kind,pc)
 local row=nameAccess[key]
 if row then row.hits=row.hits+1;row.min=math.min(row.min,a);row.max=math.max(row.max,a);row.last=frame
 else nameAccess[key]={kind=kind,pc=pc,hits=1,min=a,max=a,first=frame,last=frame,lr=s['cpu.r14']} end
end
emu.addMemoryCallback(function(a,v) nameAccessAt('read',a,v) end,emu.callbackType.read,0x02026280,0x02026295)
emu.addMemoryCallback(function(a,v) nameAccessAt('write',a,v) end,emu.callbackType.write,0x02026280,0x02026295)
for _,pc in ipairs({0x08032AC6,0x080355B6,0x0803558C,0x0803104E,0x08032F06,0x0803355A,0x08037366,0x0803737A,0x08037386}) do
 emu.addMemoryCallback(function()
  local s=emu.getState();local r0=s['cpu.r0'];local r1=s['cpu.r1']
  if pc==0x08032AC6 and not (r0>=0x02026080 and r0<0x02026296 or r1>=0x02026080 and r1<0x02026296) then return end
  if #nameEvents>=20000 then error('name events overflow') end
  local record=0;for i=0,3 do record=record+emu.read(0x02014DFC+i,emu.memType.gbaMemory)*2^(8*i) end
  local field='';if record>=0x020011F0 and record<0x020031D0 then field=nameHex(record,32) end
  nameEvents[#nameEvents+1]=string.format('{"frame":%d,"pc":%d,"r0":%d,"r1":%d,"r2":%d,"r3":%d,"r5":%d,"lr":%d,"record":%d,"record_hex":"%s","ui_hex":"%s","stage_hex":"%s","pool0_hex":"%s","pool1_hex":"%s","pool2_hex":"%s"}',frame,pc,r0,r1,s['cpu.r2'],s['cpu.r3'],s['cpu.r5'],s['cpu.r14'],record,field,nameHex(s['cpu.r5'],16),nameHex(0x02026280,22),nameHex(0x02026080,41),nameHex(0x02026100,41),nameHex(0x02026180,41))
 end,emu.callbackType.exec,pc,pc)
end
local function dumpNameLifetime(name)
 local rows={};for _,r in pairs(nameAccess) do rows[#rows+1]=string.format('{"kind":"%s","pc":%d,"hits":%d,"min":%d,"max":%d,"first":%d,"last":%d,"lr":%d}',r.kind,r.pc,r.hits,r.min,r.max,r.first,r.last,r.lr) end
 write(name..'_name_lifetime.json','{"observer_only":true,"accesses":['..table.concat(rows,',')..'],"stage_writes":['..table.concat(nameWrites,',')..'],"events":['..table.concat(nameEvents,',')..'],"stage_hex":"'..nameHex(0x02026280,22)..'","pool0_hex":"'..nameHex(0x02026080,41)..'"}')
end
'''

def main():
    def arg(k):return sys.argv[sys.argv.index(k)+1]
    rp=Path(arg('--rom'));require_hash(rp,arg('--expect-rom-sha256'));rom=rp.read_bytes()
    profile=json.loads((ROOT/'project.json').read_text())['source_profile'];source=ROOT/profile['filename'];require_hash(source,profile['sha256']);original=source.read_bytes()
    guards=[]
    for a,b in ((0x3100A,0x31068),(0x32EFE,0x32F26),(0x3354A,0x335AC),(0x3558C,0x355AE)):
        if original[a:b]!=rom[a:b]:raise ValueError('native route changed')
        guards.append(dict(offset=a,bytes=b-a,sha256=sha(original[a:b])))
    anchor='local function capture(name)\n'
    if runner.LUA_TEMPLATE.count(anchor)!=1:raise ValueError('observer anchor')
    runner.LUA_TEMPLATE=runner.LUA_TEMPLATE.replace(anchor,EXTRA+anchor+' dumpNameLifetime(name)\n',1)
    rc=runner.main();out=Path(arg('--out'))
    (out/'name_lifetime_environment.json').write_text(json.dumps(dict(observer_only=True,no_RAM_or_save_injection=True,
        tool_sha256=sha(Path(__file__).read_bytes()),runner_sha256=sha(Path(runner.__file__).read_bytes()),rom_sha256=sha(rom),native_code=guards,
        limits=['Stage22 selected-address CPU access only; absence cannot prove free RAM or complete lifetime.','Unchanged native keyboard/default paths only; no Hangul input hooks or save/reset/reload proof.']),indent=2),encoding='utf8')
    return rc


if __name__=='__main__':raise SystemExit(main())
