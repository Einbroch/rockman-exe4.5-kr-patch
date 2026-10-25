"""Close one development batch's evidence, never package or approve a release."""
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write

def main():
    folder=ROOT/'analysis/pending500_022_v2';rp=ROOT/'poc/output/pending500_022_v2.gba';m=read(rp.with_suffix('.json'));h='7363567b1263dac0700e2430da1046e47aa9ba65c8d9c2125b1ab9b3bd2928a1';require_hash(rp,h)
    if m['output_sha256']!=h or m['translated_units']!=12122 or len(m['archives'])!=405 or m['unchanged_archives']!=327 or not m['final_diff_audited']:raise ValueError('022 product denominator/final audit')
    repro=rp.with_name(rp.stem+'_repro.gba');require_hash(repro,h)
    if rp.read_bytes()!=repro.read_bytes():raise ValueError('022 independent byte identity')
    names=['delta.json','integration.json','hint_cpu.json','selector_cpu.json','hint_integrity.json','hint_dispatch.json','display_runtime.json','normal_runtime.json','visual_review.json','protected_artifacts.json']
    reports={name:read(folder/name) for name in names}
    for name,r in reports.items():
        if name!='protected_artifacts.json' and r['rom_sha256']!=h:raise ValueError('022 report binding '+name)
        if 'passed' in r and r['passed'] is not True:raise ValueError('022 failed report '+name)
    if reports['integration.json']['new_units']!=500 or reports['integration.json']['total_units']!=12122 or not reports['integration.json']['artifact_audit']['reproducible_byte_identical']:raise ValueError('022 cumulative/independent audit')
    if reports['hint_cpu.json']['vectors']!=5652 or reports['selector_cpu.json']['vectors']!=3195 or reports['hint_integrity.json']['rejected_fixture_count']!=11:raise ValueError('022 CPU/negative denominator')
    if not reports['hint_dispatch.json']['original_entry_script0_byte_identical'] or not reports['hint_dispatch.json']['original_script10_byte_identical'] or reports['hint_dispatch.json']['script_table_read_changed'] is not False or reports['hint_dispatch.json']['additional_translated_units']!=0:raise ValueError('022 original dispatch evidence scope')
    display=reports['display_runtime.json'];normal=reports['normal_runtime.json'];visual=reports['visual_review.json']
    if len(display['pages'])!=9 or not display['ordinary_native_hint_fallback_verified'] or display['natural_selected_hint_event_verified'] is not False:raise ValueError('022 display evidence scope')
    if not normal['first_mail_verified'] or normal['first_mail_ordered_page_count']!=23 or not normal['first_mail_normal_reentry_verified']:raise ValueError('022 normal mail regression')
    if visual['representative_fullbox_pages_reviewed']!=9 or visual['first_mail_pages_visually_reviewed']!=23 or visual['startup_visual_review_complete_and_approved'] is not False:raise ValueError('022 visual review scope')
    for r in reports['protected_artifacts.json']['unchanged']:require_hash(ROOT/r['path'],r['sha256'])
    frozen_write(folder/'batch_status.json',dict(schema=1,status='DEVELOPMENT_500_APPLIED_AND_SAMPLED_NOT_RELEASE',rom=str(rp.relative_to(ROOT)),rom_sha256=h,rom_bytes=m['output_bytes'],previous_units=11622,new_units=500,total_units=12122,raw_new_units=136,guarded_hint_new_units=364,primary_archives=405,physically_unchanged_source_archives=327,independent_rebuild_byte_identical=True,normal_boot_keyboard_cards_first_mail_regression=True,diagnostic_display_pages=9,diagnostic_unique_source_review_units=7,hint_wrapper_timing=display['hint_wrapper_timing'],reports=[dict(path=str((folder/name).relative_to(ROOT)),sha256=sha((folder/name).read_bytes())) for name in names],source_only500_preflight_sha256='100afd17b0af757137ceed31305559ccadbd3ba8f4143de05e81a4c0822b8ba8',new_distribution_packages_created=False,release_eligible=False,complete_integrated_request=False,open_conditions=['Automatic Hangul composition/commit/save/redisplay is unfinished; native kana keyboard/suffix remain.','Inherited PET welcome graphic tight leading remains open, with unchanged text pixels versus021.','Diagnostic loader/scene/table aliases are not natural A3 event/provider/branch/acquisition proof. Other Navi, real device/audio targets, all500 visual/semantic review and whole-game untranslated inventory remain open.']))
    print('PASS development batch022: exact500 applied; cumulative12122; independent build and sampled QA closed. NOT RELEASE.')

if __name__=='__main__':main()
