"""Normal-input cache/ABI checks plus guarded wait decisions."""
import json
from pathlib import Path
import capture_chip_copy_variant_qa as variant
from build_visibility_poc import sha


def main():
    cache = variant.cache
    fixed = cache.word.base.library.fixed
    m = json.loads(Path(fixed.value('--rom')).with_suffix('.json').read_text())
    e = m['chip_library_extension']['late_wait']
    proof = next(p for p in m['chip_library_extension']['machine_code'] if p['address'] == 0x08000000+e['offset'])
    bx = [i['address'] for i in proof['instructions'] if i['mnemonic'] == 'bx' and i['operands'] == 'r3']
    if len(bx) != 2:
        raise ValueError('wait call boundaries changed')
    cache.word.base.PROBE += f'''
local lateEligible=0
local lateFallback=0
local lateConsumed=0
local function lateRead32(a)
 local v=0;for i=0,3 do v=v+emu.read(a+i,emu.memType.gbaMemory)*2^(8*i) end;return v
end
emu.addMemoryCallback(function()
 local s=emu.getState();local root=lateRead32({e['context']});local menu=lateRead32({e['context']+0x34})
 if s['cpu.r10']~={e['context']} or emu.read(root,emu.memType.gbaMemory)~=28 or emu.read(menu,emu.memType.gbaMemory)~=8 or emu.read(menu+1,emu.memType.gbaMemory)~=4 or emu.read(0x04000004,emu.memType.gbaMemory)%2~=1 or lateRead32({e['counter']})~=1 or lateRead32({e['threshold']})~=1 then error('normal late wait guard mismatch') end
 lateEligible=lateEligible+1
end,emu.callbackType.exec,{e['skip_address']},{e['skip_address']})
emu.addMemoryCallback(function()
 if math.floor(emu.getState()['cpu.r14']/2)*2=={bx[0]+2} then lateFallback=lateFallback+1 end
end,emu.callbackType.exec,0x08000374,0x08000374)
emu.addMemoryCallback(function()
 if math.floor(emu.getState()['cpu.r14']/2)*2=={bx[1]+2} then lateConsumed=lateConsumed+1 end
end,emu.callbackType.exec,0x08000344,0x08000344)
local oldLateNormalDump=dumpChipKo
dumpChipKo=function(name)
 oldLateNormalDump(name)
 write(name..'_late_wait_normal.json',string.format('{{"eligible_skips":%d,"normal_waits":%d,"wait_next_calls":%d}}',lateEligible,lateFallback,lateConsumed))
end
'''
    cache.word.main = variant.variant_main
    rc = cache.main()
    out = Path(fixed.value('--out'))
    d = json.loads((out / 'final_late_wait_normal.json').read_text())
    valid = rc == 0 and d['wait_next_calls'] == d['eligible_skips'] + d['normal_waits'] and d['normal_waits'] > 0
    (out / 'late_wait_normal_environment.json').write_text(json.dumps({'tool_sha256': sha(Path(__file__).read_bytes()),
        'rom_sha256': m['output_sha256'], 'passed': valid, 'observed': d,
        'scope': 'normal input; each taken skip verifies active library, VBlank, exact single pending frame'}, indent=2), encoding='utf-8')
    return rc if valid else 1


if __name__ == '__main__':
    raise SystemExit(main())
