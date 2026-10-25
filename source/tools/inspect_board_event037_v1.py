"""Read-only source literal references, not executable coverage evidence."""
from pathlib import Path
from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB

r = Path('Rockman EXE 4.5 Real Operation (J)(Independent).gba').read_bytes()
d = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
for value in (0x02010730, 0x0806A4EC):
    needle = value.to_bytes(4, 'little')
    at = r.find(needle)
    while at >= 0:
        print('LITERAL', hex(value), hex(at), 'raw', r[max(0, at-16):at+16].hex(' '))
        start = max(0, at-64)
        for x in d.disasm(r[start:at], 0x08000000+start):
            print(f'{x.address:08x} {x.mnemonic} {x.op_str}')
        at = r.find(needle, at+1)
