"""Extend pinned keyitem recipe; preserve every previous artifact."""
import argparse,json,subprocess,sys
from build_visibility_poc import ROOT,require_hash
from possessions_statistics import validate,CHILD

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--name',required=True);a=ap.parse_args()
    if not a.name.replace('_','').isalnum():raise ValueError('simple artifact name required')
    validate(json.loads((ROOT/CHILD).read_text(encoding='utf8')))
    recipe=json.loads((ROOT/'analysis/keyitem_empty_v1/build_recipe.json').read_text())
    require_hash(ROOT/recipe['parent_recipe'],recipe['parent_recipe_sha256'])
    parent=json.loads((ROOT/recipe['parent_recipe']).read_text())
    out=ROOT/f'poc/output/{a.name}.gba';work=ROOT/f'poc/build/{a.name}'
    if out.exists() or work.exists():raise ValueError('preserve prior builds')
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/recipe['builder']),*parent['flags'],*recipe['additional_flags'],
        '--possessions-statistics','--work',str(work.relative_to(ROOT)),'--out',str(out.relative_to(ROOT))],check=True,cwd=ROOT)
if __name__=='__main__':main()
