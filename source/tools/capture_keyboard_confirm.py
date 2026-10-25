"""Observe native Yes/No branch, caller registers and destination; no mutation."""
import json,sys
from pathlib import Path
import capture_keyboard_native as native
from build_visibility_poc import sha

def main():
    code=r'''
local confirms={}
local function cfHex(a,n)
 local t={};for i=0,n-1 do t[#t+1]=string.format('%02x',emu.read(a+i,emu.memType.gbaMemory)) end;return table.concat(t)
end
for _,pc in ipairs({0x08034F84,0x08034F8C,0x08034F92,0x08034FA0,0x08034FA4,0x08034FA8,0x08034FB0,0x08034FB2,0x08035000,0x08035030}) do
 emu.addMemoryCallback(function()
  assert(#confirms<10000,'confirm observer overflow');local s=emu.getState()
  confirms[#confirms+1]=string.format('{"frame":%d,"pc":%d,"r0":%d,"r1":%d,"r2":%d,"r3":%d,"r4":%d,"r5":%d,"sp":%d,"lr":%d,"ui_hex":"%s","editor_hex":"%s","record_hex":"%s"}',frame,pc,s['cpu.r0'],s['cpu.r1'],s['cpu.r2'],s['cpu.r3'],s['cpu.r4'],s['cpu.r5'],s['cpu.r13'],s['cpu.r14'],cfHex(s['cpu.r5'],16),cfHex(0x0200FC40,96),cfHex(0x020010A6,10))
 end,emu.callbackType.exec,pc,pc)
end
local function dumpConfirm(name)
 write(name..'_confirm.json','{"events":['..table.concat(confirms,',')..']}')
end
'''
    anchor='local function capture(name)\n'
    if native.runner.LUA_TEMPLATE.count(anchor)!=1:raise ValueError('capture anchor')
    native.runner.LUA_TEMPLATE=native.runner.LUA_TEMPLATE.replace(anchor,code+anchor+' dumpConfirm(name)\n',1)
    rc=native.main();out=Path(sys.argv[sys.argv.index('--out')+1])
    (out/'confirm_environment.json').write_text(json.dumps(dict(observer_only=True,no_RAM_or_save_injection=True,
        tool_sha256=sha(Path(__file__).read_bytes()),native_observer_sha256=sha(Path(native.__file__).read_bytes()),
        limits=['Native Japanese normal confirmation route only; no Hangul hook or save/fresh-load.']),indent=2),encoding='utf8')
    return rc

if __name__=='__main__':raise SystemExit(main())
