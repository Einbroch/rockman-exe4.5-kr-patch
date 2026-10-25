"""Correct unsupported board-reader annotation with decoded actual source path.

Earlier source/ID/font results remain; its guessed4F780 board-reader annotation
is superseded.4F780 is the common RAW NPC call, NOT root0203C800 board reader.
"""
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write

def main():
    base=ROOT/'tools/verify_source037_v2.py';r=read('analysis/pending_insertion_500_037_source_only_v2/preflight_v1.json');require_hash(base,r['dependencies']['tools/verify_source037_v2.py']);text=base.read_text(encoding='utf8');dest=ROOT/'tools/verify_source037_v3.py'
    if dest.exists():raise ValueError('Preserve verifier version')
    derive='''    from capstone import Cs,CS_ARCH_ARM,CS_MODE_THUMB
    decoder=Cs(CS_ARCH_ARM,CS_MODE_THUMB)
    board_code=list(decoder.disasm(source[0x6A4FC:0x6A50A],0x0806A4FC))
    board_shape=[(i.mnemonic,i.op_str) for i in board_code]
    if board_shape!=[('push','{r4, r5, r6, r7, lr}'),('ldr','r0, [pc, #0xc]'),('ldrb','r1, [r5, #4]'),('bl','#0x804fb4c'),('movs','r0, #0'),('pop','{r4, r5, r6, r7, pc}')]:raise ValueError('Actual board reader decoded source contract')
    board_bl=board_code[3];board_lr=(board_bl.address+board_bl.size)|1
    if word(0x6A50C)!=0x0203C800 or rom[0x6A4FC:0x6A510]!=source[0x6A4FC:0x6A510]:raise ValueError('Actual board-reader source/current identity')
    npc_bl=list(decoder.disasm(source[0x4F76E:0x4F772],0x0804F76E))
    if len(npc_bl)!=1 or npc_bl[0].mnemonic!='bl' or npc_bl[0].op_str!='#0x804fb4c':raise ValueError('Actual cached NPC reader contract')
    npc_lr=(npc_bl[0].address+npc_bl[0].size)|1
'''
    changes=[('    for r in v[\'archives\']:',derive+'    for r in v[\'archives\']:'),('lr=0x0804F773','lr=npc_lr'),('reader=0x0804F780;lr=0x0804F785','reader=0x0806A4FC;lr=board_lr'),("ROOT/out/'preflight_v1.json'","ROOT/out/'preflight_v2.json'"),('tools/verify_source037_v2.py','tools/verify_source037_v3.py'),('source_only_old_cohort_replaced_ids=len(a-b)',"corrected_board_reader=dict(entry=0x0806A4FC,source_bl=board_bl.address,derived_return_lr=board_lr,root_literal=0x6A50C,script_provider='ldrb r1,[r5,#4]',scope='One confirmed source reader path, not all call-site or natural event coverage'),supersedes_annotation='preflight_v1 incorrectly annotated4F780/4F785 as cached board reader; that is common RAW NPC route. Source500/roundtrip/font checks unchanged; reader metadata corrected from actual source instructions.',source_only_old_cohort_replaced_ids=len(a-b)"),('525','525')]
    for old,new in changes:
        if old==new:continue
        if text.count(old)!=1:raise ValueError('037 source verifier exact correction anchor '+old)
        text=text.replace(old,new,1)
    dest.write_text(text,encoding='utf8');frozen_write(ROOT/'tools/specs/verify037_v3_version.json',dict(base=str(base.relative_to(ROOT)),base_sha256=sha(base.read_bytes()),changes=changes[:-1],output=str(dest.relative_to(ROOT)),output_sha256=sha(dest.read_bytes()),reason='Discovered source reader annotation confused common RAW NPC with cached board; source data/text unchanged'))
    print('Generated037 source verifier with actual board6A4FC/BL6A502/return6A507')

if __name__=='__main__':main()
