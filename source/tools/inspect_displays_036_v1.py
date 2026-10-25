"""Derived screenshot gallery and raw current-page state, not a QA pass."""
import struct
from PIL import Image,ImageDraw
from build_visibility_poc import ROOT
from cumulative_batch500 import read

def main():
    items=[]
    for case,steps in [('a0',[3,5,6]),('a1',[3,5,7,8,9,11]),('a3',[3,5,6,7,8,9])]:
        d=ROOT/('poc/runtime/pending500-036-v1-display-'+case)
        for step in steps:
            p=f'step_{step:03}';r=(d/(p+'_gbaExtWorkRam.bin')).read_bytes();o=(d/(p+'_gbaSpriteRam.bin')).read_bytes();a,b,k=struct.unpack_from('<3H',o)
            print(case,step,'ptr/root',*[hex(x) for x in struct.unpack_from('<2I',r,0xFA4C)],'origin',tuple(r[0xFA38:0xFA3A]),'cursor',b&511,a&255,hex(k),'flags',r[0xFA20:0xFA24].hex())
            items.append((case,step,Image.open(d/(p+'.png')).convert('RGB')))
    out=ROOT/'analysis/pending500_036_v1/diagnostic_contact_v1.png'
    if out.exists():raise ValueError('preserve gallery')
    sheet=Image.new('RGB',(960,180*((len(items)+3)//4)),'#20232a');draw=ImageDraw.Draw(sheet)
    for i,(case,step,im) in enumerate(items):
        x,y=i%4*240,i//4*180;sheet.paste(im,(x,y+20));draw.text((x+3,y+3),case+' '+str(step),fill='white')
    sheet.save(out)

if __name__=='__main__':main()
