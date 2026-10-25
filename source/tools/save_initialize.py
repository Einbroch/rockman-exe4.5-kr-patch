"""Save initialization UI9; data-only translation, never executes erase."""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from calendar_date_save import prepare as prepare_parent,validate as validate_parent,replace as replace_parent
from tpl_literals import literals,serialize,skeleton
from korean_codec import encode_character,decode_character
from verify_calendar_date_save_draft import width

PARENT='analysis/calendar_date_save_v1/selected_asset.json'
PARENT_SHA='d9cdea229702446a1c841e5aaba7cbbdc0210dbc0404618d4bbe5852e13e19a4'
DELTA='translations/save_initialize_draft_ko.json'
GENERATED='analysis/save_initialize_v1/selected_asset.json'
SCRIPTS=[96,97,98]
IDS={f'6368E8:{s}:{i}' for s,n in ((96,3),(97,5),(98,1)) for i in range(n)}
SOURCE='analysis/full_scope_v1/source_tpl/6368E8.tpl'

def validate_delta(a,original,available):
    if a['policy']!='development-draft; NON-DISTRIBUTION' or a['review']['release_eligible'] is not False:raise ValueError('development policy')
    source={x.key:x for x in literals(original)};units=a['units']
    if len(units)!=9 or {u['id'] for u in units}!=IDS:raise ValueError('initialize9 population')
    target=original;details=[]
    for u in sorted(units,key=lambda u:source[u['id']].start,reverse=True):
        x=source[u['id']];text=u['translation']
        if u['source']!=x.text or x.language!='mmbn45' or u['state']!='needs_review':raise ValueError('source/language/state')
        if not text or re.search(r'[\u3040-\u30ff\u3400-\u9fff]',text):raise ValueError('untranslated literal')
        if re.findall(r'\[[^\]]+\]|\d+',text)!=re.findall(r'\[[^\]]+\]|\d+',x.text):raise ValueError('token/number')
        widths=[width(line) for line in text.split('\n')]
        if len(widths)>3 or max(widths)>132:raise ValueError('proposed normal geometry')
        if u['id']=='6368E8:96:0' and (len(widths)!=3 or not text.endswith('\n') or widths[:2].count(0)):raise ValueError('initial question rows')
        if u['id']=='6368E8:97:2' and (not text.endswith('\n\n') or text.count('\n')!=2):raise ValueError('retry question rows')
        for c in text:
            if '\uac00'<=c<='\ud7a3' and (ord(c) not in available or decode_character(encode_character(c))[0]!=c):raise ValueError('glyph/codec')
        target=target[:x.start]+serialize(text)+target[x.end:]
        details.append(dict(id=u['id'],proposed_widths_px=widths))
    indexed={u['id']:u['translation'] for u in units}
    for s,yes,no in ((96,1,2),(97,3,4)):
        pair=[indexed[f'6368E8:{s}:{i}'] for i in (yes,no)]
        if any('\n' in t for t in pair) or 16+sum(width(t) for t in pair)>88:raise ValueError('horizontal width8 choices')
    if skeleton(original)!=skeleton(target):raise ValueError('protected command topology')
    after={x.key:x for x in literals(target)}
    if any(after[k].text!=x.text or after[k].language!=x.language for k,x in source.items() if k not in IDS):raise ValueError('unselected source')
    return details

def inputs():
    require_hash(ROOT/PARENT,PARENT_SHA);old=json.loads((ROOT/PARENT).read_text(encoding='utf8'));validate_parent(old)
    delta=json.loads((ROOT/DELTA).read_text(encoding='utf8'))
    if any(delta[k]!=old[k] for k in ('source_sha256','source_archive_sha256','archive','policy')):raise ValueError('initialize baseline')
    source=(ROOT/SOURCE).read_text(encoding='utf-8-sig')
    validate_delta(delta,source,set(range(0xAC00,0xD7A4)))
    return old,delta

def validate(a):
    old,delta=inputs()
    if a.get('parent_asset')!=dict(path=PARENT,sha256=PARENT_SHA,carry_units=55) or a['units']!=old['units']+delta['units']:raise ValueError('immutable common55/initialize9')
    return old

def replace(original,units):
    old,delta=inputs();validate(dict(parent_asset=dict(path=PARENT,sha256=PARENT_SHA,carry_units=55),units=units))
    if skeleton(original)!=skeleton((ROOT/SOURCE).read_text(encoding='utf-8-sig')):raise ValueError('source commands changed')
    target=replace_parent(original,old['units']);lookup={x.key:x for x in literals(target)}
    for u in sorted(delta['units'],key=lambda u:lookup[u['id']].start,reverse=True):
        x=lookup[u['id']]
        if x.text!=u['source']:raise ValueError('initialize source')
        target=target[:x.start]+serialize(u['translation'])+target[x.end:]
    if skeleton(original)!=skeleton(target):raise ValueError('initialize commands')
    return target

def prepare():
    prepare_parent();old,delta=inputs();a=dict(old)
    a.update(scope_variant='save-initialize-v1',parent_asset=dict(path=PARENT,sha256=PARENT_SHA,carry_units=55),units=old['units']+delta['units'],context=delta['context'],protected_policy=delta['protected_policy'],insertion_state='development input; explicit --save-initialize; generated read-only')
    validate(a);p=ROOT/GENERATED;p.parent.mkdir(exist_ok=True);p.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    return GENERATED

def main():
    old,a=inputs();cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'))
    source=ROOT/cfg['source_profile']['filename'];require_hash(source,a['source_sha256'])
    if a['source_sha256']!=cfg['source_profile']['sha256'] or sha(source.read_bytes()[0x6368E8:0x6368E8+2337])!=a['source_archive_sha256']:raise ValueError('ROM/archive')
    font=cfg['development_dependencies']['font'];require_hash(ROOT/font['path'],font['sha256'])
    available={int(line.split()[1]) for line in (ROOT/font['path']).read_text(encoding='utf8').splitlines() if line.startswith('ENCODING ')}
    details=validate_delta(a,(ROOT/SOURCE).read_text(encoding='utf-8-sig'),available)
    out=ROOT/'analysis/save_initialize_draft_v1';out.mkdir(exist_ok=True)
    result=dict(passed=True,units=9,rom_integrated=False,runtime_verified=False,release_eligible=False,asset_sha256=sha((ROOT/DELTA).read_bytes()),source_sha256=a['source_sha256'],parent_sha256=PARENT_SHA,font_sha256=font['sha256'],source_tpl_sha256=sha((ROOT/SOURCE).read_bytes()),tools={'save_initialize.py':sha((ROOT/'tools/save_initialize.py').read_bytes())},details=details,limits=['Data-only translation. Source erase/save commands, defaults and retry targets retained; no erase invocation or save-data write.', 'Draft semantics and proposed132px/3rows and width8 choices only. Actual caller/render/VRAM/screen and save regression pending.'])
    (out/'report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print('PASS9 initialization draft; NOT ROM/runtime')

if __name__=='__main__':main()
