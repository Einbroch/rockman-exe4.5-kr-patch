"""Observe the real nested4F7B6->4FB4C ABI and source F000/EDFF controls."""
from build_visibility_poc import ROOT,sha
from cumulative_batch500 import frozen_write
src=ROOT/'tools/capture_communication038_v1.py';dst=ROOT/'tools/capture_communication038_v2.py'
if dst.exists():raise ValueError('Preserve communication nested trace')
text=src.read_text(encoding='utf8')
extra=r'''
local commNested={};local commCommands={}
emu.addMemoryCallback(function()
 local s=emu.getState()
 if s['cpu.r0']==0x02024000 then
  commNested[#commNested+1]=string.format('{"frame":%d,"root":%d,"script":%d,"lr":%d,"sp":%d,"saved_outer_lr":%d}',frame,s['cpu.r0'],s['cpu.r1'],s['cpu.r14'],s['cpu.r13'],c32(s['cpu.r13']+16))
 end
end,emu.callbackType.exec,0x0804FB4C,0x0804FB4C)
for _,pc in ipairs({0x08051098,0x08050754}) do
 emu.addMemoryCallback(function()
  local s=emu.getState()
  if s['cpu.r4']>=0x02024000 and s['cpu.r4']<0x02026000 then
   commCommands[#commCommands+1]=string.format('{"frame":%d,"pc":%d,"stream":%d,"context":%d,"op":%d,"arg":%d}',frame,pc,s['cpu.r4'],s['cpu.r5'],emu.read(s['cpu.r4'],emu.memType.gbaMemory),emu.read(s['cpu.r4']+1,emu.memType.gbaMemory))
  end
 end,emu.callbackType.exec,pc,pc)
end
'''
anchor='local function dumpCommunication()\n'
if text.count(anchor)!=1:raise ValueError('Nested communication trace anchor')
text=text.replace(anchor,extra+anchor+" write('communication_nested.json','{\"calls\":['..table.concat(commNested,',')..'],\"commands\":['..table.concat(commCommands,',')..']}')\n",1)
dst.write_text(text,encoding='utf8')
frozen_write(ROOT/'tools/specs/communication_trace038_v2_version.json',dict(base=str(src.relative_to(ROOT)),base_sha256=sha(src.read_bytes()),output=str(dst.relative_to(ROOT)),output_sha256=sha(dst.read_bytes()),scope='Read-only actual038 nested common initializer entry and native zero-speed/visible-hold execution.4F7B6 does call4FB4C; existing038 descriptor domain rejects communication root, but common entry is shared. No039 code/ROM proof.'))
print('Prepared nested original communication initializer trace')
