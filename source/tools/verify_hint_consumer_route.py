"""Native hint call reached by normal L input on unchanged021."""
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write

def main():
    rp=ROOT/'poc/output/pending500_021_v1.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256'])
    folder=ROOT/'poc/runtime/pending500-022-hint-consumer-route-v1';r=read(folder/'result.json')
    if not r['complete'] or r['rom_sha256']!=m['output_sha256'] or r['return_code'] or r['steps_captured']!=r['steps_expected']:raise ValueError('Route binding')
    for name,h in r['artifacts'].items():require_hash(folder/name,h)
    actions=r['actions'].split(',')
    if actions[:7]!=['a:2:180']*6+['l:2:180']:raise ValueError('Normal input identity')
    t=read(folder/'exectrace_final.json');sites={x['pc']:x for x in t['sites']};entry=sites['0x0804F7FC'];call=sites['0x0804F802']
    if entry['hits']!=1 or call['hits']!=1 or entry['first_frame']!=1092 or call['first_frame']!=1092:raise ValueError('L-call event binding')
    if call['first_regs']['cpu.r0']!=0x0203D800 or call['first_regs']['cpu.r1']!=0:raise ValueError('Hint root/script')
    frozen_write(ROOT/'analysis/pending_insertion_500_022_selector_poc_v1/native_consumer.json',dict(schema=1,rom_sha256=m['output_sha256'],receipt=dict(path=str((folder/'result.json').relative_to(ROOT)),sha256=sha((folder/'result.json').read_bytes())),state_origin=r['state_origin'],normal_input_only=True,native_consumer_entry=0x0804F7FC,native_call=0x0804F802,root=0x0203D800,script=0,event_frame=1092,event_input='L after six A page advances from same-ROM weekday-field-v1 checkpoint',derived_bl_return_lr=0x0804F807,new_reader_installed=False,new500_installed=False,release_eligible=False,limits='Native021 route only. No new wrapper execution or selected19 archive loading/display proof; no forced scene/Navi or RAM writes. BL return LR is derived from source instruction, not a separate runtime LR sample.'))
    print('PASS natural L hint consumer: root0203D800/script0 at native4F802')

if __name__=='__main__':main()
