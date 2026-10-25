"""Adopted source/selection/quantity constraints for raw-ROM key-item clone."""
from keyitem_empty import validate_source,resolved
from tpl_literals import literals,resolve_units,skeleton
from keyitem_rom_selector import construct,INSTALL
from build_visibility_poc import sha

SCOPE=dict(consumer='normal-dialogue',complete_literal_scope=True,script_count=49,
    literal_scripts=list(range(21))+list(range(32,45)),max_literal_rows=3,
    max_line_advance=176,keyitem_raw_rom=True,preserve_literal_numerals=True)

def validate_input(source,asset):
    if (asset['archive']!='709408' or asset['source_sha256']!=sha(source) or
        asset['policy']!='development-draft; NON-DISTRIBUTION' or asset['consumer']!='normal-dialogue' or
        asset['review']['release_eligible'] is not False):raise ValueError('keyitem clone development/source policy')
    if any(u['state']!='needs_review' for u in resolve_units(asset)):raise ValueError('undeclared keyitem review state')

def validate_payload(source,native,payload,original,translated,units,layout):
    validate_source(source,native)
    if not 98<=len(payload)<=0xffff or len(resolved(payload))!=49 or skeleton(original)!=skeleton(translated):raise ValueError('full clone structure/range changed')
    prior={x.key:x.text for x in literals(original)}
    if any(prior[u['id']]!=u['source'] for u in units):raise ValueError('keyitem source wording')
    if next(u for u in units if u['id']=='709408:32:0')['translation']!='키 아이템이\n1개도 없다・・・':raise ValueError('retain current empty wording')
    spans=resolved(payload);old=resolved(native)
    if any(spans[i]!=spans[32]for i in range(21,33)) or any(spans[i]!=old[i]for i in range(45,49)):raise ValueError('native alias/blank identity')
    if source[0x30314:0x3031a]!=bytes.fromhex('085c004200bd'):raise ValueError('native count load changed')
    measured={x['id']:x['line_advance_pixels'] for x in layout};proof=[]
    for script in [6,7,16,17,18]:
        a=measured[f'709408:{script}:0'][-1];b=measured[f'709408:{script}:1'][0];worst=a+3*11+b
        if worst>SCOPE['max_line_advance']:raise ValueError('keyitem quantity aggregate exceeds adopted176px')
        proof.append(dict(script=script,unsigned_count_range=[0,255],max_digits=3,aggregate_max_advance_px=worst))
    return proof

def install(source,appended,payload,header,record,mail_payload=None,mail_header=None,mail_record=None,mission_payloads=None,equipment_payloads=None,hint_payloads=None,b0_hint_payloads=None):
    tail=bytearray(appended);tail.extend(b'\xff'*(-len(tail)%4))
    clone=0x08000000+len(source)+len(tail);tail.extend(payload);tail.extend(b'\xff'*(-len(tail)%4))
    mail=None
    if mail_payload is not None:
        mail_address=0x08000000+len(source)+len(tail)
        tail.extend(mail_payload);tail.extend(b'\xff'*(-len(tail)%4))
        mail=dict(clone_address=mail_address,payload_bytes=len(mail_payload),guard_header_hex=(mail_header if mail_header is not None else mail_payload[:16]).hex())
    missions=[];mission_records=[]
    for raw,native_header,r in mission_payloads or []:
        address=0x08000000+len(source)+len(tail);tail.extend(raw);tail.extend(b'\xff'*(-len(tail)%4))
        missions.append(dict(clone_address=address,payload_bytes=len(raw),guard_header_hex=native_header.hex(),script_count=r['script_count']))
        mission_records.append(dict(r,rom_offset=address-0x08000000,rom_sha256=sha(raw),native_ram_archive_retained=True))
    equipment=[];equipment_records=[]
    for raw,native,r,index in equipment_payloads or []:
        address=0x08000000+len(source)+len(tail);tail.extend(raw);tail.extend(b'\xff'*(-len(tail)%4))
        equipment.append(dict(clone_address=address,payload_bytes=len(raw),navi_index=index,guard_header_hex=native[:16].hex(),guard_tail_hex=native[136:152].hex()))
        equipment_records.append(dict(r,rom_offset=address-0x08000000,rom_sha256=sha(raw),navi_index=index,native_ram_archive_retained=True))
    hints=None;hint_records=[]
    if hint_payloads is not None:
        from hint_rom_data import append
        data,hints,hint_records=append(source,tail,hint_payloads);tail=bytearray(data)
    b0_hints=None;b0_records=[]
    if b0_hint_payloads is not None:
        from field_b0_rom_data import append
        data,b0_hints,b0_records=append(source,tail,b0_hint_payloads);tail=bytearray(data)
    hook=0x08000000+len(source)+len(tail);stub,code,meta=construct(source,header,clone,hook,len(payload),mail,missions or None,equipment or None,hints,b0_hints);tail.extend(code)
    meta.update(archive=record,rom_offset=clone-0x08000000,rom_bytes=len(payload),rom_sha256=sha(payload),
        selector_bytes=len(code),runtime='pending',adopted_display_range_px=176,
        scope='known callers only; unknown callers and alternate archive preserve native lookup')
    if mail is not None:meta['mail_rom_reader']=dict(mail,rom_sha256=sha(mail_payload),scope='capacity-path PoC; same77 selected body units; compressed RAM copy retained; no additional translation selected')
    if mail_record is not None:
        if mail_record['translated_units']!=120 or len(mail_payload)!=mail_record['compiled_bytes'] or sha(mail_payload)!=mail_record['compiled_sha256']:raise ValueError('full mail raw record binding')
        meta['mail_rom_reader'].update(archive=mail_record,scope='Full120 raw-ROM body; new43 units selected; bounded77 compressed RAM payload and guard preserved; acquisition QA pending')
    if missions:meta['mission_mail_archives']=mission_records
    if equipment:meta['equipment_archives']=equipment_records
    if hints is not None:meta['hint_archives']=hint_records
    if b0_hints is not None:meta['b0_hint_archives']=b0_records
    return bytes(tail),[(INSTALL,stub,'guarded key-item raw-ROM archive reader')],meta

