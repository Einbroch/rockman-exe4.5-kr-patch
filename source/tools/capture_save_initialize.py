"""Isolated QA save fixture; observe title/No only, never execute Yes/erase."""
import argparse,json,subprocess,sys
from pathlib import Path
from build_visibility_poc import ROOT,require_hash,sha
from capture_save_qa import inventory

ROM='poc/output/exe45_ko_development_save_initialize_v1.gba'
ROM_SHA='906f374acaabe9a37c70fddcae364f07c55545ae1d81b57953d727bb881415be'
MESEN='poc/runtime/isolated-mesen-chip-matrix/Mesen.exe'
MESEN_SHA='af60a18859e3253f09c8fd32f6b1c04637efbd98780f1427dd94d4629474f640'
FIXTURE_DIR='poc/runtime/input-entry-v1-cold-continue'
FIXTURE_NAME='exe45_ko_development_input_confirmation_v1.sav'
FIXTURE_SHA='ebe5584813e1bfca96dbaf5231257153d8f14ab8b62a419ce60bc6506ee2103a'

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--phase',choices=['title','prompt','cancel'],required=True);a=ap.parse_args()
    rp=ROOT/ROM;em=ROOT/MESEN;require_hash(rp,ROM_SHA);require_hash(em,MESEN_SHA)
    prefs=json.loads((em.parent/'settings.json').read_text(encoding='utf-8-sig'))['Preferences'];save=Path(prefs['SaveDataFolder']).resolve()
    safe=(ROOT/'poc/runtime').resolve()
    if not prefs['OverrideSaveDataFolder'] or not save.is_relative_to(safe) or save==safe:raise ValueError('isolated QA save folder required')
    dst=save/(rp.stem+'.sav');out=ROOT/f'poc/runtime/save-initialize-v1-{a.phase}'
    if out.exists():raise ValueError('preserve prior route')
    seedpath=ROOT/'analysis/save_initialize_v1/runtime_seed.json'
    if a.phase=='title':
        if seedpath.exists() or dst.exists() or dst.with_suffix('.rtc').exists():raise ValueError('fresh QA stem only')
        fixture=ROOT/FIXTURE_DIR;env=json.loads((fixture/'save_environment.json').read_text(encoding='utf8'));meta=env['files_after'][FIXTURE_NAME]
        if env['build_sha256']!='68260ec96c118939efa66f24f077dd06d375bdebffb8246529bcdfd6c45e87a6' or meta['bytes']!=65536 or meta['sha256']!=FIXTURE_SHA:raise ValueError('native fixture baseline')
        source=fixture/'persistent_files_after'/FIXTURE_NAME;require_hash(source,meta['sha256']);data=source.read_bytes()
        with dst.open('xb') as f:f.write(data)
        seed=dict(rom_sha256=ROM_SHA,fixture_path=str(source),fixture_sha256=meta['sha256'],fixture_origin_rom_sha256=env['build_sha256'],source_receipt_sha256=sha((fixture/'save_environment.json').read_bytes()),qa_destination=str(dst),seeded_before_cold_boot=True,old_ROM_savestate_used=False,limits=['Copied native QA SAV under fresh ROM basename only; user saves and original fixture unchanged.', 'This fixture import is explicit. No RAM intervention or save-format migration; game loading is verified separately.'])
        seedpath.write_text(json.dumps(seed,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        actions='none:1:900,start:2:120,none:1:120';state=[]
    else:
        seed=json.loads(seedpath.read_text(encoding='utf8'));require_hash(dst,seed['fixture_sha256'])
        previous=ROOT/('poc/runtime/save-initialize-v1-title' if a.phase=='prompt' else 'poc/runtime/save-initialize-v1-prompt')
        state=['--state',str(previous/'checkpoint.mss'),'--state-origin',str(previous/'result.json')]
        actions='none:1:7,up:2:15,none:1:7,a:2:120,none:1:120' if a.phase=='prompt' else 'none:1:7,b:2:120,none:1:120'
    before=inventory(save);prior=dst.read_bytes()
    rc=subprocess.call([sys.executable,'-X','utf8',str(ROOT/'tools/run_mesen_segment.py'),'--rom',str(rp),'--expect-rom-sha256',ROM_SHA,'--mesen',str(em),'--out',str(out),'--actions',actions,'--probe','snapshot','--timeout','45',*state],cwd=ROOT)
    after=inventory(save);changed=[name for name in before.keys()|after.keys() if before.get(name)!=after.get(name)]
    (out/'qa_save_before.sav').write_bytes(prior)
    result=dict(rom_sha256=ROM_SHA,seed_receipt_sha256=sha(seedpath.read_bytes()),fixture_import_before_coldboot=True,RAM_injection=False,files_before=before,files_after=after,changed_files=changed,qa_sav_before_sha256=sha(prior),qa_sav_after_sha256=sha(dst.read_bytes()),qa_sav_unchanged=prior==dst.read_bytes(),tool_sha256=sha(Path(__file__).read_bytes()),limits=['Read-only snapshot observation from a declared imported QA native save. Only title/new-game prompt/B cancel inputs; no Yes navigation or erase confirmation.'])
    (out/'qa_environment.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    if any(n not in (rp.stem+'.rtc',) for n in changed) or prior!=dst.read_bytes():raise ValueError('unexpected persistent change')
    return rc

if __name__=='__main__':raise SystemExit(main())
