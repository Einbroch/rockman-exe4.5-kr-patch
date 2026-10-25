"""Normal-input cache hit/miss pixel and scene-reset assertions."""
import json
from pathlib import Path
import capture_chip_wordcopy_qa as word
from build_visibility_poc import sha


def main():
    fixed = word.base.library.fixed
    rom = Path(fixed.value('--rom'))
    m = json.loads(rom.with_suffix('.json').read_text(encoding='utf-8'))
    e = m['chip_library_extension']
    cache = e['cache']
    if (cache['tags'], cache['bytes'], cache['reset_continuation']) != (0x06008E40, 112, 0x080427A9):
        raise ValueError('cache observation profile changed')
    code = word.base.PROBE
    old = "if c==nil then error('chip glyph copy returned without entry') end"
    if code.count(old) != 1:
        raise ValueError('cache return anchor changed')
    code = code.replace('local chipKoActive=nil', 'local chipKoActive=nil\nlocal cacheHits=0\nlocal cacheChecks=0\nlocal cacheResets=0')
    code = code.replace(old, """local s=emu.getState()
 local sp=s['cpu.r13'];local stream=0
 for i=0,3 do stream=stream+emu.read(sp+i,emu.memType.gbaMemory)*2^(i*8) end
 local index=chipWord(stream+2)
 local dst=0x06004000+s['cpu.r5']*32
 local tag=0x06008E40+s['cpu.r5']-514
 if index>=11172 or dst<0x06008040 or dst+64>0x06008E40 then error('cache result bounds') end
 if chipWord(tag)~=index+1 or bytesAt(dst,64)~=bytesAt(FONT_START+index*64,64) then error('cache hit/miss pixels or tag mismatch') end
 cacheChecks=cacheChecks+1
 if c==nil then cacheHits=cacheHits+1;return end""")
    code += """
emu.addMemoryCallback(function()
 for i=0,111 do if emu.read(0x06008E40+i,emu.memType.gbaMemory)~=0 then error('cache reset not zero') end end
 cacheResets=cacheResets+1
end,emu.callbackType.exec,0x080427A8,0x080427A8)
local oldCacheDump=dumpChipKo
dumpChipKo=function(name)
 oldCacheDump(name)
 write(name..'_cache.json',string.format('{"hits":%d,"checks":%d,"resets":%d}',cacheHits,cacheChecks,cacheResets))
end
"""
    word.base.PROBE = code
    rc = word.main()
    out = Path(fixed.value('--out'))
    d = json.loads((out / 'final_cache.json').read_text())
    valid = rc == 0 and d['hits'] > 0 and d['resets'] > 0 and d['checks'] > d['hits']
    if not valid:
        r = json.loads((out / 'result.json').read_text())
        r['complete'] = False
        (out / 'result.json').write_text(json.dumps(r, indent=2), encoding='utf-8')
    (out / 'cache_environment.json').write_text(json.dumps({'tool_sha256': sha(Path(__file__).read_bytes()),
        'rom_sha256': m['output_sha256'], 'scope': 'normal input; actual tag reset, hit/miss pixel assertions; timing unverified',
        'passed': valid, 'observed': d}, indent=2), encoding='utf-8')
    return rc if valid else 1


if __name__ == '__main__':
    raise SystemExit(main())
