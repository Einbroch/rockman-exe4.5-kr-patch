"""Record scoped036 milestones without promoting read aliases to native proof."""
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write

def main():
    rp=ROOT/'poc/output/pending500_036_v1.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);require_hash(ROOT/'poc/output/pending500_036_v1_repro.gba',m['output_sha256']);refs={}
    for name,file in [('integration','integration.json'),('startup','startup_runtime_v1.json'),('display','display_runtime_v1.json')]:
        path='analysis/pending500_036_v1/'+file;r=read(path)
        if not r['passed'] or r['rom_sha256']!=m['output_sha256']:raise ValueError('036 report applicability')
        refs[name]=dict(path=path,sha256=sha((ROOT/path).read_bytes()))
    sheets=[read(refs['startup']['path'])['contact_sheet'],dict(path='analysis/pending500_036_v1/diagnostic_contact_v1.png',screens=15)]
    for s in sheets:
        h=sha((ROOT/s['path']).read_bytes())
        if s.get('sha256',h)!=h:raise ValueError('036 screenshot sheet changed')
        s['sha256']=h
    visual='analysis/pending500_036_v1/agent_visual_review_v1.json'
    frozen_write(ROOT/visual,dict(rom_sha256=m['output_sha256'],reviewer='Codex agent directly viewed both exact-ROM contact sheets',screens_directly_viewed=34,sheets=sheets,human_presentation_approval=False,release_eligible=False,observations=['12 new NPC literal IDs in12 page-or-option displays fit their dialogue windows; no apparent clipping/residue in the samples. Pink/yellow/black native portraits match the selected source scripts.','Horizontal default/right cursor, B-cancel decline pages, ordinary PET return visible in three separate diagnostic cases.','Initial date/profile controls translated; three keyboard banks remain kana/Latin, not completed Hangul input. Previously known welcome graphic line overlap and Japanese title logo remain.'],limits='Agent observations of these34 screenshots, not human semantic approval/all500/native scene acquisition/battle outcomes or saves.'))
    refs['agent_visual_review']=dict(path=visual,sha256=sha((ROOT/visual).read_bytes()))
    frozen_write(ROOT/'analysis/pending500_036_v1/batch_status.json',dict(schema=1,status='ROM_APPLIED_STATIC_REPRO_STARTUP_AND_DIAGNOSTIC_DISPLAY_PASS_NATURAL036_LINK_PENDING',rom_path=str(rp.relative_to(ROOT)),rom_sha256=m['output_sha256'],rom_bytes=m['output_bytes'],new_units=500,total_units=m['translated_units'],new_scripts=162,new_NPC_archives=20,new_prose_or_label_ids=463,punctuation_only_ids=37,independent_rebuild_byte_identical=True,source_original_and_previous_ROMs_preserved=True,primary_build_completed=True,actual_CPU_fixture_whole_ROM_identical=True,CPU_vectors=8423,counter_boundary_CPU_vectors=3584,old_consumers_preserved=488,new_rendered_diagnostic_ids=read(refs['display']['path'])['new_rendered_ids'],diagnostic_complete_page_or_option_displays=12,screens_directly_viewed=34,normal_boot_keyboard_residency_verified=True,native036_scene_acquisition_and_selector_GBA_runtime_verified=False,automatic_Hangul_commit_save_redisplay_verified=False,distribution_packages_created=False,release_eligible=False,reports=refs,canonical_draft_ROM_unapplied_ids=11424,remaining_count_scope='11924 canonical draft IDs before036 minus this exact500; NOT whole-game/image remainder or full completion percentage',next_required='Keep exact036 fixed. Own Sunday09am normal controller route is in progress to observe source79CF04 load and NPC actor/caller ->036 scene/native identity selector -> clone -> glyph -> pages/exit/reentry/timing. No035 saved states and no diagnostic checkpoints may be used as normal evidence.',remains=['Natural036 A0/A1/A3 acquisition/selector/runtime timing and other changed paths','Full human translation/graphics/gameplay review; Japanese keyboard/logo/other content and welcome graphics overlap','Automatic Hangul composition/commit/save/redisplay integration']))
    print('Recorded036 applied500 total19122, exact-ROM scoped static/startup/diagnostic evidence; native036 link pending')

if __name__=='__main__':main()
