"""Full120 mail clone, retaining the bounded77 loader and its guard header."""
import json,struct
from build_visibility_poc import ROOT,sha,require_hash
from first_mail import selected_units,SPECS
from tpl_literals import literals,skeleton,replace_literals,serialize

ASSET='analysis/full_mail_body_v1/6DD9AC_selected_asset.json'
LAYOUT='translations/full_mail_body_layout_v1.json'
SCOPE=dict(consumer='normal-dialogue',complete_literal_scope=True,script_count=32,
    literal_scripts=[0,1,2,3,8,9,10,11,12,13,14],max_literal_rows=3,
    max_line_advance=152,preserve_literal_numerals=True)
NAME_RANGES=[(0x39E34,0x39E42),(0x39E68,0x39E6C),(0x355B6,0x355F6),
    (0x35484,0x35490),(0x35494,0x354A0),(0x35620,0x3562C),
    (0x517D0,0x51820),(0x527C8,0x527D0)]

def units():
    s=SPECS['6DD9AC'];require_hash(ROOT/s['draft'],s['draft_sha'])
    draft=json.loads((ROOT/s['draft']).read_text(encoding='utf8'))
    keep=selected_units('6DD9AC','news');ids={u['id'] for u in keep}
    new=[dict(id=u['id'],source=u['source'],translation=u['translation'],state='needs_review') for u in draft['units'] if u['id'] not in ids]
    proposal=json.loads((ROOT/LAYOUT).read_text(encoding='utf8'))
    if proposal['release_eligible'] is not False or set(proposal['layouts'])!={'6DD9AC:11:0','6DD9AC:12:0','6DD9AC:12:8','6DD9AC:14:4'}:raise ValueError('full mail individual layout authority')
    for u in new:
        if u['id'] in proposal['layouts']:
            value=proposal['layouts'][u['id']]
            if value.replace('\n',' ')!=u['translation'].replace('\n',' '):raise ValueError('full mail layout changes wording')
            u['translation']=value
    if len(keep)!=77 or len(new)!=43:raise ValueError('full mail selected denominator')
    return keep+new

def prepare():
    s=SPECS['6DD9AC'];draft=json.loads((ROOT/s['draft']).read_text(encoding='utf8'))
    require_hash(ROOT/draft['source_tpl']['path'],draft['source_tpl']['sha256'])
    selected=units();tpl=(ROOT/draft['source_tpl']['path']).read_text(encoding='utf-8-sig')
    if {x.key for x in literals(tpl)}!={u['id'] for u in selected}:raise ValueError('full120 literal population')
    asset=dict(schema=1,policy='development-draft; NON-DISTRIBUTION',archive='6DD9AC',
        source_sha256=draft['source_sha256'],source_tpl=draft['source_tpl'],source_archive_sha256=draft['source_archive_sha256'],
        consumer='normal-dialogue',context='Full120 raw-ROM clone; bounded77 RAM payload remains unchanged. New43 mail body literals only; native story commands preserved; receipt routes not established.',
        review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),units=selected)
    path=ROOT/ASSET;path.parent.mkdir(exist_ok=True)
    data=json.dumps(asset,ensure_ascii=False,indent=2)+'\n'
    if path.exists() and path.read_text(encoding='utf8')!=data:raise ValueError('preserve full mail selected input')
    if not path.exists():path.write_text(data,encoding='utf8')
    return ASSET

def replace(original,selected):
    if selected!=units():raise ValueError('full mail replace scope')
    exceptions={'6DD9AC:11:0','6DD9AC:12:0'}
    target=replace_literals(original,[u for u in selected if u['id'] not in exceptions])
    indexed={u['id']:u for u in selected}
    for item in reversed(literals(target)):
        if item.key in exceptions:
            u=indexed[item.key]
            if item.text!=u['source'] or item.language!='mmbn45' or item.text.count('\n')!=1 or u['translation'].count('\n')!=2:raise ValueError('explicit title2-to3-row policy')
            target=target[:item.start]+serialize(u['translation'])+target[item.end:]
    if skeleton(original)!=skeleton(target):raise ValueError('full mail controls changed')
    return target

def validate(source,asset,original,translated,layout):
    draft=json.loads((ROOT/SPECS['6DD9AC']['draft']).read_text(encoding='utf8'))
    if (asset['schema']!=1 or asset['policy']!='development-draft; NON-DISTRIBUTION' or asset['archive']!='6DD9AC'
        or asset['consumer']!='normal-dialogue' or asset['source_sha256']!=sha(source)
        or asset['source_tpl']!=draft['source_tpl'] or asset['source_archive_sha256']!=draft['source_archive_sha256']
        or asset['units']!=units() or asset['review']['release_eligible'] is not False or skeleton(original)!=skeleton(translated)):
        raise ValueError('full mail immutable literals/controls/policy')
    # Native actual-player-name producer (not nickname or subject descriptor).
    # r0=6 at039E34 passes to0355B6; limit stored at editor+4.
    # 035494..A0 rejects another glyph when count035620 equals limit.
    # Each editor glyph occupies one2-byte slot before03562C compaction.
    expected={0x39E34:'062024210b4a',0x39E68:'500e0002',0x35494:'142000f0c3f8',
              0x3549A:'217988426ed0',0x355D8:'2071',0x35620:'4a4b19691858401a4008f746',0x527C8:'510e00020d000000'}
    # Reject drift against pinned native instructions; no extrapolation to a future custom storage ABI.
    for at,h in expected.items():
        if source[at:at+len(bytes.fromhex(h))]!=bytes.fromhex(h):raise ValueError(f'player name producer profile {at:06X}')
    measured={x['id']:x['line_advance_pixels'] for x in layout}
    for key,widths in measured.items():
        if len(widths)==3 and widths[2]>132:raise ValueError('mail row3 arrow overlap '+key)
    joins=[(11,5,6),(11,7,8),(12,1,2),(13,2,3),(14,None,0)]
    indexed={u['id']:u for u in asset['units']};proof=[]
    for script,before,after in joins:
        a='' if before is None else indexed[f'6DD9AC:{script}:{before}']['translation']
        b=indexed[f'6DD9AC:{script}:{after}']['translation']
        if a and not a.endswith('\n'):raise ValueError('name must start at row origin')
        width=72+measured[f'6DD9AC:{script}:{after}'][0]
        rows=a.count('\n')+b.count('\n')+1
        if width>152 or rows>3:raise ValueError('full mail joined name overflow')
        proof.append(dict(script=script,before=before,after=after,native_name_max_glyphs=6,
            adopted_name_max_advance_px=72,joined_row_max_advance_px=width,page_rows=rows,
            descriptor_index=31,descriptor_pointer=0x02000E51,descriptor_copy_bytes=13))
    return dict(name_joins=proof,native_producer_ranges=[dict(start=a,end=b,sha256=sha(source[a:b])) for a,b in NAME_RANGES],
        limits='Native six-glyph player name only; does not adopt automatic Hangul input/save ABI. Human wording/presentation approval pending.')

def payload(rom,m):
    from verify_tpi_index import lz77_decompress
    meta=m.get('keyitem_rom',{}).get('mail_rom_reader')
    if meta:
        at=meta['clone_address']-0x08000000;body=rom[at:at+meta['payload_bytes']]
        if sha(body)!=meta['rom_sha256']:raise ValueError('mail reader clone hash')
        return body,meta['clone_address']
    row=next(r for r in m['archives'] if r['archive']=='6DD9AC')
    return lz77_decompress(rom,row['rom_offset'])[0],0x0202B2F4
