"""Actual040 immutable byte-image corruption refusal; no ROM files written."""
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from typed_rom_product040_v2 import verify_final


def main():
    rp=ROOT/'poc/output/pending500_040_v2.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes();audit=read('analysis/pending500_040_v2/integration.json')
    if not audit['passed'] or audit['rom_sha256']!=sha(rom):raise ValueError('040 exact audit prerequisite')
    if verify_final(source,rom,m['keyitem_rom']) is not True:raise ValueError('040 valid control must pass')
    n=m['keyitem_rom']['typed040'];cases=[('source-header',0xAC),('shared-LZ-root',0x4493C),('source-lookup',0x448E0),('common-stub',0x4FB4C),('wrapper-first',n['code_offset']),('wrapper-last',n['code_offset']+n['code_bytes']-1),('descriptor-first',n['descriptor_offset']),('descriptor-last',n['descriptor_offset']+10*28-1)]
    cases.extend([('tournament-root',0x47964),('tournament-table',0x47980),('BBS-root',0x4B824),('BBS-table',0x4B380)])
    for p in n['placements']:
        cases.append((p['source_archive']+'-native',p['native_copy_offset']+p['native_copy_bytes']//2));cases.append((p['source_archive']+'-target',p['rom_offset']+p['compiled_bytes']//2))
    results=[]
    for label,at in cases:
        bad=bytearray(rom);bad[at]^=1
        try:verify_final(source,bytes(bad),m['keyitem_rom'])
        except ValueError as exc:results.append(dict(case=label,offset=at,rejected=True,reason=str(exc)))
        else:raise ValueError('040 corruption accepted: '+label)
    if sha(rp.read_bytes())!=m['output_sha256']:raise ValueError('040 original artifact mutated')
    paths=['tools/verify_typed_corruption040_v1.py','tools/typed_rom_product040_v2.py','analysis/pending500_040_v2/integration.json']
    frozen_write(ROOT/'analysis/pending500_040_v2/corruption_v1.json',dict(passed=True,scope=__doc__,rom_sha256=sha(rom),valid_control_passed=True,corruptions_rejected=len(results),cases=results,ROM_files_written=False,dependencies={p:sha((ROOT/p).read_bytes()) for p in paths},runtime_tested=False,release_eligible=False))
    print('PASS040 actual image valid control and',len(results),'corruption refusals; no ROM writes')


if __name__=='__main__':main()
