"""Read-only save archive/root/font observer with isolated disk inventory."""
import json,sys
from pathlib import Path
import capture_roll_pet as pet
from build_visibility_poc import ROOT,require_hash,sha
from capture_save_qa import inventory

def value(flag):return sys.argv[sys.argv.index(flag)+1]

def main():
    emulator=Path(value('--mesen')).resolve();out=Path(value('--out')).resolve()
    config=json.loads((ROOT/'project.json').read_text(encoding='utf-8'));deps=config['development_dependencies']['runtime_capture']
    require_hash(emulator,deps['mesen_sha256']);require_hash(ROOT/deps['tool'],deps['tool_sha256'])
    settings=emulator.parent/'settings.json';prefs=json.loads(settings.read_text(encoding='utf-8-sig'))['Preferences'];save=Path(prefs['SaveDataFolder']).resolve()
    safe=(ROOT/'poc/runtime').resolve()
    if not prefs['OverrideSaveDataFolder'] or any(not p.is_relative_to(safe) or p==safe for p in (emulator,out,save)) or out.exists():raise ValueError('fresh isolated capture required')
    bios=emulator.parent/'Firmware/gba_bios.bin';require_hash(bios,'fd2547724b505f487e6dcb29ec2ecff3af35a841a77ab2e85fd87350abd36570')
    rp=Path(value('--rom')).resolve();require_hash(rp,value('--expect-rom-sha256'))
    before=inventory(save);pet.ARCHIVE='6DA21C';rc=pet.main();after=inventory(save)
    (out/'save_environment.json').write_text(json.dumps({'observer_only':True,'policy':'normal controller input; isolated test saves; no RAM/save import or edits','build_sha256':value('--expect-rom-sha256'),'save_directory':str(save),'files_before':before,'files_after':after,'settings_sha256':sha(settings.read_bytes()),'bios_sha256':sha(bios.read_bytes()),'self_sha256':sha(Path(__file__).read_bytes()),'observer_sha256':sha(Path(pet.__file__).read_bytes())},indent=2),encoding='utf-8')
    snapshots=out/'persistent_files_after';snapshots.mkdir()
    for name in after:(snapshots/name).write_bytes((save/name).read_bytes())
    return rc

if __name__=='__main__':raise SystemExit(main())
