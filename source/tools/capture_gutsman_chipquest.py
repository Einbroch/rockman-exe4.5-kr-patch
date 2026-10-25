"""Guts13 read-alias renderer; native printChip ABI and copy128 read observations."""
import sys,json
from pathlib import Path
import capture_gutsman_pet_talk_diagnostic as base
import capture_roll_pet as pet
from build_visibility_poc import sha,require_hash

def main():
    a=sys.argv
    if int(a[a.index('--talk-script')+1])!=13:raise ValueError('Guts chip13 only')
    rp=Path(a[a.index('--rom')+1]);m=json.loads(rp.with_suffix('.json').read_text(encoding='utf8'));require_hash(rp,m['output_sha256']);h=m['dialogue_chip_name'];native=h['native_name_stream'];name=0x08000000+h['name_offset']
    code=f'''
local chipABI={{}};local chipCopies={{}}
local function chipRegisters(label)
 local s=emu.getState();local rows={{}};for i=0,14 do rows[#rows+1]=tostring(s['cpu.r'..i]) end
 chipABI[#chipABI+1]='{{"label":"'..label..'","frame":'..frame..',"regs":['..table.concat(rows,',')..']}}'
end
emu.addMemoryCallback(function() chipRegisters('entry') end,emu.callbackType.exec,0x0805162C,0x0805162C)
emu.addMemoryCallback(function() chipRegisters('continuation') end,emu.callbackType.exec,0x08051638,0x08051638)
local function chipRead(address,value)
 local s=emu.getState()
 if s['cpu.pipeline.execute.address']~=0x0800094E then return end
 chipCopies[#chipCopies+1]=string.format('{{"address":%d,"value":%d,"source":%d,"destination":%d,"remaining":%d}}',address,value,s['cpu.r0'],s['cpu.r1'],s['cpu.r2'])
end
emu.addMemoryCallback(chipRead,emu.callbackType.read,{native},{native+127})
emu.addMemoryCallback(chipRead,emu.callbackType.read,{name},{name+127})
local function dumpGutsChip(name)
 write(name..'_chip_selector.json','{{"abi":['..table.concat(chipABI,',')..'],"copy_reads":['..table.concat(chipCopies,',')..']}}')
end
'''
    pet.PROBE+=code;runner=pet.runner;anchor='local function capture(name)\n'
    if runner.LUA_TEMPLATE.count(anchor)!=1:raise ValueError('chip observer capture anchor')
    runner.LUA_TEMPLATE=runner.LUA_TEMPLATE.replace(anchor,anchor+' dumpGutsChip(name)\n',1)
    base.SCRIPTS=[13];rc=base.main();out=Path(a[a.index('--out')+1]);p=out/'talk_environment.json';env=json.loads(p.read_text(encoding='utf8'));env.update(chip_wrapper_sha256=sha(Path(__file__).read_bytes()),observer_only=True,native_name_stream=native,korean_name_stream=name)
    p.write_text(json.dumps(env,indent=2),encoding='utf8');return rc

if __name__=='__main__':raise SystemExit(main())
