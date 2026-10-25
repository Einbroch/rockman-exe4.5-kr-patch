"""Own corrected035 coldboot and normal field route; no old ROM saved states."""
import subprocess,sys
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read
from field_npc_rom_product_035_v2 import verify_final

def main():
    rom='poc/output/pending500_035_v2.gba';rp=ROOT/rom;m=read(rp.with_suffix('.json'));h=m['output_sha256'];require_hash(rp,h)
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);verify_final(sp.read_bytes(),rp.read_bytes(),m['keyitem_rom'])
    parent=None
    for suffix,old in [('boot','poc/runtime/pending500-035-current-day4-boot'),('route','poc/runtime/pending500-035-current-day4-route'),('battle','poc/runtime/pending500-035-current-day4-battle'),('approach','poc/runtime/pending500-035-current-day4-approach')]:
        receipt=read(old+'/result.json')
        if not receipt['complete'] or receipt['rom_sha256']!='41c598d4d056b76eaacab3b111cadfa4767f2dd584ae729d03cfe09b0b859bdd':raise ValueError('button recipe incomplete or changed baseline')
        actions=receipt['actions'].split(',')
        captures=list(receipt['capture_steps'])
        if suffix=='boot':
            if len(actions)!=13 or actions[8]!='a:2:120':raise ValueError('day4 hour entry anchor')
            actions[9:9]=['up:2:30']*9
            captures=[18,22]
        folder='poc/runtime/pending500-035-fixed-daytime-v2-'+suffix
        cmd=[sys.executable,'-X','utf8','tools/capture_field_loader_035_v5.py','--rom',rom,'--expect-rom-sha256',h,'--mesen','poc/runtime/isolated-mesen-chip-matrix/Mesen.exe','--out',folder,'--actions',','.join(actions),'--probe','snapshot','--timeout','300','--capture-steps',','.join(map(str,captures))]
        if parent:cmd+=['--state',parent+'/checkpoint.mss','--state-origin',parent+'/result.json']
        subprocess.run(cmd,cwd=ROOT,check=True);parent=folder

if __name__=='__main__':main()
