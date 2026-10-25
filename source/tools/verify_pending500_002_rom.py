"""Exact500 delta, cumulative preservation and independent rebuild proof; no release claim."""
import argparse,json,struct
from build_visibility_poc import ROOT,sha,require_hash
from batch500_002_rom import entries,PREFLIGHT
from keyitem_rom_data import verify_final
from archive_scripts import script_spans
from verify_tpi_index import lz77_decompress

BASE='poc/output/exe45_ko_development_pending500_arrow_v2.gba'


def primary_records(meta):
    return meta['archives']+[meta['keyitem_rom']['archive'],meta['keyitem_rom']['mail_rom_reader']['archive']]+meta['keyitem_rom']['mission_mail_archives']


def clones(tree,path=()):
    if isinstance(tree,dict):
        if {'archive','rom_offset','compiled_bytes','compiled_sha256','layout'}<=tree.keys():yield path,tree
        for key,value in tree.items():yield from clones(value,path+(key,))
    elif isinstance(tree,list):
        for key,value in enumerate(tree):yield from clones(value,path+(key,))


def at_path(tree,path):
    for key in path:tree=tree[key]
    return tree


def read_payload(rom,record):
    if record.get('compression'):return lz77_decompress(rom,record['rom_offset'])[0]
    return rom[record['rom_offset']:record['rom_offset']+record['compiled_bytes']]


def main():
    p=argparse.ArgumentParser();p.add_argument('--rom',required=True);p.add_argument('--repro',required=True)
    p.add_argument('--cpu',required=True);p.add_argument('--out',required=True);a=p.parse_args()
    out=ROOT/a.out
    if out.exists():raise ValueError('Preserve prior evidence')
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'))
    sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    base_meta=json.loads((ROOT/BASE).with_suffix('.json').read_text(encoding='utf8'))
    require_hash(ROOT/BASE,base_meta['output_sha256']);base=(ROOT/BASE).read_bytes()
    rp=ROOT/a.rom;meta=json.loads(rp.with_suffix('.json').read_text(encoding='utf8'))
    require_hash(rp,meta['output_sha256']);rom=rp.read_bytes()
    repro=ROOT/a.repro
    if repro.read_bytes()!=rom:raise ValueError('Independent rebuild differs')
    if meta['translated_units']!=3837 or meta['translated_units']-base_meta['translated_units']!=500:
        raise ValueError('Declared new500 delta')
    old_ids={x['id'] for r in primary_records(base_meta) for x in r['layout']}
    new_ids={x['id'] for r in primary_records(meta) for x in r['layout']}
    pre=json.loads((ROOT/PREFLIGHT).read_text(encoding='utf8'))
    selected={key for r in pre['archives'] for key in r['selected_ids']}
    if len(selected)!=500 or old_ids-new_ids or new_ids-old_ids!=selected:
        raise ValueError('Actual original-ID delta or prior IDs lost')
    all_old={x['id'] for _,r in clones(base_meta) for x in r['layout']}
    all_new={x['id'] for _,r in clones(meta) for x in r['layout']}
    if all_old-all_new or all_new-all_old!=selected:raise ValueError('Duplicate or lost supplemental original IDs')
    old_main={r['archive']:r for r in base_meta['archives']}
    current={r['archive']:r for r in meta['archives']}
    preserved=[]
    for name,r in old_main.items():
        if r['compiled_sha256']!=current[name]['compiled_sha256']:raise ValueError('Prior primary payload changed '+name)
        preserved.append(name)
    if len(current)!=82 or len(preserved)!=71:raise ValueError('Primary archive count')
    # Supplemental font/library/equipment raw clones are often outside the main
    # archive list. Verify their exact bytes by their stable metadata paths too.
    supplementary=[]
    for path,old in clones(base_meta):
        if path[0] in ('archives','keyitem_rom'):continue
        now=at_path(meta,path)
        if old['compiled_sha256']!=now['compiled_sha256'] or read_payload(base,old)!=read_payload(rom,now):
            raise ValueError('Prior supplemental clone changed '+str(path))
        supplementary.append('/'.join(map(str,path)))
    proofs=[]
    raw_records={r['archive']:r for r in meta['keyitem_rom']['mission_mail_archives']}
    for path,row,asset,scope,bound,native in entries(source):
        name=asset['archive'];record=current[name] if scope['standard_relocation'] else raw_records[name]
        raw=read_payload(rom,record)
        if sha(raw)!=bound['compiled_sha256'] or record['translated_units']!=len(asset['units']):
            raise ValueError('Final selected payload binding '+name)
        if {x['id'] for x in record['layout']}!={u['id'] for u in asset['units']}:raise ValueError('Final source-ID mapping '+name)
        for ptr in row['pointers']:
            expected=0x08000000+record['rom_offset'] if scope['standard_relocation'] else struct.unpack_from('<I',source,ptr)[0]
            if struct.unpack_from('<I',rom,ptr)[0]!=expected:raise ValueError('Final pointer contract '+name)
        proofs.append(dict(archive=name,selected_units=record['translated_units'],compiled_sha256=sha(raw),
            mode='raw native pointer relocation' if scope['standard_relocation'] else 'guarded body ROM clone; native compressed pointer retained'))
    prior=next(r for r in base_meta['keyitem_rom']['mission_mail_archives'] if r['archive']=='6E01AC')
    old_spans=script_spans(read_payload(base,prior),47)
    new_spans=script_spans(read_payload(rom,raw_records['6E01AC']),47)
    if any(old_spans[s]!=new_spans[s] for s in (38,39,40)):raise ValueError('Prior26 destruction carry regressed')
    for name in ('6DE3E0','6DF988'):
        prior=next(r for r in base_meta['keyitem_rom']['mission_mail_archives'] if r['archive']==name)
        if read_payload(base,prior)!=read_payload(rom,raw_records[name]):raise ValueError('Prior body changed '+name)
    if rom[0x40548:0x40576]!=source[0x40548:0x40576] or rom[0x40658:0x4066C]!=source[0x40658:0x4066C]:raise ValueError('Native mail loader/pointers changed')
    verify_final(source,rom,meta['keyitem_rom'])
    cpu=json.loads((ROOT/a.cpu).read_text(encoding='utf8'))
    if not cpu['passed'] or cpu['rom_sha256']!=sha(rom):raise ValueError('CPU proof binding')
    report=dict(passed=True,rom=a.rom,rom_sha256=sha(rom),repro=a.repro,independent_rebuild_identical=True,
        source_unchanged=True,previous_primary_payloads_identical=preserved,previous_supplementary_clones_identical=supplementary,
        selected_new_ids=sorted(selected),new_units=500,total_units=3837,primary_archives=82,raw_mail_archives=5,
        carried_destruction26_script_bytes_identical=True,archives=proofs,cpu_vectors=cpu['vectors'],
        runtime_scene_approval=False,release_eligible=False,limits='Full500 scene/mission/reward/save QA not complete; gear153 and Navi7 deferred, Hangul composition/save still not integrated.')
    out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('PASS actual500 ROM delta; total3837; prior71 and supplemental clones preserved; rebuild identical')


if __name__=='__main__':main()
