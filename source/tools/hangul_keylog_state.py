"""64-byte key-log candidate supporting native calendar capacity10.

No cached ranks: replay into temporary composer before editing/display.
Byte0 versionA1, byte1 limit1..10, byte2 key count0..70, byte3 baseline
canonical deletions0..70. Bytes4..56 =70 six-bit keys (420 of424 bits),
bytes57..63 reserved0. External unchanged baseline remains necessary.
This is a host contract only; no game memory/CPU adoption.
"""
from hangul_keyboard_model import Composer, INITIALS, MEDIALS

KEYS = INITIALS + MEDIALS
MAX_KEYS = 70
VERSION = 0xA1


class KeylogComposer:
    def __init__(self, limit, baseline=''):
        if type(limit) != int or not 1 <= limit <= 10:
            raise ValueError('keylog capacity')
        self.limit = limit
        self.baseline = baseline
        self.keys = []
        self.deletions = 0
        self.model = Composer(limit)
        self.model.load(baseline)

    def press(self, key):
        if len(self.keys) >= MAX_KEYS or not self.model.press(key):
            return False
        self.keys.append(KEYS.index(key))
        return True

    def backspace(self):
        if not self.model.backspace():
            return False
        if self.keys:
            self.keys.pop()
        else:
            self.deletions += 1
        if self.deletions > MAX_KEYS:
            raise ValueError('baseline deletion bound')
        return True

    def serialize(self):
        bits = sum(key << (i * 6) for i, key in enumerate(self.keys))
        return bytes([VERSION, self.limit, len(self.keys), self.deletions]) + bits.to_bytes(53, 'little') + bytes(7)

    @classmethod
    def restore(cls, raw, baseline):
        if (type(raw) != bytes or len(raw) != 64 or raw[0] != VERSION or raw[2] > MAX_KEYS
                or raw[3] > MAX_KEYS or raw[56] & 0xF0 or raw[57:] != bytes(7)):
            raise ValueError('keylog structure')
        c = cls(raw[1], baseline)
        for _ in range(raw[3]):
            if not c.backspace():
                raise ValueError('excess baseline deletion')
        bits = int.from_bytes(raw[4:57], 'little')
        for i in range(raw[2]):
            key = (bits >> (i * 6)) & 63
            if key >= len(KEYS) or not c.press(KEYS[key]):
                raise ValueError('invalid keylog replay')
        if c.serialize() != raw:
            raise ValueError('unused packed keys')
        return c

    @property
    def display(self):
        return self.model.display

    def candidate(self):
        return self.model.candidate()
