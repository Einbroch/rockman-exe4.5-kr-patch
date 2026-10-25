"""Observe actual guarded wait decisions while the changing fixture runs."""
import json
from pathlib import Path
import capture_chip_burst_changing as burst
from capture_chip_wait_trace import TRACE
from build_visibility_poc import sha


def main():
    changing = burst.changing
    matrix = changing.word.matrix
    fixed = matrix.library.fixed
    m = json.loads(Path(fixed.value('--rom')).with_suffix('.json').read_text())
    e = m['chip_library_extension']['late_wait']
    matrix.PROBE += TRACE + f'''
local lateWaitSkips=0
emu.addMemoryCallback(function()
 local s=emu.getState();local c={e['context']}
 local root=waitRead32(c);local menu=waitRead32(c+0x34)
 if s['cpu.r10']~=c or emu.read(root,emu.memType.gbaMemory)~=28 or emu.read(menu,emu.memType.gbaMemory)~=8 or emu.read(menu+1,emu.memType.gbaMemory)~=4 or emu.read(0x04000004,emu.memType.gbaMemory)%2~=1 or waitRead32({e['counter']})~=1 or waitRead32({e['threshold']})~=1 then stressFail('late-wait decision guard mismatch') end
 lateWaitSkips=lateWaitSkips+1
end,emu.callbackType.exec,{e['skip_address']},{e['skip_address']})
local oldLateDump=dumpTiming
dumpTiming=function(name)
 oldLateDump(name)
 write(name..'_late_wait.json',string.format('{{"eligible_skips":%d}}',lateWaitSkips))
end
'''
    changing.word.main = burst.burst_main
    rc = changing.main()
    out = Path(fixed.value('--out'))
    (out / 'late_wait_environment.json').write_text(json.dumps({'tool_sha256': sha(Path(__file__).read_bytes()),
        'rom_sha256': m['output_sha256'], 'scope': 'actual late-wait guards and native frame waits; diagnostic changing cells'}, indent=2), encoding='utf-8')
    return rc


if __name__ == '__main__':
    raise SystemExit(main())
