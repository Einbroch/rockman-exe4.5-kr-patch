"""Read-only normal route call/cache observations; no state intervention."""
import capture_profile_cache_writers_029 as cache
import run_mesen_segment as runner

def main():
    code=cache.PROBE+r'''
local lifecycle={}
for _,pc in ipairs({0x080309EE,0x080309F2,0x08038A9E,0x08038B94,0x08051DD4,0x080517D0}) do
 emu.addMemoryCallback(function()
  local s=emu.getState()
  lifecycle[#lifecycle+1]=string.format('{"frame":%d,"pc":%d,"lr":%d,"r0":%d,"r4":%d,"r5":%d,"r10":%d}',frame,pc,s['cpu.r14'],s['cpu.r0'],s['cpu.r4'],s['cpu.r5'],s['cpu.r10'])
 end,emu.callbackType.exec,pc,pc)
end
local function dumpLifecycle(name)
 write(name..'_profile_lifecycle.json','{"events":['..table.concat(lifecycle,',')..']}')
end
'''
    anchor='local function capture(name)\n'
    if runner.LUA_TEMPLATE.count(anchor)!=1:raise ValueError('029 lifetime anchor')
    runner.LUA_TEMPLATE=runner.LUA_TEMPLATE.replace(anchor,code+anchor+' dumpProfileCache(name)\n dumpLifecycle(name)\n',1)
    return runner.main()

if __name__=='__main__':raise SystemExit(main())
