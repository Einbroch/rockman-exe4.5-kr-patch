"""Deterministic candidate selector/glyph plan, not a ROM keyboard replacement."""
import json
from pathlib import Path
from PIL import Image,ImageDraw
from build_visibility_poc import ROOT,sha,require_hash
from fixedcell_font import bdf_cells,unpack_pixels
from hangul_keyboard_model import INITIALS,MEDIALS

def main():
    profile= json.loads((ROOT/'tools/specs/exe45_fixedcell_visibility_v1.json').read_text())
    font=profile['font'];require_hash(ROOT/font['path'],font['sha256'])
    wanted=set(INITIALS+MEDIALS);cells=bdf_cells(ROOT/font['path'],wanted,profile['raster'])
    order=INITIALS+MEDIALS
    rows=[list(INITIALS[:15]),list(INITIALS[15:]),list(MEDIALS[:15]),list(MEDIALS[15:]),[],[],[]]
    selectors=[]
    for y,row in enumerate(rows):
        for x in range(15):
            ch=row[x] if x<len(row) else None
            selectors.append(dict(cell=y*15+x,column=x,row=y,active=ch is not None,action='jamo' if ch else 'reject',character=ch,glyph_index=order.index(ch) if ch else None))
    if len(selectors)!=105 or {s['character'] for s in selectors if s['active']}!=wanted or sum(s['active'] for s in selectors)!=40:raise ValueError('selector population')
    bank=b''.join(cells[c] for c in order);out=ROOT/'analysis/hangul_keyboard_v1/candidates';out.mkdir(parents=True,exist_ok=True)
    sheet=Image.new('RGB',(480,264),(16,48,56));d=ImageDraw.Draw(sheet);d.text((8,8),'Candidate layout / not game execution',fill='white')
    colors=[(16,48,56),(255,255,255),(80,144,152)]
    for s in selectors:
        if not s['active']:continue
        pixels=unpack_pixels(cells[s['character']]);im=Image.new('RGB',(8,16));im.putdata([colors[p] for row in pixels for p in row]);sheet.paste(im.resize((24,48),Image.Resampling.NEAREST),(8+s['column']*30,32+s['row']*56))
    sheet.save(out/'layout_preview.png');(out/'jamo_big_cells.bin').write_bytes(bank)
    plan=dict(schema=1,policy='implementation candidate; NOT ROM-INTEGRATED; NON-DISTRIBUTION',user_choice='automatic composition; user reply 2026-10-09',font=font,raster=profile['raster'],glyph_order=order,glyph_count=40,glyph_bytes=64,bank_sha256=sha(bank),selectors=selectors,preview_sha256=sha((out/'layout_preview.png').read_bytes()),tool_sha256=sha(Path(__file__).read_bytes()),limits=['Static font/layout preview, not emulator evidence or human presentation approval.','Native keyboard grid glyph provider/upload/init lifetime not established by this file.','Inactive cells must reject at selector handler; blank drawing alone is insufficient.','Native page switching/Latin selectors/editing controls/record format and capacity pending integration.'])
    (out/'plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf8');print('PASS candidate40 jamo glyphs/105 cell actions; native integration pending')
if __name__=='__main__':main()
