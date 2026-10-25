"""Static source/control/font/layout checks for unselected input UI draft.

No ROM build or runtime claim. Existing selected parent asset is immutable.
"""
import json
from build_visibility_poc import ROOT, sha, require_hash
from tpl_literals import literals, serialize, skeleton


def main():
    path=ROOT/'translations/input_remaining_draft_ko.json'
    a=json.loads(path.read_text(encoding='utf8'))
    profile=json.loads((ROOT/'project.json').read_text(encoding='utf8'))
    require_hash(ROOT/profile['source_profile']['filename'],a['source_sha256'])
    if a['source_sha256']!=profile['source_profile']['sha256'] or a['policy']!='development-draft; NON-DISTRIBUTION' or a['review']['release_eligible']: raise ValueError('draft/source policy')
    parent=a['parent_asset']; require_hash(ROOT/parent['path'],parent['sha256'])
    old=json.loads((ROOT/parent['path']).read_text(encoding='utf8'))
    if len(old['units'])!=parent['carry_units']: raise ValueError('parent scope')
    original=(ROOT/'analysis/full_scope_v1/source_tpl/6368E8.tpl').read_text(encoding='utf-8-sig')
    source={x.key:x for x in literals(original)}
    expected={f'6368E8:{n}:0' for n in (11,21,23,24,25,26,27,28,29,30,31,32,34,35,36,37,38,39,40,41,42)}
    units=a['units']; keys=[x['id'] for x in units]
    if set(keys)!=expected or len(keys)!=len(expected) or set(keys)&{x['id'] for x in old['units']}: raise ValueError('duplicate/omitted/inherited selection')
    font=profile['development_dependencies']['font']; require_hash(ROOT/font['path'],font['sha256'])
    available={int(line.split()[1]) for line in (ROOT/font['path']).read_text(encoding='utf8').splitlines() if line.startswith('ENCODING ')}
    details=[]; target=original
    for unit in sorted(units,key=lambda u:source[u['id']].start,reverse=True):
        x=source[unit['id']]; text=unit['translation']; notice=unit['id']=='6368E8:11:0'
        if unit['source']!=x.text or unit['state']!='needs_review' or x.language!=('mmbn45' if notice else 'mmbn45s'): raise ValueError('source/state/consumer')
        if not text or any('\u3040'<=c<='\u30ff' or '\u4e00'<=c<='\u9fff' for c in text): raise ValueError('untranslated draft')
        missing={c for c in text if '\uac00'<=c<='\ud7a3' and ord(c) not in available}
        if missing: raise ValueError('font missing '+str(missing))
        lines=text.split('\n')
        widths=[sum(12 if '\uac00'<=c<='\ud7a3' else 8 if c==' ' else 11 for c in line) for line in lines] if notice else [len(line)*8 for line in lines]
        if notice and (len(lines)>3 or max(widths)>132) or not notice and (len(lines)!=1 or len(text)>10): raise ValueError('proposed adopted layout '+unit['id'])
        target=target[:x.start]+serialize(text)+target[x.end:]
        details.append(dict(id=unit['id'],consumer=x.language,lines=len(lines),proposed_widths_px=widths))
    if skeleton(target)!=skeleton(original): raise ValueError('protected controls')
    changed={x.key:x.text for x in literals(target)}
    for key,x in source.items():
        if key not in expected and changed[key]!=x.text: raise ValueError('unselected source changed')
    out=ROOT/'analysis/input_remaining_draft_v1'; out.mkdir(exist_ok=True)
    report=dict(passed=True,rom_integrated=False,runtime_verified=False,release_eligible=False,units=len(units),asset_sha256=sha(path.read_bytes()),source_tpl_sha256=sha(original.encode()),font_sha256=font['sha256'],tools={'verify_input_remaining_draft.py':sha((ROOT/'tools/verify_input_remaining_draft.py').read_bytes())},details=sorted(details,key=lambda x:int(x['id'].split(':')[1])),limits=['Static draft-only source/control and BDF Hangul coverage. Source extraction baseline belongs to declared revision.', 'Proposed mono10-cell/normal132px layout checked, not actual provider/runtime/screen consumption.', 'No product selection, ROM modification, save or screenshot. Headings20/22 excluded pending gender-dependent wording. Human wording/presentation review pending.'])
    (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    print('PASS21 draft source/control/font/proposed layout; NOT ROM/runtime',flush=True)


if __name__=='__main__': main()
