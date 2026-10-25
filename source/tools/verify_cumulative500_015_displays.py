"""Six pages and the empty portrait region of the native msgOpen-only script."""
from PIL import Image
import verify_cumulative500_007_displays as verify
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from cumulative_batch500_015 import OUT
verify.STEM='exe45_ko_development_pending500_015_v1'
verify.PREFIX='pending500-015-v1'
verify.ASSET_FOLDER=OUT
verify.OUTPUT_DIR='analysis/pending500_015_v1'
# Both actual native initializer paths supplied52/110; world retains msgOpen
# without an inferred portrait. Independent font/pixel/clearing checks follow.
verify.CASES=[('tutorial','768800',2,13,(2,4,6,8),(52,110)),('world','7C9C44',0,23,(2,4),(52,110))]
verify.REQUIRE_CLEARING=True
def main():
    rp=ROOT/f'poc/output/{verify.STEM}.gba';m=read(str(rp.with_suffix('.json').relative_to(ROOT)));require_hash(rp,m['output_sha256']);checks=[]
    for step in (2,4):
        path=ROOT/f'poc/runtime/{verify.PREFIX}-display-world/step_{step:03}.png';im=Image.open(path).convert('RGB');bg=im.getpixel((233,110));points=[(x,y) for x in range(12,52) for y in range(110,150)]
        if any(im.getpixel(p)!=bg for p in points):raise ValueError('Unexpected ink in portrait-free region')
        checks.append(dict(step=step,png_sha256=sha(path.read_bytes()),empty_left_region_pixels=len(points)))
    verify.main()
    frozen_write(ROOT/'analysis/pending500_015_v1/portrait_free_region.json',dict(passed=True,rom_sha256=m['output_sha256'],source_portrait_declared=False,native_origin_observed=[52,110],pages=checks,scope='Observed diagnostic native msgOpen-only pages; NOT original scene speaker identity or natural caller proof'))
if __name__=='__main__':main()
