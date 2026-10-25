"""Read-only bounded cache write/reader trace on an exact-ROM normal route."""
import run_mesen_segment as runner

PROBE=r'''
local cacheSites={}
emu.addMemoryCallback(function(address,value)
 local s=emu.getState();local pc=s['cpu.pipeline.execute.address'];local lr=s['cpu.r14'];local key=tostring(pc)..':'..tostring(lr)
 if cacheSites[key]==nil then
  local rs={};for i=0,14 do rs[#rs+1]=string.format('%d',s['cpu.r'..i]) end
  cacheSites[key]={count=0,pc=pc,lr=lr,first=frame,address=address,value=value,regs=table.concat(rs,',')}
 end
 cacheSites[key].count=cacheSites[key].count+1
end,emu.callbackType.write,0x020293E0,0x0202951F)
local function dumpProfileCache(name)
 local rows={};for _,r in pairs(cacheSites) do rows[#rows+1]=string.format('{"pc":%d,"lr":%d,"first_frame":%d,"address":%d,"value":%d,"writes":%d,"first_regs":[%s]}',r.pc,r.lr,r.first,r.address,r.value,r.count,r.regs) end
 write(name..'_profile_cache_writes.json','{"sites":['..table.concat(rows,',')..']}')
end
'''


def main():
    anchor='local function capture(name)\n'
    if runner.LUA_TEMPLATE.count(anchor)!=1:raise ValueError('029 capture anchor')
    runner.LUA_TEMPLATE=runner.LUA_TEMPLATE.replace(anchor,PROBE+anchor+' dumpProfileCache(name)\n',1)
    return runner.main()


if __name__=='__main__':raise SystemExit(main())
