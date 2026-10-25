"""Explicit data-only startup UI scope; dormant packed tables stay original."""
import json
from build_visibility_poc import ROOT,sha
from tpl_literals import literals

SOURCE_SHA='588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8'
POINTERS=[168184,215496,235592,236260,237808,241528,435896,436528,437616,445720]
SCRIPTS=[30,31,32,33,34,*range(50,63),73,74,*range(79,86),88,*range(100,109),110]
ASSET='analysis/startup_ui_v1/selected_asset.json'

def prepare():
    draft=json.loads((ROOT/'translations/batch500_046_remaining_70904C_draft_ko.json').read_text(encoding='utf8'))
    if draft['source_sha256']!=SOURCE_SHA or draft['source_archive_sha256']!='bd3440e4437d06ce7049afaf83b85904a7bb7ef5b45152737922ab76bee82746':raise ValueError('startup source identity')
    native=(ROOT/draft['source_tpl']['path']).read_bytes()
    if sha(native)!=draft['source_tpl']['sha256']:raise ValueError('startup TPL identity')
    units=[dict(id=u['id'],source=u['source'],translation=u['translation'],state='needs_review') for u in draft['units'] if int(u['id'].split(':')[1]) in SCRIPTS]
    replacements={'70904C:110:0':'내비 ','70904C:110:1':'.\n선택할까요?\n'}
    for u in units:u['translation']=replacements.get(u['id'],u['translation'])
    # The whitespace-only prefix is protected and not part of the draft.
    expected={x.key for x in literals(native.decode('utf-8-sig').replace('\r\n','\n')) if int(x.key.split(':')[1]) in SCRIPTS and x.text.strip()}
    if expected!={u['id'] for u in units}:raise ValueError('startup literal denominator')
    a=dict(schema=1,policy='development-draft; NON-DISTRIBUTION',archive='70904C',source_sha256=SOURCE_SHA,source_tpl=draft['source_tpl'],source_archive_sha256=draft['source_archive_sha256'],consumer='normal-dialogue',context='Normal new-game date, gender, age, occupation, profile confirmation and Navi confirmation; proportional UI renderer080556B8 with separate F9 dispatcher, NOT fixed-cell080554A4. Packed legacy scripts24..27 protected.',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),units=units)
    p=ROOT/ASSET;p.parent.mkdir(exist_ok=True);p.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf8');return ASSET

def prepare_followups():
    results=[]
    for archive,path,scripts in [('778A4C','translations/batch500_017_navi_names_778A4C_draft_ko.json',[0,1,2,8]),('65B220','translations/mail_alerts_draft_ko.json',list(range(1,8)))]:
        original=json.loads((ROOT/path).read_text(encoding='utf8'))
        if original['source_sha256']!=SOURCE_SHA:raise ValueError('followup immutable source')
        units=[dict(id=u['id'],source=u['source'],translation=u['translation'],state='needs_review') for u in original['units'] if int(u['id'].split(':')[1]) in scripts]
        if archive=='65B220':
            for u in units:
                if int(u['id'].split(':')[1])<=3:u['translation']='、\n메일이야!!'
        a=dict(original,consumer='normal-dialogue',units=units,insertion_state='explicit startup development scope',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False))
        result=f'analysis/startup_ui_v1/{archive}_selected_asset.json';(ROOT/result).write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf8');results.append(result)
    return results

def followup_scopes():
    return {'778A4C':dict(source_bytes=186,pointers=[333644],compressed=False,consumer='normal-dialogue',literal_language='mmbn45s',max_literal_rows=1,max_line_advance=36,complete_literal_scope=False,literal_scripts=[0,1,2,8],script_count=23,context='printCurrentNavi F903; native handler080516FC copies at most128 bytes to per-text insertion buffer. Four initially selectable Navi names, each at most12 encoded bytes plus terminator.'),'65B220':dict(source_bytes=1323,pointers=[229552],compressed=False,consumer='normal-dialogue',max_literal_rows=3,max_line_advance=132,complete_literal_scope=False,literal_scripts=list(range(1,8)),literal_ids=[f'65B220:{i}:1' for i in range(1,8)],script_count=255,nickname_suffix_scripts=[1,2,3],nickname_suffix_literal=1,context='Rockman normal mail notification pages; native nickname, command/flag/tournament events and !! cue preserved. Source first-line comma retained; Korean particles avoided.')}

