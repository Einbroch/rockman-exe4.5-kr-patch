"""Bounded read-only main-loop wait tracing around first four name groups."""
import json
from pathlib import Path
import capture_chip_wordcopy_matrix as word
from build_visibility_poc import sha, require_hash

TRACE = r'''
local waitGroup=0
local waitRows={}
local function waitRead32(a)
 local v=0
 for i=0,3 do v=v+emu.read(a+i,emu.memType.gbaMemory)*2^(8*i) end
 return v
end
local function waitRecord(pc)
 if waitGroup<1 or waitGroup>4 then return end
 if #waitRows>=500 then stressFail('wait trace overflow') end
 local s=emu.getState()
 waitRows[#waitRows+1]=string.format('{"pc":%d,"group":%d,"clock":%d,"frame":%d,"scanline":%d,"cycle":%d,"raw_0200F9F0":%d,"raw_02010210":%d}',pc,waitGroup,s.masterClock,s['ppu.frameCount'],s['ppu.scanline'],s['ppu.cycle'],waitRead32(0x0200F9F0),waitRead32(0x02010210))
end
emu.addMemoryCallback(function() waitGroup=waitGroup+1;waitRecord(0x08042E50) end,emu.callbackType.exec,0x08042E50,0x08042E50)
for _,pc in ipairs({0x08042F12,0x0800025C,0x08000260,0x08000264,0x080002B4,0x080002D2,0x080002D6,0x08000344,0x08000350,0x08000360,0x08000374,0x08000380}) do
 emu.addMemoryCallback(function() waitRecord(pc) end,emu.callbackType.exec,pc,pc)
end
local previousDumpTiming=dumpTiming
dumpTiming=function(name)
 previousDumpTiming(name)
 write(name..'_wait_trace.json','{"events":['..table.concat(waitRows,',')..']}')
end
'''


def main():
    # Exact low-ROM instruction sites, not a whole-ROM control-flow claim.
    fixed = word.matrix.library.fixed
    rom = Path(fixed.value('--rom'))
    data = rom.read_bytes()
    config = json.loads((word.matrix.ROOT / 'project.json').read_text(encoding='utf-8'))
    source_path = word.matrix.ROOT / config['source_profile']['filename']
    require_hash(source_path, config['source_profile']['sha256'])
    source = source_path.read_bytes()
    if data[0x244:0x388] != source[0x244:0x388]:
        raise ValueError('main-loop trace scope changed')
    word.matrix.PROBE += TRACE
    rc = word.main()
    out = Path(fixed.value('--out'))
    (out / 'wait_trace_environment.json').write_text(json.dumps({'tool_sha256': sha(Path(__file__).read_bytes()),
        'main_loop_sha256': sha(data[0x244:0x388]), 'scope': 'read-only first four name groups; fixture remains diagnostic'}, indent=2), encoding='utf-8')
    return rc


if __name__ == '__main__':
    raise SystemExit(main())
