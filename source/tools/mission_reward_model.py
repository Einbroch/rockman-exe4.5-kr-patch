"""Source-pinned EE38 reward table and decimal-line budget, not acquisition QA."""
import struct
from build_visibility_poc import sha

SOURCE='588a77da006fb0dca0c8addbcc316d7bd4b1c3a42db24750bcfe17b170ac5ef8'

def model(source):
    if sha(source)!=SOURCE:raise ValueError('mission reward revision')
    # 68216 selects one of five sentinel-terminated 16-byte mission lists.
    # 68358..5E copies reward kind/amount from a selected four-byte row.
    # 684B0 reads that kind/amount; EE38 stores amount in context+54.
    guards={0x68358:'3878687078886882',0x684B0:'f0b5114de879698a0042f0bd',
            0x50EEE:'69650130215c',0x50F08:'e8030000'}
    for at,h in guards.items():
        if source[at:at+len(bytes.fromhex(h))]!=bytes.fromhex(h):raise ValueError('mission producer contract')
    groups=struct.unpack_from('<5I',source,0x67C38)
    if groups!=(0x08067C4C,0x08067CD0,0x08067D54,0x08067DD8,0x08067E5C):raise ValueError('mission group pointers')
    ranges=[(0x681DA,0x68362),(0x684B0,0x684BC),(0x50ED4,0x50F0C),(0x67C38,0x68060)]
    catalog=[];amounts={1:set(),2:{1000},3:set()};ids=[]
    for group,pointer in enumerate(groups):
        at=pointer-0x08000000;rows=[]
        while source[at]!=255:
            if len(rows)>=32:raise ValueError('mission sentinel missing')
            mission=source[at+2];rp=struct.unpack_from('<I',source,at+8)[0]-0x08000000
            rewards=[]
            for i in range(3):
                kind,weight,value=struct.unpack_from('<BBH',source,rp+i*4)
                if kind!=i+1 or weight!=32:raise ValueError('mission reward row population')
                amounts[kind].add(value);rewards.append(dict(kind=kind,weight=weight,amount=value))
            if source[rp+12:rp+16]!=b'\xff'*4:raise ValueError('reward sentinel')
            ranges.append((rp,rp+16));rows.append(mission);ids.append(mission)
            catalog.append(dict(group=group,mission=mission,record_offset=at,reward_offset=rp,rewards=rewards));at+=16
        if rows!=(list(range(group*8,group*8+8)) if group<4 else list(range(32))):raise ValueError('mission list denominator')
    if set(ids)!=set(range(32)) or len(catalog)!=64 or amounts[1]!={1} or amounts[2]!={1000,1500,2000,2500,3000,3500,4000,4500} or amounts[3]!=set(range(3,11)):
        raise ValueError('mission reward finite population')
    digit_advances=list(struct.unpack_from('<10I',source,0x52910))
    if digit_advances!=[11]*10:raise ValueError('native decimal digit widths')
    ranges.extend([(0x51574,0x515A4),(0x516AC,0x516FC),(0x52150,0x521E0),(0x52910,0x52938)])
    return dict(profile='protoman-mission-reward-v1',source_sha256=SOURCE,catalog=catalog,
        mission_count=32,group_records=64,zenny_values=sorted(amounts[2]),bugfrag_values=sorted(amounts[3]),
        hp_memory_already_owned_fallback=dict(kind=2,amount=1000),digit_advances=digit_advances,
        producer_ranges=[dict(start=a,end=b,sha256=sha(source[a:b])) for a,b in sorted(set(ranges))],
        scope='Native generated mission amounts; not arbitrary context-buffer values, inventory caps or acquisition/save proof')

def validate(source,units,layout):
    p=model(source);indexed={u['id']:u for u in units};measured={r['id']:r['line_advance_pixels'] for r in layout}
    if indexed['6DE3E0:29:0']['translation']!=',\n「' or indexed['6DE3E0:29:1']['translation']!='제니」\n획득!!' or indexed['6DE3E0:30:0']['translation']!=',\n「버그 조각」\n총 ' or indexed['6DE3E0:30:1']['translation']!='개 획득!!':raise ValueError('reward page composition changed')
    z=measured['6DE3E0:29:0'][-1]+4*11+measured['6DE3E0:29:1'][0]
    bug=measured['6DE3E0:30:0'][-1]+2*11+measured['6DE3E0:30:1'][0]
    if z>152 or bug>132 or measured['6DE3E0:29:1'][-1]>132:raise ValueError('mission reward aggregate overflow')
    for r in layout:
        if len(r['line_advance_pixels'])==3 and r['line_advance_pixels'][2]>132:raise ValueError('mission arrow overlaps row3 '+r['id'])
    return dict(p,composed_lines=[dict(script=29,row=2,maximum_digits=4,aggregate_pixels=z,limit_pixels=152),dict(script=30,row=3,maximum_digits=2,aggregate_pixels=bug,limit_pixels=132)],
        navi_name_and_item_widths='separate consumer verification pending',runtime='pending')
