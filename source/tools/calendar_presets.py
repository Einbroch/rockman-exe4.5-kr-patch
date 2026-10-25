"""Two bounded default-name drafts and the local confirmation logical-cell counter."""
from calendar_types_model import validate as validate_types,replace_types_literals
from korean_codec import encode_hangul
from tpl_literals import literals,serialize,skeleton
from extended_dialogue import assemble_verified

SITE=0x32F88
END=0x32F9A
EXPECTED=bytes.fromhex('585ce52805d0e42800d1013101310132f6e7')
NAMES={'6368E8:62:0':('ごはん','식사'),'6368E8:63:0':('じゅく','학원')}

def validate(units):
    if len(units)!=4 or {u['id'] for u in units}!={'6368E8:0:0','6368E8:60:0',*NAMES}:raise ValueError('preset finite scope')
    validate_types([u for u in units if u['id'] not in NAMES])
    for u in units:
        if u['id'] not in NAMES:continue
        if (u['source'],u['translation'])!=NAMES[u['id']] or u['state'] not in ('needs_review','reviewed'):raise ValueError('preset wording/state')
        b=encode_hangul(u['translation'])+b'\xe5'
        if len(b)>22 or b'\xe5' in b[:-1] or len(u['translation'])>10:raise ValueError('rawE5 copy/record/display capacity')
    return {'name_field_bytes':22,'record_bytes':32,'name_offset':10,'selected_name_bytes':9,'protected_scripts':251}

def replace(original,units):
    validate(units);target=replace_types_literals(original,[u for u in units if u['id'] not in NAMES])
    for u in units:
        if u['id'] not in NAMES:continue
        xs=[x for x in literals(target) if x.key==u['id']]
        if len(xs)!=1 or xs[0].text!=u['source'] or xs[0].language!='mmbn45s':raise ValueError('preset source literal')
        x=xs[0];target=target[:x.start]+serialize(u['translation'])+target[x.end:]
    if skeleton(original)!=skeleton(target):raise ValueError('preset controls')
    return target

def construct(source,appended):
    if source[SITE:END]!=EXPECTED:raise ValueError('native confirmation count loop changed')
    append=bytearray(appended);append.extend(b'\xff'*((-len(append))%4));at=len(source)+len(append)
    code='''push {r4}
loop:
ldrb r0, [r3, r1]
cmp r0, #0xe5
beq done
cmp r0, #0xe4
beq japanese
cmp r0, #0xf9
bne next
adds r4, r1, #1
ldrb r4, [r3, r4]
cmp r4, #0xfc
bne next
adds r1, #3
b next
japanese:
adds r1, #1
next:
adds r1, #1
adds r2, #1
b loop
done:
pop {r4}
ldr r0, continuation
push {r0}
movs r0, #0xe5
cmp r0, #0xe5
pop {pc}
'''
    blob,record=assemble_verified(code,0x08000000+at,{'continuation':0x08000001+END});append.extend(blob)
    install,irecord=assemble_verified('ldr r0, handler\nbx r0',0x08000000+SITE,{'handler':0x08000001+at})
    if len(install)!=8:raise ValueError('count install')
    install+=bytes.fromhex('c046')*((END-SITE-len(install))//2)
    return bytes(append),[(SITE,install,'calendar confirmation F9FC logical-name length')],{'install_offset':SITE,'install_bytes':len(install),'expected_hex':EXPECTED.hex(),'hook_offset':at,'hook_bytes':len(blob),'machine_code':[record,irecord],'entry':'r1=0,r2=0,r3=02026080; local confirmation name counter only','return':'32F9A; native r0=E5,r1=byte length,r2=logical cells; other registers/SP/LR and final CMP flags preserved','runtime':'pending normal preset confirmation/record/query','policy':'functional-poc; NON-DISTRIBUTION','release_eligible':False}
