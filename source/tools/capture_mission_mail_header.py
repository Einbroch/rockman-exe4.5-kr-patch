"""Quarantined mission header loader alias; not natural mission acquisition."""
import json,sys,struct
from pathlib import Path
import run_mesen_segment as runner
from build_visibility_poc import ROOT,sha,require_hash
from mission_mail_header import scope
from verify_tpi_index import lz77_decompress

def main():
    def value(k):return sys.argv[sys.argv.index(k)+1]
    rom_path=Path(value('--rom'));m=json.loads(rom_path.with_suffix('.json').read_text(encoding='utf8'))
    require_hash(rom_path,m['output_sha256']);rom=rom_path.read_bytes()
    source=(ROOT/json.loads((ROOT/'project.json').read_text(encoding='utf8'))['source_profile']['filename']).read_bytes()
    scope(source)
    if rom[0x40548:0x40576]!=source[0x40548:0x40576]:raise ValueError('native loader changed')
    target=struct.unpack_from('<I',rom,0x405e8)[0];prior=struct.unpack_from('<I',rom,0x4057c)[0]
    record=next(r for r in m['archives'] if r['archive']=='6DD864')
    payload=lz77_decompress(rom,record['rom_offset'])[0]
    extra=f'''
local missionAliases=0
emu.addMemoryCallback(function(address,value)
 local s=emu.getState()
 if address==0x0804057C and value=={prior} and s['cpu.pipeline.execute.address']==0x08040550 then
  missionAliases=missionAliases+1;return {target}
 end
end,emu.callbackType.read,0x0804057C,0x0804057F)
local function dumpMission(name)
 write(name..'_mission_alias.json','{{"loader_aliases":'..missionAliases..',"native_index":0,"diagnostic_index":27,"selected_pointer":{target}}}')
 local b={{}};for i=0,{len(payload)-1} do b[#b+1]=string.char(emu.read(0x020262F4+i,emu.memType.gbaMemory)) end
 write(name..'_mission_header.bin',table.concat(b))
end
'''
    runner.LUA_TEMPLATE=runner.LUA_TEMPLATE.replace('local function capture(name)\n',extra+'local function capture(name)\n dumpMission(name)\n',1)
    runner.LUA_TEMPLATE=runner.LUA_TEMPLATE.replace('local function finish()\n',"local function finish()\n dumpMission('final')\n",1)
    rc=runner.main();out=Path(value('--out'));result=json.loads((out/'result.json').read_text(encoding='utf8'))
    receipt=json.loads((out/'final_mission_alias.json').read_text(encoding='utf8'))
    resident=(out/'final_mission_header.bin').read_bytes()==payload
    passed=rc==0 and receipt['loader_aliases']>0 and resident
    result.update(scope='DIAGNOSTIC native header pointer-table read alias from Navi0 to Navi27. BIOS loader and RAM header renderer remain native. Body remains Rockman; NOT mission body/acquisition/save evidence.',normal_play_checkpoint_eligible=False,mission_header_diagnostic=receipt,resident_payload_exact=resident,complete=passed)
    if (out/'checkpoint.mss').exists():(out/'checkpoint.mss').rename(out/'diagnostic_checkpoint.mss')
    result['artifacts']={p.name:sha(p.read_bytes()) for p in sorted(out.iterdir()) if p.is_file() and p.name!='result.json'}
    (out/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('Mission header diagnostic:',passed,receipt,'resident',resident)
    return 0 if passed else 1

if __name__=='__main__':raise SystemExit(main())
