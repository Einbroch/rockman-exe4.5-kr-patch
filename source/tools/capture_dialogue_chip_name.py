"""Native selector/copy read-only probe plus existing quarantined PET13 alias."""
import sys,json
from pathlib import Path
import capture_roll_chipquest as base
from build_visibility_poc import sha

def main():
    a=sys.argv;rp=Path(a[a.index('--rom')+1]);m=json.loads(rp.with_suffix('.json').read_text());h=m['dialogue_chip_name'];name=0x08000000+h['name_offset']
    code=f'''
local nameABI={{}};local nameCopies={{}}
local function nameRegisters(label)
 local s=emu.getState();local rows={{}};for i=0,14 do rows[#rows+1]=tostring(s['cpu.r'..i]) end
 nameABI[#nameABI+1]='{{"label":"'..label..'","frame":'..frame..',"regs":['..table.concat(rows,',')..']}}'
end
emu.addMemoryCallback(function() nameRegisters('entry') end,emu.callbackType.exec,0x0805162C,0x0805162C)
emu.addMemoryCallback(function() nameRegisters('continuation') end,emu.callbackType.exec,0x08051638,0x08051638)
emu.addMemoryCallback(function(address,value)
 local s=emu.getState()
 if s['cpu.pipeline.execute.address']~=0x0800094E then return end
 nameCopies[#nameCopies+1]=string.format('{{"address":%d,"value":%d,"source":%d,"destination":%d,"remaining":%d}}',address,value,s['cpu.r0'],s['cpu.r1'],s['cpu.r2'])
end,emu.callbackType.read,{name},{name+127})
local function dumpDialogueName(name)
 write(name..'_name_selector.json','{{"abi":['..table.concat(nameABI,',')..'],"copy_reads":['..table.concat(nameCopies,',')..']}}')
end
'''
    base.base.normal.pet.PROBE+=code;marker='local function capture(name)\n';runner=base.base.normal.pet.runner
    if runner.LUA_TEMPLATE.count(marker)!=1:raise ValueError('name selector capture anchor')
    runner.LUA_TEMPLATE=runner.LUA_TEMPLATE.replace(marker,marker+' dumpDialogueName(name)\n',1)
    rc=base.main();out=Path(a[a.index('--out')+1]);(out/'name_selector_environment.json').write_text(json.dumps({'rom_sha256':m['output_sha256'],'tool_sha256':sha(Path(__file__).read_bytes()),'base_wrapper_sha256':sha(Path(base.__file__).read_bytes()),'observer_only':True,'name_source':name},indent=2),encoding='utf-8');return rc

if __name__=='__main__':raise SystemExit(main())
