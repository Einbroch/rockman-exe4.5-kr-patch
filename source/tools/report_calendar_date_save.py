"""Exact cumulative ROM audit relative to retained input38 candidate."""
from report_input_remaining import main as audit
from calendar_date_save import GENERATED,validate,SCRIPTS
import json
from pathlib import Path
from build_visibility_poc import ROOT,require_hash,sha
from report_fixedcell_runtime import verify_route

def main():
    result=audit(stem='exe45_ko_development_calendar_date_save_v1_r2',previous='exe45_ko_development_input_remaining_v1',generated=GENERATED,validator=validate,scripts=SCRIPTS,added=17,outdir='analysis/calendar_date_save_v1',extra_tools=('calendar_date_save.py','report_calendar_date_save.py'),limits=[
        'Static ROM ledger/header/append/roots/roundtrip audit. Other59 archives and249 unselected common scripts retained, including prior common38 literals.',
        'Normal/big/mono fonts and advances, graphics, keyitem39 retained. No Hangul keyboard/storage hook installed.',
        'Date/save17 are NON-DISTRIBUTION development drafts. Actual callers/custom window76/choices/currency/VRAM/screens and save/freshload/human review remain pending. No date change or save initialization performed.'
    ])
    path=ROOT/'poc/output/exe45_ko_development_calendar_date_save_v1_r2.gba'
    repro=ROOT/'poc/output/exe45_ko_development_calendar_date_save_v1_r2_repro.gba'
    require_hash(repro,result['rom_sha256'])
    if path.read_bytes()!=repro.read_bytes():raise ValueError('independent rebuild bytes')
    route=ROOT/'poc/runtime/calendar-date-save-v1-coldboot'
    receipt=verify_route(route,result['rom_sha256'],set())
    require_hash(Path(receipt['emulator_path']),receipt['emulator_sha256'])
    inventory=ROOT/'analysis/full_scope_calendar_date_save_v1/inventory.json'
    summary=json.loads(inventory.read_text(encoding='utf8'))['summary']
    if summary['baseline_rom_sha256']!=result['rom_sha256'] or summary['parse_errors'] or summary['selected_catalog_literal_units']!=result['translated_units']:raise ValueError('catalog identity')
    evidence=dict(rom_sha256=result['rom_sha256'],rom_bytes=path.stat().st_size,independent_rebuild_byte_identical=True,boot_route_sha256=sha((route/'result.json').read_bytes()),boot_route_complete=receipt['complete'],boot_captures=receipt['steps_captured'],emulator_sha256=receipt['emulator_sha256'],inventory_sha256=sha(inventory.read_bytes()),counts=summary['counts'],new17_runtime_verified=False,save_regression_verified=False,release_eligible=False,limits=['Read-only snapshots and normal input from cold boot. Title screenshot inspected separately; this is not new17 screen/consumer evidence.', 'No date change, save initialization, RAM/script injection, old-ROM checkpoint or user-save write. Existing baseline retained.'])
    (ROOT/'analysis/calendar_date_save_v1/rebuild_boot_catalog.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('PASS independent full-byte rebuild, boot receipt and catalog identity; NOT new17 runtime')
    return result

if __name__=='__main__':main()
