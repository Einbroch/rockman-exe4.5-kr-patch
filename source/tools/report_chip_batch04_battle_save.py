"""Exact311-unit battle, prompt and native persistence reconciliation."""
import json
from build_visibility_poc import ROOT,sha,require_hash
from report_chip_library_runtime import read,require
from report_fixedcell_runtime import verify_route


def main():
    stem='exe45_ko_development_chip_batch04_v1'
    rom=ROOT/f'poc/output/{stem}.gba';m=read(rom.with_suffix('.json'));build=m['output_sha256'];require_hash(rom,build)
    require_hash(ROOT/read(ROOT/'project.json')['source_profile']['filename'],m['source_sha256'])
    require_hash(ROOT/'poc/runtime/chip-survey-saves/exe45_ko_development_chip_library_v1.sav','99bb577ddf75253833ad57b711a9eb59930c35c7837e6ae8597cb570bdbdb470')
    evidence=[]
    for name in ('exe45_chip_batch04_tactics_target_v1.json','exe45_chip_batch04_tactics_distance_v1.json','exe45_chip_batch04_battle_names_normal_v1.json','exe45_chip_batch04_battle_description_v1.json','exe45_chip_batch04_battle_names_all120_v1.json'):
        p=ROOT/'analysis'/name;r=read(p)
        require(r['rom_sha256']==build and r['status'].startswith('PASS'),'battle evidence:'+name)
        evidence.append({'path':str(p.relative_to(ROOT)),'sha256':sha(p.read_bytes()),'status':r['status']})
    sav=stem+'.sav';chain=[];previous=None
    for part in ('cold-part1','cold-part2','normal-scroll','all120','names-all120','network-tutorial','battle-tutorial-complete','tactics-menu-return','normal-labels','tactics-info','battle-names-all120-r2','native-reboot'):
        p=ROOT/('poc/runtime/chip-batch04-v1-'+part);r=verify_route(p,build,set())
        require(r['complete'] and r['return_code']==0,'route:'+part)
        e=read(p/('save_environment.json' if part=='native-reboot' else 'probe_environment.json'))
        before,after=e['files_before'],e['files_after']
        current=before.get(sav);updated=after.get(sav)
        require(current==previous,'disk save continuity:'+part)
        require(all(after.get(k)==v for k,v in before.items() if k.endswith('.sav') and k!=sav),'other SAV changed:'+part)
        if part=='cold-part1':
            require(current is None and updated['sha256']=='71189f7fb6aed638640078fba3a35fda6c39c8962e74dcc75935aac948da9063','own initial SRAM file')
        elif part=='network-tutorial':
            require(current['sha256']=='71189f7fb6aed638640078fba3a35fda6c39c8962e74dcc75935aac948da9063' and updated['sha256']=='0619f62e766994fb66b231336417961a6453391393f0ba94776dbd74fb5ac59f','normal own save commit')
        else:require(current==updated,'unexpected own SAV change:'+part)
        if part=='native-reboot':require(r.get('state_origin') is None,'reboot state loaded')
        chain.append({'route':part,'result_sha256':sha((p/'result.json').read_bytes()),'before':current,'after':updated,'other_existing_sav_preserved':True})
        previous=updated
    out=ROOT/'analysis/exe45_chip_batch04_battle_save_v1.json';require(not out.exists(),'refuse overwrite')
    out.write_text(json.dumps({'status':'PASS bounded311-unit battle/prompt/native-save milestone; NON-DISTRIBUTION','rom_sha256':build,'evidence':evidence,'save_disk_chain':chain,'native_reboot_no_state':True,'limits':['Diagnostic120 battle names are not120 normally acquired chips.','Normal battle description scope is MiniBomb; other descriptions have CPU/folder evidence only.','Other Navi voices, D2B58 consumer and most dialog/graphics remain unverified/native.','New-ROM foreign-font/input lifetime/max-workload timing still pending.','Wording/presentation needs human review; no audio/hardware/full-game/release claim.']},ensure_ascii=False,indent=2),encoding='utf-8')
    print('PASS311-unit battle/prompt,120-name diagnostic and native own SAV chain')


if __name__=='__main__':main()
