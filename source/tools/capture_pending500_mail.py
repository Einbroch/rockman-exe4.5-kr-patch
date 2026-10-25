"""Quarantined native-loader/table aliases for pending500 display diagnostics."""
import json,struct,sys
from pathlib import Path
import run_mesen_segment as runner
from build_visibility_poc import ROOT,sha,require_hash
from verify_tpi_index import lz77_decompress

def main():
    def value(k):return sys.argv[sys.argv.index(k)+1]
    index=int(value('--navi-index'));i=sys.argv.index('--navi-index');del sys.argv[i:i+2]
    script=int(value('--body-script'));i=sys.argv.index('--body-script');del sys.argv[i:i+2]
    if (index,script) not in ((25,33),(27,33),(28,38),(25,61),(25,63),(27,34),(27,35),(27,37),(27,38),(27,42),(27,51),(26,41),(26,49),(26,55),(28,36),(24,33)):raise ValueError('explicit diagnostic population')
    rp=Path(value('--rom'));m=json.loads(rp.with_suffix('.json').read_text(encoding='utf8'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes()
    bodyptr=struct.unpack_from('<I',rom,0x405F8+index*4)[0]
    headerptr=struct.unpack_from('<I',rom,0x4057C+index*4)[0]
    original=lz77_decompress(rom,bodyptr-0x08000000)[0]
    guard=next(g for g in m['keyitem_rom']['mission_guards'] if g['guard_header_hex']==original[:16].hex())
    root=guard['clone_address'];raw=rom[root-0x08000000:root-0x08000000+guard['payload_bytes']]
    first,selected=[struct.unpack_from('<H',raw,n*2)[0] for n in (0,script)]
    setup=index in (25,26)
    alias_address=root+64 if setup else root
    alias_value=struct.unpack_from('<H',raw,64)[0] if setup else first
    alias_pc=0x0804FD20 if setup else 0x0804FB76
    alias_index=64 if setup else 0
    priorbody=struct.unpack_from('<I',rom,0x405F8)[0];priorheader=struct.unpack_from('<I',rom,0x4057C)[0]
    extra=f'''
local hAliases=0;local bAliases=0;local sAliases=0;local selectedRoots=0
emu.addMemoryCallback(function(address,value)
 local s=emu.getState()
 if value=={priorheader} and s['cpu.pipeline.execute.address']==0x08040550 then hAliases=hAliases+1;return {headerptr} end
end,emu.callbackType.read,0x0804057C,0x0804057F)
emu.addMemoryCallback(function(address,value)
 local s=emu.getState()
 if value=={priorbody} and s['cpu.pipeline.execute.address']==0x0804055E then bAliases=bAliases+1;return {bodyptr} end
end,emu.callbackType.read,0x080405F8,0x080405FB)
emu.addMemoryCallback(function(address,value)
 local s=emu.getState()
 if s['cpu.pipeline.execute.address']==0x0804FB76 and s['cpu.r0']=={root} then
  selectedRoots=selectedRoots+1
 end
end,emu.callbackType.read,{root},{root+1})
emu.addMemoryCallback(function(address,value)
 local s=emu.getState()
 if sAliases==0 and s['cpu.pipeline.execute.address']=={alias_pc} and s['cpu.r0']=={root} and s['cpu.r1']=={alias_index} and value=={alias_value} then
  sAliases=sAliases+1;return {selected}
 end
end,emu.callbackType.read,{alias_address},{alias_address+1})
local function dumpPending(name)
 write(name..'_pending500_alias.json','{{"header_aliases":'..hAliases..',"body_aliases":'..bAliases..',"script_aliases":'..sAliases..',"selected_roots":'..selectedRoots..',"root":{root},"script":{script},"navi_index":{index}}}')
 local b={{}};for n=0,{len(original)-1} do b[#b+1]=string.char(emu.read(0x0202B2F4+n,emu.memType.gbaMemory)) end
 write(name..'_native_body.bin',table.concat(b))
end
'''
    runner.LUA_TEMPLATE=runner.LUA_TEMPLATE.replace('local function capture(name)\n',extra+'local function capture(name)\n dumpPending(name)\n',1)
    runner.LUA_TEMPLATE=runner.LUA_TEMPLATE.replace('local function finish()\n',"local function finish()\n dumpPending('final')\n",1)
    rc=runner.main();out=Path(value('--out'));r=json.loads((out/'result.json').read_text(encoding='utf8'))
    receipt=json.loads((out/'final_pending500_alias.json').read_text(encoding='utf8'))
    resident=(out/'final_native_body.bin').read_bytes()==original
    passed=rc==0 and resident and receipt['body_aliases']>0 and receipt['header_aliases']>0 and receipt['script_aliases']==1 and receipt['selected_roots']>0
    r.update(scope='DIAGNOSTIC native loader/table read aliases; native RAM body retained and guarded ROM root selected. NOT natural mission acquisition/reward/save verification.',normal_play_checkpoint_eligible=False,pending500_diagnostic=receipt,native_body_resident_exact=resident,entry_script0_setup_preserved=setup,complete=passed)
    if (out/'checkpoint.mss').exists():(out/'checkpoint.mss').rename(out/'diagnostic_checkpoint.mss')
    r['artifacts']={p.name:sha(p.read_bytes()) for p in out.iterdir() if p.is_file() and p.name!='result.json'}
    (out/'result.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('Pending500 diagnostic',passed,receipt,'native RAM',resident)
    return 0 if passed else 1

if __name__=='__main__':raise SystemExit(main())
