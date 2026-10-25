"""Replay verified036 controller recipes, but037 coldboot and037 states only.

Each old receipt supplies input only. No runtime result is transferred to037.
"""
import subprocess,sys
from pathlib import Path
from build_visibility_poc import ROOT,sha,require_hash
from native037_loaded_guards import arguments as loaded_guards
from cumulative_batch500 import read,frozen_write


def main():
    rom='poc/output/pending500_037_v2.gba';m=read(rom.replace('.gba','.json'));require_hash(ROOT/rom,m['output_sha256'])
    audit=read('analysis/pending500_037_v2/integration.json')
    if not audit['passed'] or audit['rom_sha256']!=m['output_sha256'] or not audit['independent_rebuild_byte_identical']:raise ValueError('037 artifact audit prerequisite')
    history=read('analysis/pending500_036_v1/normal_field_progress_v2.json');parent=None;receipts=[]
    for i,item in enumerate(reversed(history['chain']),1):
        require_hash(ROOT/item['path'],item['sha256']);old=read(item['path'])
        if not old['complete'] or old['rom_sha256']!='0d85748e6c8c9b6abd561972f319b2687d6791778092c5ff1e9b15abb868876a' or old.get('normal_play_checkpoint_eligible') is False:raise ValueError('Normal historical input recipe applicability')
        folder='poc/runtime/pending500-037-normal-v1-'+str(i).zfill(2)
        cmd=[sys.executable,'-X','utf8','tools/capture_field_loader_037_v1.py','--rom',rom,'--expect-rom-sha256',m['output_sha256'],'--mesen','poc/runtime/isolated-mesen-chip-matrix/Mesen.exe','--out',folder,'--probe','snapshot','--actions',old['actions'],'--capture-steps',','.join(map(str,old['capture_steps'])),'--timeout','300']
        cmd+=loaded_guards(rom,m)
        if parent:cmd+=['--state',parent+'/checkpoint.mss','--state-origin',parent+'/result.json']
        subprocess.run(cmd,cwd=ROOT,check=True);receipts.append(dict(path=folder+'/result.json',sha256=sha((ROOT/folder/'result.json').read_bytes()),recipe=item));parent=folder
        print('037 own normal segment',i,'complete',flush=True)
    frozen_write(ROOT/'analysis/pending500_037_v2/normal_recipe_receipts_v1.json',dict(passed=True,scope='Own037 normal coldboot/controller completion only; selected new dialogues/display not inferred',rom_sha256=m['output_sha256'],segments=receipts,latest_checkpoint=parent+'/checkpoint.mss',latest_origin=parent+'/result.json',old_states_used=False,source_alias_or_RAM_injection=False,new037_native_acquisition_verified=False,new037_display_verified=False,release_eligible=False))


if __name__=='__main__':main()
