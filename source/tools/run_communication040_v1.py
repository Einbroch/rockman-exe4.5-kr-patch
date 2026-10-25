"""Own040 replay of039 normal communication INPUTS; no foreign states."""
import subprocess,sys
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from typed040_loaded_guards import arguments


def main():
    rom='poc/output/pending500_040_v2.gba';m=read(rom.replace('.gba','.json'));require_hash(ROOT/rom,m['output_sha256']);audit=read('analysis/pending500_040_v2/integration.json');normal=read('analysis/pending500_040_v2/normal_recipe_receipts_v1.json');history=read('analysis/pending500_039_v1/communication_recipe_receipts_v1.json');parent='poc/runtime/pending500-040-normal-v1-16';receipts=[]
    if not audit['passed'] or not normal['passed'] or normal['rom_sha256']!=m['output_sha256'] or not history['passed']:raise ValueError('040 audited own coldboot prerequisite')
    for i,item in enumerate(history['segments'],1):
        require_hash(ROOT/item['path'],item['sha256']);old=read(item['path'])
        if not old['complete'] or old['rom_sha256']!='bfb80e29c8f72ed4595a0453ca43fa6445a94d98d6d2054158f886fde2b38430' or old.get('normal_play_checkpoint_eligible') is False:raise ValueError('040 original039 input recipe identity')
        folder='poc/runtime/pending500-040-communication-v1-'+str(i).zfill(2);cmd=[sys.executable,'-X','utf8','tools/capture_communication040_v1.py','--rom',rom,'--expect-rom-sha256',m['output_sha256'],'--mesen','poc/runtime/isolated-mesen-chip-matrix/Mesen.exe','--out',folder,'--probe','snapshot','--actions',old['actions'],'--capture-steps',','.join(map(str,old['capture_steps'])),'--state',parent+'/checkpoint.mss','--state-origin',parent+'/result.json','--timeout','300']+arguments(rom,m)
        subprocess.run(cmd,cwd=ROOT,check=True);receipts.append(dict(path=folder+'/result.json',sha256=sha((ROOT/folder/'result.json').read_bytes()),input_recipe=item));parent=folder;print('040 own communication segment',i,'complete',flush=True)
    frozen_write(ROOT/'analysis/pending500_040_v2/communication_recipe_receipts_v1.json',dict(passed=True,scope='040 controller completion only, preserved039 communication; not new040151 help pages',rom_sha256=m['output_sha256'],segments=receipts,latest_checkpoint=parent+'/checkpoint.mss',latest_origin=parent+'/result.json',old_states_used=False,source_alias_or_RAM_injection=False,release_eligible=False))


if __name__=='__main__':main()
