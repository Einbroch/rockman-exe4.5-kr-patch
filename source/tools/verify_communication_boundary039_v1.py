"""Source038 communication load/residency/nested caller/hold observations.

This establishes the original boundary for039 integration; it does NOT
transfer038 gameplay or Japanese screenshots into039 Korean runtime proof.
"""
import struct
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from verify_tpi_index import lz77_decompress
from capstone import Cs,CS_ARCH_ARM,CS_MODE_THUMB

def main():
    rp=ROOT/'poc/output/pending500_038_v2.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    selection=read('analysis/pending_insertion_500_039_communication_words_v1/selection.json');compiled=read('analysis/pending_insertion_500_039_communication_words_v1/verification_v1.json');cpu=read('analysis/pending_insertion_500_039_communication_words_v1/native_controls_cpu_v1.json')
    if not all(x['baseline_sha256']==sha(rom) for x in (selection,compiled,cpu)) or not compiled['passed'] or not cpu['passed']:raise ValueError('Exact038 source-stage applicability')
    # The first static survey stopped at4F7B6; inspect the helper itself.
    decoder=Cs(CS_ARCH_ARM,CS_MODE_THUMB);code=[]
    for lo,hi in [(0x448BC,0x448DC),(0x4F7B6,0x4F7CC)]:
        if source[lo:hi]!=rom[lo:hi]:raise ValueError('Original communication/helper code drift')
        ins=list(decoder.disasm(source[lo:hi],0x08000000+lo))
        if sum(i.size for i in ins)!=hi-lo:raise ValueError('Bounded communication/helper decode extent')
        code.extend(dict(address=i.address,mnemonic=i.mnemonic,operands=i.op_str,bytes=i.bytes.hex()) for i in ins)
    expected={0x080448C2:('bl','#0x804f7b6'),0x0804F7B6:('push','{r4, r5, r6, r7, lr}'),0x0804F7B8:('bl','#0x804fb4c')}
    for at,value in expected.items():
        i=next(i for i in code if i['address']==at)
        if (i['mnemonic'],i['operands'])!=value:raise ValueError('Original nested initializer contract')
    d=ROOT/'poc/runtime/pending500-038-communication-observe-v7';nextd=ROOT/'poc/runtime/pending500-038-communication-observe-v8';r=read(d/'result.json');q=read(nextd/'result.json');receipts={}
    for folder,receipt in [(d,r),(nextd,q)]:
        if not receipt['complete'] or receipt['rom_sha256']!=sha(rom) or receipt.get('normal_play_checkpoint_eligible') is False or len(receipt['loaded_rom_guards'])!=4:raise ValueError('Normal own038 observation identity')
        for name,h in receipt['artifacts'].items():require_hash(folder/name,h)
        receipts[str((folder/'result.json').relative_to(ROOT))]=sha((folder/'result.json').read_bytes())
    if q['state_origin']!=str(d/'result.json') or q['state_sha256']!=r['artifacts']['checkpoint.mss']:raise ValueError('Same038 load-to-reader state edge')
    require_hash(d/'checkpoint.mss',q['state_sha256'])
    chain=[];current=q
    while current.get('state_origin'):
        origin=ROOT/current['state_origin'];parent=read(origin)
        if not parent['complete'] or parent['rom_sha256']!=sha(rom) or parent.get('normal_play_checkpoint_eligible') is False or current['state_sha256']!=parent['artifacts']['checkpoint.mss']:raise ValueError('Exact own038 normal ancestry')
        require_hash(origin.parent/'checkpoint.mss',current['state_sha256']);chain.append(dict(path=str(origin.relative_to(ROOT)),sha256=sha(origin.read_bytes())));current=parent
    if not chain or not chain[-1]['path'].endswith('pending500-038-normal-v1-01/result.json'):raise ValueError('Own038 coldboot ancestor not reached')
    trace=read(d/'communication_trace.json');loads=[e for e in trace['events'] if e['pc']==0x080448D6]
    if trace['loads']!=1 or len(loads)!=1 or (loads[0]['registers']['0'],loads[0]['registers']['1'])!=(0x086F56B8,0x02024000):raise ValueError('Original communication table/source/LZ/root')
    native=lz77_decompress(source,0x6F56B8)[0]
    if (d/'communication_native_001.bin').read_bytes()!=native:raise ValueError('Full original communication LZ result')
    nested=read(nextd/'communication_nested.json');calls=nested['calls']
    if len(calls)!=1 or (calls[0]['root'],calls[0]['script'],calls[0]['lr'],calls[0]['saved_outer_lr'])!=(0x02024000,16,0x0804F7BD,0x080448C7):raise ValueError('Actual nested common-entry ABI')
    calls2=[e for e in read(nextd/'communication_trace.json')['events'] if e['pc']==0x080448C2]
    if len(calls2)!=1 or (calls2[0]['registers']['0'],calls2[0]['registers']['1'])!=(0x02024000,16):raise ValueError('Actual outer provider/script arguments')
    commands=nested['commands'];zero=[e for e in commands if e['pc']==0x08051098];holds=[e for e in commands if e['pc']==0x08050754]
    if len(zero)!=1 or not holds or any((e['op'],e['arg'],e['context'])!=(0xED,0xFF,0x0200FA20) for e in holds):raise ValueError('Actual native zero-speed/visible hold path')
    for folder,steps in [(d,(1,2)),(nextd,(1,2))]:
        for step in steps:
            mem=(folder/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes()
            if mem[0x24000:0x24000+len(native)]!=native or tuple(mem[0xFA38:0xFA3A])!=(92,110):raise ValueError('Native residency/origin changed before consumption')
    shown=(nextd/'step_002_gbaExtWorkRam.bin').read_bytes();ptr,root=struct.unpack_from('<2I',shown,0xFA4C)
    if root!=0x02024000 or shown[ptr-0x02000000:ptr-0x02000000+4]!=bytes.fromhex('edff0000'):raise ValueError('Visible original terminal hold state')
    exited=(nextd/'step_003_gbaExtWorkRam.bin').read_bytes()
    if struct.unpack_from('<I',exited,0xFA50)[0]==0x02024000:raise ValueError('Communication cancel did not return to PET consumer')
    deps=['tools/verify_communication_boundary039_v1.py','tools/capture_communication038_v1.py','tools/capture_communication038_v2.py','analysis/pending_insertion_500_039_communication_words_v1/selection.json','analysis/pending_insertion_500_039_communication_words_v1/verification_v1.json','analysis/pending_insertion_500_039_communication_words_v1/native_controls_cpu_v1.json']
    frozen_write(ROOT/'analysis/pending_insertion_500_039_communication_words_v1/baseline_boundary_v1.json',dict(passed=True,scope=__doc__,baseline_rom=str(rp.relative_to(ROOT)),baseline_sha256=sha(rom),source_sha256=sha(source),native_archive='6F56B8',native_bytes=len(native),native_sha256=sha(native),normal_coldboot_ancestry=chain,receipts=receipts,load_events=loads,actual_nested_calls=calls,actual_source_control_counts=dict(F000=len(zero),EDFF=len(holds)),native_source_RAM_retained_until_consumer=True,visible_hold_origin=[92,110],cancel_to_PET_consumer_verified=True,source_code=code,shared_entry_4FB4C_reached=True,existing038_descriptor_domain_matches_communication=False,classification_correction='4F7B6 DOES invoke4FB4C with LR4F7BD; its saved caller at incomingSP+16 is448C7. Earlier source survey saying the common entry was not reached was incomplete. Existing038 typed guards still do not admit root02024000. No039 hook is implemented by this finding.',Navi_identity_limit='6F56B8 is shared by source table Navi0/13/14; no individual Navi identity inferred from payload identity alone.',ROM_written=False,rom_written=False,new_units_applied=0,runtime039_tested=False,release_eligible=False,dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},limits=['Actual038 original/Japanese communication menu only; not039 Korean font/pixel/interaction proof.','No partner negotiation/link battle was selected; serial traffic, multiplayer outcome, hardware and audio not certified.','No aliases, forced caller/root/PC, gameRAM/ROM writes; ordinary gameplay changes only own test state.']))
    print('PASS039 prerequisite: own038 full native communication load -> residency -> nested4F7B6/4FB4C source caller -> F000/EDFF -> cancel; NOT039 runtime')

if __name__=='__main__':main()
