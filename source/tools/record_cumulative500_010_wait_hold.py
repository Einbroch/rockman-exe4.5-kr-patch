"""Retain a rejected display probe without mutating the applicable ROM."""
import json,struct
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
def main():
    rp=ROOT/'poc/output/exe45_ko_development_pending500_010_v1.gba';meta=read(str(rp.with_suffix('.json').relative_to(ROOT)));require_hash(rp,meta['output_sha256']);rom=rp.read_bytes()
    folder=ROOT/'poc/runtime/pending500-010-v1-display-new-loss';receipt=json.loads((folder/'result.json').read_text(encoding='utf8'))
    if receipt['rom_sha256']!=sha(rom) or receipt.get('normal_play_checkpoint_eligible') is not False:raise ValueError('Probe artifact identity')
    observations=[]
    for step in (1,2,3):
        ptr,root=struct.unpack_from('<2I',(folder/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes(),0xFA4C)
        observations.append(dict(step=step,current_pointer=ptr,current_root=root,screenshot_sha256=sha((folder/f'step_{step:03}.png').read_bytes())))
    asset=read('analysis/pending_insertion_500_010_cumulative_v1/6989B0_selected_asset.json')
    require_hash(ROOT/asset['source_tpl']['path'],asset['source_tpl']['sha256'])
    tpl=(ROOT/asset['source_tpl']['path']).read_text(encoding='utf-8-sig');section=tpl.split('script 2 ')[1].split('script ')[0]
    if 'keyWait' in section or 'waitHold' not in section:raise ValueError('Declared source wait contract')
    target=next(r for r in meta['archives'] if r['archive']=='6989B0')
    if any(x['current_root']==0x08000000+target['rom_offset'] for x in observations[1:]):raise ValueError('Probe observation changed')
    out=ROOT/'analysis/pending500_010_v1/wait_hold_probe_unverified.json'
    if out.exists():raise ValueError('Preserve evidence')
    frozen_write(out,dict(rom_sha256=sha(rom),archive='6989B0',script=2,source_has_keywait=False,source_has_waithold=True,lookup_alias_receipt=receipt['alert_diagnostic'],observations=observations,display_verification_passed=False,product_defect_established=False,rom_changed_for_probe=False,normal_battle_outcome_or_save_verified=False,next_requirement='Observe with verified native battle-outcome caller and waitHold context; PET diagnostic snapshots returned to default menu and cannot prove stable loss display.'))
    print('Recorded unverified waitHold display probe; applicable ROM unchanged')
if __name__=='__main__':main()
