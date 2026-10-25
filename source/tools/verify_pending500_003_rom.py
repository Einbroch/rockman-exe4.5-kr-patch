"""Bind the third actual 500-unit addition to ROM bytes and preserved history."""
import argparse,json,struct
from build_visibility_poc import ROOT,sha,require_hash
from batch500_003_rom import entries,PREFLIGHT
from keyitem_rom_data import verify_final
from verify_pending500_002_rom import primary_records,clones,at_path,read_payload

BASE='poc/output/exe45_ko_development_pending500_002_v1.gba'

def records(meta):
    return primary_records(meta)+meta['keyitem_rom'].get('equipment_archives',[])

def main():
    p=argparse.ArgumentParser()
    for key in ('rom','repro','cpu','out'):p.add_argument('--'+key,required=True)
    a=p.parse_args();out=ROOT/a.out
    if out.exists():raise ValueError('Preserve prior evidence')
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'))
    sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    bp=ROOT/BASE;old=json.loads(bp.with_suffix('.json').read_text(encoding='utf8'));require_hash(bp,old['output_sha256']);base=bp.read_bytes()
    rp=ROOT/a.rom;meta=json.loads(rp.with_suffix('.json').read_text(encoding='utf8'));require_hash(rp,meta['output_sha256']);rom=rp.read_bytes()
    if (ROOT/a.repro).read_bytes()!=rom:raise ValueError('Independent rebuild differs')
    if meta['translated_units']!=4337 or meta['translated_units']-old['translated_units']!=500:raise ValueError('Declared delta')
    pre=json.loads((ROOT/PREFLIGHT).read_text(encoding='utf8'))
    selected={key for r in pre['archives'] for key in r['selected_ids']}
    before={x['id'] for r in records(old) for x in r['layout']}
    after={x['id'] for r in records(meta) for x in r['layout']}
    all_before={x['id'] for _,r in clones(old) for x in r['layout']}
    all_after={x['id'] for _,r in clones(meta) for x in r['layout']}
    if len(selected)!=500 or before-after or after-before!=selected or all_before-all_after or all_after-all_before!=selected:raise ValueError('Actual original-ID delta')
    current={r['archive']:r for r in meta['archives']}
    if len(current)!=125 or len(old['archives'])!=82:raise ValueError('Primary archive count')
    preserved=[]
    for path,r in clones(old):
        now=current[r['archive']] if path[0]=='archives' else at_path(meta,path)
        if r['compiled_sha256']!=now['compiled_sha256'] or read_payload(base,r)!=read_payload(rom,now):raise ValueError('Prior payload changed '+str(path))
        preserved.append('/'.join(map(str,path)))
    equipment={r['archive']:r for r in meta['keyitem_rom']['equipment_archives']}
    proofs=[]
    for path,row,asset,scope,bound,native in entries(source):
        name=asset['archive'];record=current[name] if scope['standard_relocation'] else equipment[name]
        raw=read_payload(rom,record)
        if sha(raw)!=bound['compiled_sha256'] or record['translated_units']!=len(asset['units']):raise ValueError('Payload binding '+name)
        if {x['id'] for x in record['layout']}!={u['id'] for u in asset['units']}:raise ValueError('Source-ID mapping '+name)
        for ptr in row['pointers']:
            expected=0x08000000+record['rom_offset'] if scope['standard_relocation'] else struct.unpack_from('<I',source,ptr)[0]
            if struct.unpack_from('<I',rom,ptr)[0]!=expected:raise ValueError('Pointer contract '+name)
        proofs.append(dict(archive=name,selected_units=len(asset['units']),compiled_sha256=sha(raw),standard_relocation=scope['standard_relocation']))
    if source[0x3EFAA:0x3EFAE]!=bytes.fromhex('ab8bf364'):raise ValueError('uint16 producer source')
    if rom[0x3EFAA:0x3EFAE]!=source[0x3EFAA:0x3EFAE]:raise ValueError('Numeric producer changed')
    verify_final(source,rom,meta['keyitem_rom'])
    cpu=json.loads((ROOT/a.cpu).read_text(encoding='utf8'))
    if not cpu['passed'] or cpu['rom_sha256']!=sha(rom):raise ValueError('CPU evidence binding')
    report=dict(passed=True,rom=a.rom,rom_sha256=sha(rom),repro=a.repro,independent_rebuild_identical=True,
        new_units=500,total_units=4337,primary_archives=125,new_raw_equipment_archives=3,
        selected_new_ids=sorted(selected),previous_payloads_identical=preserved,archives=proofs,cpu_vectors=cpu['vectors'],
        source_unchanged=True,runtime_scene_approval=False,release_eligible=False,
        limits='Whole500 natural scene/reward/save QA incomplete; Hangul composition/save not integrated. Previously translated 111 source aliases are not new units.')
    out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('PASS actual500 ROM delta; total4337; prior payloads preserved; independent rebuild identical')

if __name__=='__main__':main()
