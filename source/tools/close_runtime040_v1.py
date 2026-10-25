"""Close bounded040 QA, not distribution or full-game completion."""
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write


def main():
    rom=ROOT/'poc/output/pending500_040_v2.gba';m=read(rom.with_suffix('.json'));require_hash(rom,m['output_sha256'])
    repro=ROOT/'poc/output/pending500_040_v2_repro.gba'
    if rom.read_bytes()!=repro.read_bytes():raise ValueError('independent reproduction differs')
    cfg=read('project.json');require_hash(ROOT/cfg['source_profile']['filename'],cfg['source_profile']['sha256'])
    names=['integration','corruption_v1','normal_path_v1','communication_runtime_v1','new_communication_runtime_v1','tournament_runtime_v1','bbs_runtime_v1']
    reports={};checked=0
    def refs(value):
        nonlocal checked
        if isinstance(value,dict):
            if isinstance(value.get('path'),str) and 'sha256' in value:
                require_hash(ROOT/value['path'],value['sha256']);checked+=1
            for x in value.values():refs(x)
        elif isinstance(value,list):
            for x in value:refs(x)
    for name in names:
        p=ROOT/'analysis/pending500_040_v2'/(name+'.json');r=read(p)
        if not r['passed'] or r['rom_sha256']!=m['output_sha256']:raise ValueError('040 report baseline '+name)
        for path,h in r.get('dependencies',{}).items():require_hash(ROOT/path,h);checked+=1
        refs(r);reports[name]=dict(path=str(p.relative_to(ROOT)),sha256=sha(p.read_bytes()))
    groups={'pending500-040-bbs-v2':[14,16,17,18,19,20,21,22,23,24,25,26], 'pending500-039-bbs-terminal040-v1':[24,25,27], 'pending500-040-tournament-v1':[11,12,13,14,17], 'pending500-040-new-communication-v1':[3,4,5], 'pending500-040-normal-v1-16':[1,2,3,4], 'pending500-040-bbs-v1':[27]}
    images=[]
    for folder,steps in groups.items():
        d=ROOT/'poc/runtime'/folder;r=read(d/'result.json')
        for step in steps:
            name=f'step_{step:03}.png';require_hash(d/name,r['artifacts'][name]);images.append(dict(path=str((d/name).relative_to(ROOT)),sha256=r['artifacts'][name]))
    result=dict(passed=True,date='2026-10-23',rom_sha256=m['output_sha256'],rom_bytes=rom.stat().st_size,independent_reproduction_byte_identical=True,reports=reports,verified_evidence_references=checked,agent_visual_review=dict(images=images,observed='Korean body glyphs readable in sampled pages; page transitions clear; BBS final confirmation auto-closes to Japanese list and reopens correctly; normal dialogue closes and player moves; communication cancels to PET.',human_approval=False,remaining_visible_Japanese='BBS title, post headings/list, tournament banner, small communication labels, region label remain Japanese.'),new_applied_IDs=500,cumulative_IDs=21122,canonical_unapplied_draft_IDs=9424,all500_screens_observed=False,own040_normal_coldboot_verified=True,three_changed_consumers_qualified_runtime_verified=True,natural_acquisition_of_qualified_content_verified=False,release_eligible=False,distribution_packages_created=0,ROM_modified_during_this_QA=False,checker_corrections=['Normal v1 accidentally substituted a numeric RAM address; v2 restored original39800.','Typed v1 expected script16 at step4; actual script16 is step3 and script15 step4.','BBS v1 expected visible terminal hold and wrong reentry29; original caller automatically closes at25, reentry26 verified in new run.','Typed v2 incorrectly required BBS shared-RAM residency after field exit; v3 requires it during BBS lifetime and compares field-reused RAM exactly with039 original-Japanese consumer control.'],limits=['Runtime sample: tournament4 + new communication2 + BBS10 distinct pages/reentry, not all500 screens.','Qualified registration/environment/Navi reads do not prove natural acquisition, outcomes or multiplayer.','Hangul commit/save/redisplay, remaining Japanese graphics/menu/keyboard/regions, full-game, human review, hardware/audio remain incomplete.'],dependencies={'tools/close_runtime040_v1.py':sha((ROOT/'tools/close_runtime040_v1.py').read_bytes())})
    frozen_write(ROOT/'analysis/pending500_040_v2/runtime_closure_v1.json',result)
    print('PASS040 bounded QA closure; references',checked,'visual images',len(images),'no ROM writes/packages')


if __name__=='__main__':main()
