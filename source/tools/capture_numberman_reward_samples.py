"""NumberMan quarantined result-dispatch read aliases; NOT normal awards."""
import argparse,json,struct,sys
from pathlib import Path
import capture_roll_pet as normal
from build_visibility_poc import ROOT,sha,require_hash
from numberman_reward_model import model

def main():
    ap=argparse.ArgumentParser(add_help=False);ap.add_argument('--script',type=int,choices=(16,18,52,53),required=True);args,rest=ap.parse_known_args();sys.argv=[sys.argv[0]]+rest
    def value(key):return rest[rest.index(key)+1]
    rp=Path(value('--rom'));m=json.loads(rp.with_suffix('.json').read_text());require_hash(rp,m['output_sha256']);blob=rp.read_bytes()
    source=ROOT/json.loads((ROOT/'project.json').read_text())['source_profile']['filename'];original=source.read_bytes();proof=model(original)
    # The changed F9 outer table selects the adopted Hangul extension; bonus,
    # legacy decimal, branch and give handlers themselves must stay native.
    for g in proof['native_code_guards']:
        if blob[g['start']:g['end']]!=original[g['start']:g['end']]:raise ValueError('native bonus consumer modified')
    for start,end in [(0x509D0,0x50A00),(0x4FB4C,0x4FC20)]:
        if blob[start:end]!=original[start:end]:raise ValueError('native branch/init modified')
    ar=next(a for a in m['archives'] if a['archive']=='687910');pool=0x08000000+ar['rom_offset'];entry=12 if args.script<50 else 50;branch=2 if args.script in (16,52) else 3
    amount=max(proof['zenny_values'] if branch==2 else proof['bugfrag_values']);offset=struct.unpack_from('<H',blob,ar['rom_offset']+entry*2)[0]
    start=pool+offset;end=pool+struct.unpack_from('<H',blob,ar['rom_offset']+(entry+1)*2)[0]
    normal.ARCHIVE='687910'
    normal.PROBE+=f'''
local aliasInit=0;local aliasGlobals=0;local aliasAmounts=0;local formatterRows={{}};local numericDraws={{}};local numericStart=0;local numericEnd=0
emu.addMemoryCallback(function(address,value)
 local s=emu.getState()
 if aliasInit==0 and address=={pool+24} and s['cpu.pipeline.execute.address']==0x0804FB76 and s['cpu.r0']=={pool} and s['cpu.r1']==24 and s['cpu.r5']==0x0200FA20 then aliasInit=aliasInit+1;return {offset} end
end,emu.callbackType.read,{pool+24},{pool+25})
emu.addMemoryCallback(function(address,value)
 local s=emu.getState()
 if aliasInit==1 and address==0x0200FA6C and s['cpu.pipeline.execute.address']==0x080509DA and s['cpu.r5']==0x0200FA20 and s['cpu.r4']>={start} and s['cpu.r4']<{end} then aliasGlobals=aliasGlobals+1;return {branch} end
end,emu.callbackType.read,0x0200FA6C,0x0200FA6C)
emu.addMemoryCallback(function(address,value)
 local s=emu.getState();local pc=s['cpu.pipeline.execute.address']
 if aliasInit==1 and address==0x0200FA74 and (pc==0x080522BA or pc==0x080523C2 or pc==0x080516C0) and s['cpu.r5']==0x0200FA20 and s['cpu.r4']>={pool} and s['cpu.r4']<{pool+ar['compiled_bytes']} then aliasAmounts=aliasAmounts+1;return {amount} end
end,emu.callbackType.read,0x0200FA74,0x0200FA77)
emu.addMemoryCallback(function()
 local s=emu.getState();if s['cpu.r5']~=0x0200FA20 or s['cpu.r4']<{pool} or s['cpu.r4']>={pool+ar['compiled_bytes']} then return end
 numericStart=s['cpu.r2'];numericEnd=numericStart+{len(str(amount))}
 formatterRows[#formatterRows+1]=string.format('{{"frame":%d,"value":%d,"flags":%d,"buffer":%d,"source":%d}}',frame,s['cpu.r0'],s['cpu.r1'],s['cpu.r2'],s['cpu.r4'])
end,emu.callbackType.exec,0x080516DC,0x080516DC)
emu.addMemoryCallback(function()
 local s=emu.getState();if s['cpu.r4']<numericStart or s['cpu.r4']>=numericEnd or numericStart==0 then return end
 numericDraws[#numericDraws+1]=string.format('{{"frame":%d,"stream":%d,"glyph_index":%d,"offset":%d,"context":%d,"color":%d}}',frame,s['cpu.r4'],s['cpu.r1'],s['cpu.r6'],s['cpu.r5'],emu.read(s['cpu.r5']+0x9c,emu.memType.gbaMemory))
end,emu.callbackType.exec,0x03006AE0,0x03006AE0)
local function dumpReward(name)
 write(name..'_reward.json','{{"entry":{entry},"script":{args.script},"branch":{branch},"amount":{amount},"init_reads":'..aliasInit..',"global_reads":'..aliasGlobals..',"amount_reads":'..aliasAmounts..',"formatters":['..table.concat(formatterRows,',')..'],"digit_draws":['..table.concat(numericDraws,',')..']}}')
end
'''
    for old,new in [('local function capture(name)\n','local function capture(name)\n dumpReward(name)\n'),('local function finish()\n',"local function finish()\n dumpReward('final')\n")]:
        if normal.runner.LUA_TEMPLATE.count(old)!=1:raise ValueError('reward capture anchor')
        normal.runner.LUA_TEMPLATE=normal.runner.LUA_TEMPLATE.replace(old,new,1)
    rc=normal.main();out=Path(value('--out'));route=json.loads((out/'result.json').read_text());d=json.loads((out/'final_reward.json').read_text())
    scope='DIAGNOSTIC native init table-read alias12->12/50, native global5 read alias2/3, buffer3 amount-read alias to native-table maximum; no observer ROM/RAM writes. Native give commands can change diagnostic inventory. NOT minigame completion/recording/awards evidence.'
    route.update(scope=scope,normal_play_checkpoint_eligible=False)
    if (out/'checkpoint.mss').exists():
        (out/'checkpoint.mss').rename(out/'diagnostic_checkpoint.mss');route['artifacts']['diagnostic_checkpoint.mss']=route['artifacts'].pop('checkpoint.mss')
    valid=rc==0 and route['complete'] and d['init_reads']==1 and d['global_reads']>0 and d['amount_reads']>=2 and len(d['formatters'])==1
    if not valid:route['complete']=False
    (out/'result.json').write_text(json.dumps(route,indent=2),encoding='utf-8')
    (out/'reward_environment.json').write_text(json.dumps({'rom_sha256':m['output_sha256'],'tool_sha256':sha(Path(__file__).read_bytes()),'observer_sha256':sha(Path(normal.__file__).read_bytes()),'passed':valid,'scope':scope,'model':proof,**d},indent=2),encoding='utf-8')
    print('bonus diagnostic',args.script,'passed',valid,'read counts',d['init_reads'],d['global_reads'],d['amount_reads'])
    return rc if valid else 1

if __name__=='__main__':raise SystemExit(main())
