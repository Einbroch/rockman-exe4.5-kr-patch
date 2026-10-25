"""Two kana-page replacement candidate; no ROM writer or approved UI layout.

Both kana pages expose the same existing 40-jamo candidate, preserving the
three-page control ABI. Page 2 is intentionally not claimed as implemented.
The TPL literals are provenance, NOT directly reinsertable Hangul strings.
"""
import json
import re
from pathlib import Path
from build_visibility_poc import ROOT, sha, require_hash
from report_fixedcell_runtime import read
from prepare_keyboard_page_graphics import decode, encode, preview
from hangul_keyboard_action_shim import CODE
from extended_dialogue import assemble_verified


def assemble(address=0x08303000):
    old = 'cmp r2, #0\nbne action_handled'
    if CODE.count(old) != 1:
        raise ValueError('source action page guard changed')
    # Reject page 2 and malformed page IDs, rather than selecting kana tokens.
    code = CODE.replace(old, 'cmp r2, #1\nbhi action_handled')
    return assemble_verified(code, address, dict(editor=0x0200FC40,
        selectors=0x09301000, context=0x09300000, helper=0x08F0D001))


def main():
    base = ROOT/'analysis/hangul_keyboard_v1'
    out = base/'kana_replacement'; out.mkdir(exist_ok=True)
    p = base/'page_graphics/report.json'; graphics = read(p)
    if not graphics['passed'] or graphics['rom_integrated']:
        raise ValueError('graphics evidence scope')
    for name, h in graphics['tools'].items():
        require_hash(ROOT/'tools'/name, h)
    for name, h in graphics['artifacts'].items():
        require_hash(p.parent/name, h)
    plan_path = base/'candidates/plan.json'; plan = read(plan_path)
    require_hash(plan_path, graphics['plan_sha256'])
    cells = plan['selectors'][:90]
    selectors = bytes(s['glyph_index'] if s['active'] else 255 for s in cells)
    if len(selectors) != 90 or sum(v < 40 for v in selectors) != 40:
        raise ValueError('selector domain')
    profile = read(ROOT/'project.json')['source_profile']
    source = ROOT/profile['filename']; require_hash(source, profile['sha256'])
    rom = source.read_bytes()
    tpl_path = ROOT/'analysis/full_scope_v1/source_tpl/6368E8.tpl'
    tpl = tpl_path.read_text(encoding='utf8')
    catalog_path = ROOT/'analysis/full_scope_save_initialize_v1/literal_backlog.json'
    catalog = read(catalog_path)
    if catalog['source_sha256'] != profile['sha256']:
        raise ValueError('source catalog revision')
    units = {u['id']:u for u in catalog['units']}
    literals = []
    for script in (2, 3):
        match = re.search(r'script '+str(script)+r' mmbn45s \{\s*"([^"\n]+)"\s*end\s*\}', tpl)
        if not match or len(match[1]) != 85:
            raise ValueError('kana source literal structure')
        unit = units[f'6368E8:{script}:0']
        require_hash(tpl_path,unit['source_tpl_sha256'])
        if unit['source'] != match[1]: raise ValueError('protected source literal changed')
        literals.append(dict(id=f'6368E8:{script}:0', source=match[1],
            source_character_count=len(match[1]), source_tpl_sha256=sha(tpl_path.read_bytes()),
            page=script-2, disposition='structural replacement candidate; NOT reinsertion-ready'))
    candidate = decode((p.parent/'jamo_page0_tiles.bin').read_bytes(),
                       (p.parent/'jamo_page0_map.bin').read_bytes())
    palette_path = ROOT/graphics['observed_palette']['path']
    require_hash(palette_path, graphics['observed_palette']['sha256'])
    import struct
    colors = [tuple(((v >> n)&31)*255//31 for n in (0,5,10))
              for v in struct.unpack('<16H', palette_path.read_bytes()[288:320])]
    colors[0] = (170,220,220)
    pages = []
    for page in (0, 1):
        native = graphics['pages'][page]
        bank = rom[native['bank_offset']:native['bank_offset']+native['bank_bytes']]
        mapping = rom[native['map_offset']:native['map_offset']+1200]
        require_hash_bytes = (sha(bank), sha(mapping))
        if require_hash_bytes != (native['bank_sha256'], native['map_sha256']):
            raise ValueError('native asset identity')
        original = decode(bank, mapping)
        # Unchanged roundtrip is pixel equivalence, not tile-number identity.
        b, m = encode(original)
        if decode(b, m) != original: raise ValueError('native pixel roundtrip')
        pixels = [row[:] for row in original]
        for y in range(56,152):
            for x in range(16,191):
                background = 5 if (x+y)%4 == 3 else 9
                v = original[y][x]
                if v not in (5,7,8,9) or v in (5,9) and v != background:
                    raise ValueError('kana page clean-background classification')
                pixels[y][x] = candidate[y][x]
        protected = 0
        for y in range(160):
            for x in range(240):
                if not (16 <= x < 191 and 56 <= y < 152):
                    if pixels[y][x] != original[y][x]: raise ValueError('protected pixel changed')
                    protected += 1
        b, m = encode(pixels)
        if len(b)%32 or decode(b,m) != pixels: raise ValueError('candidate pixel roundtrip')
        (out/f'page{page}_tiles.bin').write_bytes(b)
        (out/f'page{page}_map.bin').write_bytes(m)
        preview(pixels, out/f'page{page}_preview.png', colors)
        pages.append(dict(page=page, bank_bytes=len(b), map_bytes=len(m),
            protected_pixels=protected, selector_table='selectors.bin',
            active_jamo_cells=40, inactive_cells=50, native=native,
            placements=graphics['candidate']['placements']))
    (out/'selectors.bin').write_bytes(selectors)
    blob, isa = assemble(); (out/'shim.bin').write_bytes(blob)
    report = dict(id='exe45.keyboard.kana-replacement.candidate.v1', passed=True,
        rom_integrated=False, human_layout_approved=False, source_sha256=profile['sha256'],
        user_choice='automatic Hangul composition', source_literals=literals, pages=pages,
        shared_jamo_layout=True, ISA=isa,
        dependencies={'page_graphics/report.json':sha(p.read_bytes()),
                      'candidates/plan.json':sha(plan_path.read_bytes()),
                      'source_catalog':sha(catalog_path.read_bytes())},
        tools={n:sha((ROOT/'tools'/n).read_bytes()) for n in
            ('prepare_keyboard_kana_replacement.py','hangul_keyboard_action_shim.py','prepare_keyboard_page_graphics.py')},
        artifacts={f.name:sha(f.read_bytes()) for f in out.iterdir() if f.suffix in ('.bin','.png')},
        limits=['Candidate aliases both kana pages to existing jamo layout; not human approval of final arrangement.',
            '85-character source literals are not 90-cell selectors. No positional kana-to-jamo transcription or direct TPL insertion.',
            'Japanese command/tab labels outside the editable grid preserved and still need localization.',
            'Page2 Latin/symbol input, native navigation reachability, upload/render/IRQ lifetime and persistence pending.',
            'Fixture addresses are NOT adopted free space; no ROM/save modification or emulator screen claim.'])
    (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    require_hash(source,profile['sha256'])
    print('PASS two kana-page structural candidates / 40 active + 50 inactive cells per page')


if __name__ == '__main__': main()
