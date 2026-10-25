"""Investigate unchanged-wording line placement on the verified016 baseline.

No new windows/pages, row-count changes, prose edits, or caller relaxation.
Freeze explicit placements outside product builds; not distribution approval.
"""
import re
from collections import defaultdict,Counter
from functools import lru_cache
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from prepare_repartition500 import layout_records
from tpl_literals import literals
from korean_codec import EXTRA_CHARACTER_INDICES
SURVEY='analysis/pending_insertion_500_017_survey_v1/survey.json'
OUT='analysis/pending_insertion_500_017_layout_survey_v1/survey.json'

def advance(text):
    return sum(12 if '\uac00'<=c<='\ud7a3' or c in EXTRA_CHARACTER_INDICES else 8 if c==' ' else 11 for c in text)

def protected_edges(source,target):
    return all(len(source)-len(strip(source))==len(target)-len(strip(target)) for strip in (lambda s:s.lstrip('\n'),lambda s:s.rstrip('\n'),lambda s:s.rstrip(' ')))

def place(text):
    rows=text.count('\n')+1
    if rows>3:return None
    if max(map(advance,text.split('\n')))<=132:return text
    flat=text.replace('\n',' ')
    # Only an existing space may become a newline, with exactly the old rows.
    @lru_cache(None)
    def solve(start,left):
        if left==1:
            tail=flat[start:]
            return (tail,) if tail and advance(tail)<=132 else None
        candidates=[]
        for at in range(start+1,len(flat)):
            if flat[at]!=' ':continue
            line=flat[start:at]
            if advance(line)>132:break
            if not line or line.endswith(' '):continue
            tail=solve(at+1,left-1)
            if tail is not None:candidates.append((line,)+tail)
        return min(candidates,key=lambda lines:(max(map(advance,lines)),sum((132-advance(l))**2 for l in lines),lines)) if candidates else None
    lines=solve(0,rows)
    if lines is None:return None
    result='\n'.join(lines)
    if result.replace('\n',' ')!=flat or result.count('\n')!=text.count('\n'):raise ValueError('Protected wording/topology')
    return result

def main(preserve_edges=False):
    s=read(SURVEY);require_hash(ROOT/s['baseline_rom'],s['baseline_sha256'])
    meta=read(s['baseline_rom'].replace('.gba','.json'))
    if meta['output_sha256']!=s['baseline_sha256'] or s['pinned_changed_inputs']:raise ValueError('Baseline corpus')
    coverage=read(s['pinned_coverage']['path']);require_hash(ROOT/s['pinned_coverage']['path'],s['pinned_coverage']['sha256'])
    pool=defaultdict(list)
    for path,digest in coverage['draft_asset_hashes'].items():
        require_hash(ROOT/path,digest)
        for u in read(path)['units']:pool[u['id']].append((path,digest,u))
    groups=list(s['candidates']);rejected=[]
    for g in s['unresolved_groups']:
        if g['reasons']!=['adopted_normal_geometry']:continue
        refs=[];placements={};widths={};parent=None
        for key in g['ids']:
            options=pool[key]
            if len({(u['source'],u['translation'],u['state']) for _,_,u in options})!=1:raise ValueError('Conflicting wording')
            path,digest,u=options[0];value=place(u['translation'])
            if value is None:break
            refs.append(dict(id=key,path=path,sha256=digest));widths[key]=list(map(advance,value.split('\n')))
            if value!=u['translation']:placements[key]=value
            parent=read(path)
        else:
            require_hash(ROOT/parent['source_tpl']['path'],parent['source_tpl']['sha256'])
            native={u.key:u for u in literals((ROOT/parent['source_tpl']['path']).read_text(encoding='utf-8-sig'))}
            if any(pool[k][0][2]['source']!=native[k].text for k in g['ids']):raise ValueError('Protected source')
            groups.append(dict(archive=g['archive'],script=g['script'],units=len(g['ids']),ids=g['ids'],drafts=refs,source_tpl=parent['source_tpl'],source_archive_sha256=parent['source_archive_sha256'],adopted_normal_advances=widths,explicit_layouts=placements))
            continue
        rejected.append(g)
    boundary_rejections=[]
    if preserve_edges:
        admitted=[]
        for g in groups:
            invalid=[]
            for key in g['ids']:
                u=pool[key][0][2];value=g.get('explicit_layouts',{}).get(key,u['translation']);source=u['source']
                if not protected_edges(source,value):invalid.append(key)
            if invalid:boundary_rejections.append(dict(archive=g['archive'],script=g['script'],ids=invalid,reason='protected leading/trailing LF and padding'))
            else:admitted.append(g)
        groups=admitted
    applied={r['archive'] for r in layout_records(meta)};registry=read('tools/specs/exe45_dialogue_archives_v1.json')['archives']
    untouched=[g for g in groups if g['archive'] not in applied and g['archive'] not in registry]
    result=dict(schema=1,source_sha256=s['source_sha256'],baseline_rom=s['baseline_rom'],baseline_sha256=s['baseline_sha256'],survey=dict(path=SURVEY,sha256=sha((ROOT/SURVEY).read_bytes())),candidate_groups=len(groups),candidate_units=sum(g['units'] for g in groups),untouched_units=sum(g['units'] for g in untouched),candidates=groups,rejected_geometry_groups=rejected,changed_layout_units=sum(len(g.get('explicit_layouts',{})) for g in groups),rom_written=False,prose_changed=False,release_eligible=False,policy='development-draft; NON-DISTRIBUTION',limits='Only same-row-count whitespace line placement under the adopted normal3-row132px scope. No other rejection waived. Not insertion readiness, full remaining population, or semantic/presentation approval.')
    if preserve_edges:result.update(protected_edge_policy=True,boundary_rejections=boundary_rejections)
    frozen_write(ROOT/OUT,result)
    print('Candidates',len(groups),sum(g['units'] for g in groups),'untouched',sum(g['units'] for g in untouched),'layout changes',sum(len(g.get('explicit_layouts',{})) for g in groups))
    print('Untouched archives',dict(Counter(g['archive'] for g in untouched)))
if __name__=='__main__':main()
