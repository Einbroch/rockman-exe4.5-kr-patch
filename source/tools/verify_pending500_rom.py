"""Exact-ROM integration and preservation evidence; not scene-wide approval."""
import argparse,json,struct
from build_visibility_poc import ROOT,require_hash,sha
from prepare_pending_batch500 import BASE,BASE_SHA
from batch500_rom import entries
from keyitem_rom_data import verify_final
from verify_tpi_index import lz77_decompress

def main():
    p=argparse.ArgumentParser();p.add_argument('--rom',required=True);p.add_argument('--repro',required=True);p.add_argument('--out',required=True);p.add_argument('--cpu',default='analysis/pending_insertion_500_rom/selector_cpu_v2.json');a=p.parse_args()
    out=ROOT/a.out
    if out.exists():raise ValueError('preserve evidence')
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    rp=ROOT/a.rom;m=json.loads(rp.with_suffix('.json').read_text(encoding='utf8'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes()
    require_hash(ROOT/BASE,BASE_SHA);baseline=json.loads((ROOT/BASE).with_suffix('.json').read_text(encoding='utf8'))
    if (ROOT/a.repro).read_bytes()!=rom or m['translated_units']!=3337:raise ValueError('reproduction/count')
    old={r['archive']:r for r in baseline['archives']};current={r['archive']:r for r in m['archives']}
    for name,r in old.items():
        if r['compiled_sha256']!=current[name]['compiled_sha256']:raise ValueError('prior archive payload changed '+name)
    if len(old)!=67 or len(current)!=71 or not verify_final(source,rom,m['keyitem_rom']):raise ValueError('integration denominator/selector')
    proof=[]
    for path,row,asset,scope,pre,native in entries(source):
        name=asset['archive'];header=asset['consumer']=='fixed-cell-big'
        record=current[name] if header else next(r for r in m['keyitem_rom']['mission_mail_archives'] if r['archive']==name)
        at=record['rom_offset'];raw=lz77_decompress(rom,at)[0] if header else rom[at:at+record['compiled_bytes']]
        if sha(raw)!=pre['compiled_sha256'] or record['translated_units']!=len(asset['units']):raise ValueError('final 500 payload '+name)
        for pointer in row['pointers']:
            expected=0x08000000+at if header else struct.unpack_from('<I',source,pointer)[0]
            if struct.unpack_from('<I',rom,pointer)[0]!=expected:raise ValueError('500 pointer contract')
        proof.append(dict(archive=name,units=record['translated_units'],compiled_sha256=sha(raw),mode='native header loader relocation' if header else 'guarded ROM clone; original compressed body pointer retained',script_count=pre['script_count']))
    if rom[0x40548:0x40576]!=source[0x40548:0x40576] or rom[0x4065C:0x4066C]!=source[0x4065C:0x4066C]:raise ValueError('native body loader changed')
    cpu=json.loads((ROOT/a.cpu).read_text(encoding='utf8'))
    if cpu['rom_sha256']!=sha(rom) or not cpu['passed']:raise ValueError('CPU evidence binding')
    result=dict(passed=True,rom=a.rom,rom_sha256=sha(rom),independent_rebuild_identical=True,source_unchanged=True,previous_67_archive_payloads_identical=True,selected_units=500,total_units=3337,main_archives=71,raw_body_clones_added=3,archives=proof,cpu_vectors=cpu['vectors'],runtime_scene_approval=False,release_eligible=False,remaining='dynamic reward/name aggregate widths and full natural mission receipt/progression/save remain unverified; development only')
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print('PASS pending500 integration; 500 units, prior67 preserved, reproduction identical')

if __name__=='__main__':main()
