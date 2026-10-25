"""Normal equipment60..62/70..75 guarded clone wrapper; no RAM/pointer growth."""
import struct
from extended_dialogue import assemble_verified
from build_visibility_poc import sha
from verify_tpi_index import lz77_decompress

POOLS={2:0x6E1554,5:0x6E1CC0,7:0x6E21B0}
SCRIPTS=[60,61,62,70,71,72,73,74,75]


def wrap(source,address,prior_entry,guards):
    if source[0x4F7B8:0x4F7BC]!=bytes.fromhex('00f0c8f9') or source[0xCEC:0xCF4]!=bytes.fromhex('5046006c4078f746'):
        raise ValueError('Native normal call/Navi query changed')
    if len(guards)!=3 or {g['navi_index'] for g in guards}!=set(POOLS):raise ValueError('Equipment scope')
    for g in guards:
        if set(g)!={'clone_address','payload_bytes','navi_index','guard_header_hex','guard_tail_hex'}:raise ValueError('Equipment guard schema')
        index=g['navi_index'];at=POOLS[index]
        if struct.unpack_from('<I',source,0x3C5BC+index*4)[0]!=0x08000000+at:raise ValueError('Equipment pool pointer identity')
        native=lz77_decompress(source,at)[0]
        if g['guard_header_hex']!=native[:16].hex() or g['guard_tail_hex']!=native[136:152].hex() or int.from_bytes(native[:2],'little')!=152:
            raise ValueError('Equipment native table identity')
        if not 152<=g['payload_bytes']<=65535 or g['clone_address']&3 or not 0x08000000<=g['clone_address']<g['clone_address']+g['payload_bytes']<=address:
            raise ValueError('Equipment clone placement')
    # All rejection branches have local conditionals plus Thumb-1 long B.
    # r0 changes only for a validated source pool + Navi + normal script.
    code='''pop {r3}
push {r2,r3,r4}
mov r2,lr
ldr r3,root
cmp r0,r3
beq root_ok
b reject
root_ok:
ldr r3,caller
cmp r2,r3
beq call_ok
b reject
call_ok:
movs r3,#255
ands r3,r1
cmp r3,r1
beq unsigned_ok
b reject
unsigned_ok:
cmp r1,#75
ble bound_ok
b reject
bound_ok:
cmp r1,#60
bge lower_ok
b reject
lower_ok:
cmp r1,#62
ble script_ok
cmp r1,#70
bge script_ok
b reject
script_ok:
mov r4,r10
ldr r4,[r4,#64]
ldrb r2,[r4,#1]
'''
    values=dict(root=0x0202BA7C,caller=0x0804F7BD,previous=prior_entry|1)
    for j,g in enumerate(sorted(guards,key=lambda g:g['navi_index'])):
        code+=f"cmp r2,#{g['navi_index']}\nbne next{j}\n"
        for i in range(4):
            code+=f'ldr r3,[r0,#{i*4}]\nldr r4,h{j}_{i}\ncmp r3,r4\nbeq h_ok{j}_{i}\nb reject\nh_ok{j}_{i}:\n'
            values[f'h{j}_{i}']=struct.unpack_from('<I',bytes.fromhex(g['guard_header_hex']),i*4)[0]
        code+='movs r4,r0\nadds r4,#136\n'
        for i in range(4):
            code+=f'ldr r3,[r4,#{i*4}]\nldr r2,t{j}_{i}\ncmp r3,r2\nbeq t_ok{j}_{i}\nb reject\nt_ok{j}_{i}:\n'
            values[f't{j}_{i}']=struct.unpack_from('<I',bytes.fromhex(g['guard_tail_hex']),i*4)[0]
        code+=f'ldr r0,clone{j}\nb reject\nnext{j}:\n';values[f'clone{j}']=g['clone_address']
    code+='reject:\npop {r2,r3,r4}\npush {r3}\nldr r3,previous\nbx r3'
    payload,proof=assemble_verified(code,address,values)
    return payload,dict(proof=proof,scope='Normal reader caller0804F7BD/root0202BA7C/scripts60..62/70..75 only; Navi+first16/last16 native table guards; source RAM and fixed/numeric paths retained',
        guards=guards,source_navi_query_sha256=sha(source[0xCEC:0xCF4]),persistent_ram_bytes=0)
