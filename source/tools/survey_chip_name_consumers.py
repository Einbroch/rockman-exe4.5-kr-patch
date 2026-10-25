"""Static candidate graph for nine source name-root pairs; not reachability QA."""
import json
import struct
from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB
from build_visibility_poc import ROOT, sha, require_hash


def branch_target(data, at):
    if at+4 > len(data):
        return None
    first, second = struct.unpack_from('<HH',data,at)
    if first & 0xF800 != 0xF000 or second & 0xF800 != 0xF800:
        return None
    delta = ((first & 0x7FF)<<12)|((second & 0x7FF)<<1)
    if delta & 0x400000:
        delta -= 0x800000
    return 0x08000000+at+4+delta


def main():
    config = json.loads((ROOT / 'project.json').read_text())
    source = ROOT / config['source_profile']['filename']
    require_hash(source,config['source_profile']['sha256'])
    data = source.read_bytes()
    decoder = Cs(CS_ARCH_ARM,CS_MODE_THUMB)
    tables = []
    for at in range(0,len(data)-8,4):
        if data[at:at+8] != struct.pack('<II',0x08765190,0x08765B18):
            continue
        pointer = struct.pack('<I',0x08000000+at)
        literals = [p for p in range(max(0,at-4096),at,4) if data[p:p+4] == pointer]
        readers = []
        for literal in literals:
            for pc in range(max(0,literal-1024),literal,2):
                opcode = struct.unpack_from('<H',data,pc)[0]
                if opcode & 0xF800 != 0x4800 or ((pc+4)&~3)+(opcode&255)*4 != literal:
                    continue
                calls = [{'pc':0x08000000+p,'target':target} for p in range(pc+2,min(pc+82,len(data)-4),2)
                         if (target:=branch_target(data,p)) is not None]
                instructions = [{'address':i.address,'hex':i.bytes.hex(),'mnemonic':i.mnemonic,'operands':i.op_str}
                                for i in decoder.disasm(data[pc:pc+32],0x08000000+pc)]
                parser = None
                if calls:
                    start = calls[0]['target']-0x08000000
                    if 0 <= start <= len(data)-64:
                        window = data[start:start+64]
                        parser = {'start':calls[0]['target'],'window_bytes':64,'sha256':sha(window),
                                  'instructions':[{'address':i.address,'hex':i.bytes.hex(),'mnemonic':i.mnemonic,'operands':i.op_str}
                                                  for i in decoder.disasm(window,calls[0]['target'])]}
                readers.append({'literal':literal,'root_table_load':0x08000000+pc,'code_window':instructions,
                                'nearby_BL_candidates':calls,'first_BL_window_candidate':parser})
        tables.append({'root_pair_offset':at,'root_values':[0x08765190,0x08765B18],
                       'table_pointer_literals':literals,'Thumb_literal_reader_candidates':readers})
    if len(tables) != 9:
        raise ValueError('source root-pair denominator changed')
    out = ROOT / 'analysis/exe45_chip_name_consumers_static_v1.json'
    if out.exists():
        raise ValueError('refuse survey overwrite')
    report = {'source_sha256':sha(data),'tool_sha256':sha(__file__ and (ROOT / 'tools/survey_chip_name_consumers.py').read_bytes()),
              'scope':'static aligned source pairs and Thumb opcode/literal candidates; code/data boundaries and runtime ownership unconfirmed',
              'root_pair_count':len(tables),'pairs':tables,
              'limits':['first nearby BL may not be a name parser; manually validate before using','no whole-engine reference completeness claim',
                        'no new hook, VRAM allocation, source pointer change or translation claim']}
    out.write_text(json.dumps(report,indent=2),encoding='utf-8')
    for t in tables:
        print(f"{t['root_pair_offset']:06X}",[(f"{r['root_table_load']:08X}",[f"{c['target']:08X}" for c in r['nearby_BL_candidates'][:2]]) for r in t['Thumb_literal_reader_candidates']])


if __name__ == '__main__':
    main()
