"""Read-only word-copy candidate probe; frozen BIOS probe is not modified."""
import json
from pathlib import Path
import capture_chip_library_qa as base
from build_visibility_poc import ROOT, require_hash, sha


def main():
    fixed = base.library.fixed
    rom = Path(fixed.value('--rom')).resolve()
    m = json.loads(rom.with_suffix('.json').read_text(encoding='utf-8'))
    require_hash(rom, m['output_sha256'])
    require_hash(Path(base.__file__), '74a86b1147ee8ca14c3c9bb74fe5ec2c10f8b53d9b59253e9c94dcf7acb6fd51')
    e = m['chip_library_extension']
    if e.get('copy_policy') != 'experimental-inline-16-words':
        raise ValueError('word-copy candidate required')
    ins = e['machine_code'][0]['instructions']
    loads = [i for i in ins if i['mnemonic'] in ('ldm', 'ldmia')]
    returns = [i['address'] for i in ins if i['mnemonic'] == 'pop' and i['operands'] == '{r0, r2, r3}']
    if len(loads) != 8 or len(returns) != 1:
        raise ValueError('copy boundaries changed')
    spec = json.loads((ROOT / 'tools/specs/exe45_chip_library_v1.json').read_text())
    values = {'ROW_BUFFER': e['buffer']['start'], 'SOURCE_POOL': 0x08000000 + spec['pool']['offset'],
              'PRIVATE_POOL': 0x08000000 + e['clone_offset'],
              'TILE_START': (e['vram']['start'] - e['vram']['char_base']) // 32,
              'INSTALL_ADDRESS': 0x08000000 + e['install']['offset'],
              'CONTINUATION': e['install']['continuation'] & ~1,
              'CACHE_START': e['vram']['start'], 'CACHE_END': e['vram']['start'] + e['vram']['bytes'],
              'FONT_START': 0x08000000 + e['font_offset'], 'COPY_HELPER': loads[0]['address'], 'COPY_RETURN': returns[0]}
    code = base.PROBE.replace("s['cpu.r2']~=64 or ", '').replace('verified_bios_copies', 'verified_word_copies').replace('real BIOS', 'real inline word')
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
    out = Path(fixed.value('--out')).resolve()
    observed = json.loads((out / 'final_chip_ko.json').read_text())
    r = json.loads((out / 'result.json').read_text())
    valid = r['complete'] and not (out / 'wordcopy_failed.txt').exists() and observed['abi_calls'] > 0 and observed['verified_word_copies'] > 0
    if not valid:
        r['complete'] = False
        (out / 'result.json').write_text(json.dumps(r, indent=2), encoding='utf-8')
    (out / 'wordcopy_environment.json').write_text(json.dumps({'tool_sha256': sha(Path(__file__).read_bytes()),
        'rom_sha256': m['output_sha256'], 'substitutions': values,
        'scope': 'normal input; actual inline loads/stores, ABI and tile checks; NOT timing proof', 'passed': valid}, indent=2), encoding='utf-8')
    return rc if valid else 1


if __name__ == '__main__':
    raise SystemExit(main())
