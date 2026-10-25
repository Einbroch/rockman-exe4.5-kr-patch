"""Read-only final tool/source/independent-build identity audit with receipt."""
import json
from report_roll_pet import ROOT,read,sha,static
from run_roll_food import STEM

def main(stem=STEM,outdir='roll_food_v1',final_suffix='_current_repro'):
    source=read(ROOT/'project.json')['source_profile'];m=read(ROOT/f'poc/output/{stem}{final_suffix}.json')
    actual={p.name:sha(p.read_bytes()) for p in sorted((ROOT/'tools').glob('*.py'))};pinned=m['build_tools_sha256']
    drift=sorted(k for k in set(actual)|set(pinned) if actual.get(k)!=pinned.get(k))
    builds={suffix:sha((ROOT/f'poc/output/{stem}{suffix}.gba').read_bytes()) for suffix in ['','_repro',final_suffix]}
    source_hash=sha((ROOT/source['filename']).read_bytes())
    if drift or len(set(builds.values()))!=1 or builds['']!=m['output_sha256'] or source_hash!=source['sha256']:raise ValueError('food final source/tools/reproduction mismatch')
    static(stem,'661858')
    result={'policy':'development-draft; NON-DISTRIBUTION','passed':True,'release_eligible':False,'source_sha256':source_hash,'output_sha256':m['output_sha256'],'builds':builds,'tool_count':len(actual),'tool_drift':drift}
    out=ROOT/'analysis'/outdir/'final_identity_audit.json';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result));return result

if __name__=='__main__':main()
