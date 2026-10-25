"""Bind source ID alias to both name row and actual description descriptor read."""
from pathlib import Path
import capture_secondary_chip_descriptions as previous

def main():
    code=Path(previous.__file__).read_text(encoding='utf-8')
    old=" if not secondaryActive then return end\n local s=emu.getState()\n if s['cpu.pipeline.execute.address']~=0x0803CB48 then return end"
    new=" local s=emu.getState()\n local pc=s['cpu.pipeline.execute.address']\n if pc~=0x0803CB48 and pc~=0x080D2922 then return end\n if pc==0x0803CB48 and not secondaryActive then return end"
    if code.count(old)!=1:raise ValueError('secondary descriptor consumer anchor')
    code=code.replace(old,new)
    ns={'__name__':'secondary_descriptions_r2','__file__':__file__}
    exec(compile(code,previous.__file__+' [description read D2922]','exec'),ns)
    return ns['main']()

if __name__=='__main__':raise SystemExit(main())
