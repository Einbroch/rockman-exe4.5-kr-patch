"""Read-only039 source LZ, nested selector, controls, Hangul/font observations.

No aliases or game writes; controller input only. Not multiplayer verification.
"""
import sys,json
from pathlib import Path
import run_mesen_segment as runner
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read
from communication_rom_selector039_v1 import source_population
from capture_roll_pet import PROBE


def main():
    def arg(k):return sys.argv[sys.argv.index(k)+1]
    rp=Path(arg('--rom'));m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);audit=read('analysis/pending500_040_v2/integration.json')
    if not audit['passed'] or audit['rom_sha256']!=m['output_sha256']:raise ValueError('039 actual audited artifact')
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes();n=m['keyitem_rom']['typed040'];pool=source_population(source,{p['source_archive'] for p in n['placements'] if p['source_class']=='communication-help'});lengths={0x08000000+int(p['archive'],16):len(p['payload']) for p in pool};proof=n['wrapper']['proof'];entry=proof['address'];exitpc=next(i['address'] for i in proof['instructions'] if i['mnemonic']=='pop' and 'r0' in i['operands']);lo=0x08000000+min(p['rom_offset'] for p in n['placements']);hi=0x08000000+max(p['rom_offset']+p['compiled_bytes'] for p in n['placements'])
    for lo0,hi0 in [(0xCEC,0xCF4),(0x448C8,0x44940)]:
        if rp.read_bytes()[lo0:hi0]!=source[lo0:hi0]:raise ValueError('040 original communication source/getter applicability')
    if int.from_bytes(source[0x4492C:0x44930],'little')!=0x086F8D00:raise ValueError('040 native Navi19 lookup')
    code=r'''
local qualifiedNavis={}
emu.addMemoryCallback(function(address,value)
 local s=emu.getState()
 if s['cpu.pipeline.execute.address']==0x08000CF0 and s['cpu.r14']==0x080448CF then
  if address~=0x02004AD1 or value~=0 or #qualifiedNavis~=0 then error('040 qualified communication Navi read applicability') end
  qualifiedNavis[#qualifiedNavis+1]=string.format('{"frame":%d,"address":%d,"original":%d,"returned":19,"pc":%d,"lr":%d}',frame,address,value,s['cpu.pipeline.execute.address'],s['cpu.r14']);return 19
 end
end,emu.callbackType.read,0x02004AD1,0x02004AD1)
local commEvents={};local commLoads=0;local commSource=nil;local commNested={};local commCommands={};local commSelect={};local pending=nil
local commLengths=LENGTHS
local function c32(a) local v=0;for j=0,3 do v=v+emu.read(a+j,emu.memType.gbaMemory)*2^(8*j) end;return v end
for _,pc in ipairs({0x080448C8,0x080448D6,0x080448BC,0x080448C2,0x080448C6}) do
 emu.addMemoryCallback(function()
  local s=emu.getState();local regs={};for j=0,14 do regs[#regs+1]=string.format('"%d":%d',j,s['cpu.r'..j]) end
  commEvents[#commEvents+1]=string.format('{"frame":%d,"pc":%d,"context":%d,"root":%d,"stream":%d,"registers":{%s}}',frame,pc,c32(s['cpu.r10']+44),c32(0x0200FA50),c32(0x0200FA4C),table.concat(regs,','))
  if pc==0x080448D6 then if s['cpu.r1']~=0x02024000 or not commLengths[s['cpu.r0']] then error('039 original communication LZ source/root differs') end;commSource=s['cpu.r0'] end
 end,emu.callbackType.exec,pc,pc)
end
emu.addMemoryCallback(function()
 if commSource then commLoads=commLoads+1;local t={};for j=0,commLengths[commSource]-1 do t[#t+1]=string.char(emu.read(0x02024000+j,emu.memType.gbaMemory)) end;write(string.format('communication_native_%03d.bin',commLoads),table.concat(t));commSource=nil end
end,emu.callbackType.exec,0x080448DA,0x080448DA)
emu.addMemoryCallback(function()
 local s=emu.getState();if s['cpu.r0']==0x02024000 then
  commNested[#commNested+1]=string.format('{"frame":%d,"root":%d,"script":%d,"lr":%d,"sp":%d,"saved_outer_lr":%d}',frame,s['cpu.r0'],s['cpu.r1'],s['cpu.r14'],s['cpu.r13'],c32(s['cpu.r13']+16))
 end
end,emu.callbackType.exec,0x0804FB4C,0x0804FB4C)
emu.addMemoryCallback(function()
 local s=emu.getState();if s['cpu.r0']==0x02024000 then pending={start=s['cpu.cycleCount'],frame=frame,script=s['cpu.r1'],lr=s['cpu.r14']} end
end,emu.callbackType.exec,ENTRY,ENTRY)
emu.addMemoryCallback(function()
 if pending then local s=emu.getState();commSelect[#commSelect+1]=string.format('{"frame":%d,"script":%d,"lr":%d,"selected_root":%d,"cycles":%d}',pending.frame,pending.script,pending.lr,c32(s['cpu.r13']),s['cpu.cycleCount']-pending.start);pending=nil end
end,emu.callbackType.exec,EXIT,EXIT)
for _,pc in ipairs({0x08051098,0x08050754}) do
 emu.addMemoryCallback(function()
  local s=emu.getState();local p=s['cpu.r4'];if p>=POOL and p<POOLEND then
   commCommands[#commCommands+1]=string.format('{"frame":%d,"pc":%d,"stream":%d,"context":%d,"op":%d,"arg":%d}',frame,pc,p,s['cpu.r5'],emu.read(p,emu.memType.gbaMemory),emu.read(p+1,emu.memType.gbaMemory))
  end
 end,emu.callbackType.exec,pc,pc)
end
local function dumpCommunication()
 write('qualified_navi040.json','{"reads":['..table.concat(qualifiedNavis,',')..']}')
 write('communication_trace.json','{"loads":'..commLoads..',"events":['..table.concat(commEvents,',')..']}')
 write('communication_nested.json','{"calls":['..table.concat(commNested,',')..'],"selectors":['..table.concat(commSelect,',')..'],"commands":['..table.concat(commCommands,',')..']}')
end
'''
    for key,value in [('LENGTHS','{'+','.join('['+str(k)+']='+str(v) for k,v in sorted(lengths.items()))+'}'),('POOLEND',str(hi)),('POOL',str(lo)),('ENTRY',str(entry)),('EXIT',str(exitpc))]:code=code.replace(key,value)
    ef=m['extension'];font=0x08000000+ef['normal_font_offset'];glyph=PROBE
    for key,value in [('PET_FONT_END',font+(ef['legacy_index_view']+11172+ef['extra_glyph_count'])*96),('PET_FONT',font),('PET_POOL',lo),('PET_END',hi)]:glyph=glyph.replace(key,str(value))
    marker='local function capture(name)\n'
    if runner.LUA_TEMPLATE.count(marker)!=1:raise ValueError('039 capture anchor')
    runner.LUA_TEMPLATE=runner.LUA_TEMPLATE.replace(marker,code+glyph+marker+' dumpRollPet(name)\n',1).replace('local function finish()\n',"local function finish()\n dumpCommunication()\n dumpRollPet('final')\n",1)
    rc=runner.main();out=Path(arg('--out'));r=read(out/'result.json');
    if (out/'checkpoint.mss').exists():(out/'checkpoint.mss').rename(out/'diagnostic_checkpoint.mss')
    r.update(scope='DIAGNOSTIC communication loader-only Navi READ0->19; actual source table/LZ/native RAM/nested caller/040 selector/render; NOT Navi acquisition or player change.',normal_play_checkpoint_eligible=False,natural_acquisition_verified=False,release_eligible=False)
    r['communication_observation']='Actual040 qualified new6F8D00 help: loader-only Navi read alias, no gameRAM/ROM/PC/caller write; not natural Navi19 acquisition or multiplayer.';r['artifacts']={p.name:sha(p.read_bytes()) for p in out.iterdir() if p.is_file() and p.name!='result.json'};(out/'result.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf8');return rc


if __name__=='__main__':raise SystemExit(main())
