"""Stage 067 (graphics only): PET top-bar weekday boxes (graphics_fix_v2) over the 066 ROM.

Regions come from graphics_fix_v2 and are recorded like v3 redirects: preceding_hex (066 ROM bytes), final_hex,
base_hex (bytes every earlier finalizer expects; same as preceding here). The date-input footer region coincides
with the base build's own footer patch; the generated build drops that patch in favour of this one, and the
034..036 'nolabel' view restores base_hex.
"""
from build_visibility_poc import ROOT,sha
import graphics_fix_v2 as graphics_fix

KEY='graphics067'
PREDECESSOR='poc/output/pending500_066_v1.gba'
TAG=' graphic fix: '


def install(source,appended,key_patches,keymeta):
    path=ROOT/PREDECESSOR;meta=__import__('json').loads(path.with_suffix('.json').read_text(encoding='utf8'))
    base=path.read_bytes()
    if sha(base)!=meta['output_sha256']:raise ValueError(KEY+' predecessor hash')
    out=[];patches=list(key_patches)
    for o,final,reason in graphics_fix.patches(source,base):
        preceding=base[o:o+len(final)]
        if final==preceding:raise ValueError(KEY+' no-op graphic %X'%o)
        patches.append((o,final,KEY+TAG+reason))
        out.append(dict(offset=o,size=len(final),reason=reason,preceding_hex=preceding.hex(),final_hex=final.hex(),base_hex=preceding.hex()))
    keymeta=dict(keymeta);keymeta[KEY]=dict(predecessor=PREDECESSOR,predecessor_sha256=meta['output_sha256'],graphics=out)
    return appended,patches,keymeta


def predecessor_view(source,target,keymeta):
    target=bytearray(target)
    for r in keymeta[KEY]['graphics']:
        o,n=r['offset'],r['size']
        if target[o:o+n]!=bytes.fromhex(r['final_hex']):raise ValueError(KEY+' graphic final %X'%o)
        target[o:o+n]=bytes.fromhex(r['preceding_hex'])
    return bytes(target)


def verify(source,target,keymeta):
    for r in keymeta[KEY]['graphics']:
        if target[r['offset']:r['offset']+r['size']]!=bytes.fromhex(r['final_hex']):raise ValueError(KEY+' graphic bytes')
    return True
