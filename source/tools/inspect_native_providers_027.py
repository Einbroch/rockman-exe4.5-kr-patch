"""Read-only source-bound native F90C descriptor/code inspection."""
import argparse,struct
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read
from extended_dialogue import Cs,CS_ARCH_ARM,CS_MODE_THUMB

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--range',nargs=2,action='append',default=[]);ap.add_argument('--data',nargs=2,action='append',default=[]);ap.add_argument('--calls',type=lambda v:int(v,16));a=ap.parse_args()
    cfg=read('project.json');path=ROOT/cfg['source_profile']['filename'];require_hash(path,cfg['source_profile']['sha256']);rom=path.read_bytes()
    for i in range(31):
        ptr,n=struct.unpack_from('<II',rom,0x526D0+i*8)
        refs={hex(v):[hex(at) for at in range(0,len(rom)-3,4) if rom[at:at+4]==struct.pack('<I',v)][:24] for v in (ptr-1,ptr)} if i in (0,2,7,8,9) else {}
        print('descriptor',i,hex(ptr),n,'aligned literal candidates',refs)
    cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB)
    for start,size in a.data:
        start,size=int(start,16),int(size,16)
        print('data',hex(start),rom[start:start+size].hex())
        if size%4==0:print('words',[hex(v) for v in struct.unpack_from('<'+'I'*(size//4),rom,start)])
    if a.calls is not None:
        for at in range(0,0x60000-3,2):
            hi,lo=struct.unpack_from('<HH',rom,at)
            if hi&0xF800!=0xF000 or lo&0xF800!=0xF800:continue
            rel=((hi&0x7FF)<<12)|((lo&0x7FF)<<1)
            if rel&0x400000:rel-=0x800000
            if 0x08000000+at+4+rel!=a.calls:continue
            print('CANDIDATE BL to',hex(a.calls),'at',hex(at))
            for ins in cs.disasm(rom[at-14:at+12],0x08000000+at-14):print(hex(ins.address),ins.mnemonic,ins.op_str)
    for start,size in a.range:
        start,size=int(start,16),int(size,16)
        print('CANDIDATE code extent',hex(start),hex(size))
        for ins in cs.disasm(rom[start:start+size],0x08000000+start):print(hex(ins.address),ins.bytes.hex(),ins.mnemonic,ins.op_str)

if __name__=='__main__':main()
