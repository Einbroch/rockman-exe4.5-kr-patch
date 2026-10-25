"""Source-bound mission metadata selection; existing draft wording is unchanged."""
import json,re,struct
from build_visibility_poc import ROOT,require_hash
from tpl_literals import literals

ASSET='analysis/mission_mail_header_v1/6DD864_selected_asset.json'
DRAFT='translations/batch500_016_mailhead_6DD864_draft_ko.json'
DRAFT_SHA='2ea08f800bee7708ee3fb591eb9b2ed2a77d577dc723647642f69086dbe43bc4'
SCRIPTS=list(range(40))+[41,65]

def selected():
    require_hash(ROOT/DRAFT,DRAFT_SHA)
    d=json.loads((ROOT/DRAFT).read_text(encoding='utf8'))
    require_hash(ROOT/d['source_tpl']['path'],d['source_tpl']['sha256'])
    units=[{k:u[k] for k in ('id','source','translation','state')} for u in d['units']]
    originals={u.key:u.text for u in literals((ROOT/d['source_tpl']['path']).read_text(encoding='utf-8-sig')) if int(u.key.split(':')[1]) in SCRIPTS}
    if len(units)!=42 or {u['id']:u['source'] for u in units}!=originals:raise ValueError('mission metadata source population')
    if any(u['state']!='needs_review' or '\n' in u['translation'] or len(u['translation'])*8>88 for u in units):raise ValueError('mission metadata state/extent')
    return d,units

def prepare():
    d,units=selected()
    asset={k:d[k] for k in ('schema','policy','archive','source_sha256','source_tpl','source_archive_sha256')}
    asset.update(consumer='fixed-cell-big',scope_variant='mission-mail-header-v1',context='Native Navi index27 header loader at08040550; same020262F4 header residency and fixed-cell renderer. Existing42 draft labels, no mission body/quest edits. Natural acquisition remains unverified.',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),units=units)
    path=ROOT/ASSET;path.parent.mkdir(parents=True,exist_ok=True)
    data=json.dumps(asset,ensure_ascii=False,indent=2)+'\n'
    if path.exists() and path.read_text(encoding='utf8')!=data:raise ValueError('preserve mission selected input')
    if not path.exists():path.write_text(data,encoding='utf8')
    return ASSET

def validate(asset):
    if asset['units']!=selected()[1] or asset.get('scope_variant')!='mission-mail-header-v1':raise ValueError('mission selected wording differs')

def scope(source):
    if source[0x40548:0x40558]!=bytes.fromhex('00b5297c89000a4840582749abf000fe'):raise ValueError('mission native header loader')
    if struct.unpack_from('<I',source,0x405f0)[0]!=0x020262f4:raise ValueError('mission header residency')
    refs=[m.start() for m in re.finditer(re.escape(struct.pack('<I',0x086dd864)),source)]
    if refs!=[0x405e8]:raise ValueError('mission header reference population')
    return dict(source_bytes=183,pointers=refs,compressed=True,compression='BIOS type-10 literal-only, 4-byte aligned, zero-padded',decompression_destination=0x020262f4,max_payload_bytes=4096,next_scene_asset=0x020272f4,consumer='fixed-cell-big',literal_language='mmbn45s',max_literal_rows=1,max_line_advance=88,literal_scripts=SCRIPTS,complete_literal_scope=False,script_count=66,preserve_literal_numerals=True,context='Mission header table index27; unchanged native loader and consumer')
