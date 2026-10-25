"""Bounded source Thumb-BL candidates to4F7FC; NOT executable coverage proof."""
import struct
from build_visibility_poc import ROOT,require_hash
from cumulative_batch500 import read
from extended_dialogue import Cs,CS_ARCH_ARM,CS_MODE_THUMB

cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes();d=Cs(CS_ARCH_ARM,CS_MODE_THUMB)
for at in range(0,len(source)-3,2):
    hi,lo=struct.unpack_from('<HH',source,at)
    if hi&0xF800!=0xF000 or lo&0xF800!=0xF800:continue
    off=((hi&0x7FF)<<12)|((lo&0x7FF)<<1)
    if off&0x400000:off-=0x800000
    if 0x08000000+at+4+off!=0x0804F7FC:continue
    print('SOURCE BL CANDIDATE',hex(0x08000000+at))
    for x in d.disasm(source[max(0,at-20):at+12],0x08000000+max(0,at-20)):print(hex(x.address),x.mnemonic,x.op_str)
