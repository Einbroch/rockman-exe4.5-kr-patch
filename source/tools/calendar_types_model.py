"""Source-pinned whole27-cell selector, six unchanged native cell segments."""
SOURCE='TVばんぐみともだちと約束ごはんじゅくそのた?????'
WIDTHS=(6,7,3,3,3,5)
LABELS=('TV 방송','친구와 약속','식사','학원','기타','?????')
def validate(units):
    from calendar_menu_model import validate as menu
    if len(units)!=2 or {u['id'] for u in units}!={'6368E8:0:0','6368E8:60:0'}:raise ValueError('type finite scope')
    menu([u for u in units if u['id']=='6368E8:0:0'])
    u=next(u for u in units if u['id']=='6368E8:60:0');text=u['translation'];at=0
    if u['source']!=SOURCE or len(text)!=27 or '\n' in text:raise ValueError('type source/cell extent')
    for width,label in zip(WIDTHS,LABELS):
        if text[at:at+width]!=label.ljust(width):raise ValueError('native type cell segment/padding')
        at+=width
    return {'cells':27,'stage_bytes':1728,'cell_segments':list(WIDTHS),'visible_labels':5,'sixth_source_segment_unchanged':True}
def replace_types_literals(tpl,units):
    from calendar_menu_model import replace_menu_literal
    from tpl_literals import literals,serialize,skeleton
    validate(units);result=replace_menu_literal(tpl,[u for u in units if u['id']=='6368E8:0:0']);u=next(u for u in units if u['id']=='6368E8:60:0');xs=[x for x in literals(result) if x.key==u['id']]
    if len(xs)!=1 or xs[0].text!=SOURCE or xs[0].language!='mmbn45s' or u['state'] not in ('needs_review','reviewed'):raise ValueError('type source language/state')
    x=xs[0];result=result[:x.start]+serialize(u['translation'])+result[x.end:]
    if skeleton(tpl)!=skeleton(result):raise ValueError('type controls')
    return result
