"""Bind035 scoped milestones without promoting diagnostics to native A0 proof."""
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write

def main():
    rp=ROOT/'poc/output/pending500_035_v1.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);require_hash(ROOT/'poc/output/pending500_035_v1_repro.gba',m['output_sha256'])
    names=['integration','npc_cpu','integrity','normal_runtime','npc_displays'];refs={}
    for name in names:
        p='analysis/pending500_035_v1/'+name+'.json';r=read(p)
        if not r['passed'] or r['rom_sha256']!=m['output_sha256']:raise ValueError('035 evidence applicability '+name)
        refs[name]=dict(path=p,sha256=sha((ROOT/p).read_bytes()))
    normal=read(refs['normal_runtime']['path']);display=read(refs['npc_displays']['path']);visual=read('analysis/pending500_035_v1/visual_inputs_v2.json')
    if not normal['native_keyboard_labels_verified'] or normal['first_mail_ordered_page_count']!=23 or not normal['first_mail_normal_reentry_verified'] or len(display['pages'])!=10 or len(display['new_rendered_ids'])!=10:raise ValueError('035 runtime denominator')
    sheets=visual['sheets']+[dict(kind='NPC-displays',screens=10,**display['contact_sheet'])]
    for s in sheets:require_hash(ROOT/s['path'],s['sha256'])
    review=dict(schema=1,rom_sha256=m['output_sha256'],reviewer='Codex agent direct image observation',human_presentation_approval=False,sheets=sheets,screens_directly_viewed=55,
        observations=['Ten new NPC clone pages fit within their windows; native portraits change in the source order. No apparent clipping/overlap in these ten samples.',
                      'Startup date/profile/card selection and first-mail pages remain displayed. Source Japanese user nickname is still present.',
                      'Known welcome graphic line overlap remains. Kana keyboard pages and title logo remain Japanese. No claim that automatic Hangul entry/save is complete.'],
        limitation='Agent visual observations of these exact screenshots only; not human semantic/presentation approval, whole500 review or natural A0 selection proof.',release_eligible=False)
    vp='analysis/pending500_035_v1/agent_visual_review_v1.json';frozen_write(ROOT/vp,review);refs['agent_visual_review']=dict(path=vp,sha256=sha((ROOT/vp).read_bytes()))
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256'])
    frozen_write(ROOT/'analysis/pending500_035_v1/batch_status.json',dict(schema=1,
        status='ROM_APPLIED_STATIC_REPRO_NORMAL_AND_DIAGNOSTIC_DISPLAY_PASS_NATIVE_A0_LINK_PENDING',
        rom_path=str(rp.relative_to(ROOT)),rom_sha256=m['output_sha256'],rom_bytes=m['output_bytes'],source_sha256=cfg['source_profile']['sha256'],
        new_units=500,total_units=m['translated_units'],new_npc_archives=9,new_scripts=160,new_prose_or_label_ids=462,timed_punctuation_ids=38,
        independent_rebuild_byte_identical=True,prior034_bytes_preserved_except_one_composed_reader_stub=True,
        original_npc_compressed_sources_references_and_RAM_extents_retained=True,primary_build_completed=True,rom_written=True,
        actual_product_npc_CPU_vectors=read(refs['npc_cpu']['path'])['vectors'],fresh_corruption_refusals=read(refs['integrity']['path'])['rejected_fixture_count'],
        normal_boot_keyboard_cards_first_mail_runtime_verified=True,new_NPC_clone_diagnostic_display_pages=10,new_NPC_clone_diagnostic_rendered_ids=display['new_rendered_ids'],screens_directly_viewed=55,
        native_A0_NPC_selector_GBA_runtime_verified=False,natural_weekday_NPC_acquisition_verified=False,automatic_Hangul_commit_save_redisplay_verified=False,
        reports=refs,distribution_packages_created=False,release_eligible=False,
        next_required='Keep this035 artifact fixed. Establish original compressed loading -> nativeA0 cached NPC caller0804F76E -> new loaded-payload selector -> actual new clone/glyph/wait and exit/reentry/timing. Existing PET read-alias samples do not prove that link. Do not count another500 or start036 before deciding this current runtime boundary.',
        limits='Development NON-DISTRIBUTION only. New500 integrated, not complete Korean localization or release approval. Known welcome graphic overlap, kana/logo and other Japanese content, Hangul composition/commit/save/redisplay and full human review remain unfinished.'))
    print('035 scoped ROM/static/repro/normal/ten-page diagnostic status recorded; nativeA0 link remains OPEN')

if __name__=='__main__':main()
