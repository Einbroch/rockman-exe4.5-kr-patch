"""Diagnostic changing-name and alternating-icon workload; no product edits."""
import json
from pathlib import Path
from collections import Counter
import capture_chip_wordcopy_matrix as word
from build_visibility_poc import sha


def main():
    matrix = word.matrix
    fixed = matrix.library.fixed
    if fixed.value('--hangul') != '56' or fixed.value('--icons') != '7':
        raise ValueError('changing fixture requires 56/7 base options')
    matrix.PROBE = matrix.replace_once(matrix.PROBE,
        "if not c then error('copy return without entry') end", 'if not c then return end')
    fixture = matrix.FIXTURE
    fixture = matrix.replace_once(fixture, 'local stressDesc=nil', 'local stressDesc=nil\nlocal stressEpoch=0\nlocal stressIconStart=0\nlocal stressLifetime=0')
    fixture = matrix.replace_once(fixture, 'local v=row*8+col', 'local v=row*8+col\n if stressEpoch%2==0 then return v+56 end')
    fixture = matrix.replace_once(fixture, 'stressDesc=timingGroup.descriptor', 'stressEpoch=stressEpoch+1\n stressIconStart=#timingIcons\n stressDesc=timingGroup.descriptor')
    fixture = matrix.replace_once(fixture, 'local off=(address-stressDesc)%4',
        'local off=(address-stressDesc)%4\n if pc==0x0804302C and off==3 and stressEpoch%2==0 then stressReads=stressReads+1;return 0 end')
    fixture += r'''
-- Check residency after the entire standard-tab update, including icon work.
emu.addMemoryCallback(function()
 if #timingIcons-stressIconStart~=(stressEpoch%2==1 and 7 or 0) then stressFail('alternating icon count') end
 for row=0,6 do for col=0,7 do
  local index=stressIndex(row,col)
  if bytesAt(0x06008040+row*512+col*64,64)~=bytesAt(FONT_START+index*64,64) then stressFail('post-icon glyph residency') end
  local at=0x06008E40+row*16+col*2
  if emu.read(at,emu.memType.gbaMemory)+256*emu.read(at+1,emu.memType.gbaMemory)~=index+1 then stressFail('post-icon cache tag') end
 end end
 stressLifetime=stressLifetime+1
end,emu.callbackType.exec,0x08042C26,0x08042C26)
local oldChangingDump=dumpStress
dumpStress=function(name)
 oldChangingDump(name)
 write(name..'_changing.json',string.format('{"epochs":%d,"post_icon_checks":%d}',stressEpoch,stressLifetime))
end
'''
    matrix.FIXTURE = fixture
    rc = word.main()
    out = Path(fixed.value('--out'))
    d = json.loads((out / 'final_timing.json').read_text())
    c = json.loads((out / 'final_changing.json').read_text())
    n = len(d['groups'])
    valid = rc == 0 and n > 100 and c == {'epochs': n, 'post_icon_checks': n}
    valid = valid and all(g['copies'] == 56 and g['rows'] == 7 for g in d['groups'])
    valid = valid and len(d['copies']) == 56*n and len(d['icons']) == ((n+1)//2)*7
    scope = 'DIAGNOSTIC every group alternates 56 glyphs (A:0..54,11171; B:56..111) and 7/0 icons; not normal gameplay or full icon visibility QA'
    r = json.loads((out / 'result.json').read_text())
    r['scope'] = scope
    if not valid:
        r['complete'] = False
    (out / 'result.json').write_text(json.dumps(r, indent=2), encoding='utf-8')
    gaps = Counter(b['start']['frame']-a['start']['frame'] for a,b in zip(d['groups'],d['groups'][1:]))
    (out / 'changing_environment.json').write_text(json.dumps({'tool_sha256': sha(Path(__file__).read_bytes()),
        'scope': scope, 'passed': valid, 'groups': n, 'cadence_frames': dict(gaps),
        'cadence_all_one': dict(gaps) == {1:n-1}}, indent=2), encoding='utf-8')
    print('changing fixture:', valid, 'groups:', n, 'frame intervals:', dict(gaps))
    return rc if valid else 1


if __name__ == '__main__':
    raise SystemExit(main())
