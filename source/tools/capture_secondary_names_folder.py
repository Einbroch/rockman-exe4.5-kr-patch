"""Read-only secondary folder observer + diagnostic descriptor ID selection."""
import json
from pathlib import Path
import capture_chip_folder_qa as normal
import capture_secondary_chip_descriptions as previous

def main():
    fixed=normal.frozen.library.fixed
    rom=Path(fixed.value('--rom'));m=json.loads(rom.with_suffix('.json').read_text())
    clone=0x08000000+m['chip_folder_extension']['secondary_clone_offset']
    probe=normal.frozen.PROBE
    for old,new in {
        'root==SOURCE_POOL':'(root==SOURCE_POOL or root==0x08765B18)',
        'if private then root=PRIVATE_POOL end':f'if private then if root==0x08765B18 then root={clone} else root=PRIVATE_POOL end end',
    }.items():
        if probe.count(old)!=1:raise ValueError('secondary row observation anchor:'+old)
        probe=probe.replace(old,new)
    normal.frozen.PROBE=probe
    code=Path(previous.__file__).read_text(encoding='utf-8')
    old=" if not secondaryActive then return end\n local s=emu.getState()\n if s['cpu.pipeline.execute.address']~=0x0803CB48 then return end"
    new=" if secondaryDesc==0 or address<secondaryDesc+8 or address>=secondaryDesc+224 or (address-secondaryDesc)%32~=8 then return end\n local s=emu.getState()\n local pc=s['cpu.pipeline.execute.address']\n if pc~=0x0803CB48 and pc~=0x080D2922 then return end\n if pc==0x0803CB48 and not secondaryActive then return end"
    if code.count(old)!=1:raise ValueError('diagnostic source ID anchor')
    code=code.replace(old,new)
    code=code.replace('import capture_fixedcell_probe as fixed','import capture_chip_folder_qa as normal\nfixed=normal.frozen.library.fixed')
    code=code.replace('rc=fixed.main()','rc=normal.main()')
    ns={'__name__':'secondary_names_folder','__file__':__file__}
    exec(compile(code,previous.__file__+' [both name roots/read aliases]','exec'),ns)
    return ns['main']()

if __name__=='__main__':raise SystemExit(main())
