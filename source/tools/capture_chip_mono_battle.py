"""Read-only mono-only battle observation; exclude per-frame big chip labels."""
from pathlib import Path
import json
import capture_chip_mono_parent as parent


def main():
    fixed=parent.library.fixed
    old=" if fixedActive~=nil or #fixedCalls>=1000 then error('fixed-cell probe nesting/limit') end\n local s=emu.getState()"
    new=" local s=emu.getState()\n if s['cpu.r6']~=0x08619EF8 then return end\n if fixedActive~=nil or #fixedCalls>=1000 then error('fixed-cell probe nesting/limit') end"
    if fixed.PROBE.count(old)!=1: raise ValueError('mono entry filter anchor')
    fixed.PROBE=fixed.PROBE.replace(old,new)
    old=" if fixedActive==nil then error('fixed-cell exit without entry') end"
    if fixed.PROBE.count(old)!=1: raise ValueError('mono exit filter anchor')
    fixed.PROBE=fixed.PROBE.replace(old,' if fixedActive==nil then return end')
    rc=parent.main()
    out=Path(fixed.value('--out'))
    failures=list(out.glob('*failed*'))
    if failures:
        r=json.loads((out/'result.json').read_text())
        r['complete']=False
        (out/'result.json').write_text(json.dumps(r,indent=2),encoding='utf-8')
        return 1
    return rc


if __name__=='__main__': raise SystemExit(main())
