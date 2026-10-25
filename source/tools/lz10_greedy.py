"""Bounded deterministic BIOS type10 compressor; not canonical source encoding."""
from verify_tpi_index import lz77_decompress

def encode(payload,*,output_limit,stored_limit):
    if not 0<len(payload)<=min(output_limit,0xFFFFFF):raise ValueError('LZ10 output budget')
    out=bytearray(b'\x10'+len(payload).to_bytes(3,'little'));at=0
    while at<len(payload):
        flag_at=len(out);out.append(0);flags=0
        for bit in range(7,-1,-1):
            if at==len(payload):break
            best=0;distance=0
            for start in range(at-1,max(-1,at-4097),-1):
                if payload[start]!=payload[at]:continue
                length=1
                while length<min(18,len(payload)-at) and payload[start+length]==payload[at+length]:length+=1
                if length>best:best=length;distance=at-start
                if best==18:break
            if best>=3:
                disp=distance-1;out.extend([((best-3)<<4)|(disp>>8),disp&255]);flags|=1<<bit;at+=best
            else:out.append(payload[at]);at+=1
        out[flag_at]=flags
    out.extend(b'\0'*(-len(out)%4))
    if len(out)>stored_limit:raise ValueError(f'LZ10 stored budget: {len(out)} > {stored_limit}')
    decoded,used=lz77_decompress(bytes(out),0)
    if decoded!=payload or used>len(out) or any(out[used:]):raise ValueError('independent LZ10 roundtrip/padding')
    return bytes(out)
