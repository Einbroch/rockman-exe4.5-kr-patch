"""Actual039 normal communication load/selector/hold/font/OBJ/pixel/cancel proof.

One natural source6F56B8/script16 help page, not all500 screens/all Navis.
Source table aliases0/13/14 do not establish one individual Navi identity.
"""
import struct
from collections import Counter
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from verify_tpi_index import lz77_decompress
from verify_pending500_005_displays import model
from report_roll_pet import pixels


def main():
    rp=ROOT/'poc/output/pending500_039_v1.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes();recipe=read('analysis/pending500_039_v1/communication_recipe_receipts_v1.json');n=m['keyitem_rom']['communication039'];record=next(r for r in n['archives'] if r['archive']=='6F56B8');ar=m['active_communication_owners039']['6F56B8'];require_hash(ROOT/ar['path'],ar['sha256']);asset=read(ar['path']);pool,units,expected,streams,ends=model(rom,m,cfg,'6F56B8',16,59,record=record,asset=asset)
    if not recipe['passed'] or recipe['rom_sha256']!=sha(rom) or len(recipe['segments'])!=8:raise ValueError('039 communication route completion')
    # Follow every039 state edge back through the first own coldboot.
    current=read(recipe['segments'][-1]['path']);chain=[]
    while True:
        if not current['complete'] or current['return_code']!=0 or current['rom_sha256']!=sha(rom) or len(current['loaded_rom_guards'])!=6 or current.get('normal_play_checkpoint_eligible') is False:raise ValueError('039 normal ancestry applicability')
        if not current['state_origin']:break
        parent=ROOT/current['state_origin'];old=read(parent);require_hash(parent.parent/'checkpoint.mss',current['state_sha256'])
        if current['state_sha256']!=old['artifacts']['checkpoint.mss']:raise ValueError('039 exact state edge')
        chain.append(dict(path=str(parent.relative_to(ROOT)),sha256=sha(parent.read_bytes())));current=old
    if not chain[-1]['path'].replace('\\','/').endswith('pending500-039-normal-v1-01/result.json'):raise ValueError('039 own coldboot not reached')
    for item in recipe['segments']:
        require_hash(ROOT/item['path'],item['sha256']);path=ROOT/item['path'];r=read(path)
        for name,h in r['artifacts'].items():require_hash(path.parent/name,h)
    d=ROOT/'poc/runtime/pending500-039-communication-v1-07';q=ROOT/'poc/runtime/pending500-039-communication-v1-08';trace=read(d/'communication_trace.json');loads=[e for e in trace['events'] if e['pc']==0x080448D6];native=lz77_decompress(source,0x6F56B8)[0]
    if trace['loads']!=1 or len(loads)!=1 or (loads[0]['registers']['0'],loads[0]['registers']['1'])!=(0x086F56B8,0x02024000) or (d/'communication_native_001.bin').read_bytes()!=native:raise ValueError('039 original table/LZ/shared RAM')
    nested=read(q/'communication_nested.json');calls=[x for x in nested['calls'] if x['script']==16];selectors=[x for x in nested['selectors'] if x['script']==16]
    if not calls or not selectors or any((x['root'],x['lr'],x['saved_outer_lr'])!=(0x02024000,0x0804F7BD,0x080448C7) for x in calls) or any((x['lr'],x['selected_root'])!=(0x0804F7BD,pool) for x in selectors):raise ValueError('039 actual nested caller/guarded ROM selection')
    commands=nested['commands'];zero=[e for e in commands if e['pc']==0x08051098];holds=[e for e in commands if e['pc']==0x08050754]
    if not zero or len(holds)<2 or any((e['op'],e['arg'],e['context'])!=(0xED,0xFF,0x0200FA20) for e in holds):raise ValueError('039 zero-speed/hold command execution')
    for folder,steps in [(d,(1,2)),(q,(1,2))]:
        for step in steps:
            ram=(folder/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes()
            if ram[0x24000:0x24000+len(native)]!=native or tuple(ram[0xFA38:0xFA3A])!=(92,110):raise ValueError('039 native residency/text origin')
    step=2;state=read(q/f'step_{step:03}_roll_pet.json');ram=(q/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes();ptr,root=struct.unpack_from('<2I',ram,0xFA4C);key='6F56B8:16:0';wanted=streams[key]
    if root!=pool or ptr!=ends[key] or rom[ptr-0x08000000:ptr-0x08000000+4]!=bytes.fromhex('edff0000'):raise ValueError('039 exact Korean stream terminal hold')
    last={x['stream']:x for x in state['draws'] if x['stream'] in wanted}
    if set(last)!=set(wanted):raise ValueError('039 displayed literal complete glyph stream')
    draws=[last[s] for s in wanted];reads={x['index']:x['reads'] for x in state['font_reads']};counts=Counter(x['glyph_index'] for x in draws)
    if any(reads.get(index,0)<24*count for index,count in counts.items()):raise ValueError('039 actual font reads')
    proof=pixels(q,step,draws,expected,rom,m,origin=(92,110),cursor_screen_background=True)
    exited=(q/'step_003_gbaExtWorkRam.bin').read_bytes()
    if struct.unpack_from('<I',exited,0xFA50)[0]==pool:raise ValueError('039 Bcancel did not leave communication consumer')
    paths=['tools/verify_communication_runtime039_v1.py','tools/capture_communication039_v1.py','tools/run_communication039_v1.py','analysis/pending500_039_v1/integration.json','analysis/pending500_039_v1/communication_recipe_receipts_v1.json']
    frozen_write(ROOT/'analysis/pending500_039_v1/communication_runtime_v1.json',dict(passed=True,scope=__doc__,rom_sha256=sha(rom),natural_source_archive='6F56B8',natural_rendered_ID=key,own039_coldboot_ancestry=chain,source_load_events=loads,native_RAM_bytes_verified=len(native),actual_nested_calls=calls,actual_selected_ROM_roots=selectors,actual_control_counts=dict(F000=len(zero),EDFF=len(holds)),full_native_initialization_GBA_path_observed=True,native_initializer_CPU_tail_skip_not_used_in_GBA=True,wording=next(u['translation'] for u in units if u['id']==key),page_pixel_proof=proof,terminal_hold_pointer=ptr,cancel_to_PET_verified=True,no_alias_or_gameRAM_write=True,multiplayer_outcome_tested=False,release_eligible=False,dependencies={p:sha((ROOT/p).read_bytes()) for p in paths},limits=['One source/script page only; 500 finite source/static coverage does not equal500 observed screens or all Navi acquisitions.','Fixed-cell communication options unchanged; option outcomes/multipage variants/reentry and more boundary pages may need further checks.','Serial traffic, multiplayer, hardware, audio, Hangul name persistence and full human review not certified.']))
    print('PASS039 natural communication native LZ -> nested selector -> Korean/font/OBJ/pixels -> EDFF hold -> Bcancel')


if __name__=='__main__':main()
