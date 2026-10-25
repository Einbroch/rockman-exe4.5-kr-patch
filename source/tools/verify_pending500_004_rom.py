"""Exact fourth500 original-ID delta, prior payloads, pointer contracts and rebuild."""
import argparse,json,struct
from build_visibility_poc import ROOT,sha,require_hash
from batch500_004_rom import entries,PREFLIGHT
from keyitem_rom_data import verify_final
from verify_pending500_002_rom import clones,at_path,read_payload

BASE='poc/output/exe45_ko_development_pending500_003_v2.gba'
TOTAL=4837
PRIMARY=152
PREVIOUS_PRIMARY=125

def main():
    p=argparse.ArgumentParser()
    for key in ('rom','repro','cpu','out'):p.add_argument('--'+key,required=True)
    a=p.parse_args();out=ROOT/a.out
    if out.exists():raise ValueError('Preserve prior evidence')
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    bp=ROOT/BASE;old=json.loads(bp.with_suffix('.json').read_text(encoding='utf8'));require_hash(bp,old['output_sha256']);base=bp.read_bytes()
    rp=ROOT/a.rom;meta=json.loads(rp.with_suffix('.json').read_text(encoding='utf8'));require_hash(rp,meta['output_sha256']);rom=rp.read_bytes()
    if (ROOT/a.repro).read_bytes()!=rom:raise ValueError('Independent rebuild differs')
    if meta['translated_units']!=TOTAL or meta['translated_units']-old['translated_units']!=500:raise ValueError('Declared unit delta')
    pre=json.loads((ROOT/PREFLIGHT).read_text(encoding='utf8'));selected={key for r in pre['archives'] for key in r['selected_ids']}
    before={x['id'] for _,r in clones(old) for x in r['layout']};after={x['id'] for _,r in clones(meta) for x in r['layout']}
    if len(selected)!=500 or before-after or after-before!=selected:raise ValueError('Actual original-ID delta')
    current={r['archive']:r for r in meta['archives']}
    if len(current)!=PRIMARY or len(old['archives'])!=PREVIOUS_PRIMARY:raise ValueError('Main archive delta')
    preserved=[]
    for path,r in clones(old):
        now=current[r['archive']] if path[0]=='archives' else at_path(meta,path)
        if r['compiled_sha256']!=now['compiled_sha256'] or read_payload(base,r)!=read_payload(rom,now):raise ValueError('Prior payload changed '+str(path))
        preserved.append('/'.join(map(str,path)))
    proofs=[]
    for _,row,asset,scope,bound,native in entries(source):
        name=asset['archive'];record=current[name];raw=read_payload(rom,record)
        if sha(raw)!=bound['compiled_sha256'] or record['translated_units']!=len(asset['units']):raise ValueError('Final compiled binding '+name)
        if {x['id'] for x in record['layout']}!={u['id'] for u in asset['units']}:raise ValueError('Final source-ID mapping '+name)
        for ptr in row['pointers']:
            if struct.unpack_from('<I',rom,ptr)[0]!=0x08000000+record['rom_offset']:raise ValueError('Raw pointer relocation '+name)
        proofs.append(dict(archive=name,selected_units=len(asset['units']),compiled_sha256=sha(raw),pointers=row['pointers']))
    verify_final(source,rom,meta['keyitem_rom'])
    cpu=json.loads((ROOT/a.cpu).read_text(encoding='utf8'))
    if not cpu['passed'] or cpu['rom_sha256']!=sha(rom):raise ValueError('CPU evidence binding')
    result=dict(passed=True,rom=a.rom,rom_sha256=sha(rom),repro=a.repro,independent_rebuild_identical=True,source_unchanged=True,
        new_units=500,total_units=TOTAL,primary_archives=PRIMARY,selected_new_ids=sorted(selected),previous_payloads_identical=preserved,
        archives=proofs,cpu_vectors=cpu['vectors'],runtime_scene_approval=False,release_eligible=False,
        limits='Full500 natural scene/progression/reward/save QA incomplete; Hangul composition/save still not integrated.')
    out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(f'PASS actual500 ROM delta; total{TOTAL}; all prior payloads preserved; independent rebuild identical')

if __name__=='__main__':main()
