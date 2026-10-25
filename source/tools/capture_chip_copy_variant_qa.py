"""Normal-input ABI/pixels/cache observations for explicitly selected copy engines."""
import json
from pathlib import Path
import capture_chip_cache_qa as cache
from build_visibility_poc import ROOT, require_hash, sha


def variant_main():
    base = cache.word.base
    fixed = base.library.fixed
    rom = Path(fixed.value('--rom')).resolve()
    m = json.loads(rom.with_suffix('.json').read_text(encoding='utf-8'))
    require_hash(rom, m['output_sha256'])
    require_hash(Path(base.__file__), '74a86b1147ee8ca14c3c9bb74fe5ec2c10f8b53d9b59253e9c94dcf7acb6fd51')
    e = m['chip_library_extension']
    ins = e['machine_code'][0]['instructions']
    returns = [i['address'] for i in ins if i['mnemonic'] == 'pop' and i['operands'] == '{r0, r2, r3}']
    if len(returns) != 1:
        raise ValueError('copy return boundary changed')
    if e.get('copy_variant') == '6+6+4':
        loads = [i for i in ins if i['mnemonic'] in ('ldm', 'ldmia')]
        if [i['operands'] for i in loads] != ['r0!, {r2, r3, r4, r5, r6, r7}']*2+['r0!, {r2, r3, r4, r5}']:
            raise ValueError('burst profile changed')
        entry = loads[0]['address']
        code = base.PROBE.replace("s['cpu.r2']~=64 or ", '')
    elif e.get('copy_variant') == 'native-0800097C':
        if e['machine_code'][0]['literal_values']['copy_helper'] != 0x0800097D:
            raise ValueError('fast helper changed')
        entry = 0x0800097C
        code = base.PROBE
    else:
        raise ValueError('unsupported copy variant')
    spec = json.loads((ROOT / 'tools/specs/exe45_chip_library_v1.json').read_text())
    values = {'ROW_BUFFER': e['buffer']['start'], 'SOURCE_POOL': 0x08000000 + spec['pool']['offset'],
              'PRIVATE_POOL': 0x08000000 + e['clone_offset'], 'TILE_START': 514,
              'INSTALL_ADDRESS': 0x08000000 + e['install']['offset'], 'CONTINUATION': e['install']['continuation'] & ~1,
              'CACHE_START': e['vram']['start'], 'CACHE_END': e['vram']['start'] + e['vram']['bytes'],
              'FONT_START': 0x08000000 + e['font_offset'], 'COPY_HELPER': entry, 'COPY_RETURN': returns[0]}
    code = code.replace('verified_bios_copies', 'verified_word_copies')
    code = "local function wordFail(s) write('wordcopy_failed.txt',s);emu.stop(1);error(s) end\n" + code.replace('error(', 'wordFail(')
    for key, value in values.items():
        code = code.replace(key, str(value))
    fixed.PROBE += code
    for name, dump in [('capture(name)', 'name'), ('finish()', "'final'")]:
        old = 'local function ' + name + '\n'
        if fixed.runner.LUA_TEMPLATE.count(old) != 1:
            raise ValueError('capture anchor drift')
        fixed.runner.LUA_TEMPLATE = fixed.runner.LUA_TEMPLATE.replace(old, old + ' dumpChipKo(' + dump + ')\n')
    rc = base.library.main()
    out = Path(fixed.value('--out'))
    r = json.loads((out / 'result.json').read_text())
    valid = rc == 0 and r['complete'] and not (out / 'wordcopy_failed.txt').exists()
    if not valid:
        r['complete'] = False
        (out / 'result.json').write_text(json.dumps(r, indent=2), encoding='utf-8')
    (out / 'copy_variant_environment.json').write_text(json.dumps({'tool_sha256': sha(Path(__file__).read_bytes()),
        'rom_sha256': m['output_sha256'], 'copy_variant': e['copy_variant'], 'copy_entry': entry,
        'passed': valid, 'scope': 'normal input; actual selected copy engine, row ABI and cache pixels'}, indent=2), encoding='utf-8')
    return rc if valid else 1


if __name__ == '__main__':
    cache.word.main = variant_main
    raise SystemExit(cache.main())
