"""Read-only035 field-loader/reader observations; no aliases or RAM writes."""
import sys,json
from pathlib import Path
import run_mesen_segment as runner
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read

def main():
    def arg(k):return sys.argv[sys.argv.index(k)+1]
    rp=Path(arg('--rom'));m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes()
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    for a,b in [(0x4F712,0x4F7B6),(0x2E42C,0x2E438),(0xEC158,0xEC15C)]:
        if source[a:b]!=rom[a:b]:raise ValueError('035 native loader applicability')
    code=r'''
local fieldEvents={};local readers={};local count=0
local function field32(a)
 local v=0;for j=0,3 do v=v+emu.read(a+j,emu.memType.gbaMemory)*2^(8*j) end;return v
end
local function recordField(pc)
 local s=emu.getState();local scene=field32(s['cpu.r10']+64)
 fieldEvents[#fieldEvents+1]=string.format('{"pc":%d,"frame":%d,"r0":%d,"r1":%d,"r4":%d,"lr":%d,"scene":%d,"sub":%d,"selector":%d}',pc,frame,s['cpu.r0'],s['cpu.r1'],s['cpu.r4'],s['cpu.r14'],emu.read(scene+4,emu.memType.gbaMemory),emu.read(scene+5,emu.memType.gbaMemory),emu.read(0x02003D57,emu.memType.gbaMemory))
end
for _,pc in ipairs({0x0804F712,0x0804F724,0x0804F730,0x0804F744}) do
 emu.addMemoryCallback(function() recordField(pc) end,emu.callbackType.exec,pc,pc)
end
emu.addMemoryCallback(function()
 count=count+1;recordField(0x0804F748)
 for _,pair in ipairs({{0x02039800,0x3000},{0x0203C800,0x1000},{0x0203D800,0x2800}}) do
  local t={};for j=0,pair[2]-1 do t[#t+1]=string.char(emu.read(pair[1]+j,emu.memType.gbaMemory)) end
  write(string.format('load_%03d_%08X.bin',count,pair[1]),table.concat(t))
 end
end,emu.callbackType.exec,0x0804F748,0x0804F748)
for _,pc in ipairs({0x0804F76E,0x0804F780,0x0804F802}) do
 emu.addMemoryCallback(function()
  local s=emu.getState();readers[#readers+1]=string.format('{"pc":%d,"frame":%d,"r0":%d,"r1":%d,"lr":%d}',pc,frame,s['cpu.r0'],s['cpu.r1'],s['cpu.r14'])
 end,emu.callbackType.exec,pc,pc)
end
local function dumpField()
 write('field_loader.json','{"loads":'..count..',"events":['..table.concat(fieldEvents,',')..'],"readers":['..table.concat(readers,',')..']}')
end
'''
    npc=m['keyitem_rom']['npc035']; proof=npc['wrapper']['proof']
    entry=proof['address']; end=next(x['address'] for x in proof['instructions'] if x['mnemonic']=='pop' and 'r0' in x['operands'])
    extra=r'''
local nativeSelectors={};local selectorPending=nil;local calendarWrites={}
emu.addMemoryCallback(function()
 local s=emu.getState()
 if s['cpu.r0']==0x02039800 then
  selectorPending={start=s['cpu.cycleCount'],script=s['cpu.r1'],frame=frame,caller=s['cpu.r14']}
 end
end,emu.callbackType.exec,ENTRY,ENTRY)
emu.addMemoryCallback(function()
 if selectorPending then
  local s=emu.getState();local root=field32(s['cpu.r13'])
  nativeSelectors[#nativeSelectors+1]=string.format('{"frame":%d,"script":%d,"root":%d,"cycles":%d,"caller_lr":%d}',selectorPending.frame,selectorPending.script,root,s['cpu.cycleCount']-selectorPending.start,selectorPending.caller)
  selectorPending=nil
 end
end,emu.callbackType.exec,EXIT,EXIT)
for _,pc in ipairs({0x0802E2C0,0x0802E316}) do
 emu.addMemoryCallback(function()
  local s=emu.getState()
  calendarWrites[#calendarWrites+1]=string.format('{"pc":%d,"frame":%d,"r0":%d,"r5":%d}',pc,frame,s['cpu.r0'],s['cpu.r5'])
 end,emu.callbackType.exec,pc,pc)
end
local function dumpNativeSelector()
 write('native_selector.json','{"selectors":['..table.concat(nativeSelectors,',')..'],"calendar_writes":['..table.concat(calendarWrites,',')..']}')
end
'''
    code+=extra.replace('ENTRY',str(entry)).replace('EXIT',str(end))
    from capture_roll_pet import PROBE as glyph_probe
    ef=m['extension'];font=0x08000000+ef['normal_font_offset']
    pool=0x08000000+min(p['rom_offset'] for p in npc['placements'])
    pool_end=0x08000000+max(p['rom_offset']+p['compiled_bytes'] for p in npc['placements'])
    for k,v in [('PET_FONT_END',font+(ef['legacy_index_view']+11172+ef['extra_glyph_count'])*96),('PET_FONT',font),('PET_POOL',pool),('PET_END',pool_end)]:glyph_probe=glyph_probe.replace(k,str(v))
    code+=glyph_probe
    code+=r'''
local npcEntries={}
emu.addMemoryCallback(function()
 local s=emu.getState();local regs={}
 for i=0,14 do regs[#regs+1]=string.format('"%d":%d',i,s['cpu.r'..i]) end
 npcEntries[#npcEntries+1]=string.format('{"frame":%d,"registers":{%s}}',frame,table.concat(regs,','))
end,emu.callbackType.exec,0x0804F764,0x0804F764)
local function dumpNPCEntries()
 write('npc_entries.json','{"entries":['..table.concat(npcEntries,',')..']}')
end
'''
    from field_npc_rom_product_035_v2 import verify_final
    verify_final(source,rom,m['keyitem_rom'])
    if rom[0x6EDE6:0x6EDF2]!=source[0x6EDE6:0x6EDF2] or source[0x6EDE6:0x6EDF2]!=bytes.fromhex('287f9c216958e0f7bafc25e0'):raise ValueError('source NPC input/BL contract')
    from verify_tpi_index import lz77_decompress
    native=lz77_decompress(source,0x79D650)[0]
    code+=r'''
local modeAliases=0;local aliasValues={}
local nativeExpected={NATIVE_BYTES}
emu.addMemoryCallback(function(address,value)
 local s=emu.getState()
 if address~=0x0200AB7C or value~=1 or s['cpu.pipeline.execute.address']~=0x0806EDEA or s['cpu.r5']~=0x0200AAE0 or s['cpu.r0']~=0 or s['cpu.r1']~=0x9C then return end
 local scene=field32(s['cpu.r10']+64)
 if emu.read(scene+4,emu.memType.gbaMemory)~=0xA0 or emu.read(scene+5,emu.memType.gbaMemory)~=0 or emu.read(scene+1,emu.memType.gbaMemory)~=0 or emu.read(0x02003D57,emu.memType.gbaMemory)~=2 then error('Native mode diagnostic scene/Navi/calendar guard') end
 if field32(0x0200AB40)~=0 or emu.read(0x0200AAFC,emu.memType.gbaMemory)~=0 then error('Native mode actor guard') end
 for i,v in ipairs(nativeExpected) do if emu.read(0x02039800+i-1,emu.memType.gbaMemory)~=v then error('Native mode actual loaded source identity mismatch') end end
 if modeAliases>=2 then error('Native mode diagnostic exceeded two declared invocations') end
 modeAliases=modeAliases+1
 aliasValues[#aliasValues+1]=string.format('{"frame":%d,"pc":%d,"address":%d,"original":%d,"returned":0,"actor":%d}',frame,s['cpu.pipeline.execute.address'],address,value,s['cpu.r5'])
 return 0
end,emu.callbackType.read,0x0200AB7C,0x0200AB7F)
local function dumpModeAlias()
 write('mode_alias.json','{"aliases":'..modeAliases..',"original_actor_mode_still":'..field32(0x0200AB7C)..',"events":['..table.concat(aliasValues,',')..']}')
end
'''.replace('NATIVE_BYTES',','.join(str(v) for v in native))
    anchor='local function capture(name)\n'
    if runner.LUA_TEMPLATE.count(anchor)!=1:raise ValueError('035 capture anchor')
    runner.LUA_TEMPLATE=runner.LUA_TEMPLATE.replace(anchor,code+anchor+' dumpRollPet(name)\n',1)
    runner.LUA_TEMPLATE=runner.LUA_TEMPLATE.replace('local function finish()\n','local function finish()\n dumpField()\n dumpModeAlias()\n dumpNPCEntries()\n dumpNativeSelector()\n dumpRollPet(\'final\')\n',1)
    rc=runner.main();out=Path(arg('--out'));r=read(out/'result.json')
    if (out/'checkpoint.mss').exists():(out/'checkpoint.mss').rename(out/'diagnostic_checkpoint.mss')
    aliases=read(out/'mode_alias.json')
    r.update(scope='DIAGNOSTIC read alias of actor dialog mode1 to0 at source6EDEA only. Preserves normal native A0 load, native6EDEC/4F764/4F76E caller, corrected selector and renderer. Bypasses actor-specific mode acquisition, NOT natural NPC selection or save proof.',normal_play_checkpoint_eligible=False,mode_alias=aliases)
    r.update(field_observation='Read-only native field loader and reader; no aliases, writes, injected state or control changes. Current035 artifact native loader observation; Korean selected NPC acquisition is not inferred from load completion.')
    r['artifacts']={p.name:sha(p.read_bytes()) for p in out.iterdir() if p.is_file() and p.name!='result.json'}
    (out/'result.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    return rc

if __name__=='__main__':raise SystemExit(main())
