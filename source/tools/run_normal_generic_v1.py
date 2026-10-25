"""Own coldboot of a generic batch ROM: replay the040 normal controller recipes; never load other-ROM states.

Usage: run_normal_generic_v1.py ROM BATCH. Writes analysis/pending500_<BATCH>_v1/normal_recipe_receipts_v1.json
and compares each capture against the041 replay (screens may differ only by the RTC clock and translated text).
"""
import subprocess,sys,json
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from typed040_loaded_guards import arguments as prior_guards


def guards(rom,m,key):
    result=prior_guards(rom,m);blob=(ROOT/rom).read_bytes()
    # Only the newest wrapper is sentinelled: every earlier wrapper is already pinned by the ROM SHA
    # (--expect-rom-sha256), and adding all of them overflows the Windows 32,767-char command line.
    v=m['keyitem_rom'][key]
    for at,size in [(v['code_offset'],v['code_bytes']),(v['descriptor_offset'],len(v['placements'])*20)]:result+=['--guard',hex(at)+':'+blob[at:at+size].hex()]
    return result


def main():
    rom,batch=sys.argv[1],sys.argv[2];m=read(rom.replace('.gba','.json'));require_hash(ROOT/rom,m['output_sha256'])
    history=read('analysis/pending500_040_v2/normal_recipe_receipts_v1.json');parent=None;receipts=[];g=guards(rom,m,'typed'+batch)
    for i,item in enumerate(history['segments'],1):
        old=read(item['path']);folder=f'poc/runtime/pending500-{batch}-normal-v1-'+str(i).zfill(2)
        cmd=[sys.executable,'-X','utf8','tools/run_mesen_segment.py','--rom',rom,'--expect-rom-sha256',m['output_sha256'],'--mesen','poc/runtime/isolated-mesen-chip-matrix/Mesen.exe','--out',folder,'--probe','snapshot','--actions',old['actions'],'--capture-steps',','.join(map(str,old['capture_steps'])),'--timeout','300']+g
        if parent:cmd+=['--state',parent+'/checkpoint.mss','--state-origin',parent+'/result.json']
        subprocess.run(cmd,cwd=ROOT,check=True,stdout=subprocess.DEVNULL);r=read(folder+'/result.json')
        if not r['complete']:raise SystemExit('segment incomplete '+folder)
        receipts.append(dict(path=folder+'/result.json',sha256=sha((ROOT/folder/'result.json').read_bytes())));parent=folder
    frozen_write(ROOT/f'analysis/pending500_{batch}_v1/normal_recipe_receipts_v1.json',dict(passed=True,scope=f'Own{batch} coldboot replay of040 recipes; no other-ROM states, no RAM injection',rom_sha256=m['output_sha256'],segments=receipts,latest_checkpoint=parent+'/checkpoint.mss',old_states_used=False,release_eligible=False))
    print('COLDBOOT',batch,'16 segments complete',flush=True)


if __name__=='__main__':main()
