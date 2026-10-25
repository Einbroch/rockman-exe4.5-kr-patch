"""Reproducible Korean command-label/space-key CPU candidate, not ROM build.

Letterforms come from the existing identified BDF, without resampling.
Only x196..223/y56..151 may change relative to the guarded page candidate.
"""
import json
import struct
from pathlib import Path
from build_visibility_poc import ROOT, sha, require_hash
from report_fixedcell_runtime import read
from prepare_keyboard_page_graphics import decode, encode, preview
from fixedcell_font import bdf_cells, unpack_pixels
from hangul_keyboard_action_shim import CODE
from extended_dialogue import assemble_verified

LABELS=(('한글2','영숫자','오른쪽','왼쪽','공백','확인'),
        ('한글1','영숫자','오른쪽','왼쪽','공백','확인'),
        ('한글1','한글2','오른쪽','왼쪽','공백','확인'))
SOURCE_LABELS=(('カタカナ','きごう','すすむ','もどる','スペース','決定'),
               ('ひらがな','きごう','すすむ','もどる','スペース','決定'),
               ('ひらがな','カタカナ','すすむ','もどる','スペース','決定'))
ACTIONS=('toggle01','toggle12','caret_right','caret_left','native_space','confirmation_request')


def assemble(address=0x08303000):
    old_page='cmp r2, #0\nbne action_handled'
    old_command='cmp r1, #3\nbne action_handled\nmovs r1, #41'
    if CODE.count(old_page)!=1 or CODE.count(old_command)!=1:
        raise ValueError('action source contract changed')
    code=CODE.replace(old_page,'cmp r2, #1\nbhi action_handled')
    code=code.replace(old_command,'''cmp r1, #3
beq action_left
cmp r1, #4
bne action_handled
movs r1, #128
lsls r1, r1, #8
b action_dispatch
action_left:
movs r1, #41''')
    # Opaque native single00 is canonical8000, not composer jamo selector0.
    return assemble_verified(code,address,dict(editor=0x0200FC40,
        selectors=0x09301000,context=0x09300000,helper=0x08F0D001))


