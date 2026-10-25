"""Exact032 stale-ink checks after vertical cancel and anniversary page clear."""
from PIL import Image
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write


def main():
    m=read('poc/output/pending500_032_v1.json');require_hash(ROOT/'poc/output/pending500_032_v1.gba',m['output_sha256']);cases=[]
    for segment,step,rect in [('pending500-032-menu-cancel',2,(52,138,224,150)),('calendar-anniversary-032-product-delete-confirm-v1',2,(52,124,234,136))]:
        folder=ROOT/'poc/runtime'/segment;receipt=read(folder/'result.json');name=f'step_{step:03}.png';require_hash(folder/name,receipt['artifacts'][name])
        if not receipt['complete'] or receipt['rom_sha256']!=m['output_sha256']:raise ValueError('032 clear scene applicability')
        im=Image.open(folder/name).convert('RGB');bg=im.getpixel((233,124));x0,y0,x1,y1=rect
        if any(im.getpixel((x,y))!=bg for y in range(y0,y1) for x in range(x0,x1)):raise ValueError('032 stale option/title row ink '+segment)
        cases.append(dict(segment=segment,step=step,rectangle=list(rect),background=list(bg),pixels=(x1-x0)*(y1-y0),screenshot=dict(path=str((folder/name).relative_to(ROOT)),sha256=sha((folder/name).read_bytes())),stale_ink_absent=True))
    frozen_write(ROOT/'analysis/pending500_032_v1/calendar_clear_runtime.json',dict(schema=1,passed=True,rom_sha256=m['output_sha256'],cases=cases,checker=dict(path='tools/verify_calendar_clear_product_032.py',sha256=sha((ROOT/'tools/verify_calendar_clear_product_032.py').read_bytes())),release_eligible=False,limits='Exact current visible empty row rectangles only; cursor/glyph supply/branches and other states have separate reports.'))
    print('032 vertical-cancel and prior-ten-title row clearing PASS',sum(c['pixels'] for c in cases),'pixels')


if __name__=='__main__':main()
