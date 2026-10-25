"""Separate observed native Metool OBJ flash from dialogue background clearing."""
import struct
from PIL import Image
from build_visibility_poc import ROOT,sha
from report_chip_library_runtime import require

SIZES={0:[(8,8),(16,16),(32,32),(64,64)],1:[(16,8),(32,8),(32,16),(64,32)],2:[(8,16),(8,32),(16,32),(32,64)]}

def frontmost_obj(p,stem,point):
    o=(p/(stem+'_gbaSpriteRam.bin')).read_bytes();v=(p/(stem+'_gbaVideoRam.bin')).read_bytes();pal=(p/(stem+'_gbaPaletteRam.bin')).read_bytes()
    io=(p/(stem+'_display_io.bin')).read_bytes();require(struct.unpack_from('<H',io)[0]&64,'native flash requires OBJ1D')
    xx,yy=point;hits=[]
    for i in range(128):
        a0,a1,a2=struct.unpack_from('<HHH',o,i*8)
        if a0&0x300 or a0&0x2000 or a0>>14>=3:continue
        w,h=SIZES[a0>>14][a1>>14];x=a1&511;y=a0&255
        if not(x<=xx<x+w and y<=yy<y+h):continue
        px=xx-x;py=yy-y
        if a1&0x1000:px=w-1-px
        if a1&0x2000:py=h-1-py
        tile=(a2&1023)+(py//8)*(w//8)+px//8
        bt=v[0x10000+tile*32+(py%8)*4+(px%8)//2];role=(bt>>(4*(px%2)))&15
        if not role:continue
        bank=a2>>12;raw=struct.unpack_from('<H',pal,0x200+bank*32+role*2)[0]
        hits.append({'index':i,'priority':(a2>>10)&3,'palette':bank,'raw_color':raw,'role':role,'rect':[x,y,w,h]})
    require(hits,'clear delta has no native opaque OBJ')
    return min(hits,key=lambda h:(h['priority'],h['index']))

def verify_background_mask(p,step,mask,baseline_mask):
    if mask==baseline_mask:return {'full_mask_match':True,'native_obj_delta_pixels':0}
    require(p.name=='roll-escape-v1-roll-confirm-sample' and step==8,'unclassified clear mask change')
    require(baseline_mask<=mask,'baseline native cream pixels disappeared')
    delta=mask-baseline_mask;require(len(delta)==130,'retained native flash delta changed')
    # Baseline69 are native HP-label OBJ7/palette14, not body palette1.
    # Independently calibrate body67FF on65 pixels above the dialogue ROI.
    shot=Image.open(p/f'step_{step:03d}.png').convert('RGB');calibration=[]
    for x in range(158,191):
        for y in range(95,110):
            try:h=frontmost_obj(p,f'step_{step:03d}',(x,y))
            except ValueError:continue
            if h['index'] in (14,16) and h['palette']==1 and h['raw_color']==0x67FF:
                require(shot.getpixel((x,y))==(248,236,212),'native sprite outside-ROI color calibration')
                calibration.append((x,y))
    require(len(calibration)==65,'native calibration denominator')
    owners={}
    for point in delta:
        h=frontmost_obj(p,f'step_{step:03d}',point)
        require(h['index'] in (14,16) and h['palette']==1 and h['raw_color']==0x67FF,'delta not calibrated native Metool foreground')
        owners[str(h['index'])]=owners.get(str(h['index']),0)+1
    return {'full_mask_match':False,'outside_native_obj_mask_matches':True,'native_obj_delta_pixels':len(delta),'frontmost_obj_owners':owners,
        'native_palette':1,'native_raw_color':0x67FF,'observed_rgb':[248,236,212],'outside_dialogue_roi_calibration_pixels':len(calibration),
        'delta_bbox':[min(x for x,y in delta),min(y for x,y in delta),max(x for x,y in delta),max(y for x,y in delta)],
        'oam_sha256':sha((p/f'step_{step:03d}_gbaSpriteRam.bin').read_bytes()),'palette_sha256':sha((p/f'step_{step:03d}_gbaPaletteRam.bin').read_bytes()),
        'scope':'130 added cream pixels are native frontmost opaque Metool OBJ14/16 palette1/color67FF, calibrated by65 independent pixels above dialogue ROI in this frame. Baseline69 HP-label pixels unchanged; not ignored text, independent color-pipeline proof, or full battlefield equality.'}
