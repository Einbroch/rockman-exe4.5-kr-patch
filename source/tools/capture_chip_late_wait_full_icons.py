"""Maximum changing 56 cells with every icon present; verify icon RAM maps."""
import json
from pathlib import Path
from collections import Counter
import capture_chip_burst_changing as burst
from build_visibility_poc import sha


def main():
    matrix = burst.changing.word.matrix
    fixed = matrix.library.fixed
    if (fixed.value('--hangul'), fixed.value('--icons')) != ('56','7'):
        raise ValueError('full-icon changing workload requires 56/7')
    m = json.loads(Path(fixed.value('--rom')).with_suffix('.json').read_text())
    e = m['chip_library_extension']['late_wait']
    matrix.PROBE = matrix.replace_once(matrix.PROBE,
        "if not c then error('copy return without entry') end", 'if not c then return end')
    fixture = matrix.FIXTURE
    fixture = matrix.replace_once(fixture, 'local stressDesc=nil', 'local stressDesc=nil\nlocal stressEpoch=0\nlocal iconMaps=0\nlocal postIcons=0\nlocal lateSkips=0')
    fixture = matrix.replace_once(fixture, 'local v=row*8+col', 'local v=row*8+col\n if stressEpoch%2==0 then return v+56 end')
    fixture = matrix.replace_once(fixture, 'stressDesc=timingGroup.descriptor', 'stressEpoch=stressEpoch+1\n stressDesc=timingGroup.descriptor')
    fixture += f'''
local function iconWord(a) return emu.read(a,emu.memType.gbaMemory)+256*emu.read(a+1,emu.memType.gbaMemory) end
emu.addMemoryCallback(function()
 local s=emu.getState();local tile=(s['cpu.r6']-0x06004000)/32
 if s['cpu.r7']<0 or s['cpu.r7']>6 then stressFail('icon map row') end
 for i=0,3 do if iconWord(s['cpu.r2']+i*2)~=0x4000+tile+i then stressFail('native icon RAM map') end end
 iconMaps=iconMaps+1
end,emu.callbackType.exec,0x0804304E,0x0804304E)
emu.addMemoryCallback(function()
 for row=0,6 do for col=0,7 do
  local index=stressIndex(row,col)
  if bytesAt(0x06008040+row*512+col*64,64)~=bytesAt(FONT_START+index*64,64) or iconWord(0x06008E40+row*16+col*2)~=index+1 then stressFail('full icon glyph/tag residency') end
 end end
 postIcons=postIcons+1
end,emu.callbackType.exec,0x08042C26,0x08042C26)
emu.addMemoryCallback(function()
 local s=emu.getState()
 if s['cpu.r10']~={e['context']} or emu.read(0x04000004,emu.memType.gbaMemory)%2~=1 or iconWord({e['counter']})~=1 or iconWord({e['threshold']})~=1 then stressFail('full-icon wait decision') end
 lateSkips=lateSkips+1
end,emu.callbackType.exec,{e['skip_address']},{e['skip_address']})
local oldFullDump=dumpStress
dumpStress=function(name)
 oldFullDump(name)
 write(name..'_full_icons.json',string.format('{{"epochs":%d,"icon_maps":%d,"post_icon_checks":%d,"late_skips":%d}}',stressEpoch,iconMaps,postIcons,lateSkips))
end
'''
    matrix.FIXTURE = fixture
    rc = burst.burst_main()
    out = Path(fixed.value('--out'))
    d = json.loads((out / 'final_timing.json').read_text())
    c = json.loads((out / 'final_full_icons.json').read_text())
    n = len(d['groups'])
    valid = rc == 0 and n > 100 and len(d['copies']) == 56*n and len(d['icons']) == 7*n
    valid = valid and all(g['copies'] == 56 and g['rows'] == 7 for g in d['groups'])
    valid = valid and c['epochs'] == c['post_icon_checks'] == n and c['icon_maps'] == 7*n
    gaps = Counter(b['start']['frame']-a['start']['frame'] for a,b in zip(d['groups'],d['groups'][1:]))
    scope = 'DIAGNOSTIC changing 56 glyphs with 7 icons every group; actual native icon RAM maps and post-icon glyph/tag residency'
    r = json.loads((out / 'result.json').read_text())
    r['scope'] = scope
    if not valid:
        r['complete'] = False
    (out / 'result.json').write_text(json.dumps(r, indent=2), encoding='utf-8')
    (out / 'full_icons_environment.json').write_text(json.dumps({'tool_sha256': sha(Path(__file__).read_bytes()),
        'rom_sha256': m['output_sha256'], 'scope':scope, 'passed':valid, 'observed':c,
        'cadence_frames':dict(gaps), 'cadence_all_one':dict(gaps)=={1:n-1}}, indent=2), encoding='utf-8')
    print('full-icon changing data:',valid,'groups:',n,'cadence:',dict(gaps),'observed:',c)
    return rc if valid else 1


if __name__ == '__main__':
    raise SystemExit(main())
