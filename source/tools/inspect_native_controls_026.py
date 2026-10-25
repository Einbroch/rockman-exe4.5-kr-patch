"""Bounded native control inspection, not consumer admission or ROM writing."""
import struct
import argparse
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read
from extended_dialogue import Cs,CS_ARCH_ARM,CS_MODE_THUMB

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--range',nargs=2,action='append',default=[]);args=ap.parse_args()
    cfg=read('project.json');p=ROOT/cfg['source_profile']['filename'];require_hash(p,cfg['source_profile']['sha256']);rom=p.read_bytes();cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB)
    for base,op in ((0x50098,0xF8),(0x50100,0xF8),(0x50098,0xEB),(0x50100,0xEB)):
        ptr=struct.unpack_from('<I',rom,base+4*(op-0xE5))[0];print('dispatch',hex(base),hex(ptr))
    for base,count in ((0x52654,16),(0x51F60,2)):
        print('data pointers',hex(base),[hex(x) for x in struct.unpack_from('<'+'I'*count,rom,base)])
    for a,n in [(int(a,16),int(n,16)) for a,n in args.range] or [(0x524A8,0xA0),(0x52534,0x40)]:
        print('CANDIDATE extent',hex(a),n)
        for i in cs.disasm(rom[a:a+n],0x08000000+a):print(hex(i.address),i.bytes.hex(),i.mnemonic,i.op_str)

if __name__=='__main__':main()
