"""Preserve three eight-character calendar menu cell groups, not byte stride."""
SOURCE='とうろく    よていをみる  さくじょ    '
def validate(units):
    if len(units)!=1 or units[0]['id']!='6368E8:0:0' or units[0]['source']!=SOURCE:raise ValueError('calendar finite source scope')
    text=units[0]['translation']
    if len(text)!=24 or '\n' in text or [text[i:i+8].rstrip() for i in (0,8,16)]!=['등록','일정 보기','삭제']:raise ValueError('calendar8-cell group boundary')
    if any(text[i:i+8]!=text[i:i+8].rstrip().ljust(8) for i in (0,8,16)):raise ValueError('calendar padding')
    return {'cell_groups':3,'cells_per_group':8,'decoded_cells':24,'expected_stage_bytes':1536,'input_default_names_unchanged':True}

def replace_menu_literal(tpl,units):
    from tpl_literals import literals,serialize,skeleton
    validate(units);u=units[0];matches=[x for x in literals(tpl) if x.key==u['id']]
    if len(matches)!=1:raise ValueError('calendar source key')
    x=matches[0]
    if x.text!=SOURCE or x.language!='mmbn45s' or u['state'] not in ('needs_review','reviewed'):raise ValueError('calendar source/language/state')
    result=tpl[:x.start]+serialize(u['translation'])+tpl[x.end:]
    if skeleton(tpl)!=skeleton(result):raise ValueError('calendar protected controls')
    # Calendar tiles require equal eight-cell groups, not identical final
    # space count used by dialogue choices. No other scope gets this policy.
    return result
