"""Original040 subchip loader/reader/default and scoped read-alias warning evidence."""
import struct
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from verify_tpi_index import lz77_decompress
from extended_dialogue import Cs,Ks,CS_ARCH_ARM,CS_MODE_THUMB,KS_ARCH_ARM,KS_MODE_THUMB

SOURCE='analysis/pending_insertion_500_041_source_v8'


def main():
    s=read(SOURCE+'/selection.json');cfg=read('project.json');require_hash(ROOT/s['baseline_rom'],s['baseline_sha256']);rom=(ROOT/s['baseline_rom']).read_bytes();require_hash(ROOT/cfg['source_profile']['filename'],s['source_sha256']);source=(ROOT/cfg['source_profile']['filename']).read_bytes();deps={}
    def receipt(folder,diagnostic=False):
        r=read(folder+'/result.json');deps[folder+'/result.json']=sha((ROOT/folder/'result.json').read_bytes())
        if not r['complete'] or r['return_code']!=0 or r['rom_sha256']!=s['baseline_sha256'] or len(r['loaded_rom_guards'])!=8 or (ROOT/folder/'loaded_rom_guard_failed.txt').exists():raise ValueError('041 exact040 subchip receipt')
        if diagnostic:
            if not r.get('state_intervention') or r.get('normal_play_checkpoint_eligible') is not False or (ROOT/folder/'checkpoint.mss').exists() or not (ROOT/folder/'diagnostic_checkpoint.mss').exists():raise ValueError('041 qualified subchip checkpoint quarantine')
        elif r.get('normal_play_checkpoint_eligible') is False:raise ValueError('041 normal source route ancestry')
        for name,h in r['artifacts'].items():require_hash(ROOT/folder/name,h);deps[folder+'/'+name]=h
        origin=read(r['state_origin']);parent=(ROOT/r['state_origin']).parent
        require_hash(parent/'checkpoint.mss',r['state_sha256']);require_hash(ROOT/folder/'input.mss',r['state_sha256'])
        if not origin['complete'] or origin['rom_sha256']!=s['baseline_sha256'] or origin.get('normal_play_checkpoint_eligible') is False:raise ValueError('041 same040 pre-boundary parent')
        return r
    normal='poc/runtime/pending500-040-native041-subchip-v11';qualified='poc/runtime/pending500-040-native041-subchip-count-v3';parent='poc/runtime/pending500-040-native041-field-intro-v1'
    # The route is ordinary input, not an invented routine call or cross-ROM state.
    for folder in ['poc/runtime/pending500-040-native041-select-route-v1',parent,normal]:receipt(folder)
    qr=receipt(qualified,True);before=(ROOT/parent/'final_gbaExtWorkRam.bin').read_bytes()
    if before[0xFD50]!=0x50:raise ValueError('041 established plugged-in PET pre-subchip entry')
    native=lz77_decompress(source,0x6F9B4C)[0]
    if len(native)!=458:raise ValueError('041 native subchip reference extent')
    observations=[]
    for folder in [normal,qualified]:
        t=read(folder+'/native_consumers041.json');loads=[x for x in t['loads'] if x['archive']=='6F9B4C']
        if len(loads)!=1 or loads[0]['source']!=0x086F9B4C or loads[0]['destination']!=0x02026C00 or loads[0]['bytes']!=len(native) or loads[0]['lr']!=0x08041E2D:raise ValueError('041 actual original source/table/LZ/destination')
        residency=[]
        for step in range(1,7):
            ram=(ROOT/folder/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes()
            same=ram[0x26C00:0x26C00+len(native)]==native;mode=ram[0xFD50]
            if mode in (0x1C,0x50):
                if not same:raise ValueError('041 actual subchip native payload lifetime')
            elif mode!=4 or struct.unpack_from('<I',ram,0xFA50)[0]==0x02026C00:raise ValueError('041 buffer reuse outside released subchip consumer')
            residency.append(dict(step=step,mode=mode,original_native_bytes_retained=same,within_subchip_or_immediate_PET_lifetime=mode in (0x1C,0x50)))
            for lo,hi in [(0x61CC,0x61FC),(0x500,0x530),(0x91F8,0x9228),(0x4AF0,0x4AF4)]:
                if ram[lo:hi]!=before[lo:hi]:raise ValueError('041 unchanged real item/availability/HP state')
        observations.append(dict(folder=folder,load=loads[0],native_payload_sha256=sha(native),residency=residency,real_inventory_availability_and_HP_preserved=True))
    t=read(qualified+'/native_consumers041.json');calls=[x for x in t['calls'] if x['registers']['0']==0x02026C00 and x['registers']['1']==6]
    if len(calls)!=1 or calls[0]['registers']['14']!=0x0804F7BD or calls[0]['stack_lr16']!=0x08041D8F or (ROOT/qualified/calls[0]['native_dump']).read_bytes()!=native:raise ValueError('041 actual native subchip script6 ABI/RAM identity')
    call=calls[0];defaults=[x for x in t['defaults'] if x['frame']==call['frame'] and x['root']==0x02026C00];draws=[x for x in t['draws'] if x['root']==0x02026C00]
    if len(defaults)!=1 or (defaults[0]['x'],defaults[0]['y'])!=(52,110) or len(draws)!=15 or any((x['x'],x['y'])!=(52,110) for x in draws):raise ValueError('041 actual quick initialization and native text draw extent')
    for step in (2,3,4):
        ram=(ROOT/qualified/f'step_{step:03}_gbaExtWorkRam.bin').read_bytes()
        if ram[0xFD50]!=0x1C or struct.unpack_from('<I',ram,0xFA50)[0]!=0x02026C00 or ram[0xFA38:0xFA3A]!=bytes((52,110)):raise ValueError('041 warning wait/clear and original subchip mode')
    final=(ROOT/qualified/'step_006_gbaExtWorkRam.bin').read_bytes()
    if final[0xFD50]!=0x50 or struct.unpack_from('<I',final,0xFA50)[0]==0x02026C00:raise ValueError('041 subchip exit to ordinary PET consumer')
    aliases=read(qualified+'/subchip_count_alias041.json')['aliases'];availability=read(qualified+'/subchip_availability_alias041.json')['aliases']
    if len(aliases)!=1 or len(availability)!=1:raise ValueError('041 exact finite diagnostic read substitutions')
    a=aliases[0];b=availability[0]
    if (a['address'],a['original'],a['returned'],a['pc'],a['lr'],a['item'],a['base'],a['navi_offset'],a['outer'])!=(0x020061F3,0,1,0x08030314,0x08005CD7,39,0x020061CC,0,0x08041A57):raise ValueError('041 actual original item list count read guard')
    if (b['address'],b['original'],b['returned'],b['pc'],b['item'],b['outer'],b['frame'])!=(0x0200921F,47,82,0x08005CEC,39,0x08041A57,a['frame']):raise ValueError('041 exact original availability comparison read guard')
    ranges=[];cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB);ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB)
    for lo,hi in [(0x5CCC,0x5CF6),(0x302F8,0x3031E),(0x41A40,0x41A68),(0x41C9C,0x41CC2),(0x41D84,0x41D98),(0x41E1C,0x41E2E)]:
        raw=source[lo:hi];ins=list(cs.disasm(raw,0x08000000+lo))
        if rom[lo:hi]!=raw or sum(i.size for i in ins)!=len(raw):raise ValueError('041 original subchip instruction applicability/extent')
        for i in ins:
            if i.size not in (2,4) or i.size==4 and i.mnemonic!='bl' or bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+i.mnemonic+' '+i.op_str,i.address)[0])!=i.bytes:raise ValueError('041 subchip ARM7TDMI Thumb1 roundtrip')
        ranges.append(dict(offset=lo,bytes=hi-lo,sha256=sha(raw),instructions=[dict(address=i.address,mnemonic=i.mnemonic,operands=i.op_str,hex=i.bytes.hex()) for i in ins]))
    # Bound the finite original lookup population sharing this native reader.
    contracts=read(SOURCE+'/native_contracts_v2.json');family=[x for x in contracts['archives'] if x['references'] and x['references'][0]['family']=='subchip'];ids=[];records=[]
    for row in family:
        arc=row['archive'];gs=[g for g in s['groups'] if g['archive']==arc];ids.extend(u for g in gs for u in g['ids'])
        if any(g['script'] not in (6,8,9,12,13) for g in gs):raise ValueError('041 finite subchip selected scripts')
        for ref in row['references']:
            if ref['reader_root']!=0x02026C00 or ref['common_return_lr']!=0x0804F7BD or ref['outer_return_lr']!=0x08041D8F or rom[ref['pointer']:ref['pointer']+4]!=source[ref['pointer']:ref['pointer']+4]:raise ValueError('041 exact source family reader/lookup contract')
        payload=lz77_decompress(source,int(arc,16))[0]
        if lz77_decompress(rom,int(arc,16))[0]!=payload:raise ValueError('041 unchanged source compressed subchip pool')
        records.append(dict(archive=arc,selected_ids=[u for g in gs for u in g['ids']],selected_scripts=sorted(g['script'] for g in gs),native_bytes=len(payload),native_sha256=sha(payload),references=row['references'],native_consumer_contract_bound=True,product_admitted=False))
    if len(ids)!=102 or len(set(ids))!=102:raise ValueError('041 finite subchip102 population')
    result=dict(passed=True,status='041_SUBCHIP_ORIGINAL_NATIVE_BOUNDARY_PASS_NEW_KOREAN_ROM_PENDING',baseline_sha256=s['baseline_sha256'],normal_loader_and_PET_exit=True,qualified_original_warning=dict(archive='6F9B4C',script=6,selected_ID='6F9B4C:6:0',root=0x02026C00,common_lr=0x0804F7BD,outer_lr=0x08041D8F,origin=[52,110],draws=len(draws),actual_native_payload=True),read_aliases=dict(quantity=aliases,availability_comparison=availability),observations=observations,source_ranges=ranges,native_consumer_contract_units=102,native_consumer_contract_archives=len(records),source_consumer_records=records,original_selected_IDs_rendered=['6F9B4C:6:0'],new_Korean_IDs_rendered=[],natural_item_acquisition_verified=False,new_ROM_applied_units=0,rom_written=False,product_admitted=False,release_eligible=False,checker_failure_history=['count-v1/v2 reached ordinary menu but0 aliases; neither proves warning consumption. Original getter has nested5CCC->CEC LR5CD7 and availability mismatch causes3031A early return, so30314 count read is not reached for absent item.','Read-only getter observation retained first500events; cap reached, not a complete trace. First absent MiniEnergy events show3031A branch; v3 qualifies both original availability comparison and later count reads, no RAM writes.'],dependencies={**deps,**{p:sha((ROOT/p).read_bytes()) for p in [SOURCE+'/selection.json',SOURCE+'/native_contracts_v2.json','tools/verify_subchip_boundary041_v1.py','tools/capture_subchip_count041_v3.py','tools/run_subchip_count041_v3.py']}},limits=['Native original script6 on exact040 only, NOT new041 Korean rendering or all102 scripts observed.','The102 are statically linked to the original loader/reader contract; selector CPU/immutable-original full500 integration/new ROM screen QA remain mandatory.','Quantity and availability were read aliases; real record stayed unchanged. No item acquisition, successful consumption, recovery or save/reload claim.','Field Start transition was acquired after additional wait/A inputs; earlier Start non-entry cause is not attributed to a specific cutscene or Select requirement.'])
    frozen_write(ROOT/SOURCE/'subchip_boundary_v1.json',result);print('PASS041 original subchip LZ/native script6 ABI/default/wait/PET exit; real records unchanged;102 share source contract; NO newROM')


if __name__=='__main__':main()
