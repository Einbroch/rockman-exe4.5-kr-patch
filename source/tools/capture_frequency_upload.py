"""Read-only write-site/register trace for the frequency OBJ residency window."""
import json
from pathlib import Path
import run_mesen_segment as runner
from build_visibility_poc import sha

EXTRA=r'''
local uploads={};local uploadKeys={};local frequencyLoads={}
local function bytesAt(a,n)
 local t={};for i=0,n-1 do t[#t+1]=string.char(emu.read(a+i,emu.memType.gbaMemory)) end
 return table.concat(t)
end
emu.addMemoryCallback(function()
 local s=emu.getState()
 if s['cpu.r0']~=0x0863673C then return end
 frequencyLoads[#frequencyLoads+1]={frame=frame,source=s['cpu.r0'],stage=s['cpu.r5'],table=s['cpu.r6'],targets=s['cpu.r7'],index=s['cpu.r4']}
end,emu.callbackType.exec,0x0802918A,0x0802918A)
emu.addMemoryCallback(function()
 local s=emu.getState()
 if s['cpu.r1']~=0x06013800 then return end
 local c=frequencyLoads[#frequencyLoads]
 if c==nil or c.frame~=frame then error('unbound frequency copy') end
 c.copy_source=s['cpu.r0'];c.copy_target=s['cpu.r1'];c.bytes=s['cpu.r2']
 if c.bytes~=1280 then error('frequency extent') end
 write(string.format('frequency_%04d_decompressed.bin',#frequencyLoads),bytesAt(c.stage,1284))
end,emu.callbackType.exec,0x080291A0,0x080291A0)
local function observeUpload(a,v)
 local s=emu.getState();local pc=s['cpu.pipeline.execute.address']
 local key=tostring(frame)..':'..tostring(pc)..':'..tostring(math.floor(a/65536))
 if uploadKeys[key] then return end
 uploadKeys[key]=true
 if #uploads>=1000 then error('upload trace overflow') end
 local regs={}
 for i=0,15 do regs[#regs+1]=tostring(s['cpu.r'..i]) end
 uploads[#uploads+1]=string.format('{"frame":%d,"address":%d,"value":%d,"pc":%d,"registers":[%s]}',frame,a,v or -1,pc,table.concat(regs,','))
end
emu.addMemoryCallback(observeUpload,emu.callbackType.write,0x06013800,0x06013CFF)
emu.addMemoryCallback(observeUpload,emu.callbackType.write,0x0201B800,0x0201BCFF)
local function dumpUploads(name)
 write(name..'_frequency_uploads.json','{"observer_only":true,"events":['..table.concat(uploads,',')..']}')
 local rows={}
 for _,c in ipairs(frequencyLoads) do
 rows[#rows+1]=string.format('{"frame":%d,"source":%d,"stage":%d,"table":%d,"targets":%d,"index":%d,"copy_source":%d,"copy_target":%d,"bytes":%d}',c.frame,c.source,c.stage,c.table,c.targets,c.index,c.copy_source or 0,c.copy_target or 0,c.bytes or 0)
 end
 write(name..'_frequency_loads.json','{"observer_only":true,"loads":['..table.concat(rows,',')..']}')
end
'''

def main():
    marker='local function capture(name)\n'
    if runner.LUA_TEMPLATE.count(marker)!=1:raise ValueError('capture anchor')
    runner.LUA_TEMPLATE=runner.LUA_TEMPLATE.replace(marker,EXTRA+marker+' dumpUploads(name)\n',1)
    rc=runner.main()
    import sys
    out=Path(sys.argv[sys.argv.index('--out')+1])
    (out/'frequency_upload_environment.json').write_text(json.dumps({
        'observer_only':True,'self_sha256':sha(Path(__file__).read_bytes()),
        'runner_sha256':sha(Path(runner.__file__).read_bytes()),
        'watch':[[0x06013800,0x06013CFF],[0x0201B800,0x0201BCFF]],
        'limits':'One first write per frame/PC; no source or loader identity claim yet.'},indent=2),encoding='utf-8')
    return rc

if __name__=='__main__':raise SystemExit(main())