def scope():
    return dict(source_bytes=956,pointers=POINTERS,compressed=False,consumer='normal-dialogue',max_literal_rows=1,max_line_advance=208,complete_literal_scope=False,literal_scripts=SCRIPTS,script_count=120,literal_ids=[u['id'] for u in json.loads((ROOT/ASSET).read_text(encoding='utf8'))['units']],literal_profiles=[dict(scripts=[s for s in SCRIPTS if s!=110],consumer='normal-dialogue',literal_language='mmbn45s',max_literal_rows=1,max_line_advance=208),dict(scripts=[110],consumer='normal-dialogue',literal_language='mmbn45',max_literal_rows=3,max_line_advance=132)],dynamic_name_script=110,context='Direct ROM archive references; proportional UI080556B8 and normal Navi confirmation. No decompression or packed-table edits.')

def construct(source,appended,extension):
    """Add F9 FC to the distinct proportional tile UI; retain legacy subcommands."""
    from extended_dialogue import assemble_verified,LEGACY_INDICES,HANGUL_COUNT
    if sha(source)!=SOURCE_SHA:raise ValueError('UI renderer source drift')
    if source[0x556A0:0x556A4].hex()!='99590508' or source[0x557D4:0x557DC].hex()!='0c290508f02f0508':raise ValueError('UI dispatch/width literals drift')
    out=bytearray(appended);layout=[]
    def alloc(data,label):
        out.extend(b'\xff'*(-len(out)%4));at=len(source)+len(out);out.extend(data);layout.append(dict(offset=at,bytes=len(data),sha256=sha(data),role=label));return at
    widths=source[0x52FF0:0x52FF0+LEGACY_INDICES*4]+(12).to_bytes(4,'little')*(HANGUL_COUNT+extension['extra_glyph_count'])
    width_at=alloc(widths,'fixed-advance UI legacy view plus extended advances')
    code='''ldrb r1, [r0, #1]
cmp r1, #0xfc
beq hangul
ldr r1, legacy
bx r1
hangul:
push {r0, r3, r4, r5, r6, r7, lr}
ldr r5, context
ldr r6, [r5, #0x14]
push {r6}
ldrb r1, [r0, #3]
lsls r1, r1, #8
ldrb r7, [r0, #2]
adds r1, r1, r7
ldr r7, bias
adds r1, r1, r7
ldr r6, font
str r6, [r5, #0x14]
ldr r7, copier
mov lr, pc
bx r7
pop {r6}
ldr r5, context
str r6, [r5, #0x14]
pop {r0, r3, r4, r5, r6, r7}
adds r0, #4
pop {pc}
'''
    at=len(source)+((len(out)+3)&~3)
    blob,isa=assemble_verified(code,0x08000000+at,dict(legacy=0x08055999,context=0x0200FBE0,bias=LEGACY_INDICES,font=0x08000000+extension['normal_font_offset'],copier=0x08055731))
    hook=alloc(blob,'proportional UI F9 FC handler')
    patches=[(0x556A0,(0x08000001+hook).to_bytes(4,'little'),'proportional UI F9 dispatch'),(0x557D4,(0x08000000+extension['advance_offset']).to_bytes(4,'little'),'UI proportional widths'),(0x557D8,(0x08000000+width_at).to_bytes(4,'little'),'UI fixed widths')]
    return bytes(out),patches,dict(layout=layout,machine_code=isa,legacy_handler=0x08055999,renderer=0x080556B8,copier=0x08055730,context=0x0200FBE0,normal_font_offset=extension['normal_font_offset'],native_font_restored_after_each_glyph=True,runtime_verified=False)

if __name__=='__main__':print(prepare())
