"""039 own coldboot and controller recipes only; never load a038 checkpoint."""
import subprocess,sys
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from communication039_loaded_guards import arguments


def main():
    rom='poc/output/pending500_039_v1.gba';m=read(rom.replace('.gba','.json'));require_hash(ROOT/rom,m['output_sha256']);audit=read('analysis/pending500_039_v1/integration.json')
    if not audit['passed'] or audit['rom_sha256']!=m['output_sha256'] or not audit['independent_rebuild_byte_identical']:raise ValueError('039 actual artifact audit prerequisite')
    history=read('analysis/pending500_038_v2/normal_recipe_receipts_v1.json');parent=None;receipts=[]
    for i,item in enumerate(history['segments'],1):
        require_hash(ROOT/item['path'],item['sha256']);old=read(item['path'])
        if not old['complete'] or old['rom_sha256']!='97759be6f1dca078fe4d0ee52acaf9e342decfb2eeafcbcd9046bbfb145d8e5b' or old.get('normal_play_checkpoint_eligible') is False:raise ValueError('038 input recipe applicability')
        folder='poc/runtime/pending500-039-normal-v1-'+str(i).zfill(2)
        cmd=[sys.executable,'-X','utf8','tools/capture_field_loader_038_v1.py','--rom',rom,'--expect-rom-sha256',m['output_sha256'],'--mesen','poc/runtime/isolated-mesen-chip-matrix/Mesen.exe','--out',folder,'--probe','snapshot','--actions',old['actions'],'--capture-steps',','.join(map(str,old['capture_steps'])),'--timeout','300']+arguments(rom,m)
        if parent:cmd+=['--state',parent+'/checkpoint.mss','--state-origin',parent+'/result.json']
        subprocess.run(cmd,cwd=ROOT,check=True);receipts.append(dict(path=folder+'/result.json',sha256=sha((ROOT/folder/'result.json').read_bytes()),recipe=item));parent=folder
        print('039 own normal segment',i,'complete',flush=True)
    frozen_write(ROOT/'analysis/pending500_039_v1/normal_recipe_receipts_v1.json',dict(passed=True,scope='Own039 normal coldboot/controller completion only; no new communication display inferred',rom_sha256=m['output_sha256'],segments=receipts,latest_checkpoint=parent+'/checkpoint.mss',latest_origin=parent+'/result.json',old_states_used=False,source_alias_or_RAM_injection=False,new039_communication_display_verified=False,release_eligible=False))


if __name__=='__main__':main()
