"""Changing fixture for a renderer executed from its private invocation stack."""
import json
from pathlib import Path
import capture_chip_cache_changing as changing
from build_visibility_poc import require_hash, sha


def stack_main():
    matrix = changing.word.matrix
    fixed = matrix.library.fixed
    rom = Path(fixed.value('--rom'))
    m = json.loads(rom.with_suffix('.json').read_text(encoding='utf-8'))
    require_hash(rom, m['output_sha256'])
    e, st = m['chip_library_extension'], m['chip_library_extension']['stack_renderer']
    render = e['machine_code'][0]
    loads = [i for i in render['instructions'] if i['mnemonic'] in ('ldm', 'ldmia')]
    ret = [i['address'] for i in render['instructions'] if i['mnemonic'] == 'pop' and i['operands'] == '{r0, r2, r3}']
    if len(loads) != 3 or len(ret) != 1 or not st['position_independent_bytes_verified']:
        raise ValueError('stack template profile changed')
    prefix = f'''
local stackRenderStart=0
local stackRenderEnd=0
local stackLoadPc=0
local stackReturnPc=0
local stackCalls=0
local stackRows=0
local stackMin=0x03008000
local stackMax=0
emu.addMemoryCallback(function()
 local s=emu.getState();local base=math.floor(s['cpu.r7']/2)*2
 if base~=s['cpu.r13'] or base%4~=0 or base<0x03007000 or base+{st['frame_bytes']+36}>0x03007F00 then stressFail('private stack scope/alignment') end
 if bytesAt(base,{st['frame_bytes']})~=bytesAt({0x08000000+st['template_offset']},{st['frame_bytes']}) then stressFail('ROM to stack template') end
 stackRenderStart=base;stackRenderEnd=base+{render['code_bytes']}
 stackLoadPc=base+{loads[0]['address']-render['address']}
 stackReturnPc=base+{ret[0]-render['address']}
 stackCalls=stackCalls+1;stackMin=math.min(stackMin,base);stackMax=math.max(stackMax,base+{st['frame_bytes']+36})
end,emu.callbackType.exec,{st['invoke_address']},{st['invoke_address']})
'''
    code = matrix.PROBE
    code = matrix.replace_once(code, "emu.addMemoryCallback(function()\n local s=emu.getState();local dst=s['cpu.r1']",
        "emu.addMemoryCallback(function(address)\n if address~=stackLoadPc then return end\n local s=emu.getState();local dst=s['cpu.r1']")
    code = matrix.replace_once(code, '0x08000956,0x08000956', '0x03000000,0x03007FFF')
    code = matrix.replace_once(code, "c['cpu.r2']~=64 or ", '')
    code = matrix.replace_once(code, 'emu.addMemoryCallback(function()\n local s=emu.getState();local c=timingCopy',
        'emu.addMemoryCallback(function(address)\n if address~=stackReturnPc then return end\n local s=emu.getState();local c=timingCopy')
    code = matrix.replace_once(code, 'COPY_RETURN,COPY_RETURN', '0x03000000,0x03007FFF')
    matrix.PROBE = prefix + code
    matrix.FIXTURE = matrix.FIXTURE.replace('pc<RENDER_START or pc>=RENDER_END', 'pc<stackRenderStart or pc>=stackRenderEnd')
    matrix.FIXTURE += f'''
emu.addMemoryCallback(function()
 if bytesAt(stackRenderStart,{st['frame_bytes']})~=bytesAt({0x08000000+st['template_offset']},{st['frame_bytes']}) then stressFail('stack code lifetime') end
 stackRows=stackRows+1
end,emu.callbackType.exec,0x08042EE4,0x08042EE4)
local oldStackDump=dumpTiming
dumpTiming=function(name)
 oldStackDump(name)
 write(name..'_stack.json',string.format('{{"invocations":%d,"rows_returned":%d,"minimum_code_base":%d,"maximum_frame_end":%d}}',stackCalls,stackRows,stackMin,stackMax))
end
'''
    rc = matrix.main()
    out = Path(fixed.value('--out'))
    d = json.loads((out / 'final_stack.json').read_text())
    groups = len(json.loads((out / 'final_timing.json').read_text())['groups'])
    valid = rc == 0 and d['invocations'] == d['rows_returned'] == groups*7
    (out / 'stack_environment.json').write_text(json.dumps({'tool_sha256': sha(Path(__file__).read_bytes()),
        'rom_sha256': m['output_sha256'], 'passed': valid, 'observed': d,
        'scope': 'actual copied Thumb execution; private invocation stack; changing diagnostic reads',
        'callback_api_source': 'https://github.com/SourMesen/Mesen2/blob/master/Core/Debugger/ScriptingContext.cpp'}, indent=2), encoding='utf-8')
    return rc if valid else 1


if __name__ == '__main__':
    changing.word.main = stack_main
    raise SystemExit(changing.main())
