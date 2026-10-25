"""Transfer bounded native CPU evidence only by complete declared byte identity."""
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write

def main():
    rp=ROOT/'poc/output/pending500_026_v1.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();checked=[]
    for path in ('analysis/pending_insertion_500_025_native_controls_v1/cpu.json','analysis/pending_insertion_500_026_native_controls_v1/cpu.json'):
        evidence=read(path)
        if not evidence['passed'] or evidence['substituted_helpers']:raise ValueError('Native CPU baseline scope')
        for region in evidence['native_ranges']:
            at,n=region['offset'],region['bytes']
            if sha(rom[at:at+n])!=region['sha256']:raise ValueError('026 native code/data applicability changed')
        checked.append(dict(path=path,sha256=sha((ROOT/path).read_bytes()),ranges=len(evidence['native_ranges']),original_cpu_cases=evidence['case_count']))
    frozen_write(ROOT/'analysis/pending500_026_v1/native_control_identity.json',dict(schema=1,passed=True,rom_sha256=sha(rom),evidence=checked,all_declared_native_code_dispatch_and_literal_bytes_identical=True,new_cpu_fixtures_executed=0,runtime_tested=False,release_eligible=False,limits='Byte-identity transfer of bounded source/024 and source/025 native CPU evidence. Not fresh CPU executions, GBA cursor/extended glyph rendering, natural caller/event/battle effects or persistence evidence.'))
    print('PASS026 native code/table/helper identity transfer; no new CPU/runtime claim')

if __name__=='__main__':main()
