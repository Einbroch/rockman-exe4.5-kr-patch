"""Read-only native keyboard selection/edit/commit boundary observation."""
import json,sys
from pathlib import Path
import run_mesen_segment as runner
from build_visibility_poc import ROOT,sha,require_hash

def main():
    def arg(k):return sys.argv[sys.argv.index(k)+1]
    rp=Path(arg('--rom'));require_hash(rp,arg('--expect-rom-sha256'));m=json.loads(rp.with_suffix('.json').read_text());require_hash(rp,m['output_sha256'])
    profile=json.loads((ROOT/'project.json').read_text())['source_profile'];srcp=ROOT/profile['filename'];require_hash(srcp,profile['sha256']);src=srcp.read_bytes();rom=rp.read_bytes()
    guards=[]
    for a,b in [(0x34fa0,0x35050),(0x32ac6,0x32ad8)]:
        if src[a:b]!=rom[a:b]:raise ValueError('native writer changed')
        guards.append(dict(start=a,end=b,sha256=sha(src[a:b])))
    code=r'''
local keyboardWrites={};local keyboardCalls={}
local function kHex(a,n)
 local rows={};for i=0,n-1 do rows[#rows+1]=string.format('%02x',emu.read(a+i,emu.memType.gbaMemory)) end;return table.concat(rows)
end
local function observeWrite(a,v)
 if #keyboardWrites>=50000 then error('keyboard observation overflow') end
 local s=emu.getState();keyboardWrites[#keyboardWrites+1]=string.format('{"frame":%d,"address":%d,"before":%d,"value":%d,"pc":%d,"r0":%d,"r1":%d,"r2":%d,"r3":%d,"r4":%d,"lr":%d}',frame,a,emu.read(a,emu.memType.gbaMemory),v,s['cpu.pipeline.execute.address'],s['cpu.r0'],s['cpu.r1'],s['cpu.r2'],s['cpu.r3'],s['cpu.r4'],s['cpu.r14'])
end
for _,region in ipairs({{0x0200FC40,0x0200FCBF},{0x02001090,0x020010BF},{0x02014E74,0x02014EB3}}) do
 emu.addMemoryCallback(observeWrite,emu.callbackType.write,region[1],region[2])
end
for _,pc in ipairs({0x08035000,0x08032AC6,0x08035030}) do
 emu.addMemoryCallback(function()
  if #keyboardCalls>=10000 then error('keyboard call overflow') end
  local s=emu.getState();keyboardCalls[#keyboardCalls+1]=string.format('{"frame":%d,"pc":%d,"r0":%d,"r1":%d,"r2":%d,"lr":%d,"edit_hex":"%s","record_window_hex":"%s","temporary_hex":"%s"}',frame,s['cpu.pipeline.execute.address'],s['cpu.r0'],s['cpu.r1'],s['cpu.r2'],s['cpu.r14'],kHex(0x0200FC40,128),kHex(0x02001090,48),kHex(0x02014E74,64))
 end,emu.callbackType.exec,pc,pc)
end
local function dumpKeyboard(name)
 write(name..'_keyboard.json','{"writes":['..table.concat(keyboardWrites,',')..'],"calls":['..table.concat(keyboardCalls,',')..'],"edit_hex":"'..kHex(0x0200FC40,128)..'","record_window_hex":"'..kHex(0x02001090,48)..'","temporary_hex":"'..kHex(0x02014E74,64)..'"}')
end
'''
    anchor='local function capture(name)\n'
    if runner.LUA_TEMPLATE.count(anchor)!=1:raise ValueError('capture anchor')
    runner.LUA_TEMPLATE=runner.LUA_TEMPLATE.replace(anchor,code+anchor+' dumpKeyboard(name)\n',1)
    rc=runner.main();out=Path(arg('--out'))
    (out/'keyboard_environment.json').write_text(json.dumps(dict(observer_only=True,no_RAM_or_save_injection=True,rom_sha256=m['output_sha256'],tool_sha256=sha(Path(__file__).read_bytes()),guards=guards,limits=['Selected windows and observed PCs only, not full field ABI/call graph.','No Hangul or keyboard replacement in this ROM.']),indent=2),encoding='utf8');return rc
if __name__=='__main__':raise SystemExit(main())
