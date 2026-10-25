"""Add direct root literal loads missed by root-table-pointer-only survey."""
import json
import struct
from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB
from build_visibility_poc import ROOT, sha, require_hash


def main():
    config = json.loads((ROOT / 'project.json').read_text())
    source = ROOT / config['source_profile']['filename']
    require_hash(source,config['source_profile']['sha256'])
    data = source.read_bytes()
    prior_path = ROOT / 'analysis/exe45_chip_name_consumers_static_v1.json'
    prior = json.loads(prior_path.read_text())
    require_hash(ROOT / 'tools/survey_chip_name_consumers.py',prior['tool_sha256'])
    decoder = Cs(CS_ARCH_ARM,CS_MODE_THUMB)
    groups = []
    for pair in prior['pairs']:
        slots = []
        for literal in (pair['root_pair_offset'],pair['root_pair_offset']+4):
            readers = []
            for pc in range(max(0,literal-1024),literal,2):
                op = struct.unpack_from('<H',data,pc)[0]
                if op & 0xF800 != 0x4800 or ((pc+4)&~3)+(op&255)*4 != literal:
                    continue
                readers.append({'pc':0x08000000+pc,'root_register':(op>>8)&7,
                                'instructions':[{'address':i.address,'hex':i.bytes.hex(),'mnemonic':i.mnemonic,'operands':i.op_str}
                                                for i in decoder.disasm(data[pc:pc+48],0x08000000+pc)]})
            slots.append({'literal':literal,'root':struct.unpack_from('<I',data,literal)[0],
                          'Thumb_PC_literal_load_candidates':readers})
        groups.append({'pair':pair['root_pair_offset'],'direct_root_slots':slots})
    windows = []
    for label,start,end in [('banked root selector',0x1F7D4,0x1F7EA),
                            ('banked script pointer lookup',0x3864C,0x3866A),
                            ('alternate row source selector',0x3CB64,0x3CB7A),
                            ('alternate eight-cell tile parser',0x3CBB0,0x3CBEA),
                            ('generic script wrapper',0x554A4,0x554C4)]:
        blob = data[start:end]
        ins = list(decoder.disasm(blob,0x08000000+start))
        if sum(i.size for i in ins) != len(blob):
            raise ValueError('bounded source instruction decoding incomplete')
        windows.append({'label':label,'start':start,'end':end,'sha256':sha(blob),
                        'instructions':[{'address':i.address,'hex':i.bytes.hex(),'mnemonic':i.mnemonic,'operands':i.op_str} for i in ins]})
    out = ROOT / 'analysis/exe45_chip_name_direct_readers_v1.json'
    if out.exists():
        raise ValueError('refuse survey overwrite')
    report = {'source_sha256':sha(data),'tool_sha256':sha((ROOT / 'tools/survey_chip_name_direct_readers.py').read_bytes()),
              'prior_survey_sha256':sha(prior_path.read_bytes()),'root_pair_count':len(groups),'groups':groups,'bounded_source_windows':windows,
              'confirmed_static_findings':[
                  '0801F7D4 masks input to 9 bits, picks bank at >255 and returns root in r0, low script in r1; MOV PC,LR at 0801F7E8 ends it',
                  '0803864C chooses direct primary/secondary root at ID255 boundary, reads uint16 script offset, returns script pointer; no glyph supply here',
                  '0803CB76 calls 0803CBB0; parser interprets one byte as two resident tile indices, writes top/bottom halfwords and pads to eight cells',
                  '080554A4 resolves script offset and BX-calls original IWRAM 03006825 through ROM literal 554C4; caller reachability is unproven'],
              'limits':['aligned opcode matches are candidate code references until boundaries/callers are verified',
                        'nine physical root pairs do not prove complete pointer/reference coverage',
                        'no runtime context, VRAM ownership or Korean implementation claim for alternate consumers']}
    out.write_text(json.dumps(report,indent=2),encoding='utf-8')
    print('direct root candidate reads:',sum(len(s['Thumb_PC_literal_load_candidates']) for g in groups for s in g['direct_root_slots']))
    for g in groups:
        print(f"{g['pair']:06X}",[[f"{r['pc']:08X}" for r in s['Thumb_PC_literal_load_candidates']] for s in g['direct_root_slots']])


if __name__ == '__main__':
    main()
