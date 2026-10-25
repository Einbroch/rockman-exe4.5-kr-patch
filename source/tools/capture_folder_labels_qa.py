"""Read-only native equipment-title reads and isolated folder-header lookup."""
import capture_chip_folder_qa as folder

EXTRA=r'''
local titleReads={};local titleTotal=0;local folderHeaderCalls={}
emu.addMemoryCallback(function(address,value)
 titleTotal=titleTotal+1
 if #titleReads>=64 then return end
 local s=emu.getState()
 titleReads[#titleReads+1]=string.format('{"address":%d,"value":%d,"frame":%d,"pc":%d,"r0":%d,"r1":%d}',address,value or -1,frame,s['cpu.pipeline.execute.address'],s['cpu.r0'],s['cpu.r1'])
end,emu.callbackType.read,0x086330A4,0x086331A3)
emu.addMemoryCallback(function()
 local s=emu.getState()
 if s['cpu.r3']~=0x06007C00 then return end
 folderHeaderCalls[#folderHeaderCalls+1]=string.format('{"frame":%d,"root":%d,"script":%d,"stage":%d,"target":%d,"width":%d,"height":%d,"font":%d,"tint":%d,"lr":%d}',frame,s['cpu.r0'],s['cpu.r1'],s['cpu.r2'],s['cpu.r3'],s['cpu.r4'],s['cpu.r5'],s['cpu.r6'],s['cpu.r7'],s['cpu.r14'])
end,emu.callbackType.exec,0x080554A4,0x080554A4)
local function dumpFolderLabels(name)
 write(name..'_folder_labels.json',string.format('{"title_read_events":%d,"title_first_reads":[%s],"header_calls":[%s]}',titleTotal,table.concat(titleReads,','),table.concat(folderHeaderCalls,',')))
end
'''

def main():
    fixed=folder.frozen.library.fixed;fixed.PROBE+=EXTRA
    marker='local function capture(name)\n'
    if fixed.runner.LUA_TEMPLATE.count(marker)!=1:raise ValueError('folder label capture anchor')
    fixed.runner.LUA_TEMPLATE=fixed.runner.LUA_TEMPLATE.replace(marker,marker+' dumpFolderLabels(name)\n',1)
    return folder.main()

if __name__=='__main__':raise SystemExit(main())
