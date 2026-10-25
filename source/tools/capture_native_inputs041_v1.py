"""Read actual hardware key register on own040; preserve native consumer observer."""
import capture_native_consumers041_v1 as base


def main():
    code=r'''
local hardwareInputs041={}
emu.addMemoryCallback(function(address,value)
 if ready and not final and #hardwareInputs041<10000 then
  local s=emu.getState()
  hardwareInputs041[#hardwareInputs041+1]=string.format('{"frame":%d,"address":%d,"value":%d,"pc":%d}',frame,address,value,s['cpu.pipeline.execute.address'])
 end
end,emu.callbackType.read,0x04000130,0x04000131)
local function dumpHardwareInputs041()
 write('hardware_inputs041.json','{"reads":['..table.concat(hardwareInputs041,',')..']}')
end
'''
    anchor='local function capture(name)\n'
    if base.runner.LUA_TEMPLATE.count(anchor)!=1:raise ValueError('041 input observer anchor')
    base.runner.LUA_TEMPLATE=base.runner.LUA_TEMPLATE.replace(anchor,code+anchor,1).replace('local function finish()\n','local function finish()\n dumpHardwareInputs041()\n',1)
    return base.main()


if __name__=='__main__':raise SystemExit(main())
