"""Self-contained76-byte mixed replay HOST candidate; not game RAM/save ABI.

cap|baselinecount<<4, cursor|active<<4 (inactive15), keycount;
10 byte-aligned LE baseline words at3..22;70 six-bit keys at23..75;
last-byte high nibble B is a version marker, not key bits.
No external baseline. Movement/native writes/canonical B rebase all cells,
including sealed partial initials; jamo B removes one accepted key. Replay
recovers exact overwritten native cells and complete reference undo history.
This reduces persistent state but does NOT bound native temporary stack.
"""
import struct
from hangul_mixed_editor import MixedEditor, Snapshot
from hangul_keyboard_model import INITIALS, MEDIALS

SIZE = 76
VERSION = 0xB
KEYS = INITIALS + MEDIALS


class MixedReplay:
    def __init__(self, capacity):
        self.model = MixedEditor(capacity)
        self.baseline = self.model.state
        self.keys = []

    def _rebase(self):
        self.baseline = self.model.state
        self.keys = []

    def load(self, cells):
        self.model.load(cells)
        self._rebase()

    def press(self, key):
        if not self.model.press(key):
            return False
        self.keys.append(KEYS.index(key))
        return True

    def move(self, delta):
        if not self.model.move(delta):
            return False
        self._rebase()
        return True

    def write_native(self, token):
        if not self.model.write_native(token):
            return False
        self._rebase()
        return True

    def backspace(self):
        if not self.model.backspace():
            return False
        if self.keys:
            self.keys.pop()
        else:
            self._rebase()
        return True

    def candidate(self):
        return self.model.candidate()

    def serialize(self):
        self.model._validate(self.baseline)
        if len(self.keys) > 70 or any(type(k) != int or not 0 <= k < 40 for k in self.keys):
            raise ValueError('mixed replay keys')
        active = 15 if self.baseline.active is None else self.baseline.active
        header = bytes([self.model.capacity | (len(self.baseline.cells) << 4),
                        self.baseline.cursor | (active << 4), len(self.keys)])
        words = self.baseline.cells + (65535,) * (10 - len(self.baseline.cells))
        bits = sum(k << (6 * i) for i, k in enumerate(self.keys))
        result = header + struct.pack('<10H', *words) + (bits | (VERSION << 420)).to_bytes(53, 'little')
        decoded = self.restore(result)
        if (decoded.model.state, decoded.model.history) != (self.model.state, self.model.history):
            raise ValueError('mixed replay state/key drift')
        return result

    @classmethod
    def restore(cls, raw):
        if type(raw) != bytes or len(raw) != SIZE or raw[75] >> 4 != VERSION or raw[2] > 70:
            raise ValueError('mixed replay header/extent')
        cap, count = raw[0] & 15, raw[0] >> 4
        cursor, active = raw[1] & 15, raw[1] >> 4
        c = cls(cap)
        words = struct.unpack_from('<10H', raw, 3)
        if count > cap or any(w != 65535 for w in words[count:]):
            raise ValueError('mixed replay baseline padding/count')
        c.baseline = Snapshot(tuple(words[:count]), cursor, None if active == 15 else active)
        c.model._validate(c.baseline)
        c.model.state = c.baseline
        bits = int.from_bytes(raw[23:76], 'little') & ((1 << 420) - 1)
        if bits >> (raw[2] * 6):
            raise ValueError('mixed replay unused keys/bits')
        for i in range(raw[2]):
            key = (bits >> (6 * i)) & 63
            if key >= 40 or not c.press(KEYS[key]):
                raise ValueError('mixed replay rejected transition')
        return c


def apply(raw, action, value=None):
    c = MixedReplay.restore(raw)
    if action == 'jamo':
        accepted = c.press(value)
    elif action == 'move':
        accepted = c.move(value)
    elif action == 'native':
        accepted = c.write_native(value)
    elif action == 'backspace' and value is None:
        accepted = c.backspace()
    else:
        raise ValueError('mixed replay action')
    return (True, c.serialize()) if accepted else (False, raw)


def editor_candidate(ui, destination, compact):
    """96-byte placement candidate, not installed/native-layout compatible.

    Preserve existing16 UI bytes; move original+28 destination to+16;
    compact state occupies+20..95. Old+16/+20/+24 pointers and+28 destination
    consumers MUST be replaced together. No claim of complete UI reader audit.
    """
    if type(ui) != bytes or len(ui) != 16 or type(destination) != int or not 0 <= destination <= 0xFFFFFFFF:
        raise ValueError('editor candidate metadata')
    c = MixedReplay.restore(compact)
    if ui[4] != c.model.capacity:
        raise ValueError('editor candidate capacity mismatch')
    return ui + struct.pack('<I', destination) + compact
