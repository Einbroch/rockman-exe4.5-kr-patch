"""Native input-answer persistence observation, preserving this QA ROM's prior save."""
import json,sys
from pathlib import Path
import capture_roll_save as base
from build_visibility_poc import ROOT,sha,require_hash

def main():
    def arg(k):return sys.argv[sys.argv.index(k)+1]
    rp=Path(arg('--rom')).resolve();require_hash(rp,arg('--expect-rom-sha256'))
    em=Path(arg('--mesen')).resolve();out=Path(arg('--out')).resolve()
    prefs=json.loads((em.parent/'settings.json').read_text(encoding='utf-8-sig'))['Preferences'];save=Path(prefs['SaveDataFolder']).resolve();safe=(ROOT/'poc/runtime').resolve()
    if out.exists() or not prefs['OverrideSaveDataFolder'] or any(not p.is_relative_to(safe) or p==safe for p in [out,em,save]):raise ValueError('own isolated persistence observation only')
    originals={rp.stem+ext:(save/(rp.stem+ext)).read_bytes() for ext in ['.sav','.rtc'] if (save/(rp.stem+ext)).exists()}
    rc=base.main();backup=out/'persistent_files_before';backup.mkdir()
    for name,data in originals.items():(backup/name).write_bytes(data)
    (out/'input_save_environment.json').write_text(json.dumps(dict(observer_only=True,no_RAM_or_save_injection=True,rom_sha256=sha(rp.read_bytes()),self_sha256=sha(Path(__file__).read_bytes()),originals_preserved={name:dict(bytes=len(data),sha256=sha(data)) for name,data in originals.items()},limits=['Only this QA ROM stem prior persistent files retained; game alone writes native save.','Does not prove Hangul input or all field/consumer persistence.']),indent=2),encoding='utf8')
    return rc
if __name__=='__main__':raise SystemExit(main())
