"""Static date/save draft source/control/codec/font and choice-layout checks.

Does not invoke date change, initialize saves, build ROM or approve semantics.
"""
import json,re
from build_visibility_poc import ROOT,sha,require_hash
from tpl_literals import literals,serialize,skeleton
from korean_codec import encode_character,decode_character

ASSET='translations/calendar_date_save_draft_ko.json'
IDS={f'6368E8:{s}:{i}' for s,n in ((76,1),(90,1),(91,5),(92,5),(93,1),(94,4)) for i in range(n)}
PROMPTS={'6368E8:91:2','6368E8:92:2','6368E8:94:1'}
CHOICES=[('6368E8:91:3','6368E8:91:4'),('6368E8:92:3','6368E8:92:4'),('6368E8:94:2','6368E8:94:3')]

def width(line):
    tokens=re.findall(r'\[z\]|.',line)
    return sum(12 if len(c)==1 and '\uac00'<=c<='\ud7a3' else 8 if c==' ' else 11 for c in tokens)

def validate(a,original,available):
    if a['policy']!='development-draft; NON-DISTRIBUTION' or a['review']['release_eligible']:raise ValueError('draft policy')
    source={x.key:x for x in literals(original)};units=a['units'];keys=[u['id'] for u in units]
    if len(keys)!=17 or set(keys)!=IDS:raise ValueError('IDs')
    target=original;details=[]
    for u in sorted(units,key=lambda u:source[u['id']].start,reverse=True):
        x=source[u['id']];text=u['translation']
        if x.text!=u['source'] or x.language!='mmbn45' or u['state']!='needs_review':raise ValueError('source/state/language')
        if not text or re.search(r'[\u3040-\u30ff\u3400-\u9fff]',text):raise ValueError('empty/untranslated')
        if re.findall(r'\[[^\]]+\]',text)!=re.findall(r'\[[^\]]+\]',x.text) or re.findall(r'\d+',text)!=re.findall(r'\d+',x.text):raise ValueError('protected token/number')
        if u['id'] in PROMPTS and (not text.endswith('\n\n') or text.count('\n')!=2):raise ValueError('choice row placement')
        if u['id']=='6368E8:92:0' and not text.endswith('\n'):raise ValueError('save trailing row')
        lines=text.split('\n');widths=[width(line) for line in lines]
        if len(lines)>3 or max(widths)>132:raise ValueError('proposed normal layout')
        for c in text:
            if '\uac00'<=c<='\ud7a3':
                if ord(c) not in available or decode_character(encode_character(c))[0]!=c:raise ValueError('glyph/codec')
        target=target[:x.start]+serialize(text)+target[x.end:]
        details.append(dict(id=u['id'],proposed_widths_px=widths))
    indexed={u['id']:u['translation'] for u in units}
    for yes,no in CHOICES:
        if '\n' in indexed[yes]+indexed[no] or 16+width(indexed[yes])+width(indexed[no])>88:raise ValueError('horizontal width8 group')
    if skeleton(target)!=skeleton(original):raise ValueError('command topology')
    after={x.key:x for x in literals(target)}
    if any(after[k].text!=x.text or after[k].language!=x.language for k,x in source.items() if k not in IDS):raise ValueError('unselected source')
    return details

def main():
    path=ROOT/ASSET;a=json.loads(path.read_text(encoding='utf8'));profile=json.loads((ROOT/'project.json').read_text(encoding='utf8'))
    src=ROOT/profile['source_profile']['filename'];require_hash(src,a['source_sha256'])
    if a['source_sha256']!=profile['source_profile']['sha256'] or sha(src.read_bytes()[0x6368E8:0x6368E8+2337])!=a['source_archive_sha256']:raise ValueError('source/archive')
    original=(ROOT/'analysis/full_scope_v1/source_tpl/6368E8.tpl').read_text(encoding='utf-8-sig')
    font=profile['development_dependencies']['font'];require_hash(ROOT/font['path'],font['sha256'])
    available={int(line.split()[1]) for line in (ROOT/font['path']).read_text(encoding='utf8').splitlines() if line.startswith('ENCODING ')}
    details=validate(a,original,available)
    table=ROOT/'external/textpet-plugins/exe45-utf8.tbl';require_hash(table,profile['textpet']['plugin_sha256']['exe45-utf8.tbl'])
    if '99=[z]' not in table.read_text(encoding='utf-8-sig').splitlines():raise ValueError('retained currency glyph99')
    out=ROOT/'analysis/calendar_date_save_draft_v1';out.mkdir(exist_ok=True)
    report=dict(passed=True,rom_integrated=False,runtime_verified=False,release_eligible=False,units=17,asset_sha256=sha(path.read_bytes()),source_sha256=a['source_sha256'],source_archive_sha256=a['source_archive_sha256'],source_tpl_sha256=sha(original.encode()),font_sha256=font['sha256'],currency_glyph=dict(token='[z]',legacy_byte='99'),tools={'verify_calendar_date_save_draft.py':sha((ROOT/'tools/verify_calendar_date_save_draft.py').read_bytes())},details=details,limits=['Static source/control/token/numeral/BDF/codec and proposed geometry only. Choice defaults/targets/callSave/callChangeTimeDate unchanged in proposal.', 'No ROM selection, date change, save initialization, disk writes to user saves or runtime screen. Script76 custom window and actual91/92/94 choices need consumer verification.', 'Wording/layout/human review and previous21 runtime remain pending.'])
    (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    print('PASS17 date/save draft; NOT ROM/runtime',flush=True)

if __name__=='__main__':main()
