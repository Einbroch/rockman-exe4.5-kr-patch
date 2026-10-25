"""035 source-derived NPC append and single-writer reader composition."""
import struct
from copy import deepcopy
from collections import defaultdict
from build_visibility_poc import ROOT,sha,require_hash,run_textpet
from cumulative_batch500 import read
from inspect_remaining_035 import BASE,BASE_SHA
from prepare_npc_inputs_035 import OUT as INPUT_DIR,SELECTION
from prepare_repartition500 import layout_records
from field_npc_rom_selector_035_v3 import wrap,source_population
from keyitem_rom_selector import INSTALL
from keyitem_rom_data_024 import verify_final as verify_previous
from verify_tpi_index import lz77_decompress,parse_tpi
from survey_aggregate_pet_033 import replace_exact
from survey_new_storage_035 import VALIDATORS
from build_development_patch import validate_characters,validate_literal_numerals
from tpl_literals import literals,skeleton
from canonical_literals_031 import canonical_literals
from archive_scripts import verify_untouched_scripts

MANIFEST=INPUT_DIR+'/manifest.json'

def load_inputs(source):
    manifest=read(MANIFEST)
    for p,h in manifest['dependencies'].items():require_hash(ROOT/p,h)
    if manifest['source_sha256']!=sha(source) or manifest['new_units']!=500 or not manifest['passed'] or manifest['rom_written']:raise ValueError('035 source500 input policy')
    require_hash(ROOT/BASE,BASE_SHA);old=read(BASE.replace('.gba','.json'));base=(ROOT/BASE).read_bytes()
    if manifest['baseline_sha256']!=BASE_SHA or manifest['baseline_rom']!=BASE:raise ValueError('035 current parent identity')
    selection=read(SELECTION);groups=defaultdict(list)
    for g in selection['groups']:groups[g['archive']].append(g)
    applied={u['id'] for r in layout_records(old) for u in r['layout']};seen=set();validators=dict(VALIDATORS)
    cfg=read('project.json');require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256']);catalog={f"{r['offset']:X}":r for r in parse_tpi(ROOT/cfg['text_catalog']['path'])}
    result=[]
    for r in manifest['archives']:
        arc=r['archive'];row=r['source_row']
        if row!=catalog[arc] or not row['compressed'] or row['size_header'] or r['storage']!='npc-A0-ROM-clone':raise ValueError('035 registered compressed-retained route')
        for key in ('asset','compiled','source_tpl','target_tpl'):require_hash(ROOT/r[key]['path'],r[key]['sha256'])
        a=read(r['asset']['path']);ids={u['id'] for u in a['units']};payload=(ROOT/r['compiled']['path']).read_bytes();native,used=lz77_decompress(source,row['offset'])
        if a['policy']!='development-draft; NON-DISTRIBUTION' or a['review']['release_eligible'] is not False or a['archive']!=arc or a['source_sha256']!=sha(source) or a['source_archive_sha256']!=sha(native):raise ValueError('035 asset source/development policy')
        if used!=r['native_stored_consumed_bytes'] or sha(native)!=r['source_payload_sha256'] or len(native)!=r['native_bytes'] or base[row['offset']:row['offset']+used]!=source[row['offset']:row['offset']+used] or any(base[p:p+4]!=source[p:p+4] for p in row['pointers']):raise ValueError('035 retained native extent/reference')
        if len(ids)!=len(a['units']) or ids!=set(r['new_ids']) or ids&seen or ids&applied or len(ids)!=r['translated_units']:raise ValueError('035 disjoint new IDs')
        original=(ROOT/r['source_tpl']['path']).read_text(encoding='utf-8-sig');target=(ROOT/r['target_tpl']['path']).read_text(encoding='utf-8-sig');source_lit={u.key:u.text for u in literals(original)}
        if any(u['state']!='needs_review' or source_lit[u['id']]!=u['source'] for u in a['units']):raise ValueError('035 source literal/state')
        if skeleton(original)!=skeleton(target) or [(u.key,u.text) for u in literals(target)]!=[(u.key,u.text) for u in literals(replace_exact(original,{u['id']:u['translation'] for u in a['units']}))]:raise ValueError('035 full target/skeleton')
        if r['scope']['consumer']!='normal-dialogue' or r['scope']['literal_language']!='mmbn45' or set(r['scope']['literal_ids'])!=ids or r['scope']['storage']!='npc-A0-ROM-clone':raise ValueError('035 explicit scope')
        for g in groups[arc]:
            if validators[g['profile']](original,target,[g['script']],set(g['ids']),99)!=g['geometry']:raise ValueError('035 source-bound geometry')
        validate_literal_numerals(a['units'],dict(preserve_literal_numerals=True))
        if len(payload)>65535 or len(payload)!=r['compiled_bytes'] or sha(payload)!=r['compiled_sha256'] or verify_untouched_scripts(native,payload,255,set(r['new_scripts']))!=r['unselected_scripts']:raise ValueError('035 payload/untouched scripts')
        seen|=ids;result.append((r,payload))
    if len(seen)!=500 or seen!=set(selection['selected_ids']) or len(result)!=9:raise ValueError('035 exact500/9')
    source_population(source,{r['archive'] for r,_ in result})
    return result