def verify_final(source,target,meta):
    at=meta['rom_offset'];payload=target[at:at+meta['rom_bytes']]
    if sha(payload)!=meta['rom_sha256']:raise ValueError('final keyitem ROM clone')
    stub,code,_=construct(source,bytes.fromhex(meta['guard_header_hex']),0x08000000+at,meta['hook_address'],len(payload),meta.get('mail_guard'),meta.get('mission_guards'),meta.get('equipment_guards'),meta.get('hint_guard'),meta.get('b0_hint_guard'))
    if meta.get('hint_guard'):
        from layout500_product_024 import verify_hints
        verify_hints(source,target,meta)
    if meta.get('b0_hint_guard'):
        from field_b0_rom_data import verify_final as verify_b0
        verify_b0(source,target,meta)
    for g,r in zip(meta.get('equipment_guards') or [],meta.get('equipment_archives') or []):
        ea=g['clone_address']-0x08000000
        if sha(target[ea:ea+g['payload_bytes']])!=r['compiled_sha256'] or g['payload_bytes']!=r['compiled_bytes']:raise ValueError('Final equipment clone')
    for g,r in zip(meta.get('mission_guards') or [],meta.get('mission_mail_archives') or []):
        ma=g['clone_address']-0x08000000
        if sha(target[ma:ma+g['payload_bytes']])!=r['compiled_sha256'] or g['payload_bytes']!=r['compiled_bytes']:raise ValueError('final mission ROM clone')
    if meta.get('mail_rom_reader'):
        mail=meta['mail_rom_reader'];ma=mail['clone_address']-0x08000000
        if sha(target[ma:ma+mail['payload_bytes']])!=mail['rom_sha256'] or {k:mail[k] for k in ('clone_address','payload_bytes','guard_header_hex')}!=meta['mail_guard']:raise ValueError('final mail ROM clone identity')
        if mail.get('archive'):
            if mail['archive']['compiled_sha256']!=mail['rom_sha256'] or mail['archive']['compiled_bytes']!=mail['payload_bytes']:raise ValueError('final full mail record identity')
            for r in mail['archive']['mail_player_name_proof']['native_producer_ranges']:
                if target[r['start']:r['end']]!=source[r['start']:r['end']]:raise ValueError('player-name producer modified')
    h=meta['hook_address']-0x08000000
    if target[INSTALL:INSTALL+len(stub)]!=stub or target[h:h+len(code)]!=code:raise ValueError('final selector machine code')
    return True
