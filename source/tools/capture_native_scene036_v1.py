"""Qualified native loader/caller diagnostics, not natural A1/A3 acquisition.

Only CPU read results for the first NPC table lookup's scene/sub/weekday and
the036 selector's scene are aliased. Actual source table reads, native LZ77,
RAM residency, normal actor script/mode/caller and renderer execute unchanged.
No ROM/RAM/actor/flag writes; all diagnostic checkpoints are quarantined.
"""
import sys,struct,json
from pathlib import Path
import capture_field_loader_036_v1 as native
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read
from field_npc_rom_selector_036_v1 import source_population
from field_npc_rom_product_036_v1 import verify_final

def main():
    def arg(k):return sys.argv[sys.argv.index(k)+1]
    case=arg('--native-scene');i=sys.argv.index('--native-scene');del sys.argv[i:i+2]
    if case not in ('a1','a3'):raise ValueError('Declared native scene classes only')
    arc,scene={'a1':('7AAF94',0xA1),'a3':('7B469C',0xA3)}[case];rp=Path(arg('--rom'));m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes();verify_final(source,rom,m['keyitem_rom'])
    for lo,hi in [(0x4F712,0x4F7B6),(0x2E42C,0x2E438),(0xEC158,0xEC15C)]:
        if rom[lo:hi]!=source[lo:hi]:raise ValueError('Native lookup/load applicability')
    row=next(x for x in source_population(source,{arc:scene}) if x['archive']==arc and x['scene']==scene)
    if (row['sub'],row['slot'])!=(3,5) or len(row['payload'])>0x3000:raise ValueError('Qualified lookup/capacity preconditions')
    n=m['keyitem_rom']['npc036'];place=next(p for p in n['placements'] if p['source_archive']==arc);scene_pcs=[x['address'] for x in n['wrapper']['proof']['instructions'] if x['mnemonic']=='ldrb' and x['operands']=='r3, [r2, #4]']
    if len(scene_pcs)!=1:raise ValueError('036 exact scene-read instruction')
    code=r'''
local qLookup=false;local qLoader=false;local qLoads=0;local qCalendar=0;local qScenes=0;local qSubs=0;local qSelect=0;local qSource=0
local function q32(a) local v=0;for j=0,3 do v=v+emu.read(a+j,emu.memType.gbaMemory)*2^(8*j) end;return v end
emu.addMemoryCallback(function()
 local s=emu.getState();local ctx=q32(s['cpu.r10']+64)
 if ctx~=0x02004AD0 then error('Qualified scene callback address applicability') end
 qLoader=emu.read(ctx+4,emu.memType.gbaMemory)==0xA0
end,emu.callbackType.exec,0x0804F712,0x0804F712)
emu.addMemoryCallback(function(address,value)
 local s=emu.getState()
 if qLoader and s['cpu.pipeline.execute.address']==0x0802E42E and address==0x02003D57 then qCalendar=qCalendar+1;return 5 end
end,emu.callbackType.read,0x02003D57,0x02003D57)
emu.addMemoryCallback(function()
 local s=emu.getState();qLookup=qLoader and s['cpu.r0']==0x08053700 and s['cpu.r14']==0x0804F721
end,emu.callbackType.exec,0x0804F790,0x0804F790)
emu.addMemoryCallback(function(address,value)
 local s=emu.getState();local pc=s['cpu.pipeline.execute.address']
 if qLookup and pc==0x0804F796 and address==s['cpu.r7']+4 then qScenes=qScenes+1;return SCENE end
 if qLookup and pc==0x0804F79A and address==s['cpu.r7']+5 then qSubs=qSubs+1;return 3 end
 if qLoads>0 and pc==SELECTPC and address==s['cpu.r2']+4 then
  for j=0,NATIVEBYTES-1 do if emu.read(0x02039800+j,emu.memType.gbaMemory)~=emu.read(NATIVECOPY+j,emu.memType.gbaMemory) then error('Native decompressed identity not resident before scene diagnostic') end end
  qSelect=qSelect+1;return SCENE
 end
end,emu.callbackType.read,0x02004AD4,0x02004AD5)
emu.addMemoryCallback(function() qLookup=false end,emu.callbackType.exec,0x0804F7A4,0x0804F7A4)
emu.addMemoryCallback(function()
 if qLoader then local s=emu.getState();qSource=s['cpu.r0'];if qSource~=SOURCE then error('Native scene/sub/slot did not select target source') end end
end,emu.callbackType.exec,0x0804F724,0x0804F724)
emu.addMemoryCallback(function() if qLoader then qLoads=qLoads+1 end;qLoader=false end,emu.callbackType.exec,0x0804F748,0x0804F748)
local function dumpQualified(name)
 write(name..'_qualified_scene.json',string.format('{"native_loads":%d,"weekday_reads":%d,"lookup_scene_reads":%d,"lookup_sub_reads":%d,"selector_scene_reads":%d,"source":%d}',qLoads,qCalendar,qScenes,qSubs,qSelect,qSource))
end
'''
    for k,v in [('SELECTPC',scene_pcs[0]),('NATIVEBYTES',len(row['payload'])),('NATIVECOPY',0x08000000+place['native_copy_offset']),('SOURCE',0x08000000+int(arc,16)),('SCENE',scene)]:code=code.replace(k,str(v))
    marker='local function capture(name)\n'
    if native.runner.LUA_TEMPLATE.count(marker)!=1:raise ValueError('Capture insertion anchor')
    native.runner.LUA_TEMPLATE=native.runner.LUA_TEMPLATE.replace(marker,code+marker+' dumpQualified(name)\n',1)
    native.runner.LUA_TEMPLATE=native.runner.LUA_TEMPLATE.replace('local function finish()\n',"local function finish()\n dumpQualified('final')\n",1)
    rc=native.main();out=Path(arg('--out'));r=read(out/'result.json');q=read(out/'final_qualified_scene.json')
    passed=rc==0 and r['complete'] and (q['native_loads'],q['weekday_reads'],q['lookup_scene_reads'],q['lookup_sub_reads'])==(1,1,1,1) and q['selector_scene_reads']>=1 and q['source']==0x08000000+int(arc,16)
    if (out/'checkpoint.mss').exists():(out/'checkpoint.mss').rename(out/'diagnostic_checkpoint.mss')
    r.update(complete=passed,scope='DIAGNOSTIC native scene/sub/weekday read aliases for NPC loader and selector scene only; not natural A1/A3 progression/calendar/acquisition',field_observation='Qualified native lookup -> actual source LZ77 -> RAM -> normal actor/cached caller ->036 selector -> clone/font/video; four read-result aliases, no ROM/RAM/actor/flag writes',normal_play_checkpoint_eligible=False,qualified_scene_case=case,qualified_scene=q,target_archive=arc,target_scene=scene,alias_contract=dict(loader_scene=scene,loader_sub=3,loader_weekday=5,selector_scene=scene,actor_script_mode_root_and_caller_unchanged=True),artifacts={p.name:sha(p.read_bytes()) for p in out.iterdir() if p.is_file() and p.name!='result.json'})
    (out/'result.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print('Qualified native scene',case,passed,q);return 0 if passed else 1

if __name__=='__main__':raise SystemExit(main())