def install(source,appended,key_patches,keymeta,inputs,common,plugins,work):
    if len(key_patches)!=1 or key_patches[0][0]!=INSTALL or len(key_patches[0][1])!=12:raise ValueError('035 unique preceding reader writer')
    work.mkdir(parents=True,exist_ok=False);tail=bytearray(appended);records=[];placements=[]
    def alloc(data):
        tail.extend(b'\xff'*(-len(tail)%4));offset=len(source)+len(tail);tail.extend(data);return offset
    for r,precompiled in inputs:
        arc=r['archive'];a=read(r['asset']['path']);original=(ROOT/r['source_tpl']['path']).read_text(encoding='utf-8-sig');target=replace_exact(original,{u['id']:u['translation'] for u in a['units']})
        folder=work/arc;folder.mkdir();tp=folder/'target.tpl';bp=folder/(arc+'.msg');tp.write_text(canonical_literals(target),encoding='utf-8',newline='\n')
        run_textpet(common+['Read-Text-Archives',str(tp),'--format','tpl','Write-Text-Archives',str(bp),'--format','bin'],folder/'compile.log');payload=bp.read_bytes()
        if payload!=precompiled:raise ValueError('035 primary source recompile mismatch')
        layout=validate_characters(target,plugins/'exe45-utf8.tbl',r['scope'],set(r['new_ids']))
        if layout!=r['layout']:raise ValueError('035 primary current glyph metrics')
        native=lz77_decompress(source,r['source_row']['offset'])[0];np=alloc(native);cp=alloc(payload)
        placements.append(dict(source_archive=arc,native_copy_offset=np,native_copy_bytes=len(native),native_copy_sha256=sha(native),rom_offset=cp,compiled_bytes=len(payload),compiled_sha256=sha(payload),source_row=r['source_row']))
        records.append(dict(archive=arc,compiled_bytes=len(payload),compiled_sha256=sha(payload),rom_offset=cp,translated_units=len(a['units']),layout=layout,script_count=255,source_sha256=sha(native),source_bytes=len(native),native_roundtrip=True,semantic_roundtrip=True,binary_roundtrip=True,
                            protected_controls_unchanged=True,native_ram_archive_retained=True,source_pointers_retained=r['source_row']['pointers'],
                            cumulative035=dict(scope=r['scope'],new_ids=r['new_ids'],new_scripts=r['new_scripts'],manifest=MANIFEST,manifest_sha256=sha((ROOT/MANIFEST).read_bytes())),
                            unselected_script_bytes_preserved=r['unselected_scripts']))
    desc=alloc(bytes(9*16));desc_at=desc-len(source)
    for i,p in enumerate(placements):struct.pack_into('<4I',tail,desc_at+i*16,0x08000000+p['rom_offset'],0x08000000+p['native_copy_offset'],p['native_copy_bytes'],0)
    tail.extend(b'\xff'*(-len(tail)%4));code_offset=len(source)+len(tail);code,proof=wrap(source,0x08000000+code_offset,keymeta['entry_address'],0x08000000+desc);tail.extend(code)
    from extended_dialogue import assemble_verified
    stub,stub_proof=assemble_verified('push {r3}\nldr r3,target\nbx r3',0x08000000+INSTALL,dict(target=0x08000000+code_offset+1))
    if len(stub)!=12:raise ValueError('035 composed entry size')
    keymeta['npc035']=dict(descriptor_offset=desc,code_offset=code_offset,code_bytes=len(code),code_sha256=sha(code),wrapper=proof,stub=stub_proof,
                           preceding_stub_hex=key_patches[0][1].hex(),final_stub_hex=stub.hex(),placements=placements,original_compressed_sources_and_references_retained=True,persistent_ram_bytes=0,runtime='pending')
    return bytes(tail),[(INSTALL,stub,'035 NPC reader composed over full prior034 reader chain')],keymeta,records

