"""Read-only frequency ROM lookup and 128-byte event buffer write trace."""
import json,sys,struct
from pathlib import Path
import capture_roll_pet as pet
import capture_gutsman_calendar_management as parent
from build_visibility_poc import sha,require_hash
from archive_scripts import script_spans
PROBE=r'''
local frequencyReads={};local frequencyWrites={};local frequencyLookups={};local frequencyStages={};local frequencyTransfers={}
local function freqHex(address,size)
 local t={};for i=0,size-1 do t[#t+1]=string.format('%02x',emu.read(address+i,emu.memType.gbaMemory)) end;return table.concat(t)
end
local function freqState(address,value)
 local s=emu.getState()
 return string.format('{"frame":%d,"address":%d,"value":%d,"pc":%d,"lr":%d,"r0":%d,"r1":%d,"r2":%d,"r3":%d,"r4":%d,"r5":%d,"r6":%d,"r7":%d}',frame,address,value or 0,s['cpu.r15'],s['cpu.r14'],s['cpu.r0'],s['cpu.r1'],s['cpu.r2'],s['cpu.r3'],s['cpu.r4'],s['cpu.r5'],s['cpu.r6'],s['cpu.r7'])
end
emu.addMemoryCallback(function(address,value)
 if #frequencyReads>=4096 then error('frequency read bound') end
 frequencyReads[#frequencyReads+1]=freqState(address,value)
end,emu.callbackType.read,FREQUENCY_START,FREQUENCY_END-1)
emu.addMemoryCallback(function(address,value)
 if #frequencyWrites>=4096 then error('frequency write bound') end
 frequencyWrites[#frequencyWrites+1]=freqState(address,value)
end,emu.callbackType.write,0x02010C40,0x02010CBF)
emu.addMemoryCallback(function()
 local s=emu.getState();local id=s['cpu.r1']
 if s['cpu.r0']~=FREQUENCY_ROOT or id<119 or id>123 then return end
 frequencyLookups[#frequencyLookups+1]=freqState(s['cpu.r0'],id)
end,emu.callbackType.exec,0x08032AB6,0x08032AB6)
emu.addMemoryCallback(function()
 local s=emu.getState();if s['cpu.r0']<FREQUENCY_START or s['cpu.r0']>=FREQUENCY_END then return end
 frequencyStages[#frequencyStages+1]=string.format('{"frame":%d,"source":%d,"target":%d,"bytes":%d,"hex32":"%s"}',frame,s['cpu.r0'],s['cpu.r1'],s['cpu.r3']+1,freqHex(s['cpu.r1'],32))
end,emu.callbackType.exec,0x08032AD4,0x08032AD4)
emu.addMemoryCallback(function()
 local s=emu.getState();if s['cpu.r1']~=0x02010C40 then return end
 frequencyTransfers[#frequencyTransfers+1]=string.format('{"frame":%d,"source":%d,"target":%d,"bytes":%d,"lr":%d,"hex32":"%s"}',frame,s['cpu.r0'],s['cpu.r1'],s['cpu.r2'],s['cpu.r14'],freqHex(s['cpu.r0'],32))
end,emu.callbackType.exec,0x0800094C,0x0800094C)
local function dumpFrequency(name)
 write(name..'_frequency_copy.json','{"reads":['..table.concat(frequencyReads,',')..'],"writes":['..table.concat(frequencyWrites,',')..'],"lookups":['..table.concat(frequencyLookups,',')..'],"stages":['..table.concat(frequencyStages,',')..'],"transfers":['..table.concat(frequencyTransfers,',')..']}')
end
'''
def main():
    rp=Path(sys.argv[sys.argv.index('--rom')+1]);m=json.loads(rp.with_suffix('.json').read_text());require_hash(rp,m['output_sha256']);r=rp.read_bytes();a=next(a for a in m['archives']if a['archive']=='6368E8');p=r[a['rom_offset']:a['rom_offset']+a['compiled_bytes']];sp=script_spans(p,255)
    start=0x08000000+a['rom_offset']+struct.unpack_from('<H',p,119*2)[0];end=0x08000000+a['rom_offset']+struct.unpack_from('<H',p,123*2)[0]+len(sp[123])
    pet.PROBE=PROBE.replace('FREQUENCY_START',str(start)).replace('FREQUENCY_END',str(end)).replace('FREQUENCY_ROOT',str(0x08000000+a['rom_offset']))+pet.PROBE
    pet.PROBE=pet.PROBE.replace('local function dumpRollPet(name)','local function dumpRollPet(name)\n dumpFrequency(name)',1)
    rc=parent.main();out=Path(sys.argv[sys.argv.index('--out')+1]);env=out/'calendar_prompts_environment.json';e=json.loads(env.read_text());e.update(frequency_observer_sha256=sha(Path(__file__).read_bytes()),frequency_source_range=[start,end],frequency_write_range=[0x02010C40,0x02010CC0]);env.write_text(json.dumps(e,indent=2),encoding='utf8')
    result=json.loads((out/'result.json').read_text())
    if result['steps_captured']!=result['steps_expected']:raise ValueError('frequency observer incomplete captures; preserve failure')
    return rc
if __name__=='__main__':raise SystemExit(main())
