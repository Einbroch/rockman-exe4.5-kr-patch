"""Source-bound classification of nine historical deferrals, not a build gate."""
import re
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from prepare_repartition500 import layout_records
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of
from tpl_literals import literals
from korean_codec import EXTRA_CHARACTER_INDICES
BASE='poc/output/exe45_ko_development_pending500_014_v1.gba'
BASE_SHA='6cdcae37d8682c03a909b08d3ddefea02ad825c6a272899c38bcc5f316be9245'
PLAN=[('translations/batch500_046_remaining_768800_draft_ko.json',['768800:2:1','768800:2:3']),('translations/batch500_046_remaining_7B4184_draft_ko.json',['7B4184:0:0','7B4184:0:3','7B4184:4:0']),('translations/final_047_remaining_7C9C44_draft_ko.json',['7C9C44:0:0','7C9C44:0:1']),('translations/profile_data_manager_draft_ko.json',['7CC6A0:76:0','7CC6A0:78:0'])]
def advance(text):
    return [sum(12 if '\uac00'<=c<='\ud7a3' or c in EXTRA_CHARACTER_INDICES else 8 if c==' ' else 11 for c in line) for line in text.split('\n')]
def main():
    require_hash(ROOT/BASE,BASE_SHA);meta=read(BASE.replace('.gba','.json'))
    if meta['output_sha256']!=BASE_SHA:raise ValueError('Artifact identity')
    cfg=read('project.json');require_hash(ROOT/cfg['source_profile']['filename'],cfg['source_profile']['sha256']);source=(ROOT/cfg['source_profile']['filename']).read_bytes()
    require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256']);rows={format(r['offset'],'06X'):r for r in parse_tpi(ROOT/cfg['text_catalog']['path'])}
    applied={u['id'] for r in layout_records(meta) for u in r['layout']};records=[]
    for path,keys in PLAN:
        asset=read(path);a=asset['archive'];require_hash(ROOT/asset['source_tpl']['path'],asset['source_tpl']['sha256'])
        if asset['source_sha256']!=sha(source) or sha(payload_of(source,rows[a]))!=asset['source_archive_sha256']:raise ValueError('Source payload identity')
        tpl=(ROOT/asset['source_tpl']['path']).read_text(encoding='utf-8-sig');native={u.key:u for u in literals(tpl)}
        sections={int(m.group(1)):m.group() for m in re.finditer(r'^script\s+(\d+)\s+\w+\s*\{[\s\S]*?(?=^script\s|\Z)',tpl,re.M)}
        units={u['id']:u for u in asset['units']}
        for key in keys:
            u=units[key];s=int(key.split(':')[1]);section=sections[s]
            if key in applied or native[key].text!=u['source'] or u['state']!='needs_review':raise ValueError('Pending source/review identity')
            group=[v for v in asset['units'] if int(v['id'].split(':')[1])==s]
            for v in group:
                if native[v['id']].text!=v['source']:raise ValueError('Whole script source identity')
            small=native[key].language!='mmbn45';choice=bool(re.search(r'^\s*(option|select|positionOption\w*)\b',section,re.M))
            category='small-renderer' if small else 'choice-dialogue' if choice else 'normal-dialogue'
            geometry=[dict(id=v['id'],language=native[v['id']].language,applied=v['id'] in applied,adopted_normal_advances=advance(v['translation']),exceeds_adopted_normal_range=max(advance(v['translation']))>132) for v in group]
            next_action='Establish mmbn45s small-renderer encoding/glyph supply and caller, not normal-dialogue insertion.' if small else 'Preserve horizontal choice widths/padding/targets; validate complete script geometry and both outcomes.' if choice else 'Use whole-script cumulative merge and exact-artifact render verification; source-only selection is not ROM integration.'
            records.append(dict(id=key,draft=dict(path=path,sha256=sha((ROOT/path).read_bytes())),source_tpl=asset['source_tpl'],source_archive_sha256=asset['source_archive_sha256'],language=native[key].language,category=category,portrait_declared=bool(re.search(r'^\s*mugshotShow\b',section,re.M)),print_controls=sorted(set(re.findall(r'^\s*(print\w+)\b',section,re.M))),whole_script_geometry=geometry,next_action=next_action,wording_approved=False))
    if len(records)!=9 or len({r['id'] for r in records})!=9:raise ValueError('Finite backlog denominator')
    frozen_write(ROOT/'analysis/pending_insertion_500_015_partial_preflight_v1/backlog_consumers.json',dict(schema=1,baseline_rom=BASE,baseline_sha256=BASE_SHA,source_sha256=sha(source),pending_historic_ids=9,records=records,measurement='Existing adopted normal range132px/conservative advance rule; not confirmed small/choice consumer capacity',new_wording_preflight_ids=['7C9C44:0:0','7C9C44:0:1'],rom_written=False,runtime_tested=False,release_eligible=False))
    print('Nine pending source IDs verified:',[(r['id'],r['category']) for r in records])
if __name__=='__main__':main()
