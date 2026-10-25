"""Caller-selected fixed-width mixed committed-record CANDIDATE, not save ABI.

Preserves old pure-Hangul candidate bytes; extends cap1..10/native identities.
Width2*cap+2: marker80|nonempty count, capLE words, finalE5. Occupied words
complete ranks0..11171 or structural native tags8000..80E3/8100..81FF;
emptyFFFF. Partials forbidden. Marker is NOT proven legacy discrimination.
Neither automatic format detection nor native save migration is implemented.
"""
import struct
from hangul_mixed_display import display,CODE as DISPLAY
from hangul_mixed_replay_state import MixedReplay
from hangul_mixed_cache_bridge import scoped
from hangul_mixed_keyedit_thumb import assemble as assemble_code


def pack_surface(raw):
    display(raw,1)  # validates entire surface and rejects all partials/empty.
    count,cap=raw[:2]
    return bytes([0x80|count])+raw[4:4+2*cap]+b'\xE5'


def unpack_selected_record(record,cap):
    if type(cap)!=int or not 1<=cap<=10 or type(record)!=bytes or len(record)!=2*cap+2:
        raise ValueError('selected mixed record extent/capacity')
    count=record[0]-0x80
    if not 1<=count<=cap or record[-1]!=0xE5:raise ValueError('selected marker/count/terminator')
    words=struct.unpack_from('<'+'H'*cap,record,1)
    raw=bytes([count,cap,0,255])+struct.pack('<10H',*(words+(65535,)*(10-cap)))
    display(raw,1)
    c=MixedReplay(cap);c.load(words[:count])
    return c.serialize()


def surface_from_compact(raw):
    c=MixedReplay.restore(raw);s=c.model.state
    return bytes([len(s.cells),c.model.capacity,s.cursor,255 if s.active is None else s.active])+struct.pack('<10H',*(s.cells+(65535,)*(10-len(s.cells))))


# r0surface24,r1record,r2inputAvailable low16|outputAvailable high16,r3=0.
# Returns fixed record width or0, failure no external writes. r4..r11/SP
# preserved. Own60+display36=96 stack, byte alignment supported.
# Caller owns disjoint source/output/stack; encoding/table/glyph membership and
# original normalize/commit/reader/save hooks are NOT adopted by this helper.
ENCODE='''push {r4, r5, r6, lr}
sub sp, #44
movs r4, r0
movs r5, r1
cmp r3, #0
bne record_fail
lsls r0, r2, #16
lsrs r0, r0, #16
cmp r0, #24
blo record_fail
movs r0, r4
adds r0, #24
cmp r0, r4
blo record_fail
ldrb r6, [r4, #1]
cmp r6, #1
blo record_fail
cmp r6, #10
bhi record_fail
lsls r1, r6, #1
adds r1, #2
lsrs r2, r2, #16
cmp r2, r1
blo record_fail
adds r1, r1, r5
cmp r1, r5
blo record_fail
cmp r4, r1
bhs record_disjoint
cmp r5, r0
blo record_fail
record_disjoint:
movs r0, r4
mov r1, sp
movs r2, #41
movs r3, #1
bl record_validate
cmp r0, #0
beq record_fail
ldrb r0, [r4]
adds r0, #128
strb r0, [r5]
lsls r6, r6, #1
movs r3, #0
record_words:
adds r0, r3, #4
ldrb r1, [r4, r0]
adds r0, r3, #1
strb r1, [r5, r0]
adds r3, #1
cmp r3, r6
blo record_words
adds r0, r6, #1
movs r1, #229
strb r1, [r5, r0]
adds r0, r6, #2
b record_return
record_fail:
movs r0, #0
record_return:
add sp, #44
pop {r4, r5, r6, pc}
record_validate:
'''+scoped(DISPLAY,'rec_display_')


def assemble_encoder(address=0x08F04000):
    return assemble_code(address,ENCODE)
