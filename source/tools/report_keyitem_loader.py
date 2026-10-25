"""Record the established native UI link; do not claim buffer growth support."""
import json, struct
from build_visibility_poc import ROOT, require_hash, sha
from verify_tpi_index import lz77_decompress

def main():
    original=ROOT/'Rockman EXE 4.5 Real Operation (J)(Independent).gba'
    require_hash(original,'588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8')
    rom=ROOT/'poc/output/exe45_ko_development_gutsman_calendar_inventory_v1.gba'
    require_hash(rom,'2adcc7111363c377628071f9b3ac313ead4615c157a7478f842c316a410a80d1')
    data=original.read_bytes();payload,consumed=lz77_decompress(data,0x709408)
    rt=ROOT/'poc/runtime/keyitem-loader-v1-enter'
    result=json.loads((rt/'result.json').read_text())
    loads=json.loads((rt/'step_003_keyitem_loads.json').read_text())['loads']
    if len(loads)!=1:raise ValueError('unexpected source archive load count')
    regs=loads[0]['registers']
    if (regs['r0'],regs['r1'],regs['r14'])!=(0x08709408,0x02020800,0x080349f1):
        raise ValueError('native loader identity changed')
    if data[0x349e8:0x349ec]!=bytes.fromhex('10481149'):
        raise ValueError('UI PC-relative root/destination loads changed')
    ram=(rt/'step_003_gbaExtWorkRam.bin').read_bytes()
    if ram[0x20800:0x20800+len(payload)]!=payload:
        raise ValueError('native decompression bytes mismatch')
    if any(struct.unpack_from('<I',data,p)[0]!=0x08709408 for p in [0x34a2c,0x4c5e8]):
        raise ValueError('shared roots changed')
    report=dict(policy='analysis only; NOT RELEASE EVIDENCE FOR TRANSLATED ASSET',
        original_sha256=sha(data),tested_rom_sha256=sha(rom.read_bytes()),
        source_payload_bytes=len(payload),source_consumed_bytes=consumed,
        source_payload_sha256=sha(payload),native_source_decompression_exact=True,
        ui_consumer=dict(function='080349DC',root_literal='08034A2C',
            destination_literal='08034A30',destination='02020800',caller_lr='080349F1',
            input_route='same-ROM select-gutsman -> left -> A',
            screenshot='poc/runtime/keyitem-loader-v1-enter/step_003.png'),
        other_consumer=dict(function='0804C5B4',root_literal='0804C5E8',
            destination='02031000',runtime_reached=False),
        unresolved=['Maximum destination extent and shared lifetime for both consumers.',
                    'Translated output compression and actual Korean rendering not yet tested.',
                    'Global Hangul entry/edit, record redisplay, fresh persistent reload and old-save compatibility remain open.'],
        rom_modified=False,release_eligible=False,segment_result_sha256=sha((rt/'result.json').read_bytes()))
    out=ROOT/'analysis/keyitem_translation_draft_v1/loader.json'
    text=json.dumps(report,indent=2)+'\n'
    if out.exists() and out.read_text()!=text:raise ValueError('preserve loader evidence')
    if not out.exists():out.write_text(text,encoding='utf8')
    print(json.dumps(report))

if __name__=='__main__':main()
