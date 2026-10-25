"""Source-bound040 consumer contracts; not complete callgraph/runtime proof."""
import struct
from collections import defaultdict
from extended_dialogue import Cs,Ks,CS_ARCH_ARM,CS_MODE_THUMB,KS_ARCH_ARM,KS_MODE_THUMB
from communication_rom_selector039_v1 import contracts as comm_contracts,source_population as comm_population
from verify_tpi_index import lz77_decompress

CLASSES={
    'communication-help':dict(root=0x02024000,caller_lr=0x0804F7BD,outer_lr=0x080448C7),
    'battle-BBS-trial':dict(root=0x02032000,caller_lr=0x0804B5AF,outer_lr=0),
    'compressed-normal':dict(root=0x02024000,caller_lr=0x08047963,outer_lr=0),
}


def contracts(source):
    comm_contracts(source);cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB);ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB);ranges=[]
    specs=[(0x47958,0x47964),(0x47968,0x4797C),(0x4B7FC,0x4B81C),(0x4B59C,0x4B5AE)]
    for lo,hi in specs:
        raw=source[lo:hi];ins=list(cs.disasm(raw,0x08000000+lo))
        if sum(i.size for i in ins)!=hi-lo:raise ValueError('040 exact source instruction extent')
        for i in ins:
            if i.size not in (2,4) or i.size==4 and i.mnemonic!='bl' or bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+i.mnemonic+' '+i.op_str,i.address)[0])!=i.bytes:raise ValueError('040 source Thumb1 asm/disasm applicability')
        ranges.append(dict(offset=lo,bytes=hi-lo,instructions=[dict(address=i.address,mnemonic=i.mnemonic,operands=i.op_str,hex=i.bytes.hex()) for i in ins]))
    word=lambda at:struct.unpack_from('<I',source,at)[0]
    expected={0x47964:0x02024000,0x4797C:0x08047980,0x479DC:0x02024000,0x4B81C:0x0804B380,0x4B820:0x0202E000,0x4B824:0x02032000,0x4B62C:0x02022000}
    if any(word(a)!=v for a,v in expected.items()):raise ValueError('040 native tables/roots/post map')
    by={i['address']:(i['mnemonic'],i['operands']) for r in ranges for i in r['instructions']}
    for at,op in {0x0804795E:('bl','#0x804fb4c'),0x08047976:('bl','#0x80ec158'),0x0804B816:('bl','#0x80ec158'),0x0804B5AA:('bl','#0x804fb4c'),0x0804B5A4:('ldr','r0, [r7, #4]'),0x0804B5A8:('ldrb','r1, [r1, r2]')}.items():
        if by.get(at)!=op:raise ValueError('040 exact source argument/loading call')
    return dict(classes=CLASSES,source_ranges=ranges,literals=expected,scope='Bounded explicit argument providers/loaders only; not whole-ROM reference completeness',runtime_required=True)


def source_population(source,selected):
    contracts(source);pool=[];comm={a for a,k in selected.items() if k=='communication-help'}
    for p in comm_population(source,comm or {'6F56B8'}):pool.append(dict(p,source_class='communication-help',**CLASSES['communication-help']))
    normal=defaultdict(list)
    for navi in range(23):
        ptr=0x47980+navi*4;address=struct.unpack_from('<I',source,ptr)[0];normal[f'{address-0x08000000:X}'].append(dict(navi=navi,pointer=ptr))
    if set(normal)!={'6E93C8'}:raise ValueError('04023-Navi same normal source table')
    for arc,refs in normal.items():pool.append(dict(archive=arc,references=refs,payload=lz77_decompress(source,int(arc,16))[0],source_class='compressed-normal',**CLASSES['compressed-normal']))
    for board in range(6):
        ptr=0x4B384+board*8;off=struct.unpack_from('<I',source,ptr)[0]-0x08000000
        if not 0<=off<len(source) or source[off]!=0x10:raise ValueError('040 finite BBS source table')
        pool.append(dict(archive=f'{off:X}',references=[dict(board=board,pointer=ptr)],payload=lz77_decompress(source,off)[0],source_class='battle-BBS-trial',**CLASSES['battle-BBS-trial']))
    for arc,kind in selected.items():
        found=[p for p in pool if (p['archive'],p['source_class'])==(arc,kind)]
        if len(found)!=1:raise ValueError('040 source class ownership')
        a=found[0]
        for b in pool:
            if b is a or (b['root'],b['caller_lr'],b['outer_lr'])!=(a['root'],a['caller_lr'],a['outer_lr']):continue
            n=min(len(a['payload']),len(b['payload']))
            if a['payload'][:n]==b['payload'][:n]:raise ValueError('040 ambiguous native prefix in typed domain')
    return pool
