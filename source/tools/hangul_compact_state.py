"""64-byte state candidate with external immutable baseline; NOT native RAM ABI.

Header4, ranks16, accepted selectors packed into42 bytes (56 six-bit keys),
baseline canonical-deletion count1, reserved zero1. No copy of the baseline.
Native replay may use temporary stack state, rather than276 persistent bytes.
The game must preserve the same baseline throughout edit/No/reentry until commit.
"""
import struct
from hangul_keyboard_model import Composer
from hangul_composer_thumb import KEYS,EMPTY,tail_rank

class CompactComposer:
    def __init__(self,limit,baseline=''):
        if type(limit)!=int or not 1<=limit<=8:raise ValueError('compact capacity')
        self.limit=limit;self.baseline=baseline;self.keys=[];self.deletions=0
        self.model=Composer(limit);self.model.load(baseline)
    def press(self,key):
        if len(self.keys)>=56 or not self.model.press(key):return False
        self.keys.append(KEYS.index(key));return True
    def backspace(self):
        if not self.model.backspace():return False
        if self.keys:self.keys.pop()
        else:self.deletions+=1
        if self.deletions>56:raise ValueError('canonical baseline deletion bound')
        return True
    def serialize(self):
        s=self.model.state;words=[ord(c)-0xac00 for c in s.committed]+([] if s.l is None else [tail_rank(s)])
        key_bits=sum(key<<(index*6) for index,key in enumerate(self.keys))
        return bytes([len(words),self.limit,len(self.keys),int(s.l is not None)])+struct.pack('<8H',*(words+[EMPTY]*(8-len(words))))+key_bits.to_bytes(42,'little')+bytes([self.deletions,0])
    @classmethod
    def restore(cls,raw,baseline):
        if type(raw)!=bytes or len(raw)!=64 or raw[2]>56 or raw[62]>56 or raw[63]!=0:raise ValueError('compact structure')
        c=cls(raw[1],baseline)
        for _ in range(raw[62]):
            if not c.backspace():raise ValueError('excess baseline deletions')
        bits=int.from_bytes(raw[20:62],'little')
        for index in range(raw[2]):
            key=(bits>>(index*6))&63
            if key>=40 or not c.press(KEYS[key]):raise ValueError('invalid replay selector')
        if c.serialize()!=raw:raise ValueError('noncanonical keys/header/rank/padding')
        return c

    @property
    def display(self):return self.model.display
    def candidate(self):return self.model.candidate()
