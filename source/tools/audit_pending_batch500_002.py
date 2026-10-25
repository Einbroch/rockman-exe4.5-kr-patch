"""Source/cumulative mail capacity and explicit word-boundary investigation; no ROM writes."""
import argparse
import itertools
import json
import re
import struct
from build_visibility_poc import ROOT, sha, require_hash, run_textpet
from tpl_literals import literals, replace_literals, skeleton
from textpet_korean import command
from archive_scripts import script_spans, verify_untouched_scripts
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of
from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB
from keyitem_rom_selector import construct
from prepare_pending_batch500_002 import BASE, BASE_SHA, LAYOUT


def width(text):
    return sum(12 if '\uac00' <= ch <= '\ud7a3' or ch == ',' else 8 if ch == ' ' else 11 for ch in text)


def word_partitions(text, rows):
    words = text.replace('\n', ' ').split(' ')
    solutions = []
    for cuts in itertools.combinations(range(1, len(words)), rows - 1):
        boundaries = (0,) + cuts + (len(words),)
        lines = [' '.join(words[a:b]) for a,b in zip(boundaries,boundaries[1:])]
        widths = [width(line) for line in lines]
        if all(w <= (132 if rows == 3 and i == 2 else 152) for i,w in enumerate(widths)):
            solutions.append(dict(lines=lines,widths=widths))
    return solutions


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--preflight',default='analysis/pending_insertion_500_002_r3/preflight.json')
    p.add_argument('--out',default='analysis/pending_insertion_500_002_capacity_v1')
    a = p.parse_args()
    out = ROOT / a.out
    if out.exists():
        raise ValueError('Preserve prior evidence')
    cfg = json.loads((ROOT/'project.json').read_text(encoding='utf8'))
    original = ROOT/cfg['source_profile']['filename']
    require_hash(original,cfg['source_profile']['sha256'])
    source = original.read_bytes()
    require_hash(ROOT/BASE,BASE_SHA)
    baseline = (ROOT/BASE).read_bytes()
    meta = json.loads((ROOT/BASE).with_suffix('.json').read_text(encoding='utf8'))
    prepath = ROOT/a.preflight
    pre = json.loads(prepath.read_text(encoding='utf8'))
    require_hash(ROOT/LAYOUT,pre['individual_layout']['sha256'])
    if pre['total_units'] != 500 or pre['baseline_sha256'] != BASE_SHA or pre['rom_written']:
        raise ValueError('Preflight scope mismatch')
    pre_dir = prepath.parent
    for path, expected in pre['artifacts'].items():
        require_hash(pre_dir/path,expected)
    mail_rows = []
    for index, archive in [(24,'6DE2C8'),(26,'6DED88'),(28,'6E01AC')]:
        pointer = 0x405F8+4*index
        if struct.unpack_from('<I',source,pointer)[0] != 0x08000000+int(archive,16):
            raise ValueError('Native mail pointer identity')
        if source[pointer:pointer+4] != baseline[pointer:pointer+4]:
            raise ValueError('Baseline changed native mail pointer')
        record = next(r for r in pre['archives'] if r['archive']==archive)
        mail_rows.append(dict(navi_index=index,archive=archive,pointer_offset=pointer,
            original_payload_bytes=record['source_bytes'],batch_only_bytes=record['compiled_bytes'],
            decompression_destination=0x0202B2F4,next_mail_asset=0x0202D2F4,
            comparison_bytes=8192,batch_only_overflow=record['compiled_bytes']>8192))
    # Exact verified source constants, not a claim about every loader or lifetime.
    for at, value in [(0x40578,0x0804057C),(0x405F0,0x020262F4),
                      (0x405F4,0x080405F8),(0x4066C,0x0202B2F4)]:
        if struct.unpack_from('<I',source,at)[0] != value:
            raise ValueError('Native loader constant identity: '+hex(at))
    instructions = list(Cs(CS_ARCH_ARM,CS_MODE_THUMB).disasm(source[0x40548:0x40576],0x08040548))
    if [(i.address,i.mnemonic,i.op_str) for i in instructions if i.address in (0x08040550,0x0804055E)] != [
        (0x08040550,'ldr','r0, [r0, r1]'),(0x0804055E,'ldr','r0, [r0, r1]')]:
        raise ValueError('Loader table consumers changed')
    out.mkdir(parents=True)
    record = next(r for r in pre['archives'] if r['archive']=='6E01AC')
    require_hash(ROOT/record['draft_path'],record['draft_sha256'])
    draft = json.loads((ROOT/record['draft_path']).read_text(encoding='utf8'))
    require_hash(ROOT/draft['source_tpl']['path'],draft['source_tpl']['sha256'])
    tpl = (ROOT/draft['source_tpl']['path']).read_text(encoding='utf-8-sig')
    layout = json.loads((ROOT/LAYOUT).read_text(encoding='utf8'))['layouts']
    units = [dict(x) for x in draft['units']]
    for x in units:
        if x['id'] in layout:
            x['translation'] = layout[x['id']]
    if len(units)!=131:
        raise ValueError('Full destruction population')
    translated = replace_literals(tpl,units)
    target = out/'translated.tpl'
    target.write_text(translated,encoding='utf8')
    (out/'compiled').mkdir()
    compiled = out/'compiled/6E01AC.msg'
    common = command(pre_dir/'plugins')
    run_textpet(common+['Read-Text-Archives',str(target),'--format','tpl',
        'Write-Text-Archives',str(compiled),'--format','bin'],out/'compile.log')
    raw = compiled.read_bytes()
    reverse = out/'reverse.tpl'
    run_textpet(common+['Read-Text-Archives',str(compiled),'--format','bin',
        'Write-Text-Archives',str(reverse),'--format','tpl'],out/'reverse.log')
    back = reverse.read_text(encoding='utf-8-sig')
    if skeleton(back)!=skeleton(tpl) or [(x.key,x.text) for x in literals(back)]!=[(x.key,x.text) for x in literals(translated)]:
        raise ValueError('Cumulative protected/semantic roundtrip')
    rebuilt = out/'rebuilt.msg'
    run_textpet(common+['Read-Text-Archives',str(reverse),'--format','tpl',
        'Write-Text-Archives',str(rebuilt),'--format','bin'],out/'rebuild.log')
    if rebuilt.read_bytes()!=raw:
        raise ValueError('Cumulative binary roundtrip')
    prior = next(r for r in meta['keyitem_rom']['mission_mail_archives'] if r['archive']=='6E01AC')
    prior_raw = baseline[prior['rom_offset']:prior['rom_offset']+prior['compiled_bytes']]
    if sha(prior_raw)!=prior['compiled_sha256']:
        raise ValueError('Baseline compiled clone identity')
    old_spans,new_spans = script_spans(prior_raw,47),script_spans(raw,47)
    carried = [38,39,40]
    if any(old_spans[s]!=new_spans[s] for s in carried):
        raise ValueError('Previously applied destruction scripts regressed')
    require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row = next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==0x6E01AC)
    native = payload_of(source,row)
    untouched = verify_untouched_scripts(native,raw,47,{int(x['id'].split(':')[1]) for x in units})
    # Assemble a four-body selector in a virtual address layout only. No ROM is emitted.
    address = (0x08000000+len(baseline)+3)&~3
    guards = [dict(g) for g in meta['keyitem_rom']['mission_guards'][:2]]
    guards.append(dict(clone_address=address,payload_bytes=len(raw),guard_header_hex=native[:16].hex(),script_count=47))
    address = (address+len(raw)+3)&~3
    shadow = next(r for r in pre['archives'] if r['archive']=='6DED88')
    shadow_native = (pre_dir/'6DED88/source.msg').read_bytes()
    guards.append(dict(clone_address=address,payload_bytes=shadow['compiled_bytes'],
        guard_header_hex=shadow_native[:16].hex(),script_count=66))
    address = (address+shadow['compiled_bytes']+3)&~3
    selector_meta = meta['keyitem_rom']
    stub, code, proof = construct(source,bytes.fromhex(selector_meta['guard_header_hex']),
        selector_meta['clone_address'],address,selector_meta['rom_bytes'],selector_meta['mail_guard'],guards)
    (out/'virtual_selector.bin').write_bytes(code)
    investigations = []
    for candidate in pre['layout_candidates']:
        r = next(r for r in pre['archives'] if r['archive']==candidate['id'].split(':')[0])
        d = json.loads((ROOT/r['draft_path']).read_text(encoding='utf8'))
        u = next(x for x in d['units'] if x['id']==candidate['id'])
        same_rows = u['translation'].count('\n')+1
        investigations.append(dict(id=u['id'],wording_unchanged=True,source_rows=same_rows,
            same_row_word_boundary_solutions=word_partitions(u['translation'],same_rows),
            three_row_word_boundary_solutions=word_partitions(u['translation'],3),
            action='investigate explicit extra LF/page policy; do not shorten or silently split words'))
    report = dict(schema=1,passed=True,scope='static compilation/Thumb assembly only; NOT CPU ABI/GBA loader/render/save evidence',
        source_sha256=sha(source),baseline_rom_sha256=BASE_SHA,preflight_path=a.preflight,preflight_sha256=sha(prepath.read_bytes()),
        mail_loader_code_sha256=sha(source[0x40548:0x40576]),mail_loaders=mail_rows,
        cumulative_destruction=dict(selected_units=131,new_units=105,carried_units=26,
            compiled_bytes=len(raw),compiled_sha256=sha(raw),overflow_existing_8192=len(raw)>8192,
            prior_selected_script_bytes_exact=carried,unselected_native_scripts_exact=untouched),
        four_body_selector=dict(virtual_only=True,stub_hex=stub.hex(),bytes=len(code),proof=proof,cpu_tested=False),
        layout_investigations=investigations,rom_written=False,rom_applied_units=0,release_eligible=False)
    report['artifacts']={str(p.relative_to(out)):sha(p.read_bytes()) for p in sorted(out.rglob('*')) if p.is_file()}
    (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('Cumulative destruction',len(raw),'prior26 preserved; four-body assembly',len(code),'bytes; ROM unchanged')


if __name__=='__main__':
    main()
