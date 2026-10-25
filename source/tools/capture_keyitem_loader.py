"""Read-only trace of the shared key-item archive's native loaders."""
import run_mesen_segment as runner

PROBE = r'''
local keyLoads={}
emu.addMemoryCallback(function()
 local s=emu.getState()
 if s['cpu.r0']~=0x08709408 then return end
 local regs={}
 for i=0,15 do regs[#regs+1]=string.format('"r%d":%d',i,s['cpu.r'..i]) end
 keyLoads[#keyLoads+1]='{"frame":'..frame..',"registers":{'..table.concat(regs,',')..'}}'
end,emu.callbackType.exec,0x080EC158,0x080EC158)
local function dumpKeyLoads(name)
 write(name..'_keyitem_loads.json','{"observer_only":true,"loads":['..table.concat(keyLoads,',')..']}')
end
'''

def main():
    marker='local function capture(name)\n'
    if runner.LUA_TEMPLATE.count(marker)!=1:
        raise ValueError('keyitem observer anchor')
    runner.LUA_TEMPLATE=runner.LUA_TEMPLATE.replace(marker,PROBE+marker+' dumpKeyLoads(name)\n',1)
    return runner.main()

if __name__=='__main__':
    raise SystemExit(main())
