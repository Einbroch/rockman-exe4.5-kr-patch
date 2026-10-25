"""Read-only native equipment root/script/consumer calls and fixed-cell stage."""
import capture_fixedcell_probe as fixed

EXTRA=r'''
local equipmentRoots={}
emu.addMemoryCallback(function()
 local s=emu.getState()
 equipmentRoots[#equipmentRoots+1]=string.format('{"frame":%d,"root":%d,"script":%d,"stage":%d,"target":%d,"width":%d,"height":%d,"font":%d,"lr":%d}',frame,s['cpu.r0'],s['cpu.r1'],s['cpu.r2'],s['cpu.r3'],s['cpu.r4'],s['cpu.r5'],s['cpu.r6'],s['cpu.r14'])
end,emu.callbackType.exec,0x080554A4,0x080554A4)
local function dumpEquipment(name)
 write(name..'_equipment_roots.json','{"calls":['..table.concat(equipmentRoots,',')..']}')
end
'''
def main():
    fixed.PROBE+=EXTRA
    marker='local function capture(name)\n'
    if fixed.runner.LUA_TEMPLATE.count(marker)!=1:raise ValueError('capture anchor')
    fixed.runner.LUA_TEMPLATE=fixed.runner.LUA_TEMPLATE.replace(marker,marker+' dumpEquipment(name)\n',1)
    return fixed.main()

if __name__=='__main__':raise SystemExit(main())
