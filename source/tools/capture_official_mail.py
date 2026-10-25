"""Quarantined native script-table read alias; NOT acquisition/playthrough QA."""
import json,struct,sys
from pathlib import Path
import run_mesen_segment as runner
from build_visibility_poc import ROOT,sha,require_hash
from verify_tpi_index import lz77_decompress

def main():
    args=sys.argv
    def value(k):return args[args.index(k)+1]
    script=int(value('--mail-script'));i=args.index('--mail-script');del args[i:i+2]
    matching='--corresponding-header' in args
    if matching:args.remove('--corresponding-header')
    header_only='--header-only' in args
    if header_only:args.remove('--header-only')
    if header_only and not matching:raise ValueError('header-only requires corresponding header')
    if script not in (1,2,3,8,9,10,11,12,13,14):raise ValueError('explicit mail diagnostic script scope')
    rom_path=Path(value('--rom'));manifest=json.loads(rom_path.with_suffix('.json').read_text(encoding='utf8'))
    require_hash(rom_path,manifest['output_sha256']);rom=rom_path.read_bytes()
    source=ROOT/json.loads((ROOT/'project.json').read_text(encoding='utf8'))['source_profile']['filename']
    require_hash(source,manifest['source_sha256']);native=source.read_bytes()
    from keyitem_rom_data import verify_final
    if not verify_final(native,rom,manifest['keyitem_rom']):raise ValueError('retained guarded key-item initializer')
    # The composed selector replays4FB4C..58. Old artifacts preserve the RAM
    # body root; explicit mail-reader artifacts select an identical ROM clone.
    for a,b in [(0x40548,0x40576),(0x4F7B6,0x4F7D0),(0x4FB58,0x4FB84)]:
        if rom[a:b]!=native[a:b]:raise ValueError('native mail/initializer bytes changed')
    record=next(r for r in manifest['archives'] if r['archive']=='6DD9AC')
    from full_mail_body import payload
    body,root=payload(rom,manifest)
    if script>=11 and not manifest['keyitem_rom'].get('mail_rom_reader',{}).get('archive'):raise ValueError('remaining43 require explicit full clone')
    offset0,offset=struct.unpack_from('<H',body,0)[0],struct.unpack_from('<H',body,script*2)[0]
    # Original native Official entries begin with flagClear 623/624/625.
    original=lz77_decompress(native,0x6DD9AC)[0]
    prefix=original[int.from_bytes(original[script*2:script*2+2],'little'):][:4]
    expected='e90b' if script==14 else 'fc10' if script>=8 else 'e901'
    if body[offset:offset+4]!=prefix or prefix[:2]!=bytes.fromhex(expected):raise ValueError('mail native flag/quest entry prefix')
    header_map={1:(2,3),2:(4,5),3:(6,7),8:(16,17),9:(18,19),10:(20,21),11:(22,23),12:(24,25),13:(26,27),14:(28,29)}
    header_extra='';header_receipt='null';header_pair=None
    if matching:
        header_pair=header_map[script];header_record=next(r for r in manifest['archives'] if r['archive']=='6DD63C')
        header=lz77_decompress(rom,header_record['rom_offset'])[0];header_root=0x020262F4
        h0,h1,hs,ht=[struct.unpack_from('<H',header,n*2)[0] for n in (0,1,*header_pair)]
        header_extra=f'''
local senderAliases=0
local titleAliases=0
emu.addMemoryCallback(function(address,value)
 if value=={h0} then senderAliases=senderAliases+1;return {hs} end
end,emu.callbackType.read,{header_root},{header_root+1})
emu.addMemoryCallback(function(address,value)
 if value=={h1} then titleAliases=titleAliases+1;return {ht} end
end,emu.callbackType.read,{header_root+2},{header_root+3})
local function dumpHeaderAlias(name)
 write(name..'_mail_header_alias.json','{{"sender_aliases":'..senderAliases..',"title_aliases":'..titleAliases..',"body_script":{script},"sender_script":{header_pair[0]},"title_script":{header_pair[1]},"header_root":{header_root}}}')
end
'''
        header_receipt="dumpHeaderAlias(name)\n"
    extra=f'''
local mailAliases=0
emu.addMemoryCallback(function(address,value)
 local s=emu.getState()
 if mailAliases==0 and address=={root} and value=={offset0} and s['cpu.pipeline.execute.address']==0x0804FB76 and s['cpu.r0']=={root} and s['cpu.r1']==0 and s['cpu.r5']==0x0200FA20 then
  mailAliases=mailAliases+1;return {offset}
 end
end,emu.callbackType.read,{root},{root+1})
local function dumpMailAlias(name)
 write(name..'_mail_alias.json','{{"aliases":'..mailAliases..',"displayed_script":{script},"native_script":0,"source_offset":{offset0},"target_offset":{offset}}}')
end
'''+header_extra
    anchor='local function capture(name)\n'
    if runner.LUA_TEMPLATE.count(anchor)!=1:raise ValueError('mail capture anchor')
    runner.LUA_TEMPLATE=runner.LUA_TEMPLATE.replace(anchor,extra+anchor+' dumpMailAlias(name)\n '+header_receipt,1)
    anchor='local function finish()\n'
    if runner.LUA_TEMPLATE.count(anchor)!=1:raise ValueError('mail finish anchor')
    runner.LUA_TEMPLATE=runner.LUA_TEMPLATE.replace(anchor,anchor+" dumpMailAlias('final')\n"+(" dumpHeaderAlias('final')\n" if matching else ''),1)
    rc=runner.main();out=Path(value('--out'));result=json.loads((out/'result.json').read_text(encoding='utf8'))
    receipt=json.loads((out/'final_mail_alias.json').read_text(encoding='utf8'))
    passed=rc==0 and (receipt['aliases']==0 if header_only else receipt['aliases']==1)
    header_result=None
    if matching:
        header_result=json.loads((out/'final_mail_header_alias.json').read_text(encoding='utf8'))
        passed=passed and header_result['sender_aliases']>0 and header_result['title_aliases']>0
    scope=('DIAGNOSTIC mail header list before body selection.' if header_only else 'DIAGNOSTIC mail: one native body-table read alias after actual decompression.')
    scope+=(' Corresponding sender/title table reads are also aliased for isolated rendering.' if matching else ' Header remains first I.P.C. header.')
    scope+=' NOT acquisition/title lookup/save compatibility evidence.'
    result.update(scope=scope,normal_play_checkpoint_eligible=False,official_mail_diagnostic=receipt,mail_header_diagnostic=header_result,complete=passed)
    if (out/'checkpoint.mss').exists():(out/'checkpoint.mss').rename(out/'diagnostic_checkpoint.mss')
    result['artifacts']={p.name:sha(p.read_bytes()) for p in sorted(out.iterdir()) if p.is_file() and p.name!='result.json'}
    (out/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('Official diagnostic',script,passed,receipt)
    return 0 if passed else 1

if __name__=='__main__':raise SystemExit(main())
