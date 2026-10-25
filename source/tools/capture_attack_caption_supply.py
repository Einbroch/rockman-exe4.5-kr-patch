"""Read-only caption VRAM write provenance, no text/CPU/state injection."""
import capture_equipment_guides as guides
EXTRA=r'''
local captionWrites={};local captionWriteTotal=0;local captionLoads={};local captionPending=nil;local captionOutputs={}
emu.addMemoryCallback(function()
 local s=emu.getState();if s['cpu.r0']==0x08512FA0 then captionPending={target=s['cpu.r1'],frame=frame} end
end,emu.callbackType.exec,0x080EC158,0x080EC158)
emu.addMemoryCallback(function()
 if captionPending==nil then return end
 local data={};for i=0,1155 do data[#data+1]=string.char(emu.read(captionPending.target+i,emu.memType.gbaMemory)) end
 local name=string.format('caption_decompressed_%03d.bin',#captionOutputs+1);write(name,table.concat(data))
 captionOutputs[#captionOutputs+1]=string.format('{"frame":%d,"target":%d,"file":"%s"}',captionPending.frame,captionPending.target,name);captionPending=nil
end,emu.callbackType.exec,0x08029190,0x08029190)
emu.addMemoryCallback(function()
 local s=emu.getState();if s['cpu.r1']~=0x06013C00 then return end
 local rows={};for i=0,255 do rows[#rows+1]=string.format('%02x',emu.read(s['cpu.r0']+i,emu.memType.gbaMemory)) end
 captionLoads[#captionLoads+1]=string.format('{"frame":%d,"source":%d,"target":%d,"lr":%d,"prefix_hex":"%s"}',frame,s['cpu.r0'],s['cpu.r1'],s['cpu.r14'],table.concat(rows))
end,emu.callbackType.exec,0x080EC154,0x080EC154)
for _,site in ipairs({0x080EC140,0x080EC158}) do
 emu.addMemoryCallback(function()
  local s=emu.getState();local target=s['cpu.r1']
  if target~=0x06013C00 and not(site==0x080EC158 and target>=0x02000000 and target<0x02040000) then return end
  local rows={};for i=0,95 do rows[#rows+1]=string.format('%02x',emu.read(s['cpu.r0']+i,emu.memType.gbaMemory)) end
  local caller=0;for i=0,3 do caller=caller+emu.read(s['cpu.r13']+16+i,emu.memType.gbaMemory)*2^(i*8) end
  captionLoads[#captionLoads+1]=string.format('{"site":%d,"frame":%d,"source":%d,"target":%d,"r2":%d,"lr":%d,"outer_lr_at_sp16":%d,"prefix_hex":"%s"}',site,frame,s['cpu.r0'],target,s['cpu.r2'],s['cpu.r14'],caller,table.concat(rows))
 end,emu.callbackType.exec,site,site)
end
emu.addMemoryCallback(function(address,value)
 captionWriteTotal=captionWriteTotal+1;if #captionWrites>=80 then return end
 local s=emu.getState();local r={};for i=0,14 do r[#r+1]=tostring(s['cpu.r'..i]) end
 captionWrites[#captionWrites+1]=string.format('{"address":%d,"value":%d,"frame":%d,"pc":%d,"regs":[%s]}',address,value or -1,frame,s['cpu.pipeline.execute.address'],table.concat(r,','))
end,emu.callbackType.write,0x06013C00,0x06013EFF)
local function dumpCaption(name)
 write(name..'_caption_supply.json',string.format('{"total":%d,"outputs":[%s],"loads":[%s],"writes":[%s]}',captionWriteTotal,table.concat(captionOutputs,','),table.concat(captionLoads,','),table.concat(captionWrites,',')))
end
'''
def main():
    fixed=guides.labels.fixed;fixed.PROBE+=EXTRA
    marker='local function capture(name)\n';fixed.runner.LUA_TEMPLATE=fixed.runner.LUA_TEMPLATE.replace(marker,marker+' dumpCaption(name)\n',1)
    return guides.main()
if __name__=='__main__':raise SystemExit(main())
