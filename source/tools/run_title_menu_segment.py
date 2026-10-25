"""Read-only native title decompressor/VRAM transfer observer with normal input."""
import run_mesen_segment as runner

OBSERVER = r'''
emu.addMemoryCallback(function()
 local st=emu.getState()
 if st['cpu.r6']==0x0802910C and st['cpu.r4']==0 then
  local bytes={}
  for i=0,1667 do bytes[#bytes+1]=string.char(emu.read(st['cpu.r5']+i,emu.memType.gbaMemory)) end
  write('native_title_decompressed.bin',table.concat(bytes))
 end
end,emu.callbackType.exec,0x08029190,0x08029190)
emu.addMemoryCallback(function()
 local st=emu.getState()
 if st['cpu.r6']==0x0802910C and st['cpu.r4']==0 then
  write('native_title_copy.json',string.format('{"source":%d,"destination":%d,"bytes":%d}',st['cpu.r0'],st['cpu.r1'],st['cpu.r2']))
 end
end,emu.callbackType.exec,0x080291A0,0x080291A0)
'''

if __name__ == '__main__':
    runner.LUA_TEMPLATE = runner.LUA_TEMPLATE.replace('local fontHits={}', OBSERVER+'\nlocal fontHits={}', 1)
    raise SystemExit(runner.main())
