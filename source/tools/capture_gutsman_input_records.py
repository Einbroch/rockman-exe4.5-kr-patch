"""Read-only native input/answer RAM observation; no alias or forced record."""
import json,sys
from pathlib import Path
import capture_roll_family as base
from build_visibility_poc import ROOT,sha,require_hash

def main():
    def arg(key):return sys.argv[sys.argv.index(key)+1]
    rp=Path(arg('--rom'));m=json.loads(rp.with_suffix('.json').read_text());require_hash(rp,m['output_sha256']);rom=rp.read_bytes()
    sp=ROOT/json.loads((ROOT/'project.json').read_text())['source_profile']['filename'];require_hash(sp,m['source_sha256']);source=sp.read_bytes();guards=[]
    for a,b in [(0x94c,0x956),(0x517d0,0x5181c),(0x5181c,0x51820),(0x518f8,0x518fc),(0x527b0,0x527c8)]:
        if source[a:b]!=rom[a:b]:raise ValueError('native input-buffer consumer changed')
        guards.append(dict(start=a,end=b,sha256=sha(source[a:b])))
    code=r'''
local answerWrites={};local answerCopies={};local answerCommands={}
local function answerHex(a,n)
 local b={};for i=0,n-1 do b[#b+1]=string.format('%02x',emu.read(a+i,emu.memType.gbaMemory)) end;return table.concat(b)
end
local function answerRoot()
 local n=0;for i=0,3 do n=n+emu.read(0x0200FA50+i,emu.memType.gbaMemory)*2^(8*i) end;return n
end
emu.addMemoryCallback(function(a,v)
 if #answerWrites>=50000 then error('answer record write observation overflow') end
 local s=emu.getState();answerWrites[#answerWrites+1]=string.format('{"frame":%d,"address":%d,"value":%d,"pc":%d,"r0":%d,"r1":%d,"r2":%d,"r3":%d,"root":%d,"script":%d}',frame,a,v,s['cpu.pipeline.execute.address'],s['cpu.r0'],s['cpu.r1'],s['cpu.r2'],s['cpu.r3'],answerRoot(),emu.read(0x0200FA21,emu.memType.gbaMemory))
end,emu.callbackType.write,0x02026080,0x0202637f)
emu.addMemoryCallback(function()
 local s=emu.getState();if s['cpu.r2']~=512 or s['cpu.r0']<0x02026080 or s['cpu.r0']>0x02026180 then return end
 answerCopies[#answerCopies+1]=string.format('{"frame":%d,"source":%d,"destination":%d,"bytes":%d,"lr":%d,"script":%d}',frame,s['cpu.r0'],s['cpu.r1'],s['cpu.r2'],s['cpu.r14'],emu.read(0x0200FA21,emu.memType.gbaMemory))
end,emu.callbackType.exec,0x0800094C,0x0800094C)
emu.addMemoryCallback(function()
 local s=emu.getState();if s['cpu.r5']~=0x0200FA20 then return end
 local index=emu.read(s['cpu.r4']+2,emu.memType.gbaMemory)
 if index<28 or index>30 then return end
 answerCommands[#answerCommands+1]=string.format('{"frame":%d,"stream":%d,"index":%d,"root":%d,"script":%d}',frame,s['cpu.r4'],index,answerRoot(),emu.read(0x0200FA21,emu.memType.gbaMemory))
end,emu.callbackType.exec,0x080517D0,0x080517D0)
local function dumpAnswerRecords(name)
 write(name..'_answer_records.json','{"writes":['..table.concat(answerWrites,',')..'],"copies":['..table.concat(answerCopies,',')..'],"commands":['..table.concat(answerCommands,',')..'],"record_region_hex":"'..answerHex(0x02026080,768)..'","display_output_hex":"'..answerHex(0x02010AC0,512)..'"}')
end
'''
    anchor='local function capture(name)\n'
    if base.pet.runner.LUA_TEMPLATE.count(anchor)!=1:raise ValueError('answer record capture anchor')
    base.pet.runner.LUA_TEMPLATE=base.pet.runner.LUA_TEMPLATE.replace(anchor,code+anchor+' dumpAnswerRecords(name)\n',1);base.ARCHIVE='667044'
    rc=base.main();out=Path(arg('--out'))
    (out/'answer_records_environment.json').write_text(json.dumps(dict(observer_only=True,no_aliases=True,no_external_RAM_writes=True,rom_sha256=m['output_sha256'],self_sha256=sha(Path(__file__).read_bytes()),family_observer_sha256=sha(Path(base.__file__).read_bytes()),probe_sha256=sha(Path(base.pet.__file__).read_bytes()),native_guards=guards,watched_write_range=[0x02026080,0x0202637f],limits=['Watched addresses originate from static printStringBuffer descriptors. No claim of complete input-buffer/writer population.','Absence of writes is not proof of no commit or no save. Editing fields may live elsewhere.','Only sourceBuffer descriptors consumer/copy calls are observed; storage and persistence need separate native traces.']),indent=2),encoding='utf8');return rc

if __name__=='__main__':raise SystemExit(main())
