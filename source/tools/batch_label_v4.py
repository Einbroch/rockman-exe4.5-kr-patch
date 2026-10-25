"""Label batches v4 (065+): v3 plus fixes from user screenshots (2026-10-25).

* Nickname suffix table 63720C (くん/ちゃん/さま/どの) is copied by 0x08032AB6 into the nickname buffer
  0x02000E5E..0x02000E74 (23 bytes) after the name; Korean suffixes are one syllable (4 bytes, no 0xE5 byte),
  so name(<=6) + suffix(4) + E5 fits. Redirected via its only literal 0x08038F84.
* Item name table 778B08 (key items such as 수험표) is printed in dialogue through a fixed 0x80-byte copy
  (0x0805163E) and drawn by 0x080554A4 elsewhere; all six literals now point at its newest combined clone.
* Chip name pools 0x08765190 / 0x08765B18 (helper 0x0801F7D4 -> 0x080554A4 at result screen, folder lists
  etc.) map to the existing Korean library clones in the v2 label lookup.
"""
from batch_label_v3 import RedirectLabelComponent,REDIRECT,latest_redirects
from build_visibility_poc import ROOT,sha
from cumulative_batch500 import read

V4_REDIRECT={'63720C':[0x38F84],'778B08':[0x349C4,0x419B8,0x4CA10,0x4CB0C,0x51660,0xD2A98]}
REDIRECT.update(V4_REDIRECT)
import batch_label_v3
batch_label_v3.REDIRECT_POINTERS=frozenset(p for ps in REDIRECT.values() for p in ps)


def latest_clone(keymeta,arc):
    best=None
    for k,v in keymeta.items():
        if k.startswith('typed') and k[5:].isdigit() and isinstance(v,dict):
            for r in v.get('archives',[]) or []:
                if r.get('archive')==arc and (best is None or int(k[5:])>best[0]):best=(int(k[5:]),r['rom_offset'])
    return best[1] if best else None


class FixLabelComponent(RedirectLabelComponent):
    def extra_rom_roots(self,image,keymeta):
        meta=read(self.base.replace('.gba','.json'));e=meta['chip_library_extension'];out={}
        for lay,root in zip(e['layout'],(0x08765190,0x08765B18)):
            body=image[lay['offset']:lay['offset']+lay['size']]
            if sha(body)!=lay['sha256']:raise ValueError(self.batch+' chip clone bytes')
            out[root]=(0x08000000+lay['offset'],int.from_bytes(body[:2],'little')//2)
        return out

    def install(self,source,appended,key_patches,keymeta,inputs,common,plugins,work):
        tail,patches,keymeta,records=super().install(source,appended,key_patches,keymeta,inputs,common,plugins,work)
        n=keymeta[self.key];mine={r['archive'] for r in records};fixed=[];newp=[]
        for r in n['redirects']:
            if r['archive'] in V4_REDIRECT and r['archive'] not in mine:
                c=latest_clone(keymeta,r['archive'])
                if c is not None:
                    final=(0x08000000+c).to_bytes(4,'little');r=dict(r,final_hex=final.hex())
            fixed.append(r)
        for o,b,w in patches:
            rr=next((x for x in fixed if x['offset']==o),None)
            newp.append((o,bytes.fromhex(rr['final_hex']),w) if rr else (o,b,w))
        have={o for o,_,_ in newp}
        for r in fixed:
            if r['offset'] not in have and bytes.fromhex(r['final_hex'])!=source[r['offset']:r['offset']+4]:newp.append((r['offset'],bytes.fromhex(r['final_hex']),self.batch+' redirect %s pointer %X'%(r['archive'],r['offset'])))
        n['redirects']=fixed
        return tail,newp,keymeta,records
