"""Read-only quantity getter observations before another qualified alias attempt."""
import capture_native_consumers041_v1 as base


def main():
    code=r'''
local itemGetter041={}
local function getterWord041(a) local v=0;for j=0,3 do v=v+emu.read(a+j,emu.memType.gbaMemory)*2^(8*j) end;return v end
for _,pc in ipairs({0x080302F8,0x08030300,0x08030314,0x0803031A}) do
 emu.addMemoryCallback(function()
  if #itemGetter041>=500 then error('041 getter observation budget') end
  local s=emu.getState()
  itemGetter041[#itemGetter041+1]=string.format('{"frame":%d,"pc":%d,"r0":%d,"r1":%d,"r2":%d,"lr":%d,"sp":%d,"stack0":%d,"stack4":%d}',frame,pc,s['cpu.r0'],s['cpu.r1'],s['cpu.r2'],s['cpu.r14'],s['cpu.r13'],getterWord041(s['cpu.r13']),getterWord041(s['cpu.r13']+4))
 end,emu.callbackType.exec,pc,pc)
end
local function dumpGetter041()
 write('item_getter041.json','{"events":['..table.concat(itemGetter041,',')..']}')
end
'''
    anchor='local function capture(name)\n'
    base.runner.LUA_TEMPLATE=base.runner.LUA_TEMPLATE.replace(anchor,code+anchor,1).replace('local function finish()\n','local function finish()\n dumpGetter041()\n',1)
    return base.main()


if __name__=='__main__':raise SystemExit(main())
