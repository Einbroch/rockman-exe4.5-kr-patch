"""Source/current field-loader binding; adjacent pool is not lifetime proof."""
import struct
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from extended_dialogue import Cs,Ks,CS_ARCH_ARM,CS_MODE_THUMB,KS_ARCH_ARM,KS_MODE_THUMB
from inspect_remaining_035 import BASE,BASE_SHA
from prepare_source500_035 import OUT as SELECTION

OUT='analysis/pending_insertion_500_035_loader_analysis_v1/analysis.json'
COMPILE='analysis/pending_insertion_500_035_source_compile500_v1/verification.json'
CODE=((0x4F712,0x4F74A),(0x4F790,0x4F7A6),(0x4F7A6,0x4F7B6),(0x4F764,0x4F786))

def verify(source,rom,selection,compiled):
    for a,b in CODE:
        if source[a:b]!=rom[a:b]:raise ValueError('Native loader code drift')
    if source[0x4F74C:0x4F764]!=rom[0x4F74C:0x4F764]:raise ValueError('Native loader literal drift')
    pools=struct.unpack_from('<6I',source,0x4F74C)
    if pools!=(0x08053700,0x02039800,0x080537CC,0x0203C800,0x08053FA0,0x0203D800):raise ValueError('Source three loader pools')
    if struct.unpack_from('<I',source,0x53780)[0]!=0x08053898:raise ValueError('Source A0 scene table')
    if source[0x53780:0x53784]!=rom[0x53780:0x53784] or source[0x53898:0x538A8]!=rom[0x53898:0x538A8]:raise ValueError('Current field table drift')
    selected={g['archive']:g for g in selection['groups']};compiled={r['archive']:r for r in compiled['archives']};out=[]
    for arc,g in sorted(selected.items()):
        ptrs=g['source_row']['pointers']
        if len(ptrs)!=1:raise ValueError('Exact source field reference')
        found=[]
        for sub in range(4):
            table=struct.unpack_from('<I',source,0x53898+4*sub)[0]-0x08000000
            if table!=0x538A8+32*sub:raise ValueError('Source sub-area table identity')
            for slot in range(8):
                at=table+4*slot
                if struct.unpack_from('<I',source,at)[0]==0x08000000+int(arc,16):found.append((sub,slot,at))
        if len(found)!=1 or found[0][2]!=ptrs[0]:raise ValueError('Field source lookup binding')
        if any(source[p:p+4]!=rom[p:p+4] for p in ptrs):raise ValueError('Current selected field reference drift')
        c=compiled[arc]['compression_analysis'];headroom=0x0203C800-0x02039800
        if not 0<c['target_decoded_bytes']<=headroom:raise ValueError('Target crosses adjacent loader destination')
        out.append(dict(archive=arc,scene_major=0xA0,sub_area=found[0][0],time_selector_slot=found[0][1],pointer_offset=found[0][2],
                        native_destination=0x02039800,next_loader_destination=0x0203C800,adjacent_destination_distance=headroom,
                        source_decoded_bytes=c['source_decoded_bytes'],target_decoded_bytes=c['target_decoded_bytes'],
                        preserves_next_loader_destination=True,entire_gap_free_or_lifetime_safe_proven=False))
    return out

def main():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    require_hash(ROOT/BASE,BASE_SHA);rom=(ROOT/BASE).read_bytes();selection=read(SELECTION);compiled=read(COMPILE)
    for report in (selection,compiled):
        for p,h in report['dependencies'].items():require_hash(ROOT/p,h)
    result=verify(source,rom,selection,compiled);cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB);ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB);disassembly=[]
    for a,b in CODE:
        rows=list(cs.disasm(source[a:b],0x08000000+a))
        if sum(i.size for i in rows)!=b-a:raise ValueError('Loader decode extent')
        for i in rows:
            if i.size not in (2,4) or i.size==4 and i.mnemonic!='bl' or bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+i.mnemonic+' '+i.op_str,i.address)[0])!=i.bytes:raise ValueError('Loader Thumb1 roundtrip')
            disassembly.append(dict(address=i.address,bytes=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str))
    mutations=[]
    for at in (0x4F712,0x4F724,0x4F790,0x4F7A6,0x4F764,0x4F750,0x53780,0x53898,0x538AC,0x53900):
        broken=bytearray(rom);broken[at]^=1
        try:verify(source,bytes(broken),selection,compiled)
        except ValueError as ex:mutations.append(dict(offset=at,rejected=str(ex)))
        else:raise ValueError('Missed loader drift')
    deps=[SELECTION,COMPILE,'tools/inspect_compressed_loader_035.py','tools/inspect_remaining_035.py']
    frozen_write(ROOT/OUT,dict(schema=1,status='STATIC_NATIVE_LOADER_BINDING_PASS_NOT_RUNTIME_OR_PRODUCT_ADMISSION',passed=True,
        source_sha256=sha(source),baseline_rom=BASE,baseline_sha256=BASE_SHA,archives=result,native_disassembly=disassembly,
        source_code_and_current_rom_identity=True,negative_mutations=mutations,
        dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},rom_written=False,new_units_applied=0,release_eligible=False,
        limits='Native 0804F712 loads selected NPC archives into02039800 before independent0203C800 and0203D800 assets. The source lookup yields sceneA0/sub-area/8-way selector slots, NOT a proven calendar weekday mapping. Adjacent start gives a necessary non-overlap bound only; intervening users, target BIOS decompression, residency, natural caller, all affected routes and actual Korean runtime remain unproven. No ROM writes authorized by this report.'))
    print('035 static loader',len(result),'archives;',len(mutations),'drift refusals;NO ROM')

if __name__=='__main__':main()
