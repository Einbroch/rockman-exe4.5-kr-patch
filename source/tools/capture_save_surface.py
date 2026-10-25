"""Read-only save title ROM copy and existing fixed-cell observations."""
import capture_fixedcell_probe as fixed
TITLE=r'''
local titleReads={};local titleTotal=0
emu.addMemoryCallback(function(address,value)
 titleTotal=titleTotal+1;if #titleReads>=128 then return end
 local s=emu.getState()
 titleReads[#titleReads+1]=string.format('{"address":%d,"value":%d,"pc":%d,"r0":%d,"r1":%d,"r2":%d,"lr":%d,"frame":%d}',address,value or -1,s['cpu.r15'],s['cpu.r0'],s['cpu.r1'],s['cpu.r2'],s['cpu.r14'],frame)
end,emu.callbackType.read,0x086333A4,0x086334A3)
local function dumpSaveTitle(name)
 write(name..'_save_title.json',string.format('{"observer_only":true,"read_events":%d,"first_reads":[%s]}',titleTotal,table.concat(titleReads,',')))
end
'''

def main():
    fixed.PROBE+=TITLE
    marker='local function capture(name)\n'
    if fixed.runner.LUA_TEMPLATE.count(marker)!=1:raise ValueError('title observer anchor')
    fixed.runner.LUA_TEMPLATE=fixed.runner.LUA_TEMPLATE.replace(marker,marker+' dumpSaveTitle(name)\n',1)
    return fixed.main()

if __name__=='__main__':raise SystemExit(main())
