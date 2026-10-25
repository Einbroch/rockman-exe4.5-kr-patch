"""Bind168bounded CPU cases to actual030 native wide-name input observations.

No game/ROM changes or claim about unavailable peer/link initialization.
"""
import struct
from PIL import Image,ImageDraw
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from compile_layout_candidates_024 import ref

OUT='analysis/pending_insertion_500_031_packet_boundary_v1/verification.json'

def main():
    base='poc/output/pending500_030_v1.gba';m=read(base.replace('.gba','.json'));require_hash(ROOT/base,m['output_sha256']);prior=read('analysis/pending500_030_v1/batch_status.json')
    for n,h in m['build_tools_sha256'].items():require_hash(ROOT/'tools'/n,h)
    for p,h in prior['protected_artifacts'].items():require_hash(ROOT/p,h)
    cp='analysis/pending_insertion_500_031_packet_cpu_v1/cpu.json';cpu=read(cp)
    if not cpu['passed'] or cpu['baseline_sha256']!=m['output_sha256'] or cpu['case_count']!=168 or cpu['native_helpers_substituted'] or cpu['modeled_services']:raise ValueError('031 CPU identity/claim')
    for p,h in cpu['dependencies'].items():require_hash(ROOT/p,h)
    groups={
        'packet-writes-031-menu-v2':'pending500-030-v1-complete',
        'packet-writes-031-comm-v1':'packet-writes-031-menu-v2',
        'packet-writes-031-battle-v1':'packet-writes-031-comm-v1',
        'packet-name-031-picker-route-v3':'pending500-030-v1-pagecycle',
        'packet-name-031-six-wide-v4':'packet-name-031-picker-route-v3',
    };receipts=[]
    for folder,parent in groups.items():
        d=ROOT/'poc/runtime'/folder;r=read(d/'result.json');pr=ROOT/'poc/runtime'/parent/'result.json'
        if not r['complete'] or r['return_code']!=0 or r['rom_sha256']!=m['output_sha256'] or r['steps_captured']!=r['steps_expected'] or r.get('normal_play_checkpoint_eligible') is False or (d/'diagnostic_checkpoint.mss').exists() or not(d/'checkpoint.mss').exists():raise ValueError('031 normal sameROM receipt')
        if (ROOT/r['state_origin']).resolve()!=pr.resolve() or read(pr)['rom_sha256']!=m['output_sha256']:raise ValueError('031 native state lineage')
        for p,h in r['artifacts'].items():require_hash(d/p,h)
        receipts.append(ref(d/'result.json'))
    folder=ROOT/'poc/runtime/packet-name-031-six-wide-v4';observed=[]
    for step,n in ((1,0),(2,1),(6,5),(7,6),(8,6)):
        ram=(folder/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes()
        if list(ram[0xFC44:0xFC49])!=[6,36,6,5,0] or any(struct.unpack_from('<I',ram,a)[0]!=0x0200FC60+n*2 for a in (0xFC54,0xFC58)) or ram[0xFC60:0xFC6D]!=b'\xE4\x06'*n+b'\x98\x00'*(6-n)+b'\xE5':raise ValueError('031 native2byte picker/length')
        observed.append(dict(step=step,logical_length=n,capacity=6,selected_page=0,column=6,row=5,source_token_hex='e406'))
    for step in (11,12):
        ram=(folder/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes()
        if ram[0xE50:0xE5E]!=b'\x01'+b'\xE4\x06'*6+b'\xE5':raise ValueError('031 native committed13byte name')
    menu=[]
    for name,step in (('packet-writes-031-menu-v2',8),('packet-writes-031-comm-v1',3),('packet-writes-031-battle-v1',4)):
        d=ROOT/'poc/runtime'/name;r=read(d/f'step_{step:03}_packet_writes.json');ram=(d/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes()
        if r['writes'] or r['calls'] or any(ram[0xF560:0xF5A0]):raise ValueError('031 bounded unconnected route observation changed')
        menu.append(dict(segment=name,step=step,packet64bytes_zero=True,watched_writer_events=0,watched_export_import_stats_calls=0))
    out=ROOT/OUT;out.parent.mkdir(parents=True,exist_ok=False);items=[('packet-writes-031-menu-v2',8),('packet-writes-031-comm-v1',3),('packet-writes-031-battle-v1',4)]+[('packet-name-031-six-wide-v4',i) for i in (7,8,10,11)]
    sheet=Image.new('RGB',(960,360),'#20232a');draw=ImageDraw.Draw(sheet)
    for n,(name,step) in enumerate(items):
        x,y=(n%4)*240,(n//4)*180;sheet.paste(Image.open(ROOT/'poc/runtime'/name/f'step_{step:03}.png').convert('RGB'),(x,y+20));draw.text((x+3,y+3),name.split('031-')[1]+' '+str(step),fill='white')
    sheet.save(out.parent/'contact.png')
    paths=[cp,'tools/verify_packet_boundary_runtime_031.py','tools/capture_packet_writes_031.py']
    frozen_write(out,dict(schema=1,passed=True,meaning='Packet boundary experiment and native input observations verified; NOT multiplayer feature pass',baseline_rom=base,baseline_sha256=m['output_sha256'],cpu=ref(ROOT/cp),native_edit_observations=observed,sixth_accepted=True,seventh_rejected=True,normal_native_wide_name_committed=True,committed_name_hex=(b'\xE4\x06'*6+b'\xE5').hex(),committed_name_bytes=13,unconnected_menu_observations=menu,receipts=receipts,contact=dict(path=str((out.parent/'contact.png').relative_to(ROOT)),sha256=sha((out.parent/'contact.png').read_bytes()),screens=len(items)),dependencies={p:sha((ROOT/p).read_bytes()) for p in paths},screenshot_directly_viewed=False,packet_terminator_ownership_resolved=False,new_units_applied=0,actual_applied_total=16122,new_rom_created=False,new_distribution_packages_created=False,release_eligible=False,limits=['The normal input route confirms six E406 chars are reachable and committed, not merely synthetic editor state. No Hangul input/save/reset/reload proof.','The bounded native export/import CPU slices omitE5 at max2byte6glyphs and leave13th destination byte unchanged. Natural transport preparation/calls/peer/import initialization are not executed.','Communication menu/battle preparation reaches an unready-peer message. Packet64bytes remainzero and watched calls did not run on this bounded route. No assertion that these code paths are globally unreachable or the probe covers all writers.','Not a confirmed original-game error or permission to add a terminator into unproven neighboring storage. No player-name/opponent-name profile admission or500cohort.']))
    print('PASS031 168CPU +normal native six2byte input/commit; transport terminator unresolved; ROM applied delta0')

if __name__=='__main__':main()
