"""Final source/write-ledger/append/input/tool pins and reproducibility audit."""
import ast,json,shutil,argparse
from build_visibility_poc import ROOT,sha,require_hash
from run_possessions_statistics import STEM
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--refresh-manifest',action='store_true');args=ap.parse_args()
    p=ROOT/f'poc/output/{STEM}_current_repro_r2.json';m=json.loads(p.read_text(encoding='utf8'))
    if args.refresh_manifest:
        # Corrected input-policy metadata changes no ROM bytes. Preserve the
        # first generated manifest; publish the latest builder-emitted metadata
        # only after confirming byte identity of both referenced ROMs.
        main=ROOT/f'poc/output/{STEM}.json';backup=ROOT/'analysis/possessions_statistics_v1/initial_build_manifest.json'
        if backup.exists():raise ValueError('preserve first manifest snapshot')
        old=json.loads(main.read_text(encoding='utf8'))
        require_hash(main.with_suffix('.gba'),m['output_sha256']);require_hash(p.with_suffix('.gba'),m['output_sha256'])
        if old['output_sha256']!=m['output_sha256']:raise ValueError('metadata refresh cannot change product bytes')
        shutil.copy2(main,backup);shutil.copy2(p,main)
        (backup.parent/'manifest_refresh.json').write_text(json.dumps(dict(reason='Correct policy metadata: source0x40 is カ, not a count prefix. Product bytes unchanged.',preserved_manifest_sha256=sha(backup.read_bytes()),fresh_builder_manifest_sha256=sha(p.read_bytes()),rom_sha256=m['output_sha256']),ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        print('Manifest refreshed; original manifest preserved; ROM byte identity verified');return
    r=p.with_suffix('.gba').read_bytes();cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'))
    source=ROOT/cfg['source_profile']['filename'];require_hash(source,cfg['source_profile']['sha256']);s=source.read_bytes()
    outputs={}
    for suffix in ['', '_repro','_current_repro','_current_repro_r2']:
        f=ROOT/f'poc/output/{STEM}{suffix}.gba';require_hash(f,m['output_sha256']);outputs[f.name]=sha(f.read_bytes())
    if r[:192]!=s[:192] or len(r)!=len(s)+m['append_bytes'] or sha(r[len(s):])!=m['append_sha256']:raise ValueError('header/append/size')
    rebuilt=bytearray(s);occupied=set()
    for w in m['expected_writes']:
        at=w['offset'];n=w['bytes'];data=bytes.fromhex(w['final_hex'])
        if len(data)!=n or s[at:at+n]!=bytes.fromhex(w['expected_hex']) or occupied.intersection(range(at,at+n)):raise ValueError('ledger source/overlap/extent')
        occupied.update(range(at,at+n));rebuilt[at:at+n]=data
    if bytes(rebuilt)!=r[:len(s)]:raise ValueError('unplanned source differences')
    for a in m['translation_assets']:require_hash(ROOT/a['path'],a['sha256'])
    tools={p.name:sha(p.read_bytes()) for p in (ROOT/'tools').glob('*.py')}
    drift=sorted(set(tools)^set(m['build_tools_sha256'])|{k for k in tools.keys()&m['build_tools_sha256'].keys() if tools[k]!=m['build_tools_sha256'][k]})
    if drift:raise ValueError('tool drift '+str(drift))
    for f in (ROOT/'tools').glob('*.py'):ast.parse(f.read_text(encoding='utf-8-sig'),filename=str(f))
    reports={}
    for name in ['runtime.json','statistics_runtime.json']:
        f=ROOT/'analysis/possessions_statistics_v1'/name;a=json.loads(f.read_text(encoding='utf8'))
        if a['rom_sha256']!=m['output_sha256'] or not a['passed']:raise ValueError('runtime identity')
        reports[name]=sha(f.read_bytes())
    result=dict(passed=True,rom_sha256=m['output_sha256'],source_unchanged=True,byte_identical_outputs=outputs,current_build_manifest=str(p.relative_to(ROOT)),tool_count=len(tools),tool_drift=drift,python_ast_pass=True,final_write_ledger_verified=True,header_unchanged=True,append_verified=True,translation_asset_hashes_verified=True,runtime_reports=reports,release_eligible=False)
    f=ROOT/'analysis/possessions_statistics_v1/final_identity.json';f.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
