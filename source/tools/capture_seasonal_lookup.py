"""Read-only NumberMan seasonal root lookup context; no diagnostic mutation."""
import capture_roll_pet as pet

if __name__=='__main__':
    pet.ARCHIVE='68BBB4'
    pet.PROBE+=r'''
local seasonalReads={}
emu.addMemoryCallback(function(address,value)
 local s=emu.getState()
 seasonalReads[#seasonalReads+1]=string.format('{"frame":%d,"address":%d,"value":%d,"pc":%d,"r0":%d,"r1":%d,"r2":%d,"r3":%d,"r5":%d}',frame,address,value,s['cpu.pipeline.execute.address'],s['cpu.r0'],s['cpu.r1'],s['cpu.r2'],s['cpu.r3'],s['cpu.r5'])
end,emu.callbackType.read,0x080382AC,0x080382AF)
local function dumpSeasonalLookup(name)
 write(name..'_seasonal_lookup.json','{"reads":['..table.concat(seasonalReads,',')..']}')
end
'''
    marker='local function capture(name)\n'
    if pet.runner.LUA_TEMPLATE.count(marker)!=1:raise ValueError('capture anchor')
    pet.runner.LUA_TEMPLATE=pet.runner.LUA_TEMPLATE.replace(marker,marker+' dumpSeasonalLookup(name)\n',1)
    anchor='local function finish()\n'
    if pet.runner.LUA_TEMPLATE.count(anchor)!=1:raise ValueError('finish anchor')
    pet.runner.LUA_TEMPLATE=pet.runner.LUA_TEMPLATE.replace(anchor,anchor+" dumpSeasonalLookup('final')\n",1)
    raise SystemExit(pet.main())
