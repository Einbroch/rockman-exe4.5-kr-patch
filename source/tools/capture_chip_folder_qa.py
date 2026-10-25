"""Exact folder clone, palette/bias, cache and real word-copy assertions."""
import json
from pathlib import Path
import capture_chip_library_qa as frozen
from build_visibility_poc import ROOT,sha,require_hash


def main():
    fixed=frozen.library.fixed
    rom=Path(fixed.value('--rom')).resolve()
    m=json.loads(rom.with_suffix('.json').read_text())
    require_hash(rom,m['output_sha256'])
    require_hash(Path(frozen.__file__),'74a86b1147ee8ca14c3c9bb74fe5ec2c10f8b53d9b59253e9c94dcf7acb6fd51')
    e=m['chip_folder_extension']
    spec=json.loads((ROOT/e['spec_path']).read_text())
    require_hash(ROOT/e['spec_path'],e['spec_sha256'])
    ins=e['machine_code'][0]['instructions']
    loads=[i for i in ins if i['mnemonic'] in ('ldm','ldmia')]
    returns=[i['address'] for i in ins if i['mnemonic']=='pop' and i['operands']=='{r0, r2, r3}']
    if len(loads)!=3 or len(returns)!=1 or e['native_tile_bias']!=16:
        raise ValueError('folder renderer profile')
    code=frozen.PROBE.replace("local id=math.floor(s['cpu.r1']/0x1000000)","local id=s['cpu.r1']%256")
    code=code.replace("s['cpu.r6']%4096==0","s['cpu.r6']%4096==16")
    code=code.replace('tile=TILE_START+(s[\'cpu.r2\']-ROW_BUFFER)/2+count*2',
                      'tile=TILE_START+(s[\'cpu.r2\']-ROW_BUFFER)/2+count*2-16')
    code=code.replace("s['cpu.r2']~=64 or ",'').replace('verified_bios_copies','verified_word_copies')
    # Native empty row: 0803CB62 jumps to the continuation without selector.
    code=code.replace("if c==nil then error('chip selector return without entry') end",'if c==nil then return end')
    old="if c==nil then error('chip glyph copy returned without entry') end"
    if code.count(old)!=1:
        raise ValueError('folder copy-return anchor')
    code=code.replace('local chipKoActive=nil','local chipKoActive=nil\nlocal folderChecks=0\nlocal folderHits=0\nlocal folderResets=0')
    code=code.replace(old,r'''local s=emu.getState();local stream=0
 for i=0,3 do stream=stream+emu.read(s['cpu.r13']+i,emu.memType.gbaMemory)*2^(i*8) end
 local index=chipWord(stream+2)
 local dst=0x06004000+s['cpu.r5']*32
 local tag=0x06008E40+s['cpu.r5']-514
 if index>=11172 or dst<0x06008040 or dst+64>0x06008E40 then error('folder cache bounds') end
 if chipWord(tag)~=index+1 or bytesAt(dst,64)~=bytesAt(FONT_START+index*64,64) then error('folder cache glyph/tag') end
 folderChecks=folderChecks+1
 if c==nil then folderHits=folderHits+1;return end''')
    code+=f'''
emu.addMemoryCallback(function()
 for i=0,111 do if emu.read(0x06008E40+i,emu.memType.gbaMemory)~=0 then error('folder init reset tags') end end
 folderResets=folderResets+1
end,emu.callbackType.exec,{e['cache']['reset_probe']},{e['cache']['reset_probe']})
local oldFolderDump=dumpChipKo
dumpChipKo=function(name)
 oldFolderDump(name)
 write(name..'_folder_cache.json',string.format('{{"checks":%d,"hits":%d,"resets":%d}}',folderChecks,folderHits,folderResets))
end
'''
    values={'ROW_BUFFER':e['buffer']['start'],'SOURCE_POOL':0x08000000+spec['pool']['offset'],
            'PRIVATE_POOL':0x08000000+e['clone_offset'],'TILE_START':514,
            'INSTALL_ADDRESS':0x08000000+e['install']['offset'],'CONTINUATION':e['install']['continuation']&~1,
            'CACHE_START':e['vram']['start'],'CACHE_END':e['vram']['start']+e['vram']['bytes'],
            'FONT_START':0x08000000+e['font_offset'],'COPY_HELPER':loads[0]['address'],'COPY_RETURN':returns[0]}
    for key,value in values.items():
        code=code.replace(key,str(value))
    code="local function folderFail(s) write('folder_qa_failed.txt',s);emu.stop(1);error(s) end\n"+code.replace('error(','folderFail(')
    fixed.PROBE+=code
    for old,new in [('local function capture(name)\n','local function capture(name)\n dumpChipKo(name)\n'),
                    ('local function finish()\n',"local function finish()\n dumpChipKo('final')\n")]:
        if fixed.runner.LUA_TEMPLATE.count(old)!=1:
            raise ValueError('folder dump anchor')
        fixed.runner.LUA_TEMPLATE=fixed.runner.LUA_TEMPLATE.replace(old,new,1)
    rc=frozen.library.main()
    out=Path(fixed.value('--out'))
    result=json.loads((out/'result.json').read_text())
    valid=False
    if result['complete'] and (out/'final_folder_cache.json').exists():
        c=json.loads((out/'final_folder_cache.json').read_text())
        copies=json.loads((out/'final_chip_ko.json').read_text())['verified_word_copies']
        valid=rc==0 and c['resets']>0 and c['hits']>0 and copies>0 and c['checks']==copies+c['hits']
    if not valid:
        result['complete']=False
        (out/'result.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    (out/'folder_qa_environment.json').write_text(json.dumps({'tool_sha256':sha(Path(__file__).read_bytes()),
        'rom_sha256':m['output_sha256'],'passed':valid,'substitutions':values,
        'scope':'normal input; folder clone/row ABI, palette+native bias, actual inline copies, hit pixels and init reset; not timing proof'},indent=2),encoding='utf-8')
    print('folder actual copy/cache/ABI:',valid)
    return rc if valid else 1


if __name__=='__main__':
    raise SystemExit(main())
