"""Bounded normal035 segments; preserve day4 input checkpoint and actual LR."""
import subprocess,sys
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read

def main():
    rom='poc/output/pending500_035_v1.gba';h='41c598d4d056b76eaacab3b111cadfa4767f2dd584ae729d03cfe09b0b859bdd'
    require_hash(ROOT/rom,h);parent='poc/runtime/pending500-035-current-day4-boot'
    groups=[('route',['pagecycle','complete','field-walk-v2','field-walk-v3','field-portal-v1','field-portal-v2','internet-intro-v1']),('battle',['tutorial-battle-v1','tutorial-battle-v2','tutorial-battle-v3']),('approach',['tutorial-exit-v1','npc-approach-v1','npc-approach-v2','npc-approach-v3','npc-approach-v4'])]
    for tag,suffixes in groups:
        actions=[];caps=[]
        for suffix in suffixes:
            if suffix in ['pagecycle','complete']:old='poc/runtime/pending500-022-weekday-'+('complete-trace' if suffix=='complete' else suffix)
            else:old='poc/runtime/pending500-035-baseline034-'+suffix
            actions+=read(old+'/result.json')['actions'].split(',');caps.append(len(actions))
        folder='poc/runtime/pending500-035-current-day4-'+tag
        cmd=[sys.executable,'-X','utf8','tools/capture_field_loader_035_v5.py','--rom',rom,'--expect-rom-sha256',h,'--mesen','poc/runtime/isolated-mesen-chip-matrix/Mesen.exe','--out',folder,'--actions',','.join(actions),'--probe','snapshot','--timeout','300','--capture-steps',','.join(map(str,caps)),'--state',parent+'/checkpoint.mss','--state-origin',parent+'/result.json']
        subprocess.run(cmd,cwd=ROOT,check=True);parent=folder

if __name__=='__main__':main()
