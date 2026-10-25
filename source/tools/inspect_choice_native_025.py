"""Bounded native choice/control disassembly for025 interaction evidence."""
import struct
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from extended_dialogue import Cs,CS_ARCH_ARM,CS_MODE_THUMB

def main():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB)
    dispatch={hex(op):hex(struct.unpack_from('<I',source,0x50098+4*(op-0xE5))[0]&~1) for op in (0xE5,0xEA,0xEC)}
    records=[]
    for begin,length in ((0x50750,0x200),(0x508A0,0x280),(0x50A00,0x280)):
        records.append(dict(offset=begin,bytes=length,sha256=sha(source[begin:begin+length]),instructions=[dict(address=i.address,hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str) for i in cs.disasm(source[begin:begin+length],0x08000000+begin)]))
    print(dispatch)
    for key,value in dispatch.items():
        at=int(value,16)-0x08000000
        print(key,value)
        for i in cs.disasm(source[at:at+384],0x08000000+at):print(hex(i.address),i.mnemonic,i.op_str)
    frozen_write(ROOT/'analysis/pending_insertion_500_025_choice_inspection_v1/disassembly.json',dict(source_sha256=sha(source),dispatch=dispatch,ranges=records,complete_function_extent_verified=False,not_machine_code_admission=True))

if __name__=='__main__':main()
