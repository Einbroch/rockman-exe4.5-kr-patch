"""Close exact500 development evidence; never create a release package."""
import re
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write


def main():
    rp=ROOT/'poc/output/pending500_023_v1.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();require_hash(rp.with_name(rp.stem+'_repro.gba'),sha(rom))
    folder=ROOT/'analysis/pending500_023_v1'
    names=['integration.json','b0_cpu.json','a3_cpu.json','integrity.json','natural_b0_runtime.json','exit_runtime.json','normal_runtime.json','visual_review.json']
    reports={n:read(folder/n) for n in names}
    for name,r in reports.items():
        if r['rom_sha256']!=sha(rom) or 'passed' in r and not r['passed']:raise ValueError('023 report baseline/pass: '+name)
    integ=reports['integration.json'];runtime=reports['natural_b0_runtime.json'];normal=reports['normal_runtime.json'];visual=reports['visual_review.json']
    if (integ['new_units']!=500 or integ['total_units']!=12622 or not integ['independent_rebuild_byte_identical']
            or not runtime['ordinary_L_caller'] or runtime['loader_scene_script_table_progress_aliases']
            or not normal['first_mail_verified'] or normal['first_mail_ordered_page_count']!=23
            or not normal['first_mail_normal_reentry_verified'] or not visual['agent_sampled_visual_review_performed']):raise ValueError('023 completion scope')
    protected=[]
    cfg=read('project.json')
    for path,h in [(cfg['source_profile']['filename'],cfg['source_profile']['sha256']),('poc/output/pending500_022_v2.gba','7363567b1263dac0700e2430da1046e47aa9ba65c8d9c2125b1ab9b3bd2928a1'),('patches/exe45_ko_development_news_mail_20261013.zip','2440478730a064cd9eb5e55bb64ddd95cab4ed76df5396ab243112d8777b7af6')]:
        require_hash(ROOT/path,h);protected.append(dict(path=path,sha256=h))
    extraction=read('analysis/field_b0_hints_v1/extraction.json');selected=set(integ['selected_ids']);remaining=[u['id'] for r in extraction['archives'] for u in r['units'] if u['id'] not in selected and re.search(r'[\u3040-\u30ff\u3400-\u9fff]',u['source'])]
    result=dict(schema=1,status='DEVELOPMENT_500_APPLIED_REBUILT_AND_NATURAL_B0_SAMPLED_NOT_RELEASE',rom=str(rp.relative_to(ROOT)),rom_sha256=sha(rom),rom_bytes=len(rom),previous_units=12122,new_units=500,total_units=12622,primary_archives=len(m['archives']),physically_unchanged_catalogued_source_archives=m['unchanged_archives'],b0_hint_clones=21,independent_rebuild_byte_identical=True,normal_B0_MegaMan_default_hint_verified=True,diagnostic_loader_scene_table_aliases=False,reports=[dict(path=str((folder/n).relative_to(ROOT)),sha256=sha((folder/n).read_bytes())) for n in names],protected_artifacts=protected,new_distribution_packages_created=False,remaining_Japanese_units_in_this_B0_table=remaining,remaining_population_scope='Only extracted21 B0 hint archives; not whole-game untranslated count.',release_eligible=False,complete_integrated_request=False,open_conditions=['Automatic Hangul composition/commit/save/redisplay unfinished; native kana entry and honorific suffix remain.','Most500 source identities share previously drafted wording; no human approval or every-page/Navi/progress-branch render claim.','Name/chip insertion display boundaries outside the sampled default hint, natural A3 progress/provider branches and real hardware/audio remain unverified.','Inherited welcome tight leading, field date HUD and other untranslated UI/graphics remain open.'])
    frozen_write(folder/'batch_status.json',result)
    print('PASS 023 development500 applied; total12622; natural B0 default, reproducible product and regression verified; NOT RELEASE')


if __name__=='__main__':main()
