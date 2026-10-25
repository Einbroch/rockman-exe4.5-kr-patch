"""041 own coldboot: replay the040 normal controller recipes on the exact041 ROM; never load040 states."""
import subprocess,sys
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from typed041_loaded_guards import arguments


def main():
    rom='poc/output/pending500_041_v1.gba';m=read(rom.replace('.gba','.json'));require_hash(ROOT/rom,m['output_sha256'])
    history=read('analysis/pending500_040_v2/normal_recipe_receipts_v1.json');parent=None;receipts=[]
    for i,item in enumerate(history['segments'],1):
        require_hash(ROOT/item['path'],item['sha256']);old=read(item['path'])
        folder='poc/runtime/pending500-041-normal-v1-'+str(i).zfill(2)
        cmd=[sys.executable,'-X','utf8','tools/capture_field_loader_038_v1.py','--rom',rom,'--expect-rom-sha256',m['output_sha256'],'--mesen','poc/runtime/isolated-mesen-chip-matrix/Mesen.exe','--out',folder,'--probe','snapshot','--actions',old['actions'],'--capture-steps',','.join(map(str,old['capture_steps'])),'--timeout','300']+arguments(rom,m)
        if parent:cmd+=['--state',parent+'/checkpoint.mss','--state-origin',parent+'/result.json']
        subprocess.run(cmd,cwd=ROOT,check=True);receipts.append(dict(path=folder+'/result.json',sha256=sha((ROOT/folder/'result.json').read_bytes()),recipe=item['path']));parent=folder
        print('041 own normal segment',i,'complete',flush=True)
    frozen_write(ROOT/'analysis/pending500_041_v1/normal_recipe_receipts_v1.json',dict(passed=True,scope='Own041 coldboot/controller replay of040 recipes; no040 states, no RAM injection',rom_sha256=m['output_sha256'],segments=receipts,latest_checkpoint=parent+'/checkpoint.mss',latest_origin=parent+'/result.json',old_states_used=False,release_eligible=False))


if __name__=='__main__':main()
