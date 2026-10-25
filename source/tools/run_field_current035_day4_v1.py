"""Normal day4 date entry, no state edits; native035 loader/selector trace."""
import subprocess,sys
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read

def main():
    rom='poc/output/pending500_035_v1.gba';h='41c598d4d056b76eaacab3b111cadfa4767f2dd584ae729d03cfe09b0b859bdd'
    require_hash(ROOT/rom,h)
    boot=read('poc/runtime/pending500-022-weekday-boot/result.json')['actions'].split(',')
    if boot[5:7]!=['up:2:120','up:2:120']:raise ValueError('date day input recipe drift')
    boot.insert(7,'up:2:120')
    actions=[]
    for suffix in ['pagecycle','complete']:
        actions+=read('poc/runtime/pending500-022-weekday-'+('complete-trace' if suffix=='complete' else suffix)+'/result.json')['actions'].split(',')
    for suffix in ['field-walk-v2','field-walk-v3','field-portal-v1','field-portal-v2','internet-intro-v1','tutorial-battle-v1','tutorial-battle-v2','tutorial-battle-v3','tutorial-exit-v1','npc-approach-v1','npc-approach-v2','npc-approach-v3','npc-approach-v4']:
        actions+=read('poc/runtime/pending500-035-baseline034-'+suffix+'/result.json')['actions'].split(',')
    parent=None
    for suffix,seq,caps in [('boot',boot,'8,13'),('field',actions,str(len(actions)))]:
        folder='poc/runtime/pending500-035-current-day4-'+suffix
        cmd=[sys.executable,'-X','utf8','tools/capture_field_loader_035_v4.py','--rom',rom,'--expect-rom-sha256',h,'--mesen','poc/runtime/isolated-mesen-chip-matrix/Mesen.exe','--out',folder,'--actions',','.join(seq),'--probe','snapshot','--timeout','300','--capture-steps',caps]
        if parent:cmd+=['--state',parent+'/checkpoint.mss','--state-origin',parent+'/result.json']
        subprocess.run(cmd,cwd=ROOT,check=True)
        parent=folder

if __name__=='__main__':main()
