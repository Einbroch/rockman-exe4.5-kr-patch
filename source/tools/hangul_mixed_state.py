"""Fixed-width mixed editor/undo HOST codec candidate; NOT game allocation/save ABI.

588 bytes: B1/cap/count/cursor/active/depth/reserved16 +10 LE words;
70 eight-byte undo deltas: prior count/cursor/active/reserved +2 old words.
Inactive cells use FFFF, inactive history bytes use zero. Each delta restores
the at-most-two overwritten cells, including native values, before a jamo.
Decode verifies that every link can be an accepted jamo transition.
"""
import struct
from hangul_mixed_editor import MixedEditor, Snapshot
from hangul_keyboard_model import INITIALS, MEDIALS

SIZE = 588
HEADER = 28
VERSION = 0xB1
EMPTY = 0xFFFF
KEYS = INITIALS + MEDIALS


def active_byte(active):
    return 0xFF if active is None else active


def checked(cap, state):
    m = MixedEditor(cap)
    m._validate(state)
    return m


def restore(cap, after, entry):
    count, cursor, active, reserved, first, second = struct.unpack('<BBBBHH', entry)
    if reserved or count > cap:
        raise ValueError('undo header')
    active = None if active == 0xFF else active
    p = cursor if active is None else active
    if not 0 <= p <= count or p >= cap:
        raise ValueError('undo position')
    cells = list(after.cells[:count])
    if len(cells) != count:
        raise ValueError('undo count')
    for offset, word in enumerate((first, second)):
        i = p + offset
        if i < count:
            cells[i] = word
        elif word != EMPTY:
            raise ValueError('undo unused word')
    prior = Snapshot(tuple(cells), cursor, active)
    m = checked(cap, prior)
    # This is semantic validation, not just structural acceptance of forged
    # snapshots. No destination writes occur before the entire chain passes.
    for key in KEYS:
        m.state = prior
        m.history = []
        if m.press(key) and m.state == after:
            return prior
    raise ValueError('undo is not an accepted jamo transition')


def unpack(blob):
    if type(blob) != bytes or len(blob) != SIZE:
        raise ValueError('mixed state extent/type')
    version, cap, count, cursor, active, depth, reserved = struct.unpack_from('<BBBBBBH', blob)
    if version != VERSION or reserved or depth > 70 or count > cap:
        raise ValueError('mixed state header')
    words = struct.unpack_from('<10H', blob, 8)
    if any(w != EMPTY for w in words[count:]):
        raise ValueError('mixed state unused cells')
    current = Snapshot(tuple(words[:count]), cursor, None if active == 0xFF else active)
    m = checked(cap, current)
    if depth and current.active is None:
        raise ValueError('history without active composition')
    if any(blob[HEADER + depth * 8:]):
        raise ValueError('mixed state unused history')
    reverse = []
    after = current
    for i in range(depth - 1, -1, -1):
        after = restore(cap, after, blob[HEADER + i * 8:HEADER + (i + 1) * 8])
        reverse.append(after)
    m.state = current
    m.history = list(reversed(reverse))
    return m


def pack(m):
    checked(m.capacity, m.state)
    if len(m.history) > 70:
        raise ValueError('mixed history capacity')
    s = m.state
    out = bytearray(SIZE)
    struct.pack_into('<BBBBBBH', out, 0, VERSION, m.capacity, len(s.cells), s.cursor,
                     active_byte(s.active), len(m.history), 0)
    struct.pack_into('<10H', out, 8, *(s.cells + (EMPTY,) * (10 - len(s.cells))))
    for i, prior in enumerate(m.history):
        checked(m.capacity, prior)
        p = prior.cursor if prior.active is None else prior.active
        old = tuple(prior.cells[j] if j < len(prior.cells) else EMPTY for j in (p, p + 1))
        struct.pack_into('<BBBBHH', out, HEADER + i * 8, len(prior.cells), prior.cursor,
                         active_byte(prior.active), 0, *old)
    result = bytes(out)
    decoded = unpack(result)
    if (decoded.state, decoded.history) != (m.state, m.history):
        raise ValueError('mixed state roundtrip')
    return result


def apply(blob, action, value=None):
    """Atomic host transaction: rejected action returns the identical bytes.

    Invalid serialized input raises before any output; action is not a native
    handler ABI. Successful actions return fully revalidated candidate bytes.
    """
    m = unpack(blob)
    if action == 'jamo':
        accepted = m.press(value)
    elif action == 'move':
        accepted = m.move(value)
    elif action == 'native':
        accepted = m.write_native(value)
    elif action == 'backspace' and value is None:
        accepted = m.backspace()
    else:
        raise ValueError('mixed action')
    return (True, pack(m)) if accepted else (False, blob)
