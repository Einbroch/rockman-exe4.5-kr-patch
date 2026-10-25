"""Synthetic changing 56-cell folder load; no product or save-memory edits."""
import json
import struct
from collections import Counter
from pathlib import Path
import capture_library_qa as library
from build_visibility_poc import sha,require_hash

PROBE=r'''
local fg=nil;local fr=nil;local fc=nil
local groups={};local copies=0;local epoch=0;local reads=0;local names=0
local firstFailure=nil
local function fail(s) if not firstFailure then firstFailure=s;write('folder_changing_failed.txt',s) end;emu.stop(1);error(s) end
local function index(row,col)
 local v=row*8+col
 if epoch%2==0 then return v+56 end
 if v==55 then return 11171 end
 return v
end
local function word(a) return emu.read(a,emu.memType.gbaMemory)+256*emu.read(a+1,emu.memType.gbaMemory) end
emu.addMemoryCallback(function()
 local s=emu.getState()
 if s['cpu.r2']~=0x0202A680 or s['cpu.r5']~=7 then return end
 if fg then fail('nested folder group') end
 epoch=epoch+1;fg={start=s,rows=0,copies=0,descriptor=s['cpu.r1']+s['cpu.r0']*32}
end,emu.callbackType.exec,0x0803CB20,0x0803CB20)
emu.addMemoryCallback(function(address,value)
 if not fg then return end
 local s=emu.getState()
 if s['cpu.pipeline.execute.address']~=0x0803CB48 then return end
 if address<fg.descriptor+8 or address>=fg.descriptor+224 or (address-fg.descriptor)%32~=8 then fail('descriptor bounds') end
 reads=reads+1;return 128
end,emu.callbackType.read,0x02000000,0x0203FFFF)
emu.addMemoryCallback(function()
 if not fg then return end
 local s=emu.getState()
 if fr then fail('nested folder row') end
 fr={s=s,row=math.floor((s['cpu.r2']-0x0202A680)/32),copies=0}
 if fr.row<0 or fr.row>6 or s['cpu.r1']~=1 then fail('folder row input') end
end,emu.callbackType.exec,INSTALL,INSTALL)
emu.addMemoryCallback(function(address,value)
 if not fr then return end
 local s=emu.getState();local pc=s['cpu.pipeline.execute.address']
 if pc<RENDER_START or pc>=RENDER_END then return end
 local n=address-STREAM
 if n<0 or n>32 then fail('synthetic stream bounds') end
 names=names+1
 if n==32 then return 0xE5 end
 local ix=index(fr.row,math.floor(n/4));local part=n%4
 if part==0 then return 0xF9 elseif part==1 then return 0xFC elseif part==2 then return math.floor(ix%256) else return math.floor(ix/256) end
end,emu.callbackType.read,STREAM,STREAM+32)
emu.addMemoryCallback(function()
 if not fr or fc then fail('copy nesting') end
 fc=emu.getState()
end,emu.callbackType.exec,COPY_ENTRY,COPY_ENTRY)
emu.addMemoryCallback(function()
 if not fc then fail('changing cache hit or missing copy') end
 if bytesAt(fc['cpu.r0'],64)~=bytesAt(fc['cpu.r1'],64) then fail('actual inline copy mismatch') end
 copies=copies+1;fr.copies=fr.copies+1;fg.copies=fg.copies+1;fc=nil
end,emu.callbackType.exec,COPY_RETURN,COPY_RETURN)
emu.addMemoryCallback(function()
 if not fg then return end
 if not fr then fail('row without selector') end
 local s=emu.getState();local b=fr.s;local row=fr.row
 if s['cpu.r0']~=STREAM+32 or s['cpu.r1']~=0xE5 or s['cpu.r2']~=b['cpu.r2']+16 or s['cpu.r3']~=b['cpu.r3']+16 or fr.copies~=8 then fail('changing row ABI/count') end
 if s['cpu.r14']~=0x0803CB7B then fail('selector return LR') end
 for _,r in ipairs({4,6,7,13}) do if s['cpu.r'..r]~=b['cpu.r'..r] then fail('row preservation') end end
 for col=0,7 do
  local top=0x2202+row*16+col*2
  if word(b['cpu.r2']+col*2)~=top or word(b['cpu.r3']+col*2)~=top+1 then fail('changing tile map') end
  if bytesAt(0x06008040+row*512+col*64,64)~=bytesAt(FONT+index(row,col)*64,64) then fail('changing glyph residency') end
  if word(0x06008E40+row*16+col*2)~=index(row,col)+1 then fail('changing tag') end
 end
 fg.rows=fg.rows+1;fr=nil
end,emu.callbackType.exec,0x0803CB7A,0x0803CB7A)
emu.addMemoryCallback(function()
 if not fg then return end
 local s=emu.getState()
 if fr or fc or fg.rows~=7 or fg.copies~=56 then fail(string.format('group denominator rows=%d copies=%d active_row=%s active_copy=%s r9=%d',fg.rows,fg.copies,tostring(fr~=nil),tostring(fc~=nil),s['cpu.r9'])) end
 for row=0,6 do for col=0,7 do
  if bytesAt(0x06008040+row*512+col*64,64)~=bytesAt(FONT+index(row,col)*64,64) then fail('postgroup glyph') end
 end end
 groups[#groups+1]=string.format('{"frame":%d,"scanline":%d,"cycles":%d,"rows":%d,"copies":%d}',fg.start['ppu.frameCount'],fg.start['ppu.scanline'],s.masterClock-fg.start.masterClock,fg.rows,fg.copies)
 fg=nil
end,emu.callbackType.exec,0x0803CB88,0x0803CB88)
local function dumpFolderChanging(name)
 write(name..'_folder_changing.json',string.format('{"groups":[%s],"copies":%d,"descriptor_reads":%d,"name_reads":%d}',table.concat(groups,','),copies,reads,names))
end
'''


