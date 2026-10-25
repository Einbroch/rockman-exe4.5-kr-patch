"""Read-only normal B0 hint observer. No loader/scene/table/flag aliases."""
import json,sys
from pathlib import Path
import capture_roll_pet as pet
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read


def main():
    def value(k):return sys.argv[sys.argv.index(k)+1]
    rp=Path(value('--rom'));m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256'])
    r=next(x for x in m['keyitem_rom']['b0_hint_archives'] if x['archive']=='78BF28')
    pool=0x08000000+r['rom_offset'];ef=m['extension'];font=0x08000000+ef['normal_font_offset'];code=pet.PROBE
    for key,val in [('PET_FONT_END',font+(ef['legacy_index_view']+11172+ef['extra_glyph_count'])*96),('PET_FONT',font),('PET_POOL',pool),('PET_END',pool+r['compiled_bytes'])]:code=code.replace(key,str(val))
    w=m['keyitem_rom']['b0_hint_wrapper']['proof'];entry=w['address'];previous=w['literal_values']['previous']&~1
    code+=f'''
local b0Calls=0;local b0Entries=0;local b0Selections=0;local b0Start=nil;local b0Cycles={{}}
local function b0native()
 local bytes={{}}
 for j=0,{r['native_copy_bytes']-1} do
  local v=emu.read(0x0203D800+j,emu.memType.gbaMemory)
  if v~=emu.read({0x08000000+r['native_copy_offset']}+j,emu.memType.gbaMemory) then error('B0 native payload lifetime') end
  bytes[#bytes+1]=string.char(v)
 end
 return table.concat(bytes)
end
emu.addMemoryCallback(function()
 local s=emu.getState()
 if s['cpu.r0']~=0x0203D800 or s['cpu.r1']~=0 then error('B0 native L caller root/script') end
 b0Calls=b0Calls+1
end,emu.callbackType.exec,0x0804F802,0x0804F802)
emu.addMemoryCallback(function()
 local s=emu.getState()
 if s['cpu.r0']==0x0203D800 and s['cpu.r1']==0 and s['cpu.r14']==0x0804F807 then
  if emu.read(0x02004AD4,emu.memType.gbaMemory)~=0xB0 or emu.read(0x02004AD1,emu.memType.gbaMemory)~=0 then error('Normal initial B0/Navi0 context') end
  b0Entries=b0Entries+1;b0Start=s['cpu.cycleCount'];write('b0_native_'..b0Entries..'.bin',b0native())
 end
end,emu.callbackType.exec,{entry},{entry})
emu.addMemoryCallback(function()
 if b0Start~=nil then
  local s=emu.getState()
  if s['cpu.r0']~={pool} or s['cpu.r1']~=0 or s['cpu.r14']~=0x0804F807 then error('B0 selected clone/ABI') end
  b0Selections=b0Selections+1;b0Cycles[#b0Cycles+1]=s['cpu.cycleCount']-b0Start;b0Start=nil
 end
end,emu.callbackType.exec,{previous},{previous})
local function dumpB0(name)
 write(name..'_b0.json','{{"calls":'..b0Calls..',"entries":'..b0Entries..',"selections":'..b0Selections..',"root":{pool},"wrapper_cycles":['..table.concat(b0Cycles,',')..']}}')
end
'''
    for marker,replacement in [('local function capture(name)\n',code+'local function capture(name)\n dumpRollPet(name)\n dumpB0(name)\n'),('local function finish()\n',"local function finish()\n dumpB0('final')\n")]:
        if pet.runner.LUA_TEMPLATE.count(marker)!=1:raise ValueError('Natural B0 observer anchor')
        pet.runner.LUA_TEMPLATE=pet.runner.LUA_TEMPLATE.replace(marker,replacement,1)
    rc=pet.runner.main();out=Path(value('--out'));receipt=read(out/'result.json');d=read(out/'final_b0.json') if (out/'final_b0.json').exists() else {}
    passed=rc==0 and receipt['complete'] and d.get('calls')==d.get('entries')==d.get('selections')==2
    receipt.update(complete=passed,normal_play_checkpoint_eligible=True,observer_only=True,loader_scene_table_flag_aliases=False,natural_b0_hint=d,scope='Same-ROM ordinary Monday B0 field and normal L input. Read-only probes; no loader/scene/script table/progress/RAM substitution. Native source load and original script0/default10 execution, glyph font/OBJ/screen/wait/exit/reentry verification separate.')
    receipt['artifacts']={p.name:sha(p.read_bytes()) for p in out.iterdir() if p.is_file() and p.name!='result.json'}
    (out/'result.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('Natural B0 hint observer',passed,d);return 0 if passed else 1


if __name__=='__main__':raise SystemExit(main())
