"""Read-only temporal ordering of folder initialization and first name rows."""
import json
from pathlib import Path
import capture_chip_folder_lifetime_v2 as lifetime
from build_visibility_poc import sha


def main():
    fixed=lifetime.base.consumer.base.library.fixed
    fixed.PROBE+=r'''
local initSequence=0
local initRows=0
local initWrites=0
local initLastWrite=nil
local initEvents={}
local function initEvent(label)
 local s=emu.getState();initSequence=initSequence+1
 initEvents[#initEvents+1]=string.format('{"sequence":%d,"label":"%s","frame":%d,"pc":%d,"writes_so_far":%d,"r0":%d,"r1":%d,"r2":%d,"r5":%d,"sp":%d,"lr":%d}',initSequence,label,frame,s['cpu.pipeline.execute.address'],initWrites,s['cpu.r0'],s['cpu.r1'],s['cpu.r2'],s['cpu.r5'],s['cpu.r13'],s['cpu.r14'])
end
for _,entry in ipairs({{0x0803D878,'folder-init-entry'},{0x0803D8E6,'after-three-asset-loads'},
                      {0x0803D8FC,'before-list-function'},{0x0803D900,'after-list-function'},
                      {0x0803D97C,'folder-init-exit'}}) do
 local pc=entry[1];local label=entry[2]
 emu.addMemoryCallback(function() initEvent(label) end,emu.callbackType.exec,pc,pc)
end
emu.addMemoryCallback(function()
 initRows=initRows+1
 if initRows<=7 then initEvent('first-seven-name-row') end
end,emu.callbackType.exec,0x0803CBB0,0x0803CBB0)
emu.addMemoryCallback(function(address,value)
 initWrites=initWrites+1
 local s=emu.getState()
 initLastWrite=string.format('{"frame":%d,"pc":%d,"address":%d}',frame,s['cpu.pipeline.execute.address'],address)
end,emu.callbackType.write,0x06008040,0x06008EAF)
local function dumpInit(name)
 write(name..'_folder_init.json',string.format('{"rows":%d,"private_bank_writes":%d,"last_write":%s,"events":[%s]}',initRows,initWrites,initLastWrite or 'null',table.concat(initEvents,',')))
end
'''
    for old,new in [('local function capture(name)\n','local function capture(name)\n dumpInit(name)\n'),
                    ('local function finish()\n',"local function finish()\n dumpInit('final')\n")]:
        if fixed.runner.LUA_TEMPLATE.count(old)!=1:
            raise ValueError('folder init capture anchor drift')
        fixed.runner.LUA_TEMPLATE=fixed.runner.LUA_TEMPLATE.replace(old,new,1)
    rc=lifetime.main()
    out=Path(fixed.value('--out'))
    (out/'folder_init_environment.json').write_text(json.dumps({'tool_sha256':sha(Path(__file__).read_bytes()),
        'scope':'read-only initializer/asset/name temporal ordering; no reset installed'},indent=2),encoding='utf-8')
    print('folder init sequence recorded')
    return rc


if __name__=='__main__':
    raise SystemExit(main())
