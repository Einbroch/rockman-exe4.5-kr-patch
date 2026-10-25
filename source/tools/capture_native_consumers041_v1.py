"""Observe exact040 source consumers for041 admission; controller input only."""
import sys,json
from pathlib import Path
import run_mesen_segment as runner
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read
from verify_tpi_index import lz77_decompress


def main():
    def arg(k):return sys.argv[sys.argv.index(k)+1]
    rp=Path(arg('--rom'));m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);s=read('analysis/pending_insertion_500_041_source_v7/selection.json')
    if m['output_sha256']!=s['baseline_sha256']:raise ValueError('041 investigation exact040 baseline')
    cfg=read('project.json');require_hash(ROOT/cfg['source_profile']['filename'],s['source_sha256']);source=(ROOT/cfg['source_profile']['filename']).read_bytes();rom=rp.read_bytes();pool={}
    for g in s['groups']:
        row=g['source_row']
        if not row['compressed']:continue
        for address in {0x08000000+row['offset']}|{int.from_bytes(rom[p:p+4],'little') for p in row['pointers']}:
            payload=lz77_decompress(rom,address-0x08000000)[0];entry=dict(archive=g['archive'],bytes=len(payload),sha256=sha(payload))
            if address in pool and pool[address]!=entry:raise ValueError('041 ambiguous observed source pointer')
            pool[address]=entry
    for a,b in [(0x3C5A4,0x3C5B8),(0x41128,0x4113C),(0x479E0,0x479F4),(0x4F7B6,0x4F7CC),(0xEC158,0xEC15C)]:
        if rom[a:b]!=source[a:b]:raise ValueError('041 source loader/initializer changed')
    code=r'''
local observedSources=SOURCE_MAP
local nativeLoads={};local nativeCalls={};local nativeEntries={};local nativeDefaults={};local nativeDraws={};local recentRoots={};local captureCount=0
local function n32(a) local v=0;for j=0,3 do v=v+emu.read(a+j,emu.memType.gbaMemory)*2^(8*j) end;return v end
local function nregs(s) local t={};for j=0,14 do t[#t+1]=string.format('"%d":%d',j,s['cpu.r'..j]) end;return '{'..table.concat(t,',')..'}' end
emu.addMemoryCallback(function()
 local s=emu.getState();local src=s['cpu.r0'];local dest=s['cpu.r1'];local p=observedSources[src]
 recentRoots[dest]=nil
 if p then local e={source=src,dest=dest,archive=p.archive,bytes=p.bytes,frame=frame,lr=s['cpu.r14']};recentRoots[dest]=e;nativeLoads[#nativeLoads+1]=string.format('{"frame":%d,"source":%d,"destination":%d,"archive":"%s","bytes":%d,"lr":%d}',frame,src,dest,p.archive,p.bytes,s['cpu.r14']) end
end,emu.callbackType.exec,0x080EC158,0x080EC158)
for _,pc in ipairs({0x0803C5A4,0x0803C478,0x08041128,0x080479E0,0x0804F7B6}) do
 emu.addMemoryCallback(function()
  local s=emu.getState();nativeEntries[#nativeEntries+1]=string.format('{"pc":%d,"frame":%d,"registers":%s}',pc,frame,nregs(s))
 end,emu.callbackType.exec,pc,pc)
end
emu.addMemoryCallback(function()
 local s=emu.getState();local e=recentRoots[s['cpu.r0']];local file=''
 if e then captureCount=captureCount+1;file=string.format('native_call_%03d_%s.bin',captureCount,e.archive);local t={};for j=0,e.bytes-1 do t[#t+1]=string.char(emu.read(s['cpu.r0']+j,emu.memType.gbaMemory)) end;write(file,table.concat(t)) end
 nativeCalls[#nativeCalls+1]=string.format('{"frame":%d,"registers":%s,"stack_lr16":%d,"native_dump":"%s"}',frame,nregs(s),n32(s['cpu.r13']+16),file)
 if #nativeCalls>1000 then error('041 native-call observation budget') end
end,emu.callbackType.exec,0x0804FB4C,0x0804FB4C)
emu.addMemoryCallback(function()
 local s=emu.getState();local ctx=n32(s['cpu.r10']+44);nativeDefaults[#nativeDefaults+1]=string.format('{"frame":%d,"context":%d,"root":%d,"stream":%d,"x":%d,"y":%d}',frame,ctx,n32(ctx+48),n32(ctx+44),emu.read(ctx+24,emu.memType.gbaMemory),emu.read(ctx+25,emu.memType.gbaMemory))
end,emu.callbackType.exec,0x0804F7CA,0x0804F7CA)
emu.addMemoryCallback(function()
 local s=emu.getState();local ctx=s['cpu.r5'];if ctx~=0x0200FA20 or #nativeDraws>=20000 then return end
 nativeDraws[#nativeDraws+1]=string.format('{"frame":%d,"stream":%d,"glyph":%d,"offset":%d,"x":%d,"y":%d,"root":%d}',frame,s['cpu.r4'],s['cpu.r1'],s['cpu.r6'],emu.read(ctx+24,emu.memType.gbaMemory),emu.read(ctx+25,emu.memType.gbaMemory),n32(ctx+48))
end,emu.callbackType.exec,0x03006AE0,0x03006AE0)
local function dumpNative041()
 write('native_consumers041.json','{"loads":['..table.concat(nativeLoads,',')..'],"calls":['..table.concat(nativeCalls,',')..'],"entries":['..table.concat(nativeEntries,',')..'],"defaults":['..table.concat(nativeDefaults,',')..'],"draws":['..table.concat(nativeDraws,',')..']}')
end
'''
    entries=','.join('['+str(k)+']={archive="'+v['archive']+'",bytes='+str(v['bytes'])+'}' for k,v in sorted(pool.items()));code=code.replace('SOURCE_MAP','{'+entries+'}')
    anchor='local function capture(name)\n'
    if runner.LUA_TEMPLATE.count(anchor)!=1:raise ValueError('041 native observer capture anchor')
    runner.LUA_TEMPLATE=runner.LUA_TEMPLATE.replace(anchor,code+anchor,1).replace('local function finish()\n','local function finish()\n dumpNative041()\n',1)
    rc=runner.main();out=Path(arg('--out'));r=read(out/'result.json');r['native041_observation']='Read-only source lookup/LZ/actual common ABI/default-origin/draw observation on own040 normal inputs. No aliases, gameRAM/ROM/PC/flags/caller writes. NOT041 Korean runtime.';r['source_lookup_payloads']=pool;r['artifacts']={p.name:sha(p.read_bytes()) for p in out.iterdir() if p.is_file() and p.name!='result.json'};(out/'result.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf8');return rc


if __name__=='__main__':raise SystemExit(main())
