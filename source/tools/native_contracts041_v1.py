"""Finite041 source consumers and original Thumb-1 providers; not runtime admission."""
import struct,json
from collections import defaultdict,Counter
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from extended_dialogue import Cs,Ks,CS_ARCH_ARM,CS_MODE_THUMB,KS_ARCH_ARM,KS_MODE_THUMB
from verify_tpi_index import lz77_decompress
from consumer_links040_v1 import contracts as previous_contracts

SOURCE='analysis/pending_insertion_500_041_source_v8'


def main():
    s=read(SOURCE+'/selection.json');cfg=read('project.json');require_hash(ROOT/cfg['source_profile']['filename'],s['source_sha256']);source=(ROOT/cfg['source_profile']['filename']).read_bytes();require_hash(ROOT/s['baseline_rom'],s['baseline_sha256']);rom=(ROOT/s['baseline_rom']).read_bytes();previous_contracts(source)
    word=lambda at:struct.unpack_from('<I',source,at)[0]
    expected={0x3C488:0x0202BA7C,0x3C5B8:0x0803C5BC,0x3C618:0x0202BA7C,0x4113C:0x08041140,0x4119C:0x02024000,0x41F34:0x08041F38,0x41F94:0x02026C00,0x41D98:0x02026C00,0x479F4:0x080479F8,0x47A54:0x02024000,0x4F74C:0x08053700,0x4F750:0x02039800,0x4F78C:0x02039800,0x537C8:0x08053E10,0x53894:0x08053F78}
    if any(word(at)!=v for at,v in expected.items()):raise ValueError('041 source literal applicability')
    cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB);ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB);ranges=[]
    spans=[(0x3C478,0x3C486),(0x3C5A4,0x3C5B8),(0x41128,0x4113C),(0x41E1C,0x41E2E),(0x41D84,0x41D98),(0x479E0,0x479F4),(0x4F712,0x4F74A),(0x4F764,0x4F786),(0x4F790,0x4F7B6)]
    for a,b in spans:
        ins=list(cs.disasm(source[a:b],0x08000000+a))
        if sum(i.size for i in ins)!=b-a:raise ValueError('041 exact bounded instruction extent')
        for i in ins:
            if i.size not in (2,4) or i.size==4 and i.mnemonic!='bl' or bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+i.mnemonic+' '+i.op_str,i.address)[0])!=i.bytes:raise ValueError('041 bounded Thumb-1 asm/disasm')
        if a!=0x3C478 and rom[a:b]!=source[a:b]:raise ValueError('041 original source provider changed')
        ranges.append(dict(offset=a,bytes=b-a,source_sha256=sha(source[a:b]),current040_same_as_source=rom[a:b]==source[a:b],instructions=[dict(address=i.address,mnemonic=i.mnemonic,operands=i.op_str,hex=i.bytes.hex()) for i in ins]))
    pool=defaultdict(list)
    for family,table,entries,root,lr,outer in [('equipment',0x3C5BC,23,0x0202BA7C,0x0804F7BD,0x0803C485),('mail-notification',0x41140,23,0x02024000,0x0804F7BD,None),('subchip',0x41F38,23,0x02026C00,0x0804F7BD,0x08041D8F),('tournament-main',0x47980,23,0x02024000,0x08047963,0),('tournament-secondary',0x479F8,23,0x02024000,None,None)]:
        for navi in range(entries):
            p=table+4*navi;arc=f'{word(p)-0x08000000:X}';pool[arc].append(dict(family=family,pointer=p,navi=navi,load_root=root,reader_root=root,common_return_lr=lr,outer_return_lr=outer,source_reader_proven=lr is not None and outer is not None))
    for board in range(6):
        p=0x4B384+board*8;arc=f'{word(p)-0x08000000:X}';pool[arc].append(dict(family='BBS',pointer=p,board=board,load_root=0x02032000,reader_root=0x02032000,common_return_lr=0x0804B5AF,outer_return_lr=0,source_reader_proven=True))
    # Extend the established A0..B1 index scope explicitly, NOT by pointer gaps.
    # B2 has ten source subarea entries fixed by this supported-source contract.
    if [word(0x53E10+4*i) for i in range(10)]!=[0x08053E38+32*i for i in range(10)]:raise ValueError('041 finite B2 NPC subarea table')
    for sub in range(10):
        days=word(0x53E10+4*sub)-0x08000000
        for slot in range(7):
            p=days+slot*4;arc=f'{word(p)-0x08000000:X}';pool[arc].append(dict(family='B2-cached-NPC',pointer=p,scene=0xB2,sub=sub,slot=slot,load_root=0x02039800,reader_root=0x02039800,common_return_lr=0x0804F773,outer_return_lr=0,source_reader_proven=True))
        p=0x53F78+sub*4;arc=f'{word(p)-0x08000000:X}';pool[arc].append(dict(family='B2-board',pointer=p,scene=0xB2,sub=sub,load_root=0x0203C800,reader_root=0x0203C800,common_return_lr=0x0806A507,outer_return_lr=0,source_reader_proven=True))
    groups=defaultdict(list)
    for g in s['groups']:groups[g['archive']].append(g)
    rows=[];counts=Counter();unresolved=[]
    for arc,gs in sorted(groups.items()):
        refs=pool.get(arc,[]);declared=set(gs[0]['source_row']['pointers']);matched={p['pointer'] for p in refs};n=sum(g['units'] for g in gs)
        if refs and matched!=declared:raise ValueError('041 exact selected TPI/provider references '+arc)
        if refs:
            native=lz77_decompress(source,int(arc,16))[0]
            if sha(native)!=gs[0]['source_archive_sha256']:raise ValueError('041 native source identity')
            counts[refs[0]['family']]+=n
        else:
            unresolved.append(dict(archive=arc,new_units=n,reason='Raw original source references are known, but exact ordinary reader/caller boundary still pending. No synthetic ABI assigned.'));counts['raw-reader-pending']+=n
        rows.append(dict(archive=arc,new_units=n,references=refs,source_reference_membership_proven=bool(refs),product_admitted=False,runtime_verified=False))
    if sum(counts.values())!=500 or len(rows)!=53:raise ValueError('041 selected consumer denominator')
    frozen_write(ROOT/SOURCE/'native_contracts_v1.json',dict(passed=True,status='041_FINITE_SOURCE_CONTRACTS_NOT_PRODUCT_OR_FULL_RUNTIME',baseline_sha256=s['baseline_sha256'],source_sha256=sha(source),family_unit_counts=dict(counts),source_reference_bound_units=500-counts['raw-reader-pending'],unresolved=unresolved,archives=rows,source_code_ranges=ranges,source_literals=expected,rom_written=False,product_admitted=False,release_eligible=False,dependencies={p:sha((ROOT/p).read_bytes()) for p in [SOURCE+'/selection.json','tools/native_contracts041_v1.py','tools/consumer_links040_v1.py']},limits=['B2 source lookup is newly enumerated, not natural B2 map acquisition or script rendering.','The102 literals at41F38 are subchip-use messages, not folder UI; load root026C00 differs from reader literal024000 and must be traced before selector design.','Source reader at41D84 points024000 while loader41E28 writes026C00: no implicit equivalence is adopted.','Mail observed intro9 does not establish all notification script callers; secondary tournament reader pending.','Equipment source entry3C478 is already redirected by adopted old guide hook; exact040 runtime trace is authoritative for its actual ABI.']))
    print('041 selected source memberships',dict(counts),'bound',500-counts['raw-reader-pending'],'/500; not full ABI/runtime admission')


if __name__=='__main__':main()
