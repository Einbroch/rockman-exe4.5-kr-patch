"""Cell budget of every fixed-cell label call: for each bl to 0x080554A4/C8/D0, read r0's literal root and the
immediate r4 (cells per row) / r5 (rows) set in the same basic block before the call.

Returns {root(int): [ (caller, cells, rows, script_imm_or_None) ...]}; roots are ROM archive addresses or
EWRAM buffers. Only calls whose r0 comes from a pc-relative literal and r4/r5 from movs immediates are
counted; anything else is reported as unresolved.
"""
import capstone,struct
from collections import defaultdict

TARGETS={0x080554A4,0x080554C8,0x080554D0}


def scan(src):
    md=capstone.Cs(capstone.CS_ARCH_ARM,capstone.CS_MODE_THUMB);md.detail=False
    calls=[]
    for a in range(0,0x800000-4,2):
        hw1=int.from_bytes(src[a:a+2],'little');hw2=int.from_bytes(src[a+2:a+4],'little')
        if (hw1&0xF800)==0xF000 and (hw2&0xF800)==0xF800:
            off=((hw1&0x7FF)<<12)|((hw2&0x7FF)<<1)
            if off&0x400000:off-=0x800000
            if 0x08000000+a+4+off in TARGETS:calls.append(a)
    out=defaultdict(list);unresolved=[]
    for a in calls:
        start=max(0,a-40);ins=[i for i in md.disasm(src[start:a],0x08000000+start)]
        # keep only the straight-line tail that ends exactly at the call
        while ins and ins[-1].address+ins[-1].size!=0x08000000+a:ins=ins[:-1]
        cut=0
        for j,i in enumerate(ins):
            if i.mnemonic in ('bl','b','bx','pop') or i.mnemonic.startswith('b') and i.mnemonic not in ('bic','bics'):cut=j+1
        ins=ins[cut:];r0=r4=r5=r1=None
        for i in ins:
            ops=i.op_str.replace(' ','')
            if i.mnemonic=='ldr' and ops.startswith('r0,[pc,#'):
                imm=int(ops[len('r0,[pc,#'):-1],0);lit=((i.address+4)&~3)+imm;r0=struct.unpack_from('<I',src,lit-0x08000000)[0]
            elif i.mnemonic=='movs' and ops.startswith('r4,#'):r4=int(ops[4:],0)
            elif i.mnemonic=='movs' and ops.startswith('r5,#'):r5=int(ops[4:],0)
            elif i.mnemonic=='movs' and ops.startswith('r1,#'):r1=int(ops[4:],0)
            elif ops.startswith('r0,') and i.mnemonic!='cmp':r0=r0 if i.mnemonic=='ldr' and ops.startswith('r0,[pc') else None
        if r0 is None or r4 is None:unresolved.append(0x08000000+a);continue
        out[r0].append((0x08000000+a,r4,r5,r1))
    return out,unresolved
