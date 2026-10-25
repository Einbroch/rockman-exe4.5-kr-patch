"""Narrow descriptor-address observation before querying expensive CPU state."""
from pathlib import Path
import capture_secondary_chip_descriptions_r2 as previous

def main():
    code=Path(previous.__file__).read_text(encoding='utf-8')
    old='new=" local s=emu.getState()\\n local pc='
    new='new=" if secondaryDesc==0 or address<secondaryDesc+8 or address>=secondaryDesc+224 or (address-secondaryDesc)%32~=8 then return end\\n local s=emu.getState()\\n local pc='
    if code.count(old)!=1:raise ValueError('narrow descriptor callback anchor')
    code=code.replace(old,new)
    ns={'__name__':'secondary_descriptions_r3','__file__':__file__}
    exec(compile(code,previous.__file__+' [narrow descriptor addresses]','exec'),ns)
    return ns['main']()

if __name__=='__main__':raise SystemExit(main())
