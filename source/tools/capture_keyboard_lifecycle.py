"""Observe initialization/import/No/commit without changing ROM or game state."""
import json
import sys
from pathlib import Path
import capture_keyboard_native as native
from build_visibility_poc import sha


def main():
    if '--probe' not in sys.argv or sys.argv[sys.argv.index('--probe') + 1] != 'snapshot':
        raise ValueError('lifecycle evidence requires --probe snapshot')
    code = r'''
local lifecycle={}
local function lHex(a,n)
 local rows={};for i=0,n-1 do rows[#rows+1]=string.format('%02x',emu.read(a+i,emu.memType.gbaMemory)) end;return table.concat(rows)
end
for _,pc in ipairs({0x080355B6,0x080355C4,0x080355F4,0x0803558C,0x080355AA,0x08034E34,0x08035000}) do
 emu.addMemoryCallback(function()
  if pc==0x08034E34 then return end
  if #lifecycle>=10000 then error('lifecycle observation overflow') end
  local s=emu.getState()
  lifecycle[#lifecycle+1]=string.format('{"frame":%d,"pc":%d,"r0":%d,"r1":%d,"r2":%d,"r3":%d,"r4":%d,"r5":%d,"sp":%d,"lr":%d,"edit_hex":"%s","record_hex":"%s"}',frame,pc,s['cpu.r0'],s['cpu.r1'],s['cpu.r2'],s['cpu.r3'],s['cpu.r4'],s['cpu.r5'],s['cpu.r13'],s['cpu.r14'],lHex(0x0200FC40,96),lHex(0x020010A6,10))
 end,emu.callbackType.exec,pc,pc)
end
local function dumpLifecycle(name)
 write(name..'_lifecycle.json','{"events":['..table.concat(lifecycle,',')..']}')
end
'''
    anchor = 'local function capture(name)\n'
    if native.runner.LUA_TEMPLATE.count(anchor) != 1:
        raise ValueError('capture anchor')
    native.runner.LUA_TEMPLATE = native.runner.LUA_TEMPLATE.replace(
        anchor, code + anchor + ' dumpLifecycle(name)\n', 1)
    rc = native.main()
    out = Path(sys.argv[sys.argv.index('--out') + 1])
    (out / 'lifecycle_environment.json').write_text(json.dumps(dict(
        observer_only=True, no_RAM_or_save_injection=True,
        tool_sha256=sha(Path(__file__).read_bytes()),
        native_observer_sha256=sha(Path(native.__file__).read_bytes()),
        limits=['Bounded native initialization/import and weak-subject record path only.',
                'No Hangul integration or complete record-reader/save compatibility claim.']), indent=2), encoding='utf8')
    return rc


if __name__ == '__main__':
    raise SystemExit(main())
