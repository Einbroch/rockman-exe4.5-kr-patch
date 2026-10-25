"""Own036 Sunday09am coldboot then previously verified controller route only."""
import subprocess,sys
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read

def main():
    rom='poc/output/pending500_036_v1.gba';m=read(rom.replace('.gba','.json'));require_hash(ROOT/rom,m['output_sha256']);parent=None
    for suffix in ('boot','route'):
        old=read('poc/runtime/pending500-035-fixed-daytime-v2-'+suffix+'/result.json')
        if not old['complete'] or old['rom_sha256']!='41fdee5673329c00f80989e5de2d98db6b3b0980c9a30c5e4b8202fd8dd4d95d':raise ValueError('historical controller recipe applicability')
        actions=old['actions'].split(',')
        if suffix=='boot':
            if len(actions)!=22 or actions[5:8]!=['up:2:120']*3:raise ValueError('036 day4 controller anchor')
            del actions[6:8]  # Jan4 -> Jan2 Sunday, ordinary key input only.
            captures='16,20'
        else:captures=','.join(map(str,old['capture_steps']))
        folder='poc/runtime/pending500-036-sunday-v1-'+suffix
        cmd=[sys.executable,'-X','utf8','tools/capture_field_loader_036_v1.py','--rom',rom,'--expect-rom-sha256',m['output_sha256'],'--mesen','poc/runtime/isolated-mesen-chip-matrix/Mesen.exe','--out',folder,'--probe','snapshot','--actions',','.join(actions),'--capture-steps',captures,'--timeout','300']
        if parent:cmd+=['--state',parent+'/checkpoint.mss','--state-origin',parent+'/result.json']
        subprocess.run(cmd,cwd=ROOT,check=True);parent=folder
    print('036 Sunday normal route receipts completed; actual source/selector/display requires inspection')

if __name__=='__main__':main()
