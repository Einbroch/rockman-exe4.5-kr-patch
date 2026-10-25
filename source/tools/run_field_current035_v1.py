"""Replay established controller routes on035, never034 saved states."""
import subprocess,sys
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read

def main():
    rom='poc/output/pending500_035_v1.gba'
    h='41c598d4d056b76eaacab3b111cadfa4767f2dd584ae729d03cfe09b0b859bdd'
    require_hash(ROOT/rom,h)
    parent=None
    segments=[]
    for suffix in ['boot','pagecycle','complete']:
        old='poc/runtime/pending500-022-weekday-'+('complete-trace' if suffix=='complete' else suffix)+'/result.json'
        segments.append((suffix,read(old)['actions']))
    for suffix in ['field-walk-v2','field-walk-v3','field-portal-v1','field-portal-v2','internet-intro-v1','tutorial-battle-v1','tutorial-battle-v2','tutorial-battle-v3','tutorial-exit-v1','npc-approach-v1','npc-approach-v2','npc-approach-v3','npc-approach-v4']:
        old='poc/runtime/pending500-035-baseline034-'+suffix+'/result.json'
        segments.append((suffix,read(old)['actions']))
    for suffix,actions in segments:
        folder='poc/runtime/pending500-035-current-native-'+suffix
        tool='run_mesen_segment.py' if suffix in ['boot','pagecycle'] else 'capture_field_loader_035_v3.py'
        n=len(actions.split(','))
        cmd=[sys.executable,'-X','utf8','tools/'+tool,'--rom',rom,'--expect-rom-sha256',h,'--mesen','poc/runtime/isolated-mesen-chip-matrix/Mesen.exe','--out',folder,'--actions',actions,'--probe','snapshot','--timeout','240','--capture-steps',str(n)]
        if parent:cmd+=['--state',parent+'/checkpoint.mss','--state-origin',parent+'/result.json']
        subprocess.run(cmd,cwd=ROOT,check=True)
        parent=folder
        print('Current035 normal native route '+suffix+' complete',flush=True)

if __name__=='__main__':main()
