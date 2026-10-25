"""Read-only normal-handler rank alias: comma to middle dot, glyph diagnostic only."""
import json,struct,sys
from pathlib import Path
from capstone import Cs,CS_ARCH_ARM,CS_MODE_THUMB
import capture_pending500_004_alert as observer
from archive_scripts import script_spans
from build_visibility_poc import require_hash,sha

def main():
    def value(k):return sys.argv[sys.argv.index(k)+1]
    rp=Path(value('--rom'));m=json.loads(rp.with_suffix('.json').read_text(encoding='utf8'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes()
    ar=next(x for x in m['archives'] if x['archive']=='68C2CC');raw=rom[ar['rom_offset']:ar['rom_offset']+ar['compiled_bytes']];span=script_spans(raw,5)[3]
    comma=bytes.fromhex('f9fca42b')
    if span.count(comma)!=1:raise ValueError('Unique existing comma anchor')
    token=0x08000000+ar['rom_offset']+struct.unpack_from('<H',raw,6)[0]+span.index(comma)
    code=m['extension']['machine_code'][0];pc=next(x['address'] for x in code['instructions'] if x['mnemonic']=='ldrb' and x['operands']=='r7, [r4, #2]')
    instruction=list(Cs(CS_ARCH_ARM,CS_MODE_THUMB).disasm(rom[pc-0x08000000:pc-0x08000000+2],pc))
    if len(instruction)!=1 or instruction[0].mnemonic!='ldrb' or instruction[0].op_str!='r7, [r4, #2]':raise ValueError('Final normal handler read boundary')
    extra=f'''
local dotReads=0
emu.addMemoryCallback(function(address,value)
 local s=emu.getState()
 if address=={token+2} and value==164 and s['cpu.pipeline.execute.address']=={pc} and s['cpu.r4']=={token} and s['cpu.r5']==0x0200FA20 then dotReads=dotReads+1;return 165 end
end,emu.callbackType.read,{token+2},{token+2})
local function dumpDot(name)
 write(name..'_middle_dot.json','{{"aliases":'..dotReads..',"stream":{token},"handler_pc":{pc},"source_rank":11172,"target_rank":11173}}')
end
'''
    anchor='local function capture(name)\n';observer.pet.runner.LUA_TEMPLATE=observer.pet.runner.LUA_TEMPLATE.replace(anchor,extra+anchor+' dumpDot(name)\n',1)
    observer.TARGET_ARCHIVE='68C2CC';observer.SCRIPT_COUNT=5;observer.SCRIPTS=(3,);sys.argv+=['--alert-script','3']
    rc=observer.main();out=Path(value('--out'));r=json.loads((out/'result.json').read_text(encoding='utf8'));d=json.loads((out/'step_002_middle_dot.json').read_text(encoding='utf8'))
    r.update(scope='DIAGNOSTIC NumberMan table aliases plus one existing comma rank read changed to middle dot. Glyph-supply evidence only; ROM text unchanged, not a translated literal or gameplay/save claim.',middle_dot_diagnostic=d,complete=r['complete'] and d['aliases']>0)
    (out/'result.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print('Middle-dot glyph alias',r['complete']);return rc if r['complete'] else 1

if __name__=='__main__':raise SystemExit(main())
