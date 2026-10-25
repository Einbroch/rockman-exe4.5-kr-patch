"""Actual product delta, prior clone bytes/consumer contracts and writer audit."""
import argparse
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from verify_pending500_002_rom import clones,at_path,read_payload
from keyitem_rom_data import verify_final
from field_b0_rom_data import verify_final as verify_b0,MANIFEST


def main():
    p=argparse.ArgumentParser();p.add_argument('--rom',default='poc/output/pending500_023_v1.gba');p.add_argument('--repro');p.add_argument('--out',default='analysis/pending500_023_v1/integration.json');a=p.parse_args()
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    pre=read(MANIFEST);bp=ROOT/pre['baseline_rom'];require_hash(bp,pre['baseline_sha256']);base=bp.read_bytes();old=read(bp.with_suffix('.json'))
    rp=ROOT/a.rom;m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes()
    verify_final(source,rom,m['keyitem_rom']);selected=verify_b0(source,rom,m['keyitem_rom'])
    before={u['id'] for _,r in clones(old) for u in r['layout']};after={u['id'] for _,r in clones(m) for u in r['layout']}
    if before-after or after-before!=selected or len(selected)!=500 or m['translated_units']!=old['translated_units']+500 or m['translated_units']!=12622:
        raise ValueError('Actual023 new500/old-ID preservation/total')
    preserved=[]
    for path,r in clones(old):
        now=at_path(m,path)
        if read_payload(base,r)!=read_payload(rom,now) or any(r.get(k)!=now.get(k) for k in ('compiled_sha256','layout','translated_units','source_sha256','protected_controls_unchanged')):
            raise ValueError('Prior clone payload/consumer changed: '+str(path))
        preserved.append('/'.join(map(str,path)))
    matching=[e for e in m['translation_assets'] if e['path'].replace('\\','/')==MANIFEST]
    if len(matching)!=1 or matching[0]['sha256']!=sha((ROOT/MANIFEST).read_bytes()) or [e for e in m['translation_assets'] if e not in matching]!=old['translation_assets']:
        raise ValueError('Primary input lineage changed beyond new manifest')
    if len(m['archives'])!=len(old['archives']) or m['unchanged_archives']!=old['unchanged_archives'] or rom[:0xC0]!=source[:0xC0]:raise ValueError('Primary/source/header denominator')
    # All source-extent differences remain exactly the old writes except the
    # single composed reader stub, now pointing through B0 then A3/readers.
    differences=[i for i,(x,y) in enumerate(zip(base,rom)) if i<len(source) and x!=y]
    if any(not 0x4FB4C<=i<0x4FB58 for i in differences):raise ValueError('Unrelated source-extent writer changed')
    boundary=old['keyitem_rom']['hook_address']-0x08000000
    if rom[0x4FB58:boundary]!=base[0x4FB58:boundary] or rom[:0x4FB4C]!=base[:0x4FB4C]:
        raise ValueError('Previously verified fonts/code/graphics/pools/descriptors changed before new B0 tail')
    intervals=[]
    for record in m['keyitem_rom']['b0_hint_archives']:
        cp,np=record['rom_offset'],record['native_copy_offset']
        intervals.extend(((np,np+record['native_copy_bytes']),(cp,cp+record['compiled_bytes'])))
        for gate in (m['dialogue_chip_name']['command_stream'],m['dialogue_chip_name']['gutsman_command_stream']):
            if 0x08000000+cp<=gate<0x08000000+cp+record['compiled_bytes']:raise ValueError('B0 clone collides with old exact chip104 Korean selector stream')
    desc=m['keyitem_rom']['b0_hint_guard']['descriptor_address']-0x08000000
    intervals.append((desc,desc+23*16));ordered=sorted(intervals)
    if min(a for a,b in ordered)<boundary or any(b>c for (a,b),(c,d) in zip(ordered,ordered[1:])) or max(b for a,b in ordered)>m['keyitem_rom']['hook_address']-0x08000000:
        raise ValueError('B0 source-copy/clone/descriptor placement overlap or preceding code invasion')
    coverage=bytearray(len(source));writers=[]
    for w in m['expected_writes']:
        at,n=w['offset'],w['bytes']
        # Append has its own immutable-source absence/derived-tail contract.
        if at==len(source):
            if n!=len(rom)-len(source):raise ValueError('Append expected-write extent')
            continue
        if not 0<=at<=len(source)-n or any(coverage[at:at+n]) or source[at:at+n].hex()!=w['expected_hex'] or rom[at:at+n].hex()!=w['final_hex']:raise ValueError('Expected-write source/final/overlap')
        coverage[at:at+n]=bytes([1])*n;writers.append(w['writer'])
    if any(x!=y and not coverage[i] for i,(x,y) in enumerate(zip(source,rom))) or sha(rom[len(source):])!=m['append_sha256'] or len(rom)-len(source)!=m['append_bytes']:
        raise ValueError('Unexplained complete final diff')
    repro=False
    if a.repro:
        other=ROOT/a.repro
        if other.read_bytes()!=rom:raise ValueError('Independent rebuild byte mismatch')
        repro=True
    frozen_write(ROOT/a.out,dict(schema=1,passed=True,rom_sha256=sha(rom),rom_bytes=len(rom),source_sha256=sha(source),baseline_sha256=sha(base),new_units=500,total_units=m['translated_units'],primary_archives=len(m['archives']),unchanged_source_archives=m['unchanged_archives'],preserved_clone_count=len(preserved),preserved_clone_paths=preserved,entire_prior_prefix_except_reader_stub_byte_identical_through=boundary,source_delta_only_composed_reader_stub=True,selected_ids=sorted(selected),new_descriptor_and_original_storage_verified=True,final_selector_regenerated=True,expected_writes_and_complete_diff_verified=True,independent_rebuild_byte_identical=repro,runtime_tested=False,release_eligible=False,limits='Static actual product verification only. No GBA display/normal branch/timing/automatic Hangul input completion or release claim.'))
    print('PASS actual023 delta500, total12622, carry clones',len(preserved),'source/write/descriptor/selector verified; repro',repro)


if __name__=='__main__':main()
