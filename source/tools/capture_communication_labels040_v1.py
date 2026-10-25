"""Read-only039 untranslated small labels: caller/provider/cell geometry."""
import sys,json
from pathlib import Path
import run_mesen_segment as runner
from build_visibility_poc import sha,require_hash
from cumulative_batch500 import read


def main():
    def arg(k):return sys.argv[sys.argv.index(k)+1]
    rp=Path(arg('--rom'));m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256'])
    if 'communication039' not in m['keyitem_rom']:raise ValueError('039 exact consumer prerequisite')
    code=r'''
local labelEntries={};local labelGlyphs={}
local function labelRead(pc,target)
 local s=emu.getState();local p=s['cpu.r0']
 if p>=0x02024000 and p<0x02026000 then
  local regs={};for j=0,14 do regs[#regs+1]=string.format('"%d":%d',j,s['cpu.r'..j]) end
  target[#target+1]=string.format('{"frame":%d,"pc":%d,"registers":{%s}}',frame,pc,table.concat(regs,','))
 end
end
emu.addMemoryCallback(function() labelRead(0x03006824,labelEntries) end,emu.callbackType.exec,0x03006824,0x03006824)
emu.addMemoryCallback(function() labelRead(0x0300689C,labelGlyphs) end,emu.callbackType.exec,0x0300689C,0x0300689C)
local function dumpLabels()
 write('communication_labels.json','{"entries":['..table.concat(labelEntries,',')..'],"glyphs":['..table.concat(labelGlyphs,',')..']}')
end
'''
    marker='local function capture(name)\n'
    if runner.LUA_TEMPLATE.count(marker)!=1:raise ValueError('040 label observer anchor')
    runner.LUA_TEMPLATE=runner.LUA_TEMPLATE.replace(marker,code+marker,1).replace('local function finish()\n','local function finish()\n dumpLabels()\n',1)
    rc=runner.main();out=Path(arg('--out'));r=read(out/'result.json');r['label_observation']='Read-only actual039 original Japanese small-label caller/provider/cell path; NOT040 Korean labels.';r['artifacts']={p.name:sha(p.read_bytes()) for p in out.iterdir() if p.is_file() and p.name!='result.json'};(out/'result.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf8');return rc


if __name__=='__main__':raise SystemExit(main())
