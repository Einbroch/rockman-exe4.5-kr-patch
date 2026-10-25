"""Read-only inspection of native moving OBJ masks at one retained close."""
import struct
from PIL import Image
from build_visibility_poc import ROOT

def inspect():
    p=ROOT/'poc/runtime/roll-escape-v1-roll-confirm-sample';stem='step_008'
    o=(p/(stem+'_gbaSpriteRam.bin')).read_bytes();v=(p/(stem+'_gbaVideoRam.bin')).read_bytes();pal=(p/(stem+'_gbaPaletteRam.bin')).read_bytes()
    baseline=Image.open(ROOT/'poc/runtime/roll-escape-v1-battle-tutorial-complete/step_104.png').convert('RGB');shot=Image.open(p/(stem+'.png')).convert('RGB')
    color=(248,236,212);delta={(x,y) for x in range(52,236) for y in range(110,138) if (shot.getpixel((x,y))==color)!=(baseline.getpixel((x,y))==color)}
    sizes={0:[(8,8),(16,16),(32,32),(64,64)],1:[(16,8),(32,8),(32,16),(64,32)],2:[(8,16),(8,32),(16,32),(32,64)]}
    hits={};counts={}
    for i in range(128):
        a0,a1,a2=struct.unpack_from('<HHH',o,i*8)
        if a0&0x300 or a0&0x2000 or a0>>14>=3:continue
        w,h=sizes[a0>>14][a1>>14];x=a1&511;y=a0&255
        for xx,yy in delta:
            if not(x<=xx<x+w and y<=yy<y+h):continue
            px=xx-x;py=yy-y
            if a1&0x1000:px=w-1-px
            if a1&0x2000:py=h-1-py
            tile=(a2&1023)+(py//8)*(w//8)+px//8
            bt=v[0x10000+tile*32+(py%8)*4+(px%8)//2];role=(bt>>(4*(px%2)))&15
            if not role:continue
            raw=struct.unpack_from('<H',pal,0x200+(a2>>12)*32+role*2)[0]
            hits.setdefault((xx,yy),[]).append((i,role,hex(raw)))
            key=(i,role,hex(raw),shot.getpixel((xx,yy)));counts[key]=counts.get(key,0)+1
    print('delta',len(delta),'covered opaque OBJ',len(hits),'uncovered',sorted(delta-hits.keys())[:10])
    print('counts',counts)
    return delta,hits

if __name__=='__main__':inspect()
