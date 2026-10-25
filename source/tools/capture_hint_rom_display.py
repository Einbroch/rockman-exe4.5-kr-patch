"""Quarantined native-loader/reader/display diagnostic; no event-selection claim."""
import json,struct,sys
from pathlib import Path
import capture_roll_pet as pet
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read
from archive_scripts import script_spans
from keyitem_rom_data import verify_final

def main():
    def value(k):return sys.argv[sys.argv.index(k)+1]
    script=int(value('--hint-script'));i=sys.argv.index('--hint-script');del sys.argv[i:i+2]
    if script not in (0,11,15):raise ValueError('Declared representative hint script or original dispatcher only')
    rp=Path(value('--rom'));m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes()
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes();meta=m['keyitem_rom'];verify_final(source,rom,meta)
    ar=next(r for r in meta['hint_archives'] if r['archive']=='786D38')
    if ar['navi_index']!=0:raise ValueError('Source MegaMan hint identity')
    pool=0x08000000+ar['rom_offset'];payload=rom[ar['rom_offset']:ar['rom_offset']+ar['compiled_bytes']]
    original=0x08000000+int(ar['archive'],16);pointer=0x08054238;old=struct.unpack_from('<I',source,pointer-0x08000000)[0]
    if struct.unpack_from('<I',source,0x53FA0+(0xB0-0x80)*4)[0]!=pointer:raise ValueError('Source B0 scene table')
    if old!=0x0878BF28 or rom[pointer-0x08000000:pointer-0x08000000+4]!=struct.pack('<I',old):raise ValueError('Own Monday field slot/source unchanged')
    if script:
        if not script_spans(payload,255)[script].startswith(bytes.fromhex('f40017e700')):raise ValueError('Original MegaMan/msgOpen entry')
    else:
        native=rom[ar['native_copy_offset']:ar['native_copy_offset']+ar['native_copy_bytes']]
        if script_spans(payload,255)[0]!=script_spans(native,255)[0]:raise ValueError('Original dispatcher must be byte-identical')
    ins=meta['hint_wrapper']['proof']['instructions'];scene=[r['address'] for r in ins if r['mnemonic']=='ldrb' and r['operands']=='r3, [r2, #4]']
    if len(scene)!=1:raise ValueError('Exact scene read instruction')
    initial,target=[struct.unpack_from('<H',payload,s*2)[0] for s in (0,script)]
    wrapper=meta['hint_wrapper']['proof']['address'];previous=meta['hint_wrapper']['proof']['literal_values']['previous']&~1
    ef=m['extension'];font=0x08000000+ef['normal_font_offset'];code=pet.PROBE
    for k,v in [('PET_FONT_END',font+(ef['legacy_index_view']+11172+ef['extra_glyph_count'])*96),('PET_FONT',font),('PET_POOL',pool),('PET_END',pool+len(payload))]:code=code.replace(k,str(v))
    code+=f'''
local loads=0;local scenes=0;local entries=0;local hintCalls=0
local cycleStart=nil;local wrapperCycles={{}}
emu.addMemoryCallback(function()
 local s=emu.getState()
 if s['cpu.r0']==0x0203D800 and s['cpu.r1']==0 and s['cpu.r14']==0x0804F807 then
  if cycleStart~=nil then error('Nested hint timing') end
  cycleStart=s['cpu.cycleCount']
 end
end,emu.callbackType.exec,{wrapper},{wrapper})
emu.addMemoryCallback(function()
 if cycleStart~=nil then
  local s=emu.getState();if s['cpu.r0']~={pool} or s['cpu.r1']~=0 or s['cpu.r14']~=0x0804F807 then error('Hint wrapper timing continuation') end
  wrapperCycles[#wrapperCycles+1]=s['cpu.cycleCount']-cycleStart;cycleStart=nil
 end
end,emu.callbackType.exec,{previous},{previous})
local function rd32(a)
 local n=0;for j=0,3 do n=n+emu.read(a+j,emu.memType.gbaMemory)*2^(j*8) end;return n
end
emu.addMemoryCallback(function(address,value)
 local s=emu.getState()
 if address=={pointer} and value=={old} and s['cpu.pipeline.execute.address']==0x0804F740 and s['cpu.r0']=={pointer} and s['cpu.r4']==0 then
  if loads~=0 then error('Unexpected repeated field load') end
  loads=loads+1;return {original}
 end
end,emu.callbackType.read,{pointer},{pointer+3})
emu.addMemoryCallback(function(address,value)
 local s=emu.getState()
 if s['cpu.pipeline.execute.address']=={scene[0]} and s['cpu.r0']==0x0203D800 and s['cpu.r1']==0 then
  if loads~=1 or value~=0xB0 or s['cpu.r2']~=0x02004AD0 or emu.read(s['cpu.r2']+1,emu.memType.gbaMemory)~=0 then error('Own field scene/Navi prerequisite') end
  if address~=s['cpu.r2']+4 then error('Scene read address') end
  local b={{}};for j=0,{ar['native_copy_bytes']-1} do
   local v=emu.read(0x0203D800+j,emu.memType.gbaMemory)
   if v~=emu.read({0x08000000+ar['native_copy_offset']}+j,emu.memType.gbaMemory) then error('Native payload identity/lifetime') end
   b[#b+1]=string.char(v)
  end
  scenes=scenes+1;write('hint_native_'..scenes..'.bin',table.concat(b));return 0xA3
 end
end,emu.callbackType.read,0x02004AD4,0x02004AD4)
emu.addMemoryCallback(function(address,value)
 local s=emu.getState()
 if address=={pool} and value=={initial} and s['cpu.pipeline.execute.address']==0x0804FB76 and s['cpu.r0']=={pool} and s['cpu.r1']==0 and s['cpu.r5']==0x0200FA20 then entries=entries+1;return {target} end
end,emu.callbackType.read,{pool},{pool+1})
emu.addMemoryCallback(function()
 local s=emu.getState();if s['cpu.r0']~=0x0203D800 or s['cpu.r1']~=0 then error('Native hint call ABI') end
 hintCalls=hintCalls+1
end,emu.callbackType.exec,0x0804F802,0x0804F802)
local function dumpHint(name)
 write(name..'_hint_alias.json','{{"loads":'..loads..',"scenes":'..scenes..',"entries":'..entries..',"calls":'..hintCalls..',"root":{pool},"script":{script},"wrapper_cycles":['..table.concat(wrapperCycles,',')..']}}')
end
'''
    for anchor,new in [('local function capture(name)\n',code+'local function capture(name)\n dumpRollPet(name)\n dumpHint(name)\n'),('local function finish()\n',"local function finish()\n dumpHint('final')\n")]:
        if pet.runner.LUA_TEMPLATE.count(anchor)!=1:raise ValueError('Capture anchor')
        pet.runner.LUA_TEMPLATE=pet.runner.LUA_TEMPLATE.replace(anchor,new,1)
    rc=pet.runner.main();out=Path(value('--out'));r=read(out/'result.json');d=read(out/'final_hint_alias.json') if (out/'final_hint_alias.json').exists() else {}
    passed=rc==0 and r['complete'] and d.get('loads')==1 and d.get('scenes')==d.get('entries')==d.get('calls')==2
    r.update(scope='DIAGNOSTIC: original compressed MegaMan source substituted at native Monday field loader read; wrapper scene read B0 -> A3; clone script0 table read -> selected script. Native load/whole-payload guard/reader/msgOpen/font/wait/exit/reentry only. NOT natural scene/event/branch selection or save proof.',normal_play_checkpoint_eligible=False,hint_diagnostic=d,complete=passed)
    if script==0:
        r.update(scope='DIAGNOSTIC original script0 dispatcher: native compressed MegaMan loader and wrapper scene read aliases only; table observer returns the original unchanged script0 offset. Original jump/flag checks execute in the ROM clone. NOT natural A3 event/provider/progression proof.',original_dispatcher_preserved=True,table_read_value_changed=False)
    if (out/'checkpoint.mss').exists():(out/'checkpoint.mss').rename(out/'diagnostic_checkpoint.mss')
    r['artifacts']={p.name:sha(p.read_bytes()) for p in out.iterdir() if p.is_file() and p.name!='result.json'}
    (out/'result.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print('Hint diagnostic',script,passed,d);return 0 if passed else 1

if __name__=='__main__':raise SystemExit(main())
