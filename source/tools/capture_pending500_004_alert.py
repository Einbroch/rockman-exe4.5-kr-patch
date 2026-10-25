"""Quarantined NumberMan alert renderer diagnostic; read aliases only, no progress claim."""
import json,struct,sys
from pathlib import Path
import capture_roll_pet as pet
from build_visibility_poc import ROOT,sha,require_hash
from archive_scripts import script_spans
from keyitem_rom_data import verify_final

TARGET_ARCHIVE='68BAAC'
SCRIPT_COUNT=5
SCRIPTS=(1,2)

def main():
    def value(k):return sys.argv[sys.argv.index(k)+1]
    script=int(value('--alert-script'));i=sys.argv.index('--alert-script');del sys.argv[i:i+2]
    if script not in SCRIPTS:raise ValueError('Explicit NumberMan display scope')
    rp=Path(value('--rom'));m=json.loads(rp.with_suffix('.json').read_text(encoding='utf8'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes()
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,m['source_sha256']);source=sp.read_bytes()
    for a,b in ((0x37F0C,0x37F54),(0x4F7B6,0x4F7D0),(0x4FB70,0x4FC20)):
        if rom[a:b]!=source[a:b]:raise ValueError('Native caller/initializer drift')
    verify_final(source,rom,m['keyitem_rom'])
    ar=next(x for x in m['archives'] if x['archive']==TARGET_ARCHIVE);pool=0x08000000+ar['rom_offset'];payload=rom[ar['rom_offset']:ar['rom_offset']+ar['compiled_bytes']]
    spans=script_spans(payload,SCRIPT_COUNT)
    if not spans[script].startswith(bytes.fromhex('f6000a0c01e702f6025c6e03f604e18d')):raise ValueError('Native target window setup')
    pointer=0x080382B0;old=struct.unpack_from('<I',rom,pointer-0x08000000)[0]
    initial,target=[struct.unpack_from('<H',payload,s*2)[0] for s in (0,script)]
    ef=m['extension'];font=0x08000000+ef['normal_font_offset'];code=pet.PROBE
    for k,v in [('PET_FONT_END',font+(ef['legacy_index_view']+11172+ef['extra_glyph_count'])*96),('PET_FONT',font),('PET_POOL',pool),('PET_END',pool+len(payload))]:code=code.replace(k,str(v))
    code+=f'''
local rootAliases=0;local entryAliases=0;local nativeNavi=-1
emu.addMemoryCallback(function(address,value)
 local s=emu.getState()
 if rootAliases==0 and address=={pointer} and value=={old} and s['cpu.pipeline.execute.address']==0x08037F20 and s['cpu.r1']==0 then
  local ctx=0;for j=0,3 do ctx=ctx+emu.read(s['cpu.r10']+0x40+j,emu.memType.gbaMemory)*2^(j*8) end
  nativeNavi=emu.read(ctx+1,emu.memType.gbaMemory)
  if nativeNavi~=8 then error('Own NumberMan normal state required') end
  rootAliases=1;return {pool}
 end
end,emu.callbackType.read,{pointer},{pointer+3})
emu.addMemoryCallback(function(address,value)
 local s=emu.getState()
 if rootAliases==1 and entryAliases==0 and address=={pool} and value=={initial} and s['cpu.pipeline.execute.address']==0x0804FB76 and s['cpu.r0']=={pool} and s['cpu.r1']==0 and s['cpu.r5']==0x0200FA20 then entryAliases=1;return {target} end
end,emu.callbackType.read,{pool},{pool+1})
local function dumpAlert(name)
 write(name..'_alert_alias.json','{{"root_aliases":'..rootAliases..',"entry_aliases":'..entryAliases..',"native_navi":'..nativeNavi..',"root":{pool},"script":{script}}}')
end
'''
    for anchor,new in [('local function capture(name)\n',code+'local function capture(name)\n dumpRollPet(name)\n dumpAlert(name)\n'),('local function finish()\n',"local function finish()\n dumpAlert('final')\n")]:
        if pet.runner.LUA_TEMPLATE.count(anchor)!=1:raise ValueError('Capture anchor')
        pet.runner.LUA_TEMPLATE=pet.runner.LUA_TEMPLATE.replace(anchor,new,1)
    rc=pet.runner.main();out=Path(value('--out'));receipt=json.loads((out/'result.json').read_text(encoding='utf8'));d=json.loads((out/'final_alert_alias.json').read_text(encoding='utf8'))
    passed=rc==0 and receipt['complete'] and d['root_aliases']==d['entry_aliases']==1 and d['native_navi']==8
    receipt.update(scope=f'DIAGNOSTIC native NumberMan PET pointer/table read aliases to {TARGET_ARCHIVE}:{script}. Original window/portrait retained; NOT natural event/battle/calendar selection, progression or save proof.',normal_play_checkpoint_eligible=False,alert_diagnostic=d,display_archive=TARGET_ARCHIVE,complete=passed)
    if (out/'checkpoint.mss').exists():(out/'checkpoint.mss').rename(out/'diagnostic_checkpoint.mss')
    receipt['artifacts']={p.name:sha(p.read_bytes()) for p in out.iterdir() if p.is_file() and p.name!='result.json'}
    (out/'result.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('NumberMan alert diagnostic',passed,d);return 0 if passed else 1

if __name__=='__main__':raise SystemExit(main())
