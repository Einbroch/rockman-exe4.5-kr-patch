"""Compose frozen alternating fixture with native icon-map set/clear checks."""
import json
from pathlib import Path
import capture_chip_late_wait_changing as late
from build_visibility_poc import sha


def main():
    burst = late.burst
    original = burst.burst_main
    matrix = burst.changing.word.matrix
    fixed = matrix.library.fixed

    def observed_main():
        matrix.FIXTURE += r'''
local iconSetRows=0
local iconClearRows=0
local iconMapReturns=0
local function mapWord(a) return emu.read(a,emu.memType.gbaMemory)+256*emu.read(a+1,emu.memType.gbaMemory) end
emu.addMemoryCallback(function()
 local s=emu.getState();local tile=(s['cpu.r6']-0x06004000)/32
 if s['cpu.r7']<0 or s['cpu.r7']>6 then stressFail('icon clear row index') end
 for i=0,3 do
  local expected=stressEpoch%2==1 and (0x4000+tile+i) or 0
  if mapWord(s['cpu.r2']+i*2)~=expected then stressFail('native alternating icon map set/clear') end
 end
 if stressEpoch%2==1 then iconSetRows=iconSetRows+1 else iconClearRows=iconClearRows+1 end
end,emu.callbackType.exec,0x0804304E,0x0804304E)
emu.addMemoryCallback(function()
 if iconSetRows+iconClearRows~=stressEpoch*7 then stressFail('icon map update denominator') end
 iconMapReturns=iconMapReturns+1
end,emu.callbackType.exec,0x08042C26,0x08042C26)
local oldIconClearDump=dumpStress
dumpStress=function(name)
 oldIconClearDump(name)
 write(name..'_icon_clear.json',string.format('{"set_rows":%d,"clear_rows":%d,"post_updates":%d}',iconSetRows,iconClearRows,iconMapReturns))
end
'''
        return original()

    burst.burst_main = observed_main
    rc = late.main()
    out = Path(fixed.value('--out'))
    d = json.loads((out / 'final_timing.json').read_text())
    c = json.loads((out / 'final_icon_clear.json').read_text())
    n = len(d['groups'])
    valid = rc == 0 and n > 100 and c == {'set_rows':((n+1)//2)*7,'clear_rows':(n//2)*7,'post_updates':n}
    r = json.loads((out / 'result.json').read_text())
    r['scope'] += '; native RAM icon-map four-entry set/clear verified per row'
    if not valid:
        r['complete'] = False
    (out / 'result.json').write_text(json.dumps(r,indent=2),encoding='utf-8')
    (out / 'icon_clear_environment.json').write_text(json.dumps({'tool_sha256':sha(Path(__file__).read_bytes()),
        'rom_sha256':r['rom_sha256'],'passed':valid,'observed':c,
        'scope':'diagnostic native RAM map set/clear; no scanout tearing or audio claim'},indent=2),encoding='utf-8')
    print('native icon-map set/clear:',valid,c)
    return rc if valid else 1


if __name__ == '__main__':
    raise SystemExit(main())
