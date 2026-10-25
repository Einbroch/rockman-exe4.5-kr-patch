"""Additional bounded original reader/caller contracts; no natural acquisition claim."""
import struct
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from extended_dialogue import Cs,Ks,CS_ARCH_ARM,CS_MODE_THUMB,KS_ARCH_ARM,KS_MODE_THUMB
from prepare_repartition500 import layout_records

SOURCE='analysis/pending_insertion_500_041_source_v8'


def main():
    s=read(SOURCE+'/selection.json');cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,s['source_sha256']);source=sp.read_bytes();rp=ROOT/s['baseline_rom'];require_hash(rp,s['baseline_sha256']);rom=rp.read_bytes();m=read(rp.with_suffix('.json'))
    cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB);ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB);ranges=[];decoded={}
    # Only verified code intervals, never arbitrary literal/data windows.
    for lo,hi in [(0x6AAF8,0x6AB10),(0x213A2,0x213AC),(0x20420,0x2044E),(0x47958,0x47964),(0x471F4,0x47202),(0x474FC,0x47516),(0x47630,0x47644)]:
        raw=source[lo:hi];ins=list(cs.disasm(raw,0x08000000+lo))
        if sum(i.size for i in ins)!=len(raw) or rom[lo:hi]!=raw:raise ValueError('041 source reader code extent/applicability')
        for i in ins:
            if i.size not in (2,4) or i.size==4 and i.mnemonic!='bl' or bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+i.mnemonic+' '+i.op_str,i.address)[0])!=i.bytes:raise ValueError('041 bounded ARM7TDMI Thumb1 roundtrip')
            decoded[i.address]=(i.mnemonic,i.op_str)
        ranges.append(dict(offset=lo,bytes=hi-lo,sha256=sha(raw),instructions=[dict(address=i.address,mnemonic=i.mnemonic,operands=i.op_str,hex=i.bytes.hex()) for i in ins]))
    expected={0x0806AAFA:('ldr','r0, [pc, #0x284]'),0x0806AAFC:('ldr','r1, [r5, #8]'),0x0806AAFE:('bl','#0x804fb4c'),0x080213A4:('ldr','r0, [pc, #4]'),0x080213A6:('bl','#0x804fb4c'),0x08020442:('movs','r1, #5'),0x08020444:('bl','#0x80213a2'),0x0804795A:('adds','r1, r0, #0'),0x0804795C:('ldr','r0, [pc, #4]'),0x0804795E:('bl','#0x804fb4c'),0x080471FA:('movs','r0, #0xf'),0x080471FC:('bl','#0x8047958'),0x08047504:('movs','r0, #0x3c'),0x08047506:('bl','#0x8047958'),0x08047638:('movs','r0, #0x3e'),0x0804763A:('bl','#0x8047958')}
    if any(decoded.get(pc)!=op for pc,op in expected.items()):raise ValueError('041 actual reader argument contract')
    rows=[]
    for arc,literal,reader,lr,scripts in [('6FE8D4',0x6AD80,0x0806AAF8,0x0806AB03,[23]),('768BD0',0x213AC,0x080213A2,0x080213AB,[5])]:
        if struct.unpack_from('<I',source,literal)[0]!=0x08000000+int(arc,16):raise ValueError('041 original direct root literal')
        parents=[a for a in layout_records(m) if a['archive']==arc and a.get('rom_offset') is not None]
        if len(parents)!=1:raise ValueError('041 exact existing raw consumer ownership')
        parent=parents[0];root=0x08000000+parent['rom_offset']
        if struct.unpack_from('<I',rom,literal)[0]!=root or sha(rom[parent['rom_offset']:parent['rom_offset']+parent['compiled_bytes']])!=parent['compiled_sha256']:raise ValueError('041 current raw pointer and consumed payload identity')
        units=[u for g in s['groups'] if g['archive']==arc and g['script'] in scripts for u in g['ids']]
        rows.append(dict(archive=arc,selected_scripts=scripts,selected_units=units,reader=reader,common_entry=0x0804FB4C,common_return_lr=lr,outer_return_lr=0,root_pointer=literal,current_root=root,current_payload_sha256=parent['compiled_sha256'],argument_provider='r1=[r5+8], original dynamic trader script selection' if arc=='6FE8D4' else 'original20442 mov r1,5 -> BL213A2 -> original root literal -> common',runtime_verified=False,full_native_admission=False))
    if sum(len(x['selected_units']) for x in rows)!=5:raise ValueError('041 additional raw caller denominator')
    if struct.unpack_from('<I',source,0x47964)[0]!=0x02024000:raise ValueError('041 shared tournament reader RAM root')
    secondary=dict(archive='6EAD18',reader=0x08047958,common_return_lr=0x08047963,outer_return_lr=0,root=0x02024000,selected_original_direct_callers=[dict(script=15,call=0x080471FC),dict(script=60,call=0x08047506),dict(script=62,call=0x0804763A)],script50_original_selection_pending=True,source_loader_reference='native_contracts_v2.json:479E0/479F8',runtime_verified=False,full_native_admission=False)
    result=dict(passed=True,status='041_ADDITIONAL_SOURCE_READERS_NOT_RUNTIME_OR_PRODUCT_ADMISSION',baseline_sha256=s['baseline_sha256'],source_sha256=s['source_sha256'],raw_selected_source_callers=rows,raw_units_with_additional_bounded_reader_contract=5,raw_tutorial14_units_still_pending=4,tournament_secondary=secondary,source_ranges=ranges,rejected_inference='A generic tutorial reader accepting r1 does not prove original callers for script14; the213A2 direct source call5 covers only four selected literals. No original14 call discovered or absence claimed.',new_ROM_applied_units=0,rom_written=False,product_admitted=False,release_eligible=False,dependencies={p:sha((ROOT/p).read_bytes()) for p in [SOURCE+'/selection.json',SOURCE+'/native_contracts_v2.json','tools/native_callers041_v1.py']},limits=['Bounded literal/argument/return contracts only. No complete original callgraph claim.','Dynamic trader context selection23 and tutorial5 acquisition/rendering remain unobserved.','Secondary reader shares root/LR with main; native payload identity must distinguish variants and live loader/state lifetime must be preserved.','No new ROM, no new translation wording, no replacement of completed source/carry/font gates.'])
    frozen_write(ROOT/SOURCE/'native_callers_v1.json',result);print('PASS041 source raw5/9 caller contracts; tutorial14 four units remain; secondary15/60/62 bounded calls; NOT runtime')


if __name__=='__main__':main()
