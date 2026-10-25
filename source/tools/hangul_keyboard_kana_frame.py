"""Two-jamo-page navigation adapter, CPU fixture addresses only."""
from extended_dialogue import assemble_verified
from hangul_keyboard_frame_adapters import assemble as original_adapters


def assemble():
    blobs = original_adapters()
    code, isa = assemble_verified('''ldrb r1, [r5, #8]
cmp r1, #1
bhi native_navigation
ldrb r1, [r5, #7]
cmp r1, #2
bne native_navigation
ldrb r1, [r5, #6]
cmp r1, #6
beq retain_jamo
cmp r1, #8
beq retain_jamo
native_navigation:
ldr r3, original
bx r3
retain_jamo:
bx lr
''',0x08305300,dict(original=0x08035087))
    return [b if b[3]!='navigation.bin' else (0x08305300,code,isa,'navigation.bin') for b in blobs]
