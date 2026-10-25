"""Exact LZ10 token DP including flag-byte state; deterministic lossless data."""
def encode(data,*,stored_limit):
    n=len(data);matches=[]
    for i in range(n):
        maximum=0;offset=0;start=max(0,i-4096);end=i
        if i+3<=n:
            while True:
                j=data.rfind(data[i:i+3],start,end)
                if j<0:break
                length=3
                while length<18 and i+length<n and data[j+length]==data[i+length]:length+=1
                if length>maximum:maximum,offset=length,i-j
                if maximum==min(18,n-i):break
                end=j
        matches.append((maximum,offset))
    cost=[[0]*8 for _ in range(n+1)];choice=[[1]*8 for _ in range(n)]
    for i in range(n-1,-1,-1):
        maximum,_=matches[i]
        for slot in range(8):
            following=(slot+1)%8;flag=int(slot==0);best=1+flag+cost[i+1][following];selected=1
            for length in range(3,maximum+1):
                value=2+flag+cost[i+length][following]
                if value<=best:best,selected=value,length
            cost[i][slot]=best;choice[i][slot]=selected
    out=bytearray(b'\x10'+n.to_bytes(3,'little'));i=0
    while i<n:
        flag_at=len(out);out.append(0)
        for slot in range(8):
            if i>=n:break
            length=choice[i][slot]
            if length==1:out.append(data[i])
            else:
                out[flag_at]|=128>>slot
                value=((length-3)<<12)|(matches[i][1]-1);out.extend(value.to_bytes(2,'big'))
            i+=length
    if len(out)!=4+cost[0][0] or len(out)>stored_limit:raise ValueError(f'optimal LZ10 budget {len(out)} > {stored_limit}')
    return bytes(out)
