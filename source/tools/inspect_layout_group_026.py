"""Read-only exact source/draft view for one unresolved script group."""
import argparse,re
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read

def main():
    ap=argparse.ArgumentParser();ap.add_argument('archive');ap.add_argument('script',type=int);a=ap.parse_args()
    coverage=read('analysis/translation_first_v1/coverage.json')
    seen=set()
    for path,h in coverage['draft_asset_hashes'].items():
        require_hash(ROOT/path,h);asset=read(path)
        units=[u for u in asset['units'] if u['id'].startswith(a.archive+':'+str(a.script)+':')]
        if not units:continue
        ref=asset['source_tpl'];require_hash(ROOT/ref['path'],ref['sha256'])
        tpl=(ROOT/ref['path']).read_text(encoding='utf-8-sig')
        m=re.search(r'^script '+str(a.script)+r' mmbn45 \{[\s\S]*?(?=^script\s|\Z)',tpl,re.M)
        if not seen:print(m[0])
        for u in units:
            if u['id'] not in seen:print(u['id'],repr(u['source']),'=>',repr(u['translation']));seen.add(u['id'])
    if not seen:raise ValueError('No canonical draft group')

if __name__=='__main__':main()
