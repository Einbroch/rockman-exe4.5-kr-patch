"""Read-only alternate eight-cell name parser probe; missing hits are not PASS."""
import json
from pathlib import Path
import capture_library_qa as library
from build_visibility_poc import sha

PROBE = r'''
local otherActive=nil
local otherRows={}
local otherSeen={}
local otherCalls=0
local rootCalls=0
local function otherWord(a) return emu.read(a,emu.memType.gbaMemory)+256*emu.read(a+1,emu.memType.gbaMemory) end
local function otherFail(s) write('other_consumer_failed.txt',s);emu.stop(1);error(s) end
emu.addMemoryCallback(function() rootCalls=rootCalls+1 end,emu.callbackType.exec,0x0801F7D4,0x0801F7D4)
emu.addMemoryCallback(function()
 if otherActive then otherFail('nested alternate parser') end
 local s=emu.getState();local bytes={};local top={};local bot={};local n=0
 while n<8 do
  local v=emu.read(s['cpu.r0']+n,emu.memType.gbaMemory)
  if v>=0xE5 then break end
  bytes[#bytes+1]=string.format('%02X',v);top[#top+1]=s['cpu.r6']+v*2;bot[#bot+1]=s['cpu.r6']+v*2+1;n=n+1
 end
 if emu.read(s['cpu.r0']+n,emu.memType.gbaMemory)~=0xE5 then otherFail('alternate source grammar exceeds eight cells or non-E5 control') end
 while #top<8 do top[#top+1]=0;bot[#bot+1]=0 end
 otherActive={s=s,n=n,text=table.concat(bytes)..'E5',top=top,bot=bot}
end,emu.callbackType.exec,0x0803CBB0,0x0803CBB0)
emu.addMemoryCallback(function()
 local a=otherActive
 if not a then otherFail('alternate return without entry') end
 local s=emu.getState();local b=a.s
 if s['cpu.r0']~=b['cpu.r0']+a.n or s['cpu.r2']~=b['cpu.r2']+16 or s['cpu.r3']~=b['cpu.r3']+16 then otherFail('alternate parser cursor ABI') end
 for _,r in ipairs({4,6,7,13,14}) do if s['cpu.r'..r]~=b['cpu.r'..r] then otherFail('alternate parser preservation') end end
 for i=0,7 do
  if otherWord(b['cpu.r2']+i*2)~=a.top[i+1] or otherWord(b['cpu.r3']+i*2)~=a.bot[i+1] then otherFail('alternate glyph map/padding') end
 end
 local key=b['cpu.r0']..':'..b['cpu.r2']..':'..b['cpu.r6']
 if otherSeen[key] then otherSeen[key].calls=otherSeen[key].calls+1 else
  local row={stream=b['cpu.r0'],upper=b['cpu.r2'],lower=b['cpu.r3'],base=b['cpu.r6'],caller=b['cpu.r14'],text=a.text,top=hexAt(b['cpu.r2'],16),bottom=hexAt(b['cpu.r3'],16),calls=1}
  otherSeen[key]=row;otherRows[#otherRows+1]=row
 end
 otherCalls=otherCalls+1;otherActive=nil
end,emu.callbackType.exec,0x0803CB7A,0x0803CB7A)
local function dumpOther(name)
 local records={}
 for _,r in ipairs(otherRows) do records[#records+1]=string.format('{"stream":%d,"upper":%d,"lower":%d,"base":%d,"caller":%d,"text_hex":"%s","top_hex":"%s","bottom_hex":"%s","calls":%d}',r.stream,r.upper,r.lower,r.base,r.caller,r.text,r.top,r.bottom,r.calls) end
 write(name..'_other_consumer.json',string.format('{"alternate_calls":%d,"root_selector_calls":%d,"rows":[%s]}',otherCalls,rootCalls,table.concat(records,',')))
end
'''


def main():
    fixed = library.fixed
    fixed.PROBE += PROBE
    for old,new in [('local function capture(name)\n','local function capture(name)\n dumpOther(name)\n'),
                    ('local function finish()\n',"local function finish()\n dumpOther('final')\n")]:
        if fixed.runner.LUA_TEMPLATE.count(old)!=1:
            raise ValueError('consumer capture anchor drift')
        fixed.runner.LUA_TEMPLATE=fixed.runner.LUA_TEMPLATE.replace(old,new,1)
    rc=library.main()
    out=Path(fixed.value('--out'))
    d=json.loads((out/'final_other_consumer.json').read_text())
    (out/'other_consumer_environment.json').write_text(json.dumps({'tool_sha256':sha(Path(__file__).read_bytes()),
        'rom_sha256':json.loads(Path(fixed.value('--rom')).with_suffix('.json').read_text())['output_sha256'],
        'scope':'normal input, read-only alternate source stream/row/padding/ABI observation; no Korean or ownership claim',
        'hit':d['alternate_calls']>0,'root_selector_hit':d['root_selector_calls']>0},indent=2),encoding='utf-8')
    print('alternate consumer hits:',d['alternate_calls'],'root selector:',d['root_selector_calls'])
    return rc


if __name__=='__main__':
    raise SystemExit(main())
