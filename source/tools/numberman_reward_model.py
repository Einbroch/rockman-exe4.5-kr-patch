"""Source-pinned ordinary/record NumberMan native bonus composed-line model."""
import struct
from roll_reward_model import model as record_model
from build_visibility_poc import sha

def model(source):
    p=record_model(source)
    # FC030F dispatch ->363C2. Disassembly: ordinary result read then
    #363D6..363F4 shared with FC032E: RNG, same table pointers, buffer+8.
    if struct.unpack_from('<I',source,0x525C8)[0]!=0x080363C3 or sha(source[0x363C2:0x363F6])!='9debffde3fe946ec3bcb123f3cb24d81d2e6c3c74fa8824bd8a610c407a777bf':
        raise ValueError('NumberMan ordinary reward source consumer changed')
    p['native_code_guards'].append({'start':0x363C2,'end':0x363F6,'sha256':'9debffde3fe946ec3bcb123f3cb24d81d2e6c3c74fa8824bd8a610c407a777bf'})
    return dict(p,profile='numberman-minigame-buffer3-v1',scope='687910 ordinary/record native table-generated bonus readouts only; not completion or inventory proof')

def validate_layout(source,layout,scope):
    if scope.get('reward_variable_profile')!='numberman-minigame-buffer3-v1':raise ValueError('unknown NumberMan reward profile')
    p=model(source);byid={r['id']:r for r in layout};rows=[]
    for script,ids in [(16,[0]),(18,[0,1]),(52,[2]),(53,[2,3])]:
        keys=[f'687910:{script}:{i}' for i in ids]
        if not all(k in byid and len(byid[k]['line_advance_pixels'])==1 for k in keys):raise ValueError('incomplete NumberMan bonus line')
        values=p['zenny_values'] if script in (16,52) else p['bugfrag_values']
        digits=max(sum(p['digit_advances'][int(c)] for c in str(v)) for v in values)
        demand=digits+sum(byid[k]['line_advance_pixels'][0] for k in keys)
        if demand>scope['max_line_advance']:raise ValueError('NumberMan composed reward line overflow')
        row={'script':script,'units':keys,'numeric_max_advance':digits,'composed_line_advance':demand,'values':values};rows.append(row)
        for k in keys:byid[k]['reward_composed_line']=row
    return dict(p,composed_lines=rows)