def verify_final(source,target,keymeta):
    meta=keymeta['npc035'];old_stub=bytes.fromhex(meta['preceding_stub_hex']);stub=bytes.fromhex(meta['final_stub_hex'])
    if target[INSTALL:INSTALL+12]!=stub:raise ValueError('035 final composed stub')
    # Explicit predecessor component view, not a claim that old stub is installed.
    previous_view=bytearray(target);previous_view[INSTALL:INSTALL+12]=old_stub;verify_previous(source,previous_view,keymeta)
    code,proof=wrap(source,0x08000000+meta['code_offset'],keymeta['entry_address'],0x08000000+meta['descriptor_offset'])
    if proof!=meta['wrapper'] or len(code)!=meta['code_bytes'] or sha(code)!=meta['code_sha256'] or target[meta['code_offset']:meta['code_offset']+len(code)]!=code:raise ValueError('035 final placed wrapper')
    for i,p in enumerate(meta['placements']):
        a=p['rom_offset'];n=p['native_copy_offset'];native,used=lz77_decompress(source,p['source_row']['offset'])
        if target[n:n+len(native)]!=native or sha(target[a:a+p['compiled_bytes']])!=p['compiled_sha256']:raise ValueError('035 placed native/target bytes')
        if struct.unpack_from('<4I',target,meta['descriptor_offset']+i*16)!=(0x08000000+a,0x08000000+n,len(native),0):raise ValueError('035 placed descriptor')
        off=p['source_row']['offset']
        if target[off:off+used]!=source[off:off+used] or any(target[at:at+4]!=source[at:at+4] for at in p['source_row']['pointers']):raise ValueError('035 changed original compression/reference')
    return True

def finalize(source,target,result,inputs,records):
    old=read(BASE.replace('.gba','.json'));base=(ROOT/BASE).read_bytes();require_hash(ROOT/BASE,BASE_SHA)
    # Prefix equality outside one composed stub is stronger than old-consumer sampling.
    if len(target)<=len(base) or target[:INSTALL]!=base[:INSTALL] or target[INSTALL+12:len(base)]!=base[INSTALL+12:]:raise ValueError('035 changed preceding034 bytes outside composed stub')
    before=list(layout_records(old));prior=list(layout_records(result))
    if [(r['archive'],r['compiled_sha256'],r['layout']) for r in before]!=[(r['archive'],r['compiled_sha256'],r['layout']) for r in prior]:raise ValueError('035 prior record ordering/ownership changed')
    result['keyitem_rom']['npc035']['archives']=records
    oldids={u['id'] for r in before for u in r['layout']};allids={u['id'] for r in layout_records(result) for u in r['layout']};selected={k for r,_ in inputs for k in r['new_ids']}
    if len(selected)!=500 or oldids-allids or allids-oldids!=selected:raise ValueError('035 actual selected500 delta')
    result['translated_units']+=500
    if result['translated_units']!=old['translated_units']+500:raise ValueError('035 actual cumulative total')
    for r,_ in inputs:result['translation_assets'].append(dict(r['asset'],archive=r['archive'],scope='035 NPC ROM clone effective translation owner'))
    result['pending_batch500_035']=dict(new_units=500,archives=9,storage='original compression/RAM retained plus guarded ROM clones',manifest=MANIFEST,manifest_sha256=sha((ROOT/MANIFEST).read_bytes()),prior034_bytes_preserved_except_composed_stub=True,
                                       exact_new500_delta=True,rom_integrated=True,runtime='pending',release_eligible=False)
    result['primary_entry']='tools/build_development_patch_035_v2.py'
    result['limits'].append('035 exact500 NPC ROM clones; original native loading and RAM retained; final-ROM runtime/timing and semantic review pending; NON-DISTRIBUTION')
