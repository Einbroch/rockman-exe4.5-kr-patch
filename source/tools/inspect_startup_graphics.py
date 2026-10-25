"""Diagnostic 4bpp tile sheets, not translated game image assets."""
from pathlib import Path
from PIL import Image
from build_visibility_poc import ROOT
from verify_tpi_index import lz77_decompress
def main():
    rom=(ROOT/'Rockman EXE 4.5 Real Operation (J)(Independent).gba').read_bytes()
    out=ROOT/'analysis/startup_ui_v1/graphics_diagnostic';out.mkdir(parents=True,exist_ok=True)
    for at in [0x634270,0x63466C,0x634D88,0x63A4CC,0x63A71C]:
        p,_=lz77_decompress(rom,at);tiles=p[4:];n=len(tiles)//32;im=Image.new('RGB',(16*8,((n+15)//16)*8))
        for t in range(n):
            for y in range(8):
                for x in range(8):
                    v=(tiles[t*32+y*4+x//2]>>(4*(x%2)))&15
                    im.putpixel(((t%16)*8+x,(t//16)*8+y),((v*17,)*3))
        im.resize((im.width*3,im.height*3),Image.Resampling.NEAREST).save(out/f'{at:06X}.png')
if __name__=='__main__':main()
