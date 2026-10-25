"""Qualified040 PET tournament path: one registration-bit READ alias; no RAM/PC writes."""
import json,sys
from pathlib import Path
import run_mesen_segment as runner
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read
from verify_tpi_index import lz77_decompress
from capture_roll_pet import PROBE


def main():
    def arg(k):return sys.argv[sys.argv.index(k)+1]
    rp=Path(arg('--rom'));m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    for lo,hi in [(0x2A6,0x30C),(0x46530,0x46598),(0x465D0,0x466B8),(0x47958,0x479E0),(0x493B4,0x49410),(0x49708,0x49734),(0x287B2,0x287CA)]:
        if source[lo:hi]!=rom[lo:hi]:raise ValueError('040 original tournament route applicability')
    audit=read('analysis/pending500_040_v2/integration.json')
    if not audit['passed'] or audit['rom_sha256']!=m['output_sha256']:raise ValueError('040 audited actual artifact')
    n=m['keyitem_rom']['typed040'];placement=next(p for p in n['placements'] if p['source_archive']=='6E93C8');pool=0x08000000+placement['rom_offset'];poolend=pool+placement['compiled_bytes'];entry=n['wrapper']['proof']['address'];exitpc=next(i['address'] for i in n['wrapper']['proof']['instructions'] if i['mnemonic']=='pop' and 'r0' in i['operands'])
    native=lz77_decompress(source,0x6E93C8)[0]
    code=r'''
local tournamentAliases={};local tournamentEvents={};local tournamentFlags={};local tournamentLoads=0;local pendingTournament=false
local function tr32(a) local v=0;for j=0,3 do v=v+emu.read(a+j,emu.memType.gbaMemory)*2^(8*j) end;return v end
emu.addMemoryCallback(function(address,value)
 local s=emu.getState()
 if s['cpu.pipeline.execute.address']==0x080287C4 and s['cpu.r14']==0x08049721 and s['cpu.r1']==8 then
  if address~=0x02004BF7 or value~=0 or #tournamentAliases>=4 then error('040 qualified registration-read prerequisites') end
  tournamentAliases[#tournamentAliases+1]=string.format('{"frame":%d,"address":%d,"original":%d,"returned":8,"pc":%d,"lr":%d}',frame,address,value,s['cpu.pipeline.execute.address'],s['cpu.r14'])
  return 8
 end
end,emu.callbackType.read,0x02004BF7,0x02004BF7)
for _,pc in ipairs({0x080493B4,0x080493B8,0x080493BC,0x08049708,0x0804971C,0x0804972E,0x08046530,0x08046568,0x08046630,0x08046650,0x080466A4,0x080466AA,0x08047968,0x08047976,0x08047958,0x0804795E,0x0804FB4C,0x0804FB90}) do
 emu.addMemoryCallback(function()
  if #tournamentEvents>=1000 then error('040 tournament event observation cap') end
  local s=emu.getState();local regs={};for j=0,14 do regs[#regs+1]=string.format('"%d":%d',j,s['cpu.r'..j]) end
  tournamentEvents[#tournamentEvents+1]=string.format('{"frame":%d,"pc":%d,"registers":{%s},"mode":%d,"context_root":%d,"context_stream":%d,"ui_word":%d,"ui_kind":%d}',frame,pc,table.concat(regs,','),emu.read(tr32(s['cpu.r10']),emu.memType.gbaMemory),tr32(0x0200FA50),tr32(0x0200FA4C),tr32(0x02010220),emu.read(0x02010225,emu.memType.gbaMemory))
  if pc==0x08047976 then
   if s['cpu.r0']~=0x086E93C8 or s['cpu.r1']~=0x02024000 then error('040 tournament native loader arguments') end
   pendingTournament=true
  end
 end,emu.callbackType.exec,pc,pc)
end
emu.addMemoryCallback(function()
 if pendingTournament then local t={};for j=0,NATIVE_LENGTH-1 do t[#t+1]=string.char(emu.read(0x02024000+j,emu.memType.gbaMemory)) end;tournamentLoads=tournamentLoads+1;write(string.format('tournament_native_%03d.bin',tournamentLoads),table.concat(t));pendingTournament=false end
end,emu.callbackType.exec,0x0804797A,0x0804797A)
emu.addMemoryCallback(function()
 local s=emu.getState();local address=s['cpu.r3'];local value=emu.read(address,emu.memType.gbaMemory)
 if #tournamentFlags<500 and (s['cpu.r14']==0x08049721 or s['cpu.r14']>=0x08049000 and s['cpu.r14']<0x0804A000) then
  tournamentFlags[#tournamentFlags+1]=string.format('{"frame":%d,"pc":%d,"lr":%d,"address":%d,"value":%d,"mask":%d}',frame,s['cpu.pipeline.execute.address'],s['cpu.r14'],address,value,s['cpu.r1'])
 end
end,emu.callbackType.exec,0x080287C4,0x080287C4)
local typedSelections={};local typedPending=nil
emu.addMemoryCallback(function()
 local s=emu.getState();if s['cpu.r0']==0x02024000 and s['cpu.r14']==0x08047963 then typedPending={frame=frame,script=s['cpu.r1'],start=s['cpu.cycleCount']} end
end,emu.callbackType.exec,TYPED_ENTRY,TYPED_ENTRY)
emu.addMemoryCallback(function()
 if typedPending then local s=emu.getState();typedSelections[#typedSelections+1]=string.format('{"frame":%d,"script":%d,"selected_root":%d,"cycles":%d}',typedPending.frame,typedPending.script,tr32(s['cpu.r13']),s['cpu.cycleCount']-typedPending.start);typedPending=nil end
end,emu.callbackType.exec,TYPED_EXIT,TYPED_EXIT)
local function dumpTournament()
 write('typed_selections040.json','{"selections":['..table.concat(typedSelections,',')..']}')
 write('tournament_route.json','{"state_intervention":true,"registration_read_aliases":['..table.concat(tournamentAliases,',')..'],"events":['..table.concat(tournamentEvents,',')..'],"flag_reads":['..table.concat(tournamentFlags,',')..'],"loads":'..tournamentLoads..'}')
end
'''.replace('NATIVE_LENGTH',str(len(native))).replace('TYPED_ENTRY',str(entry)).replace('TYPED_EXIT',str(exitpc))
    ef=m['extension'];font=0x08000000+ef['normal_font_offset'];glyph=PROBE
    for k,v in [('PET_FONT_END',font+(ef['legacy_index_view']+11172+ef['extra_glyph_count'])*96),('PET_FONT',font),('PET_POOL',pool),('PET_END',poolend)]:glyph=glyph.replace(k,str(v))
    marker='local function capture(name)\n'
    if runner.LUA_TEMPLATE.count(marker)!=1:raise ValueError('040 tournament observation anchor')
    runner.LUA_TEMPLATE=runner.LUA_TEMPLATE.replace(marker,code+glyph+marker+' dumpRollPet(name)\n',1).replace('local function finish()\n',"local function finish()\n dumpTournament()\n dumpRollPet('final')\n",1)
    rc=runner.main();out=Path(arg('--out'));r=read(out/'result.json');r.update(scope='DIAGNOSTIC registration flag92 READ alias only inside original49708; actual PET/caller/mode/loader/reader retained. NOT natural registration; actual040 Korean consumption requires verifier.',release_eligible=False,state_intervention=True,natural_acquisition_verified=False,normal_play_checkpoint_eligible=False);
    if (out/'checkpoint.mss').exists():(out/'checkpoint.mss').rename(out/'diagnostic_checkpoint.mss')
    r['artifacts']={p.name:sha(p.read_bytes()) for p in out.iterdir() if p.is_file() and p.name!='result.json'};(out/'result.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf8');return rc


if __name__=='__main__':raise SystemExit(main())
