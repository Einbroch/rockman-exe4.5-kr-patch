"""Explicit one-slot middle-dot extension; preserve every prior glyph identity."""
import struct

def verify_middle_dot_lineage(old,new,base,rom):
    if new['extra_glyph_metrics'].get('·')!={'index':11173,'vertical_shift':0,'advance':12} or set(new['extra_glyph_metrics'])-set(old['extra_glyph_metrics'])!={'·'}:raise ValueError('Undeclared font repertoire change')
    a,b=old['hangul_keyboard_glyphs'],new['hangul_keyboard_glyphs']
    if a['mapping'].keys()!=b['mapping'].keys() or any(b['mapping'][k]!=v+1 for k,v in a['mapping'].items()):raise ValueError('Declared one-slot jamo shift')
    for key,stride,legacy in [('extension',96,old['extension']['legacy_index_view']),('fixedcell_extension',64,0)]:
        for i,(old_row,row) in enumerate(zip(old[key]['layout'][:2],new[key]['layout'][:2])):
            advance=key=='extension' and i==1;size=4 if advance else stride
            if row['size']!=old_row['size']+size:raise ValueError('Explicit font bank growth')
            count=legacy+11173;lo,hi=old_row['offset'],row['offset']
            if base[lo:lo+count*size]!=rom[hi:hi+count*size]:raise ValueError('Legacy/Hangul/comma supply changed')
            for ch,index in a['mapping'].items():
                before=lo+(legacy+index)*size;after=hi+(legacy+b['mapping'][ch])*size
                if base[before:before+size]!=rom[after:after+size]:raise ValueError('Prior jamo glyph/advance changed')
            dot=rom[hi+(legacy+11173)*size:hi+(legacy+11174)*size]
            if not any(dot) or advance and struct.unpack('<I',dot)[0]!=12:raise ValueError('New middle dot empty/advance')
