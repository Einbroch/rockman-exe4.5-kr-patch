"""Experimental fixed-width record; NOT adopted native/save ABI.

Width 2*logical_limit+2, limit1..8. Byte0 = 0x80|occupied count,
little-endian syllable ranks in occupied words, FFFF in empty words,
final E5. Proposed marker range has NOT been proven safe in legacy consumers.
"""
from korean_codec import encode_hangul

def check_limit(limit):
    if type(limit)!=int or not 1<=limit<=8:raise ValueError('candidate limit')

def pack(text,limit):
    check_limit(limit)
    if type(text)!=str or not 1<=len(text)<=limit or any(not 0xac00<=ord(c)<=0xd7a3 for c in text):raise ValueError('complete nonempty Hangul only')
    return bytes([0x80|len(text)])+b''.join((ord(c)-0xac00).to_bytes(2,'little') for c in text)+b'\xff\xff'*(limit-len(text))+b'\xe5'

def unpack(record,limit):
    check_limit(limit)
    if type(record)!=bytes or len(record)!=2*limit+2:raise ValueError('candidate width')
    count=record[0]-0x80
    if not 1<=count<=limit or record[-1]!=0xe5:raise ValueError('candidate marker/count/terminator')
    chars=[]
    for slot in range(limit):
        rank=int.from_bytes(record[1+slot*2:3+slot*2],'little')
        if slot<count:
            if rank>=11172:raise ValueError('candidate occupied rank')
            chars.append(chr(0xac00+rank))
        elif rank!=0xffff:raise ValueError('candidate noncanonical empty slot')
    return ''.join(chars)

def display_bytes(record,limit):
    return encode_hangul(unpack(record,limit))+b'\xe5'
