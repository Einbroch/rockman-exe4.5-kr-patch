"""Read-only intro/return observer across cold boot of isolated native save."""
import json,sys
from pathlib import Path
import capture_roll_pet as pet
from capture_save_qa import inventory
from build_visibility_poc import ROOT,sha,require_hash

def main():
    def value(k):return sys.argv[sys.argv.index(k)+1]
    em=Path(value('--mesen')).resolve();out=Path(value('--out')).resolve();rp=Path(value('--rom')).resolve()
    m=json.loads(rp.with_suffix('.json').read_text());require_hash(rp,value('--expect-rom-sha256'))
    cfg=em.parent/'settings.json';prefs=json.loads(cfg.read_text(encoding='utf-8-sig'))['Preferences'];save=Path(prefs['SaveDataFolder']).resolve();safe=(ROOT/'poc/runtime').resolve()
    if not prefs['OverrideSaveDataFolder'] or any(not p.is_relative_to(safe) or p==safe for p in [em,out,save]) or out.exists():raise ValueError('fresh isolated reload required')
    bios=em.parent/'Firmware/gba_bios.bin';require_hash(bios,'fd2547724b505f487e6dcb29ec2ecff3af35a841a77ab2e85fd87350abd36570')
    before=inventory(save);name=rp.with_suffix('.sav').name
    if before.get(name,{}).get('bytes')!=65536 or before[name]['sha256']==sha(bytes([255])*65536):raise ValueError('native populated save required')
    pet.ARCHIVE='6872B8';rc=pet.main();after=inventory(save)
    (out/'reload_environment.json').write_text(json.dumps(dict(observer_only=True,scope='Normal controller-only native save reload; no RAM/save import, editing or script alias.',rom_sha256=m['output_sha256'],save_directory=str(save),files_before=before,files_after=after,tool_sha256=sha(Path(__file__).read_bytes()),observer_sha256=sha(Path(pet.__file__).read_bytes()),settings_sha256=sha(cfg.read_bytes()),bios_sha256=sha(bios.read_bytes())),indent=2),encoding='utf8')
    return rc

if __name__=='__main__':raise SystemExit(main())
