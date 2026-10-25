"""Source-bound descriptor/TPL inventory, not a complete native reader graph."""
import json,re,struct
from pathlib import Path
from collections import Counter
from build_visibility_poc import ROOT,sha,require_hash
from tpl_literals import literals

def main():
    profile=json.loads((ROOT/'project.json').read_text(encoding='utf8'))['source_profile'];source=ROOT/profile['filename'];require_hash(source,profile['sha256']);rom=source.read_bytes()
    product=ROOT/'poc/output/exe45_ko_development_input_heading_v1_r2.gba';require_hash(product,'5e7bee746f23afb7192e79784f9427d1fec448ccd10405b1198d5af060e431f4')
    plugin=ROOT/'external/textpet-plugins/mmbn45-jp.ini';commands={}
    for section in re.split(r'(?m)^\[Command\]\s*$',plugin.read_text(encoding='utf8'))[1:]:
        # Only the command header before its first parameter/extension section.
        head=section.split('[',1)[0];name=re.search(r'(?m)^name\s*=\s*(\w+)\s*$',head);base=re.search(r'(?m)^base\s*=\s*F9 0C ([0-9A-F]{2})\s*$',head)
        if name and base:commands[name.group(1)]=int(base.group(1),16)
    if commands.get('printWorstSubject')!=16 or commands.get('printStringBuffer1')!=28:raise ValueError('named descriptor identity')
    inventory_path=ROOT/'analysis/full_scope_v1/inventory.json';inventory=json.loads(inventory_path.read_text(encoding='utf8'));archives=inventory['archives']
    if len(archives)!=732 or len({a['archive'] for a in archives})!=732:raise ValueError('source TPL denominator')
    references=[];counts=Counter()
    for archive in archives:
        p=ROOT/'analysis/full_scope_v1/source_tpl'/f"{archive['archive']}.tpl";require_hash(p,archive['source_tpl_sha256']);text=p.read_text(encoding='utf8')
        # Remove protected literals while retaining line positions; don't scan
        # dialogue text as commands. This inventories named command lines only.
        for item in reversed(literals(text)):
            raw=text[item.start:item.end];text=text[:item.start]+''.join('\n' if c=='\n' else ' ' for c in raw)+text[item.end:]
        script=None
        for line_no,line in enumerate(text.splitlines(),1):
            match=re.match(r'^script\s+(\d+)\s+\w+\s*\{',line)
            if match:script=int(match.group(1))
            command=re.fullmatch(r'\s+(\w+)\s*',line)
            if command and command.group(1) in commands:
                name=command.group(1);index=commands[name];counts[index]+=1
                references.append(dict(id=f"{archive['archive']}:{script}:{line_no}",archive=archive['archive'],script=script,line=line_no,command=name,descriptor_index=index))
    table=[]
    # Declared 26 structurally coherent consecutive records, not an assertion
    # that these are the game's entire name/record/consumer population.
    for n in range(26):
        at=0x3b0d0+n*16;entry=rom[at:at+16];count,index,limit=entry[:3]
        if index!=n+2 or not count or limit not in [4,6,8]:raise ValueError('candidate metadata extent')
        descriptor=0x526d0+index*8;pointer,size=struct.unpack_from('<II',rom,descriptor);offset=struct.unpack_from('<H',entry,14)[0];start=0x02000950+offset;stride=limit*2+2
        table.append(dict(id=f'exe45.input-metadata.row-{n}',metadata_offset=at,metadata_hex=entry.hex(),count=count,descriptor_index=index,native_logical_limit=limit,derived_native_stride=stride,field_start=hex(start),field_end_exclusive=hex(start+count*stride),descriptor_pointer=hex(pointer),descriptor_bytes=size,pointer_is_first_record_text=pointer==start+1,named_print_references=counts[index],runtime_metadata_confirmed=n==14))
    all_pointers=[struct.unpack_from('<II',rom,0x526d0+n*8) for n in range(32)]
    report=dict(id='exe45.hangul-keyboard.consumer-inventory.v1',source_sha256=profile['sha256'],current_rom_sha256=sha(product.read_bytes()),inventory_sha256=sha(inventory_path.read_bytes()),plugin_sha256=sha(plugin.read_bytes()),tool_sha256=sha(Path(__file__).read_bytes()),tpl_archives_checked=len(archives),named_command_references=len(references),descriptor_counts=dict(sorted(counts.items())),metadata_rows=table,descriptors=[dict(index=n,pointer=hex(p),bytes=size) for n,(p,size) in enumerate(all_pointers)],references=references,confirmed=['Plugin and named TPL commands bind printWorstSubject to F90C10 / descriptor16, not descriptor28.','Descriptor16 points directly to020010A7 with9-byte copy bound; observed native record width is10.','printStringBuffer1..3 bind distinct descriptors28..30. Their providers cannot substitute for direct subject consumers.'],limits=['Inventory covers named F90Cxx command lines in all732 pinned canonical source TPLs, not variable buffer IDs or native code reader population.','26 metadata rows are a bounded structural inventory; row14 is the normal-play observed entry, other rows require native selection/writer verification.','Marker discrimination and all save consumers remain unresolved; candidate packed format is NOT adopted.'])
    out=ROOT/'analysis/hangul_keyboard_v1/consumer_inventory.json';out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    print('source TPLs',len(archives),'named references',len(references),'weak-subject references',counts[16],'; bounded metadata rows',len(table))

if __name__=='__main__':main()
