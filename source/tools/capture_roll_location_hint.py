"""Quarantined EE33 target-read alias20->23; native jump/clear/render only."""
import json,sys
from pathlib import Path
import capture_roll_pet as normal
from build_visibility_poc import ROOT,sha,require_hash

GUARDS=[(0x50E38,0x50E54,'f322433561c94d9769f5390616c42877af74cbc5b11055c7f72df17081f6d12a'),(0x4FD18,0x4FD60,'ec8df6aca0af0c5abaae83554790d2e2f00b96167661ef5a23cefd80cd110524'),(0x5543C,0x55468,'05e0403aa9e6bb0ddc0e46be2210fc94f1e5464b18b52de4809e02ac7f17e8ac'),(0x92C,0x94C,'ee9354a91556dcf269e9aaf3c00f56abc966e4a1e749f342972f576c0c2a85d8')]

def main():
    args=sys.argv
    def value(key):return args[args.index(key)+1]
    rp=Path(value('--rom'));m=json.loads(rp.with_suffix('.json').read_text());require_hash(rp,m['output_sha256']);rom=rp.read_bytes()
    for start,end,digest in GUARDS:
        if sha(rom[start:end])!=digest:raise ValueError('native jump/clear guard')
    ar=next(x for x in m['archives'] if x['archive']=='65FF3C');pool=0x08000000+ar['rom_offset'];end=pool+ar['compiled_bytes']
    normal.ARCHIVE='65FF3C'
    normal.PROBE+=f'''
local hintAliases=0;local hintJumps=0;local hintClears={{}};local hintArmed=false
emu.addMemoryCallback(function(address,value)
 local s=emu.getState();local p=s['cpu.r4']
 if hintAliases==0 and s['cpu.pipeline.execute.address']==0x08050E40 and s['cpu.r5']==0x0200FA20 and p>={pool} and p<{end} and address==p+s['cpu.r0'] and value==20 and emu.read(p,emu.memType.gbaMemory)==0xEE and emu.read(p+1,emu.memType.gbaMemory)==0x33 then
  hintAliases=hintAliases+1;return 23
 end
end,emu.callbackType.read,{pool},{end-1})
emu.addMemoryCallback(function()
 local s=emu.getState()
 if hintAliases==1 and s['cpu.r1']==23 and s['cpu.r5']==0x0200FA20 then hintJumps=hintJumps+1;hintArmed=true end
end,emu.callbackType.exec,0x0804FD18,0x0804FD18)
emu.addMemoryCallback(function()
 local s=emu.getState();if not hintArmed or s['cpu.r5']~=0x0200FA20 then return end
 local dirty=0
 for i=0,0xEFF do
  if emu.read(0x02012F50+i,emu.memType.gbaMemory)~=0 then dirty=dirty+1 end
  if emu.read(0x02013E50+i,emu.memType.gbaMemory)~=0 then dirty=dirty+1 end
 end
 hintClears[#hintClears+1]=string.format('{{"frame":%d,"nonzero_bytes":%d,"row":%d,"x":%d,"checked_bytes":7680}}',frame,dirty,emu.read(0x0200FA2F,emu.memType.gbaMemory),emu.read(0x0200FA90,emu.memType.gbaMemory))
 hintArmed=false
end,emu.callbackType.exec,0x08055454,0x08055454)
local function dumpHint(name)
 write(name..'_location_hint.json','{{"aliases":'..hintAliases..',"jumps":'..hintJumps..',"clears":['..table.concat(hintClears,',')..']}}')
end
'''
    for old,new in [('local function capture(name)\n','local function capture(name)\n dumpHint(name)\n'),('local function finish()\n',"local function finish()\n dumpHint('final')\n")]:
        if normal.runner.LUA_TEMPLATE.count(old)!=1:raise ValueError('hint capture anchor')
        normal.runner.LUA_TEMPLATE=normal.runner.LUA_TEMPLATE.replace(old,new,1)
    rc=normal.main();out=Path(value('--out'));r=json.loads((out/'result.json').read_text());d=json.loads((out/'final_location_hint.json').read_text())
    passed=rc==0 and r['complete'] and d['aliases']==1 and d['jumps']==1 and len(d['clears'])==1 and all(c['nonzero_bytes']==0 and c['row']==0 and c['x']==0 for c in d['clears'])
    scope='DIAGNOSTIC native EE33 target byte-read alias20->23 only. Native random outcome, preceding lucky-item page, jump, staging clear and glyph renderer retained. No observer RAM/ROM writes. NOT normal location selection or item acquisition evidence.'
    r.update(scope=scope,normal_play_checkpoint_eligible=False)
    if (out/'checkpoint.mss').exists():
        (out/'checkpoint.mss').rename(out/'diagnostic_checkpoint.mss');r['artifacts']['diagnostic_checkpoint.mss']=r['artifacts'].pop('checkpoint.mss')
    if not passed:r['complete']=False
    (out/'result.json').write_text(json.dumps(r,indent=2),encoding='utf-8')
    (out/'hint_environment.json').write_text(json.dumps({'passed':passed,'scope':scope,'rom_sha256':m['output_sha256'],'tool_sha256':sha(Path(__file__).read_bytes()),'observer_sha256':sha(Path(normal.__file__).read_bytes()),'native_guards':GUARDS,**d},indent=2),encoding='utf-8')
    print('hint diagnostic',passed,d);return 0 if passed else 1

if __name__=='__main__':raise SystemExit(main())
