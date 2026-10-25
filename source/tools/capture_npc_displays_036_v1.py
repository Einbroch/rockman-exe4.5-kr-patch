"""Two native full-box display diagnostics; aliases quarantined, no battle/reward claim."""
import json,struct,sys
from pathlib import Path
import capture_roll_pet as pet
from build_visibility_poc import ROOT,sha,require_hash
from archive_scripts import script_spans
from field_npc_rom_product_036_v1 import verify_final

CASES={'a0':('79CF04',255,30,None),'a1':('7AAF94',255,0,None),'a3':('7B469C',255,0,None)}

def main():
    def value(k):return sys.argv[sys.argv.index(k)+1]
    case=value('--display-case');i=sys.argv.index('--display-case');del sys.argv[i:i+2]
    if case not in CASES:raise ValueError('Declared display cases only')
    archive,count,script,prefix=CASES[case]
    rp=Path(value('--rom'));m=json.loads(rp.with_suffix('.json').read_text(encoding='utf8'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes()
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,m['source_sha256']);source=sp.read_bytes()
    for a,b in ((0x37F0C,0x37F54),(0x4F7B6,0x4F7D0),(0x4FB58,0x4FC20)):
        if rom[a:b]!=source[a:b]:raise ValueError('Native caller/default initializer drift')
    # Native4FB58 saves four buffers and calls zero-fill090C for contextD8,
    # then restores buffers and sets the new root. No old PET position state.
    if source[0x4FB58:0x4FB70]!=bytes.fromhex('ae6d0fb45046c06ad821b0f7d3fe0fbcea642b656c65ae65'):raise ValueError('Native context reset contract')
    verify_final(source,rom,m['keyitem_rom'])
    ar=next(x for x in m['keyitem_rom']['npc036']['archives'] if x['archive']==archive);pool=0x08000000+ar['rom_offset'];payload=rom[ar['rom_offset']:ar['rom_offset']+ar['compiled_bytes']]
    spans=script_spans(payload,count)
    from verify_tpi_index import lz77_decompress
    native=lz77_decompress(source,int(archive,16))[0];ns=script_spans(native,255)[script]
    if ns.count(bytes.fromhex('e700'))!=1:raise ValueError('035 one native msgOpen')
    prefix=ns[:ns.index(bytes.fromhex('e700'))+2]
    if not spans[script].startswith(prefix):raise ValueError('Target native mugshot/msgOpen prefix')
    nm=m['keyitem_rom']['npc036'];p=next(p for p in nm['placements'] if p['source_archive']==archive);i=nm['placements'].index(p)
    if struct.unpack_from('<I',rom,nm['descriptor_offset']+i*16)[0]!=pool:raise ValueError('035 target NPC descriptor binding')
    pointer=0x080380D0;old=struct.unpack_from('<I',rom,pointer-0x08000000)[0];initial,target=[struct.unpack_from('<H',payload,s*2)[0] for s in (0,script)]
    ef=m['extension'];font=0x08000000+ef['normal_font_offset'];code=pet.PROBE
    for k,v in [('PET_FONT_END',font+(ef['legacy_index_view']+11172+ef['extra_glyph_count'])*96),('PET_FONT',font),('PET_POOL',pool),('PET_END',pool+len(payload))]:code=code.replace(k,str(v))
    code+=f'''
local roots=0;local entries=0;local navi=-1
emu.addMemoryCallback(function(address,value)
 local s=emu.getState()
 if roots==0 and address=={pointer} and value=={old} and s['cpu.pipeline.execute.address']==0x08037F20 and s['cpu.r1']==0 then
  local ctx=0;for j=0,3 do ctx=ctx+emu.read(s['cpu.r10']+0x40+j,emu.memType.gbaMemory)*2^(j*8) end
  navi=emu.read(ctx+1,emu.memType.gbaMemory);if navi~=0 then error('Own Rockman normal state required') end
  roots=1;return {pool}
 end
end,emu.callbackType.read,{pointer},{pointer+3})
emu.addMemoryCallback(function(address,value)
 local s=emu.getState()
 if roots==1 and entries==0 and address=={pool} and value=={initial} and s['cpu.pipeline.execute.address']==0x0804FB76 and s['cpu.r0']=={pool} and s['cpu.r1']==0 and s['cpu.r5']==0x0200FA20 then entries=1;return {target} end
end,emu.callbackType.read,{pool},{pool+1})
local function dumpDisplay(name)
 write(name..'_display_alias.json','{{"roots":'..roots..',"entries":'..entries..',"navi":'..navi..',"root":{pool},"script":{script}}}')
end
'''
    for anchor,new in [('local function capture(name)\n',code+'local function capture(name)\n dumpRollPet(name)\n dumpDisplay(name)\n'),('local function finish()\n',"local function finish()\n dumpDisplay('final')\n")]:
        if pet.runner.LUA_TEMPLATE.count(anchor)!=1:raise ValueError('Capture anchor')
        pet.runner.LUA_TEMPLATE=pet.runner.LUA_TEMPLATE.replace(anchor,new,1)
    rc=pet.runner.main();out=Path(value('--out'));r=json.loads((out/'result.json').read_text(encoding='utf8'));d=json.loads((out/'final_display_alias.json').read_text(encoding='utf8'))
    passed=rc==0 and r['complete'] and d['roots']==d['entries']==1 and d['navi']==0
    r.update(scope='DIAGNOSTIC PET root/script read aliases to actual036 new NPC clone; native initializer/guards/mugshot/pages/font executes. NOT native A0/A1/A3 loader/NPC selector/caller, calendar acquisition or save proof.',normal_play_checkpoint_eligible=False,display_diagnostic=d,display_case=case,complete=passed)
    if (out/'checkpoint.mss').exists():(out/'checkpoint.mss').rename(out/'diagnostic_checkpoint.mss')
    r['artifacts']={p.name:sha(p.read_bytes()) for p in out.iterdir() if p.is_file() and p.name!='result.json'}
    (out/'result.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print('Display diagnostic',case,passed,d);return 0 if passed else 1

if __name__=='__main__':raise SystemExit(main())