def main():
    fixed=library.fixed;rom=Path(fixed.value('--rom')).resolve()
    m=json.loads(rom.with_suffix('.json').read_text());require_hash(rom,m['output_sha256'])
    e=m['chip_folder_extension'];blob=rom.read_bytes();render=e['machine_code'][0]
    loads=[i for i in render['instructions'] if i['mnemonic'] in ('ldm','ldmia')]
    returns=[i['address'] for i in render['instructions'] if i['mnemonic']=='pop' and i['operands']=='{r0, r2, r3}']
    if len(loads)!=3 or len(returns)!=1: raise ValueError('folder inline-copy profile')
    stream=0x08000000+e['clone_offset']+struct.unpack_from('<H',blob,e['clone_offset']+2)[0]
    code=PROBE
    for key,value in {'COPY_ENTRY':loads[0]['address'],'COPY_RETURN':returns[0],
        'RENDER_START':render['address'],'RENDER_END':render['address']+render['code_bytes'],
        'INSTALL':0x08000000+e['install']['offset'],'STREAM':stream,'FONT':0x08000000+e['font_offset']}.items():
        code=code.replace(key,str(value))
    fixed.PROBE+=code
    for old,new in [('local function capture(name)\n','local function capture(name)\n dumpFolderChanging(name)\n'),
                    ('local function finish()\n',"local function finish()\n dumpFolderChanging('final')\n")]:
        if fixed.runner.LUA_TEMPLATE.count(old)!=1: raise ValueError('changing dump anchor')
        fixed.runner.LUA_TEMPLATE=fixed.runner.LUA_TEMPLATE.replace(old,new,1)
    rc=library.main();out=Path(fixed.value('--out'));result=json.loads((out/'result.json').read_text())
    data=json.loads((out/'final_folder_changing.json').read_text()) if (out/'final_folder_changing.json').exists() else {}
    groups=data.get('groups',[]);n=len(groups)
    valid=rc==0 and result['complete'] and not (out/'folder_changing_failed.txt').exists() and n>100 and data.get('copies')==56*n and data.get('descriptor_reads')==7*n
    gaps=Counter(b['frame']-a['frame'] for a,b in zip(groups,groups[1:]))
    scope='DIAGNOSTIC synthetic descriptor and name CPU-read substitution; every group changes 56 Hangul cells; no ROM/RAM/save edits; not product wording or normal play'
    result.update(scope=scope,normal_play_checkpoint_eligible=False)
    if (out/'checkpoint.mss').exists():
        (out/'checkpoint.mss').rename(out/'diagnostic_checkpoint.mss')
        result['artifacts']['diagnostic_checkpoint.mss']=result['artifacts'].pop('checkpoint.mss')
    if not valid: result['complete']=False
    (out/'result.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    (out/'folder_changing_environment.json').write_text(json.dumps({'tool_sha256':sha(Path(__file__).read_bytes()),
        'rom_sha256':m['output_sha256'],'passed':valid,'scope':scope,'groups':n,'cadence_frames':dict(gaps),
        'cadence_all_one':dict(gaps)=={1:n-1},'observed':data},indent=2),encoding='utf-8')
    print('folder changing 56:',valid,'groups',n,'frame intervals',dict(gaps))
    return rc if valid else 1


if __name__=='__main__':
    raise SystemExit(main())
