"""Versioned product/primary composition from pinned036 implementation.

Only declared edits generate new files. Original tools remain byte unchanged.
"""
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write


def create(name,base,text,edits):
    for before,after,count in edits:
        if text.count(before)!=count: raise ValueError((name,before,text.count(before),count))
        text=text.replace(before,after)
    path=ROOT/name
    if path.exists() and path.read_text(encoding='utf8')!=text: raise ValueError('Preserve existing '+name)
    if not path.exists(): path.write_text(text,encoding='utf8',newline='\n')
    return dict(base=base,base_sha256=sha((ROOT/base).read_bytes()),output=name,output_sha256=sha(path.read_bytes()),edits=[dict(before=a,after=b,occurrences=n) for a,b,n in edits])


def main():
    meta=read('poc/output/pending500_036_v1.json'); base='tools/field_npc_rom_product_036_v1.py'
    require_hash(ROOT/base,meta['build_tools_sha256']['field_npc_rom_product_036_v1.py']); text=(ROOT/base).read_text(encoding='utf8')
    # Uniform version lineage first; local edits below specialize typed037 ABI.
    edits=[('036','037',text.count('036')),('035','036',text.count('035'))]
    intermediate=text.replace('036','037').replace('035','036')
    old_admission=intermediate[intermediate.index('def require_admission():'):intermediate.index('\n\ndef load_inputs')]
    new_admission='''def require_admission():
    status=read('analysis/pending500_036_v1/batch_status.json')
    if status['rom_sha256']!=BASE_SHA or not status.get('natural_cached_NPC_selection_verified'):
        raise ValueError('036 normal cached NPC evidence required before037 development build')
    paths=['analysis/pending500_036_v1/integration.json','analysis/pending500_036_v1/natural_cached_display_v1.json','analysis/pending500_036_v1/native_boundaries_v1.json']
    proofs=[]
    for path in paths:
        report=read(path)
        if not report.get('passed') or report.get('rom_sha256')!=BASE_SHA:
            raise ValueError('036 audited exact-ROM evidence required')
        proofs.append(ref(ROOT/path))
    cpu=read('analysis/pending_insertion_500_037_selector_cpu_v2/cpu.json')
    if not cpu['passed'] or cpu['baseline_sha256']!=BASE_SHA or cpu['rom_written'] or cpu['descriptor_count']!=70:
        raise ValueError('037 typed source/actual caller CPU evidence required')
    proofs.append(ref(ROOT/'analysis/pending_insertion_500_037_selector_cpu_v2/cpu.json'))
    return dict(reports=proofs,scope='Development integration only;036 natural A0 plus qualified A1/A3.037 A2/board native acquisition/rendering pending',release_eligible=False)
'''
    edits += [
      ('"""037 single-writer installation component;036 natural-route gate stays shut.\n\nNo command here builds a ROM. --preflight checks500 inputs and confirms that\nthe unresolved036 admission condition refuses installation before any writes.\n"""','"""037 typed NPC/board primary component; source036 prefix retained.\n\nNo standalone ROM writer. Admission is development-only, not runtime approval.\n"""',1),
      ('prepare_npc_inputs_037_v1 import OUT as INPUT_DIR','prepare_native_inputs037_v2 import OUT as INPUT_DIR,selected_from',1),
      ('prepare_source500_037_v1','prepare_source500_037_v2',1),
      ('field_npc_rom_selector_037_v1','field_native_rom_selector_037_v2',1),
      ('field_npc_rom_product_036_v2','field_npc_rom_product_036_v1',1),
      (old_admission,new_admission,1),
      ("selected={r['archive']:r['scene'] for r in manifest['archives']}","selected=selected_from(manifest['archives'])",1),
      ("scope['storage']!='scene-native-identity-ROM-clone'", "scope['storage']!='typed-scene-native-identity-ROM-clone'",1),
      ("scope['guarded_reader_return_lr']!=0x0804F773 or scope['native_root']!=0x02039800", "scope['guarded_reader_return_lr']!=field['caller_lr'] or scope['native_root']!=field['root'] or r['source_class']!=field['source_class'] or scope['script_count']!=struct.unpack_from('<H',native)[0]//2",1),
      ("len(payload)>65535 or verify_untouched_scripts(native,payload,255,set(r['new_scripts']))", "len(payload)>65535 or len(native)>=0x1000 or verify_untouched_scripts(native,payload,r['scope']['script_count'],set(r['new_scripts']))",1),
      ("len(result)!=20", "len(result)!=70",1),
      ("source_archive=arc,scene=r['scene'],native_copy_offset=np", "source_archive=arc,source_class=r['source_class'],scene=r['scene'],root=r['scope']['native_root'],caller_lr=r['scope']['guarded_reader_return_lr'],script_count=r['scope']['script_count'],native_copy_offset=np",1),
      ("script_count=255,source_sha256=sha(native)", "script_count=r['scope']['script_count'],source_sha256=sha(native)",1),
      ("struct.pack('<4I',0x08000000+p['rom_offset'],0x08000000+p['native_copy_offset'],p['native_copy_bytes'],p['scene'])", "struct.pack('<7I',0x08000000+p['rom_offset'],0x08000000+p['native_copy_offset'],p['native_copy_bytes'],p['scene'],p['root'],p['caller_lr'],p['script_count'])",1),
      ("selected={p['source_archive']:p['scene'] for p in n['placements']}", "selected={p['source_archive']:dict(scene=p['scene'],source_class=p['source_class'],target_sha256=p['compiled_sha256'],script_count=p['script_count']) for p in n['placements']}",1),
      ("len(selected)!=20", "len(selected)!=70",1),
      ("struct.unpack_from('<4I',target,n['descriptor_offset']+i*16)!=(0x08000000+a,0x08000000+b,len(native),p['scene'])", "struct.unpack_from('<7I',target,n['descriptor_offset']+i*28)!=(0x08000000+a,0x08000000+b,len(native),p['scene'],p['root'],p['caller_lr'],p['script_count'])",1),
      ("result['translated_units']+=500", "cpu=read('analysis/pending_insertion_500_037_selector_cpu_v2/cpu.json')\n    if sha(target)!=cpu['fixture_only']['sha256'] or len(target)!=cpu['fixture_only']['bytes']:raise ValueError('037 final complete artifact differs from actual-caller CPU fixture')\n    result['translated_units']+=500",1),
      ("new_units=500,archives=20", "new_units=500,archives=70",1),
      ('tools/build_development_patch_037_v1.py','tools/build_development_patch_037_v1.py',1),
    ]
    # Remove obsolete standalone pending-gate preflight instead of retaining a false status.
    tail=intermediate[intermediate.index('\ndef preflight():'):]
    edits.append((tail,"\nif __name__=='__main__':raise SystemExit('Component only; use the037 primary build entry')\n",1))
    reports=[create('tools/field_native_rom_product_037_v1.py',base,text,edits)]
    primary='tools/build_development_patch_036_v1.py';require_hash(ROOT/primary,meta['build_tools_sha256']['build_development_patch_036_v1.py']);text=(ROOT/primary).read_text(encoding='utf8')
    changes=[
      ('    from field_npc_rom_product_036_v1 import load_inputs as load_inputs036,install as install_npc036,finalize as finalize036\n','    from field_npc_rom_product_036_v1 import load_inputs as load_inputs036,install as install_npc036,finalize as finalize036\n    from field_native_rom_product_037_v1 import load_inputs as load_inputs037,install as install_native037,finalize as finalize037\n',1),
      ('    inputs036=load_inputs036(source)\n','    inputs036=load_inputs036(source)\n    inputs037=load_inputs037(source)\n',1),
      ('    extra_chars = sorted(needed, key=EXTRA_CHARACTER_INDICES.get)\n',"    for entry037,_ in inputs037:\n        asset037=read_json(ROOT/entry037['asset']['path'])\n        needed.update(ch for u in asset037['units'] for ch in u['translation'] if ch in EXTRA_CHARACTER_INDICES)\n    extra_chars = sorted(needed, key=EXTRA_CHARACTER_INDICES.get)\n",1),
      ("        appended,key_patches,keyitem_rom,npc_records036=install_npc036(source,appended,key_patches,keyitem_rom,inputs036,common,work/'plugins',work/'npc036')\n","        appended,key_patches,keyitem_rom,npc_records036=install_npc036(source,appended,key_patches,keyitem_rom,inputs036,common,work/'plugins',work/'npc036')\n        appended,key_patches,keyitem_rom,native_records037=install_native037(source,appended,key_patches,keyitem_rom,inputs037,common,work/'plugins',work/'native037')\n",1),
      ('        from field_npc_rom_product_036_v1 import verify_final\n','        from field_native_rom_product_037_v1 import verify_final\n',1),
      ('    finalize036(source,target,result,inputs036,npc_records036)\n','    finalize036(source,target,result,inputs036,npc_records036)\n    finalize037(source,target,result,inputs037,native_records037)\n',1),
    ]
    reports.append(create('tools/build_development_patch_037_v1.py',primary,text,changes))
    frozen_write(ROOT/'tools/specs/primary037_v1_version.json',dict(generator_sha256=sha((ROOT/'tools/prepare_native_product037_v1.py').read_bytes()),changes=reports,scope='Typed70 descriptors and one037 wrapper over036; immutable original source primary, CPU whole-artifact identity mandatory; runtime pending'))
    print('PASS037 new typed product and six-edit primary generated; no ROM built')


if __name__=='__main__': main()
