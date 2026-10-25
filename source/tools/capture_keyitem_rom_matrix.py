"""Guarded renderer diagnostic. Read aliases bypass item acquisition only.

Never changes ROM/RAM or native saves; cannot establish normal item routes.
Entry prerequisites: same-ROM normal empty-item lookup evidence, loaded source
header, reader/table identity and native count-byte load; see handoff.
"""
import json,struct,sys
from pathlib import Path
import capture_roll_pet as pet
import capture_keyitem_full_rom as base
import capture_fixedcell_probe as fixed
from build_visibility_poc import ROOT,sha,require_hash
from report_fixedcell_runtime import verify_route
from keyitem_rom_data import verify_final

CASES=[(s,0)for s in list(range(21))+list(range(32,45))]+[(s,255)for s in [6,7,16,17,18]]

def main():
    global CASES
    if '--quantity-only' in sys.argv:
        sys.argv.remove('--quantity-only');CASES=[(s,c)for c in [0,255]for s in [6,7,16,17,18]]
    def value(k):return sys.argv[sys.argv.index(k)+1]
    evidence=Path(value('--lookup-evidence'));i=sys.argv.index('--lookup-evidence');del sys.argv[i:i+2]
    rp=Path(value('--rom'));m=json.loads(rp.with_suffix('.json').read_text());require_hash(rp,m['output_sha256']);rom=rp.read_bytes()
    verify_route(evidence,m['output_sha256'],set());k=m['keyitem_rom'];root=0x08000000+k['rom_offset'];blob=rom[k['rom_offset']:k['rom_offset']+k['rom_bytes']]
    source=ROOT/json.loads((ROOT/'project.json').read_text())['source_profile']['filename'];require_hash(source,m['source_sha256']);original=source.read_bytes();verify_final(original,rom,k)
    if original[0x30314:0x3031a]!=bytes.fromhex('085c004200bd'):raise ValueError('native count instruction')
    obs=json.loads((evidence/'step_002_keyitem.json').read_text());ram=(evidence/'step_002_gbaExtWorkRam.bin').read_bytes()
    if struct.unpack_from('<I',ram,0xFA50)[0]!=root or not any(c['script']==32 and c['root']==0x02020800 and c['lr']==0x0803497F for c in obs['lookups']):raise ValueError('normal selector precondition evidence')
    if original[0x516ba:0x516c4]!=bytes.fromhex('013880004c30285803e0'):raise ValueError('native printBuffer1 load')
    targets=[dict(script=s,count=c,offset=struct.unpack_from('<H',blob,s*2)[0])for s,c in CASES]
    table='{'+','.join('{script=%d,count=%d,offset=%d}'%(x['script'],x['count'],x['offset'])for x in targets)+'}'
    pet.PROBE+=f'''
local matrixCases={table};local matrixIndex=0;local countAliases=0;local matrixRows={{}}
emu.addMemoryCallback(function(address,value)
 local s=emu.getState()
 if address=={root+64} and value=={struct.unpack_from('<H',blob,64)[0]} and s['cpu.pipeline.execute.address']==0x0804FB76 and s['cpu.r0']=={root} and s['cpu.r1']==64 and s['cpu.r5']==0x0200FA20 then
  matrixIndex=matrixIndex+1;if matrixIndex>#matrixCases then error('unexpected additional lookup') end
  local c=matrixCases[matrixIndex]
  matrixRows[#matrixRows+1]=string.format('{{"entry":%d,"script":%d,"count":%d,"offset":%d,"frame":%d}}',matrixIndex,c.script,c.count,c.offset,frame)
  return c.offset
 end
end,emu.callbackType.read,{root+64},{root+65})
emu.addMemoryCallback(function(address,value)
 local s=emu.getState();local c=matrixCases[matrixIndex]
 if c and s['cpu.pipeline.execute.address']==0x080516C0 and address==0x0200FA6C and s['cpu.r5']==0x0200FA20 and s['cpu.r0']==0x4c and s['cpu.r4']>={root} and s['cpu.r4']<{root+k['rom_bytes']} and emu.read(s['cpu.r4'],emu.memType.gbaMemory)==0xf9 and emu.read(s['cpu.r4']+1,emu.memType.gbaMemory)==3 and emu.read(s['cpu.r4']+3,emu.memType.gbaMemory)==1 then
  countAliases=countAliases+1;return c.count
 end
end,emu.callbackType.read,0x0200FA6C,0x0200FA6F)
local function dumpKeyMatrix(name)
 write(name..'_key_matrix.json','{{"entries":['..table.concat(matrixRows,',')..'],"count_aliases":'..countAliases..'}}')
end
'''
    marker='local function capture(name)\n'
    if fixed.runner.LUA_TEMPLATE.count(marker)!=1:raise ValueError('diagnostic anchor')
    fixed.runner.LUA_TEMPLATE=fixed.runner.LUA_TEMPLATE.replace(marker,marker+' dumpKeyMatrix(name)\n',1)
    rc=base.main();out=Path(value('--out'));r=json.loads((out/'result.json').read_text());last_path=out/f'step_{len(CASES)*4:03d}_key_matrix.json'
    last=json.loads(last_path.read_text())if last_path.exists()else dict(entries=[],count_aliases=0)
    expected_counts=sum(s in [6,7,16,17,18]for s,c in CASES)
    passed=rc==0 and r['complete'] and len(last['entries'])==len(CASES) and last['count_aliases']==expected_counts
    scope='DIAGNOSTIC: native empty-item selector32 retained; guarded offset-table reads select item descriptions; guarded printBuffer1 word reads supply0/255 after native count gating. No ROM/RAM/save write. Not acquisition, inventory count/gating, item-selection caller, other02031000 route, or native portrait-context proof.'
    r.update(scope=scope,normal_play_checkpoint_eligible=False)
    if (out/'checkpoint.mss').exists():
        (out/'checkpoint.mss').rename(out/'diagnostic_checkpoint.mss');r['artifacts']['diagnostic_checkpoint.mss']=r['artifacts'].pop('checkpoint.mss')
    if not passed:r['complete']=False
    (out/'result.json').write_text(json.dumps(r,indent=2),encoding='utf8')
    (out/'key_matrix_environment.json').write_text(json.dumps(dict(passed=passed,scope=scope,rom_sha256=m['output_sha256'],buffer_read=0x0200FA6C,buffer_load_pc=0x080516C0,cases=targets,self_sha256=sha(Path(__file__).read_bytes()),lookup_evidence=str(evidence),lookup_sha256=sha((evidence/'step_002_keyitem.json').read_bytes()),**last),indent=2)+'\n',encoding='utf8')
    return 0 if passed else 1
if __name__=='__main__':raise SystemExit(main())
