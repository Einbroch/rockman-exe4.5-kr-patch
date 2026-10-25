"""Build a distribution package (BPS + xdelta) from the immutable original to a built product ROM.

Usage: make_release_patch_v1.py PRODUCT_ROM NAME
Creates patches/NAME/{NAME.bps,NAME.xdelta,ApplyPatch.ps1,ApplyXdelta.ps1,LICENSE-font.txt,README.ko.md,
verification.json} and patches/NAME.zip. Verifies byte-identical application (both formats), determinism,
wrong-source and corrupt-patch rejection, and that the original ROM is unchanged. Never overwrites.
"""
import hashlib,json,shutil,subprocess,sys,zipfile,tempfile
from pathlib import Path
from build_visibility_poc import ROOT

FLIPS=ROOT/'external/flips-v198/bin/flips.exe'
XDELTA=ROOT/'external/xdelta3-v3.2.2/bin/xdelta3-3.2.2-windows-x86_64/xdelta3.exe'
PREV=ROOT/'patches/exe45_ko_development_news_mail_20261013'


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def run(cmd):
    r=subprocess.run([str(c) for c in cmd],capture_output=True,text=True);return r.returncode,r.stdout.strip(),r.stderr.strip()


def main():
    product,name=Path(ROOT/sys.argv[1]),sys.argv[2];cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'))
    source=ROOT/cfg['source_profile']['filename'];src_sha=sha(source)
    if src_sha!=cfg['source_profile']['sha256']:raise SystemExit('source ROM hash differs')
    meta=json.loads(product.with_suffix('.json').read_text(encoding='utf8'))
    if sha(product)!=meta['output_sha256']:raise SystemExit('product hash differs from its build metadata')
    out=ROOT/'patches'/name
    if out.exists() or (ROOT/'patches'/(name+'.zip')).exists():raise SystemExit('Preserve existing package '+name)
    out.mkdir(parents=True);bps=out/(name+'.bps');xd=out/(name+'.xdelta')
    tmp=Path(tempfile.mkdtemp(prefix='exe45rel_'))
    try:
        rc=run([FLIPS,'--create','--bps',source,product,bps])
        if rc[0]!=0 or not bps.exists():raise SystemExit('flips create failed: '+str(rc))
        rc=run([XDELTA,'-e','-a','-A','-S','none','-9','-s',source,product,xd])
        if rc[0]!=0:raise SystemExit('xdelta create failed: '+str(rc))
        # determinism
        rc=run([FLIPS,'--create','--bps',source,product,tmp/'again.bps']);rc2=run([XDELTA,'-e','-a','-A','-S','none','-9','-s',source,product,tmp/'again.xdelta'])
        deterministic=(sha(tmp/'again.bps')==sha(bps),sha(tmp/'again.xdelta')==sha(xd))
        # application
        run([FLIPS,'--apply','--exact',bps,source,tmp/'a.gba']);run([XDELTA,'-d','-s',source,xd,tmp/'b.gba'])
        applied=(sha(tmp/'a.gba')==meta['output_sha256'],sha(tmp/'b.gba')==meta['output_sha256'])
        # wrong source / corrupt patch
        wrong=tmp/'wrong.gba';w=bytearray(source.read_bytes());w[0x200]^=0xFF;wrong.write_bytes(w)
        f_wrong=run([FLIPS,'--apply','--exact',bps,wrong,tmp/'w1.gba']);x_wrong=run([XDELTA,'-d','-s',wrong,xd,tmp/'w2.gba'])
        cb=tmp/'c.bps';b=bytearray(bps.read_bytes());b[len(b)//2]^=0xFF;cb.write_bytes(b);cx=tmp/'c.xdelta';x=bytearray(xd.read_bytes());x[8]^=0xFF;cx.write_bytes(x)
        f_corrupt=run([FLIPS,'--apply','--exact',cb,source,tmp/'c1.gba']);x_corrupt=run([XDELTA,'-d','-s',source,cx,tmp/'c2.gba'])
        if not all(applied) or not all(deterministic) or f_wrong[0]==0 or x_wrong[0]==0 or f_corrupt[0]==0 or x_corrupt[0]==0:raise SystemExit(f'verification failed {applied} {deterministic} {f_wrong[0]} {x_wrong[0]} {f_corrupt[0]} {x_corrupt[0]}')
        if sha(source)!=src_sha:raise SystemExit('source changed')
    finally:shutil.rmtree(tmp,ignore_errors=True)
    for f in ('ApplyPatch.ps1','ApplyXdelta.ps1','LICENSE-font.txt'):shutil.copyfile(PREV/f,out/f)
    ver=dict(schema=1,status='DEVELOPMENT_PATCH_NOT_FINAL_RELEASE',
        patch=dict(filename=bps.name,bytes=bps.stat().st_size,sha256=sha(bps)),
        source=dict(filename=source.name,bytes=source.stat().st_size,sha256=src_sha,header_hex=source.read_bytes()[0xA0:0xAC].hex()),
        target=dict(filename=product.name,bytes=product.stat().st_size,sha256=meta['output_sha256']),
        tool=dict(name='Floating IPS v198',sha256=sha(FLIPS),upstream='https://github.com/Sir-Walrus/Flips/releases/tag/v198'),
        xdelta_patch=dict(filename=xd.name,bytes=xd.stat().st_size,sha256=sha(xd)),
        xdelta_tool=dict(name='xdelta3 3.2.2 Windows x86_64',sha256=sha(XDELTA),upstream='https://github.com/jmacd/xdelta/releases/tag/v3.2.2'),
        xdelta_checks=dict(byte_identical_application=applied[1],deterministic_patch=deterministic[1],wrong_source_rejected=dict(exit_code=x_wrong[0],stderr=x_wrong[2]),corrupt_patch_rejected=dict(exit_code=x_corrupt[0],stderr=x_corrupt[2]),encode_options=['-e','-a','-A','-S','none','-9']),
        checks=dict(byte_identical_application=applied[0],deterministic_patch=deterministic[0],wrong_source_rejected=dict(exit_code=f_wrong[0],stdout=f_wrong[1]),corrupt_patch_rejected=dict(exit_code=f_corrupt[0],stdout=f_corrupt[1]),source_unchanged=True),
        translated_units=meta['translated_units'],build_status=str((ROOT/sys.argv[3]).relative_to(ROOT)) if len(sys.argv)>3 else None,
        public_release_eligible=False,automatic_hangul_keyboard_installed=False,hangul_persistence_verified=False,full_translation_integrated=False)
    (out/'verification.json').write_text(json.dumps(ver,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps(dict(bps=ver['patch'],xdelta=ver['xdelta_patch'],target=ver['target']),ensure_ascii=False))


if __name__=='__main__':main()
