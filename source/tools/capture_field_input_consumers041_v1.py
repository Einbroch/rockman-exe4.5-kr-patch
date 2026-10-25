"""Observe consumers of original input edges on same040 field path, read-only."""
import capture_native_inputs041_v1 as inputs


def main():
    code=r'''
local keyConsumers041={}
emu.addMemoryCallback(function(address,value)
 if ready and not final and frame>=28 and frame<=44 and #keyConsumers041<2000 then
  local s=emu.getState()
  keyConsumers041[#keyConsumers041+1]=string.format('{"frame":%d,"address":%d,"value":%d,"pc":%d,"lr":%d,"r0":%d,"r1":%d,"r2":%d,"r3":%d,"r5":%d}',frame,address,value,s['cpu.pipeline.execute.address'],s['cpu.r14'],s['cpu.r0'],s['cpu.r1'],s['cpu.r2'],s['cpu.r3'],s['cpu.r5'])
 end
end,emu.callbackType.read,0x0200FC20,0x0200FC25)
local function dumpKeyConsumers041()
 write('key_consumers041.json','{"reads":['..table.concat(keyConsumers041,',')..']}')
end
'''
    anchor='local function capture(name)\n'
    if inputs.base.runner.LUA_TEMPLATE.count(anchor)!=1:raise ValueError('041 field key observer anchor')
    inputs.base.runner.LUA_TEMPLATE=inputs.base.runner.LUA_TEMPLATE.replace(anchor,code+anchor,1).replace('local function finish()\n','local function finish()\n dumpKeyConsumers041()\n',1)
    return inputs.main()


if __name__=='__main__':raise SystemExit(main())
