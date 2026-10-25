"""Label batches v3: v2 cumulative label lookup plus pointer redirects for raw archives read by bespoke code.

778A4C (Navi name table) is read only through the literal at 0x0805174C (code 0x51718: offset table, then a
fixed 0x80-byte copy into the current-Navi name slot printed by printCurrentNavi in VWF dialogue). Its words
already point at the base build's relocated clone; v3 points them at this batch's combined clone. The base
catalog audit accepts exactly these pointer words (REDIRECT_POINTERS) and the 034..036 finalizers get the
pre-redirect value back in their 'nolabel' view.
"""
from build_visibility_poc import sha
from keyitem_rom_selector import INSTALL
from batch_label_v1 import SITES,ALLOWED
from batch_label_v2 import FastLabelComponent

# 76C944 (escape-tutorial labels) is reached only through the root-returning helper literal 0x080212E8.
REDIRECT={'778A4C':[0x5174C],'76C944':[0x212E8]}
REDIRECT_POINTERS=frozenset(p for ps in REDIRECT.values() for p in ps)


def latest_redirects(keymeta):
    best={}
    for k,v in keymeta.items():
        if k.startswith('typed') and k[5:].isdigit() and isinstance(v,dict):
            for r in v.get('redirects',[]):
                if r['offset'] not in best or best[r['offset']][0]<int(k[5:]):best[r['offset']]=(int(k[5:]),r)
    return {o:r for o,(_,r) in best.items()}


class RedirectLabelComponent(FastLabelComponent):
    def install(self,source,appended,key_patches,keymeta,inputs,common,plugins,work):
        offsets=[p[0] for p in key_patches]
        if set(offsets)-ALLOWED-REDIRECT_POINTERS:raise ValueError(self.batch+' predecessor patch set')
        carried={p[0]:p[1] for p in key_patches if p[0] in REDIRECT_POINTERS}
        tail,patches,keymeta,records=super().install(source,appended,[p for p in key_patches if p[0] not in REDIRECT_POINTERS],keymeta,inputs,common,plugins,work)
        from build_visibility_poc import ROOT
        base=(ROOT/self.base).read_bytes()   # predecessor ROM: its pointer words are the values to carry
        prev=latest_redirects(keymeta);mine={r['archive']:r['rom_offset'] for r in records};out=[]
        for arc,ptrs in REDIRECT.items():
            for ptr in ptrs:
                preceding=carried.get(ptr,base[ptr:ptr+4]);first=prev.get(ptr,{}).get('base_hex',base[ptr:ptr+4].hex())
                if ptr in prev and bytes.fromhex(prev[ptr]['final_hex'])!=preceding:raise ValueError(self.batch+' carried redirect %X'%ptr)
                final=(0x08000000+mine[arc]).to_bytes(4,'little') if arc in mine else preceding
                if final!=source[ptr:ptr+4]:patches.append((ptr,final,self.batch+' redirect %s pointer %X'%(arc,ptr)))
                out.append(dict(archive=arc,offset=ptr,preceding_hex=preceding.hex(),final_hex=final.hex(),base_hex=first))
        keymeta[self.key]['redirects']=out
        return tail,patches,keymeta,records

    def predecessor_view(self,source,target,keymeta):
        target=bytearray(target)
        for r in keymeta[self.key].get('redirects',[]):
            o=r['offset']
            if target[o:o+4]!=bytes.fromhex(r['final_hex']):raise ValueError(self.batch+' redirect final')
            target[o:o+4]=bytes.fromhex(r['preceding_hex'])
        return super().predecessor_view(source,bytes(target),keymeta)

    def verify_final(self,source,target,keymeta):
        super().verify_final(source,target,keymeta)
        for r in keymeta[self.key].get('redirects',[]):
            o=r['offset'];at=int.from_bytes(target[o:o+4],'little')-0x08000000
            if target[o:o+4]!=bytes.fromhex(r['final_hex']):raise ValueError(self.batch+' redirect word')
            rec=next((x for x in keymeta[self.key].get('archives',[]) if x['archive']==r['archive']),None)
            if rec and (at!=rec['rom_offset'] or sha(target[at:at+rec['compiled_bytes']])!=rec['compiled_sha256']):raise ValueError(self.batch+' redirect target')
        return True