def main():
    base=ROOT/'analysis/hangul_keyboard_v1';out=base/'keyboard_labels';out.mkdir(exist_ok=True)
    reports={};deps={}
    for name in ('page_graphics','kana_replacement'):
        p=base/name/'report.json';d=read(p)
        if not d['passed'] or d['rom_integrated']:raise ValueError('dependency scope')
        for n,h in d.get('tools',{}).items():require_hash(ROOT/'tools'/n,h)
        for n,h in d.get('artifacts',{}).items():require_hash(p.parent/n,h)
        deps[name+'/report.json']=sha(p.read_bytes());reports[name]=d
    profile=read(ROOT/'project.json')['source_profile'];source=ROOT/profile['filename']
    require_hash(source,profile['sha256']);rom=source.read_bytes()
    tbl=ROOT/'external/textpet-plugins/exe45-utf8.tbl'
    if tbl.read_text(encoding='utf-8-sig').splitlines()[0]!='00= ':
        raise ValueError('native space code changed')
    if rom[0x619EF8:0x619EF8+64]!=bytes([0x11])*64:
        raise ValueError('native space glyph no longer blank')
    font_profile=read(ROOT/'tools/specs/exe45_fixedcell_visibility_v1.json')
    font=font_profile['font'];require_hash(ROOT/font['path'],font['sha256'])
    require_hash(ROOT/font['license'],font['license_sha256'])
    cells=bdf_cells(ROOT/font['path'],set(''.join(''.join(row) for row in LABELS)),font_profile['raster'])
    g=reports['page_graphics'];palette_path=ROOT/g['observed_palette']['path']
    require_hash(palette_path,g['observed_palette']['sha256'])
    colors=[tuple(((v>>n)&31)*255//31 for n in (0,5,10))
            for v in struct.unpack('<16H',palette_path.read_bytes()[288:320])]
    colors[0]=(170,220,220);pages=[]
    for page in range(3):
        if page<2:
            folder=base/'kana_replacement';bank=(folder/f'page{page}_tiles.bin').read_bytes();mapping=(folder/f'page{page}_map.bin').read_bytes()
        else:
            p=g['pages'][page];bank=rom[p['bank_offset']:p['bank_offset']+p['bank_bytes']];mapping=rom[p['map_offset']:p['map_offset']+1200]
            if sha(bank)!=p['bank_sha256'] or sha(mapping)!=p['map_sha256']:raise ValueError('native page2 identity')
        original=decode(bank,mapping);b,m=encode(original)
        if decode(b,m)!=original:raise ValueError('unchanged page pixel roundtrip')
        pixels=[row[:] for row in original];labels=[]
        for row,text in enumerate(LABELS[page]):
            x0=196+(28-8*len(text))//2;y0=56+row*16
            if not text or 8*len(text)>28:raise ValueError('label width')
            for y in range(y0,y0+16):
                for x in range(196,224):
                    v=original[y][x];bg=5 if (x+y)%4==3 else 9
                    if v not in (5,8,9,11) or v in (5,9) and v!=bg:
                        raise ValueError('command background/stroke classification')
                    pixels[y][x]=bg
            for i,ch in enumerate(text):
                glyph=unpack_pixels(cells[ch])
                for j,line in enumerate(glyph):
                    for k,v in enumerate(line):
                        if v not in (0,1,2):raise ValueError('command glyph palette')
                        if v:pixels[y0+j][x0+i*8+k]={1:11,2:8}[v]
            labels.append(dict(row=row,column=15,source_label_reading=SOURCE_LABELS[page][row],
                korean=text,action=ACTIONS[row],state='needs_review',x=x0,y=y0,width=len(text)*8,height=16))
        for y in range(160):
            for x in range(240):
                if not (196<=x<224 and 56<=y<152) and pixels[y][x]!=original[y][x]:
                    raise ValueError('protected pixel changed')
        b,m=encode(pixels)
        if len(b)>0x2000 or len(b)%32 or decode(b,m)!=pixels:raise ValueError('fixture extent/pixel roundtrip')
        (out/f'page{page}_tiles.bin').write_bytes(b);(out/f'page{page}_map.bin').write_bytes(m)
        preview(pixels,out/f'page{page}_preview.png',colors)
        pages.append(dict(page=page,labels=labels,bank_bytes=len(b),map_bytes=len(m),
            before_bank_sha256=sha(bank),before_map_sha256=sha(mapping),protected_pixels=35712))
    blob,isa=assemble();(out/'shim.bin').write_bytes(blob)
    report=dict(passed=True,rom_integrated=False,human_presentation_approved=False,
        source_sha256=profile['sha256'],font=font,raster=font_profile['raster'],pages=pages,
        native_space=dict(token_hex='00',canonical_identity=0x8000,glyph_blank=True,
            table_sha256=sha(tbl.read_bytes()),native_glyph_sha256=sha(rom[0x619EF8:0x619EF8+64])),
        editable_rectangle=dict(x=196,y=56,width=28,height=96),palette=dict(ink=11,shadow=8,background=[5,9]),
        dependencies=deps,ISA=isa,
        tools={n:sha((ROOT/'tools'/n).read_bytes()) for n in
            ('prepare_keyboard_labels.py','fixedcell_font.py','prepare_keyboard_page_graphics.py','hangul_keyboard_action_shim.py')},
        artifacts={f.name:sha(f.read_bytes()) for f in out.iterdir() if f.suffix in ('.bin','.png')},
        limits=['18 labels are proposed Korean wording, not human presentation approval.',
            'Space key routes to existing native overwrite/rebase; incomplete Hangul remains uncommittable, not silently discarded.',
            'Page2 letters/symbol selection still unsupported; page controls and command actions are separate.',
            'Candidate glyph asset/CPU code only. No ROM installation, native scanout, IRQ lifetime or save/reload proof.'])
    (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    require_hash(source,profile['sha256']);print('PASS 18 Korean command labels and native-space action candidate')


if __name__=='__main__':main()
