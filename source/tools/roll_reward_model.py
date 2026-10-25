"""Source-pinned Roll bonus table/decimal consumer and composed-line checks."""
import struct
from build_visibility_poc import sha
SOURCE='588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8'
GUARDS=[[334932,334968,"7474cdbf42dd494ac68b0b93006aaffecfbcfd4b2a10f324420d91a855c3d2d0"],[335452,335480,"8dcc04a08990e409c5bc39c51113b2e2394133e4099116bd0ef5b1c6bee97e35"],[337476,337480,"93cc9830ac4cf54bf66a7c892e61a761285ae05b8fcbc0cbcbeeae0ac83f3d93"],[222070,222146,"34a55d92057286782979e8cca599d9b383649b40206030063b3631f38e1c9589"],[222200,222212,"cf72dadd2b352c4dd3e923766667f3194f2046adbbcbfc5ab5f0e022d1a8ac43"],[221892,221924,"2e10d7360888213c3e0e727f672e298a653829167f346aad7225285a9ca9e92f"],[333484,333564,"c7cdbbf65c7e7b81aedb3738c4415789d0504c51bd3f76e875df9d2610d432ba"],[336208,336336,"75eb72f23a0fda9005011284fa8c3898b8507f2081f6f8a84a1fc57895314b34"],[336536,336580,"7ed33db29f2b6a70141807e406bd335bad7aab015fdf2dc07f101138e3c59de4"],[336800,336844,"98197a37982f771113446aad989d4f5b2c5acc1c6e4ffaeb053e0a9420393894"]]
def model(source):
    if sha(source)!=SOURCE:raise ValueError('reward source revision')
    for start,end,digest in GUARDS:
        if sha(source[start:end])!=digest:raise ValueError('native reward consumer changed')
    # FC03 table slot2E ->08036376. Native RNG bits1..3 index eight
    # halfwords; bit0 carry chooses Zenny/type2 or BugFrags/type3.
    if struct.unpack_from('<I',source,0x52644)[0]!=0x08036377:raise ValueError('FC032E dispatch')
    ptrs=struct.unpack_from('<3I',source,0x363F8)
    if ptrs!=(0x0200FA6C,0x080362C4,0x080362D4):raise ValueError('reward buffer/table pointers')
    z=list(struct.unpack_from('<8H',source,0x362C4));bug=list(struct.unpack_from('<8H',source,0x362D4))
    widths=list(struct.unpack_from('<10I',source,0x5290C+4))
    if z!=[300,500,400,500,300,200,500,800] or bug!=[3,5,2,1,3,4,4,5] or widths!=[11]*10:raise ValueError('bonus/digit inventory changed')
    return {'profile':'roll-minigame-buffer3-v1','source_sha256':SOURCE,'native_code_guards':[{'start':a,'end':b,'sha256':h} for a,b,h in GUARDS],
        'zenny_values':z,'bugfrag_values':bug,'digit_advances':widths,'buffer_address':0x0200FA74,
        'context':0x0200FA20,'decimal_handler':0x080516AC,'decimal_formatter':0x08052150,
        'scope':'native table-generated bonus results only; not arbitrary printBuffer users or actual minigame reward QA'}
def validate_layout(source,layout,scope):
    if scope.get('reward_variable_profile')!='roll-minigame-buffer3-v1':raise ValueError('unknown bonus variable profile')
    proof=model(source);byid={x['id']:x for x in layout};rows=[]
    for script in (52,53,62,63):
        values=proof['zenny_values'] if script in (52,62) else proof['bugfrag_values']
        digits=max(sum(proof['digit_advances'][int(c)] for c in str(v)) for v in values)
        keys=[f'65FF3C:{script}:2'] if script in (52,62) else [f'65FF3C:{script}:2',f'65FF3C:{script}:3']
        if not all(k in byid for k in keys):raise ValueError('incomplete bonus page selection')
        if script in (53,63) and len(byid[keys[0]]['line_advance_pixels'])!=1:raise ValueError('bonus prefix row')
        demand=digits+sum(byid[k]['line_advance_pixels'][0] for k in keys)
        if demand>scope['max_line_advance']:raise ValueError(f'composed reward line overflow: {script}: {demand}')
        row={'script':script,'units':keys,'numeric_max_advance':digits,'composed_line_advance':demand,'values':values}
        rows.append(row)
        for key in keys:byid[key]['reward_composed_line']=row
    return dict(proof,composed_lines=rows)
