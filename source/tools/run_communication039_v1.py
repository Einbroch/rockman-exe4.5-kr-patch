"""Replay038 communication INPUT recipes on own039 state; no foreign states."""
import subprocess,sys
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from communication039_loaded_guards import arguments


def main():
    rom='poc/output/pending500_039_v1.gba';m=read(rom.replace('.gba','.json'));require_hash(ROOT/rom,m['output_sha256']);normal=read('analysis/pending500_039_v1/normal_recipe_receipts_v1.json');parent='poc/runtime/pending500-039-normal-v1-16';r=read(parent+'/result.json')
    if not normal['passed'] or normal['rom_sha256']!=m['output_sha256'] or not r['complete'] or r['rom_sha256']!=m['output_sha256']:raise ValueError('039 own normal checkpoint prerequisite')
    boundary=read('analysis/pending_insertion_500_039_communication_words_v1/baseline_boundary_v2.json');refs={x['path'].replace('\\','/'):x['sha256'] for x in boundary['normal_coldboot_ancestry']};refs.update({p.replace('\\','/'):h for p,h in boundary['receipts'].items()});receipts=[]
    for i in range(1,9):
        oldpath='poc/runtime/pending500-038-communication-observe-v'+str(i)+'/result.json';require_hash(ROOT/oldpath,refs[oldpath]);old=read(oldpath)
        if not old['complete'] or old['rom_sha256']!=boundary['baseline_sha256'] or old.get('normal_play_checkpoint_eligible') is False:raise ValueError('Communication input recipe applicability')
        folder='poc/runtime/pending500-039-communication-v1-'+str(i).zfill(2);cmd=[sys.executable,'-X','utf8','tools/capture_communication039_v1.py','--rom',rom,'--expect-rom-sha256',m['output_sha256'],'--mesen','poc/runtime/isolated-mesen-chip-matrix/Mesen.exe','--out',folder,'--probe','snapshot','--actions',old['actions'],'--capture-steps',','.join(map(str,old['capture_steps'])),'--state',parent+'/checkpoint.mss','--state-origin',parent+'/result.json','--timeout','300']+arguments(rom,m)
        subprocess.run(cmd,cwd=ROOT,check=True);receipts.append(dict(path=folder+'/result.json',sha256=sha((ROOT/folder/'result.json').read_bytes()),input_recipe=dict(path=oldpath,sha256=refs[oldpath])));parent=folder;print('039 own communication segment',i,'complete',flush=True)
    frozen_write(ROOT/'analysis/pending500_039_v1/communication_recipe_receipts_v1.json',dict(passed=True,scope='039 same-ROM controller completion only; traces/screens still need verification',rom_sha256=m['output_sha256'],segments=receipts,latest_checkpoint=parent+'/checkpoint.mss',latest_origin=parent+'/result.json',old_states_used=False,source_alias_or_RAM_injection=False,multiplayer_outcome_tested=False,release_eligible=False))


if __name__=='__main__':main()
