"""Typed037 NPC/board selector; immutable native buffers and predecessor ABI.

This module assembles code only. It does not write a product ROM or claim
natural acquisition/rendering. Source call sites, not assigned LRs, define ABI.
"""
import struct
from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB
from extended_dialogue import assemble_verified
from prepare_source500_037_v2 import native_lookup, board_lookup
from verify_tpi_index import lz77_decompress

FIELDS = ['clone', 'native_copy', 'native_length', 'scene', 'root', 'caller_lr', 'script_count']


def contracts(source):
    decoder = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
    result = {}
    for kind, entry, call, literal, root in [
        ('native-NPC', 0x0804F764, 0x0804F76E, 0x4F78C, 0x02039800),
        ('field-board', 0x0806A4FC, 0x0806A502, 0x6A50C, 0x0203C800),
    ]:
        decoded = list(decoder.disasm(source[call-0x08000000:call-0x08000000+4], call))
        if len(decoded) != 1 or decoded[0].size != 4 or decoded[0].mnemonic != 'bl' or decoded[0].op_str != '#0x804fb4c':
            raise ValueError('037 source BL applicability')
        if struct.unpack_from('<I', source, literal)[0] != root:
            raise ValueError('037 source root literal')
        result[kind] = dict(entry=entry, source_bl=call, caller_lr=(call+4)|1, root=root)
    npc = list(decoder.disasm(source[0x4F764:0x4F774], 0x0804F764))
    board = list(decoder.disasm(source[0x6A4FC:0x6A50A], 0x0806A4FC))
    if [(i.mnemonic, i.op_str) for i in npc] != [
        ('push','{r4, r5, r6, r7, lr}'),('tst','r1, r1'),('bne','#0x804f774'),
        ('adds','r1, r0, #0'),('ldr','r0, [pc, #0x1c]'),('bl','#0x804fb4c'),('pop','{r4, r5, r6, r7, pc}')]:
        raise ValueError('037 original cached NPC argument provider')
    if [(i.mnemonic, i.op_str) for i in board] != [
        ('push','{r4, r5, r6, r7, lr}'),('ldr','r0, [pc, #0xc]'),
        ('ldrb','r1, [r5, #4]'),('bl','#0x804fb4c'),('movs','r0, #0'),('pop','{r4, r5, r6, r7, pc}')]:
        raise ValueError('037 original board argument provider')
    return result


def source_population(source, selected):
    """Finite four-scene lookup population, typed root and exact byte identity."""
    abi = contracts(source)
    pool = []
    for kind, lookup in [('native-NPC', native_lookup(source)), ('field-board', board_lookup(source))]:
        for archive, refs in lookup.items():
            payload = lz77_decompress(source, int(archive, 16))[0]
            for ref in refs:
                pool.append(dict(archive=archive, source_class=kind, payload=payload, **ref, caller_lr=abi[kind]['caller_lr']))
    for archive, expected in selected.items():
        found = [r for r in pool if r['archive'] == archive and r['source_class'] == expected['source_class'] and r['scene'] == expected['scene']]
        if len(found) != 1:
            raise ValueError('037 selected source typed lookup uniqueness')
        chosen = found[0]
        for other in pool:
            if (other['scene'], other['root'], other['caller_lr']) != (chosen['scene'], chosen['root'], chosen['caller_lr']) or other['archive'] == archive:
                continue
            n = min(len(chosen['payload']), len(other['payload']))
            if chosen['payload'][:n] == other['payload'][:n]:
                peer = selected.get(other['archive'])
                # Exact native aliases are safe only when all owners are in
                # this cohort and compile to the exact same complete target.
                if chosen['payload'] != other['payload'] or peer is None or not expected.get('target_sha256') or (peer.get('target_sha256'),peer.get('script_count')) != (expected['target_sha256'],expected['script_count']):
                    raise ValueError('037 native identity ambiguous within typed scene')
    return pool


def wrap(source, address, previous_entry, table, count):
    abi = contracts(source)
    if type(count) is not int or not 1 <= count <= 255:
        raise ValueError('037 descriptor counter range')
    if any(type(x) is not int or x & 3 for x in (address, table)) or not 0x08000000 <= table < table+count*28 <= address < 0x0A000000 or not 0x08000000 <= previous_entry < 0x0A000000:
        raise ValueError('037 code/descriptor placement')
    code = '''pop {r3}
push {r0,r1,r2,r3,r4,r5,r6,r7}
mov r2,lr
ldr r3,npc_caller
cmp r2,r3
bne board_gate
ldr r3,npc_root
cmp r0,r3
bne fallback
b script_gate
board_gate:
ldr r3,board_caller
cmp r2,r3
bne fallback
ldr r3,board_root
cmp r0,r3
bne fallback
script_gate:
lsrs r2,r1,#8
bne fallback
mov r2,r10
ldr r2,[r2,#64]
ldrb r3,[r2,#4]
lsls r7,r3,#8
adds r7,#COUNT
ldr r3,descriptors
candidate:
mov r2,lr
ldr r4,[r3,#20]
cmp r2,r4
bne next
ldr r4,[r3,#16]
cmp r0,r4
bne next
ldr r2,[sp,#4]
ldr r4,[r3,#24]
cmp r2,r4
bhs next
lsrs r2,r7,#8
ldr r4,[r3,#12]
cmp r2,r4
bne next
movs r1,r0
ldr r5,[r3,#4]
ldr r6,[r3,#8]
compare:
ldrb r2,[r1]
ldrb r4,[r5]
cmp r2,r4
bne next
adds r1,#1
adds r5,#1
subs r6,#1
bne compare
ldr r4,[r3,#0]
str r4,[sp,#0]
b fallback
next:
adds r3,#28
subs r7,#1
lsls r2,r7,#24
bne candidate
fallback:
pop {r0,r1,r2,r3,r4,r5,r6,r7}
push {r3}
ldr r3,previous
bx r3'''.replace('COUNT', str(count))
    blob, proof = assemble_verified(code, address, dict(descriptors=table, previous=previous_entry|1, npc_caller=abi['native-NPC']['caller_lr'], npc_root=abi['native-NPC']['root'], board_caller=abi['field-board']['caller_lr'], board_root=abi['field-board']['root']))
    return blob, dict(proof=proof, contracts=abi, descriptor_slots=count, descriptor_bytes=28,
        descriptor_fields=FIELDS, comparison='actual caller LR, native root, unsigned script bound, scene, every native payload byte',
        scene_read_once=True, mutable_time_or_sub_used=False, persistent_ram_bytes=0, stack_bytes=32,
        predecessor_contract='Original r3 on stack; predecessor wrapper entry, not installation stub',
        analysis_only=True, runtime_tested=False)
