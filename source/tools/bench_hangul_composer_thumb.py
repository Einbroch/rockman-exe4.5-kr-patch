"""Execute emitted automatic composition/undo candidates against host model.

Caller memory and table residency are isolated fixtures, NOT installed hooks.
"""
import json,struct,sys
from pathlib import Path
from build_visibility_poc import ROOT,sha,require_hash
from extended_dialogue import assemble_verified
from hangul_keyboard_model import Composer,State,INITIALS,MEDIALS,FINALS,FINAL_SPLIT
from hangul_composer_thumb import FEED,UNDO,KEYS,EMPTY,EMPTY_ROW,STATE_BYTES,build_tables,state_from_rank,tail_rank
sys.path.insert(0,str(ROOT/'external/arm_bench_python'))
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB,UC_PROT_READ,UC_PROT_EXEC
from unicorn.arm_const import *

def words(state):
    return [ord(c)-0xac00 for c in state.committed]+([] if state.l is None else [tail_rank(state)])

def encode_state(c):
    w=words(c.state);hist=bytearray()
    for prior in c.history:
        old=words(prior);meta=len(old)|(int(prior.l is not None)<<8)
        hist.extend(struct.pack('<HH',meta,old[-1] if old else EMPTY))
    if len(w)>8 or len(c.history)>64:raise ValueError('fixture bounds')
    return bytes([len(w),c.limit,len(c.history),int(c.state.l is not None)])+struct.pack('<8H',*(w+[EMPTY]*(8-len(w))))+bytes(hist)+b'\xff'*(256-len(hist))

def main():
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    out=ROOT/'analysis/hangul_keyboard_v1/cpu_composer';out.mkdir(parents=True,exist_ok=True)
    feed,feed_isa=assemble_verified(FEED,0x08000000,{})
    undo,undo_isa=assemble_verified(UNDO,0x08001000,{})
    for isa in [feed_isa,undo_isa]:
        if any(len(bytes.fromhex(i['hex']))!=2 for i in isa['instructions']):raise ValueError('Thumb-1 only')
    pairs,deletes=build_tables()
    if len(pairs)!=(EMPTY_ROW+1)*40*4 or len(deletes)!=EMPTY_ROW*2:raise ValueError('serialized table extent')
    (out/'transitions.bin').write_bytes(pairs);(out/'deletions.bin').write_bytes(deletes)
    # CPU only consumes emitted bytes reread from artifacts, not Python objects.
    pairs=(out/'transitions.bin').read_bytes();deletes=(out/'deletions.bin').read_bytes()
    u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    u.mem_map(0x08000000,8192);u.mem_write(0x08000000,feed);u.mem_write(0x08001000,undo)
    u.mem_map(0x09000000,(len(pairs)+4095)&~4095);u.mem_write(0x09000000,pairs)
    u.mem_map(0x09200000,(len(deletes)+4095)&~4095);u.mem_write(0x09200000,deletes)
    u.mem_protect(0x08000000,8192,UC_PROT_READ|UC_PROT_EXEC)
    u.mem_protect(0x09000000,(len(pairs)+4095)&~4095,UC_PROT_READ)
    u.mem_protect(0x09200000,(len(deletes)+4095)&~4095,UC_PROT_READ)
    u.mem_map(0x02000000,4096);u.mem_map(0x03007000,4096);u.mem_map(0x0ff00000,4096)
    state=0x02000100;stack=0x03007f00;stop=0x0ff00000
    preserved=[UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11]
    counts=dict(feed=0,undo=0,rejected=0,malformed=0)
    def execute(before,expected,accepted,key=None,capacity=STATE_BYTES):
        u.mem_write(state-4,b'\xa7'*4+before+b'\xa7'*4)
        u.reg_write(UC_ARM_REG_CPSR,0x30)
        args=[state,capacity,0x09200000,0] if key is None else [state,key,0x09000000,capacity]
        for reg,value in zip([UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3],args):u.reg_write(reg,value)
        for n,reg in enumerate(preserved):u.reg_write(reg,0x13579000+n)
        u.reg_write(UC_ARM_REG_SP,stack);u.reg_write(UC_ARM_REG_LR,stop|1)
        u.emu_start((0x08001000 if key is None else 0x08000000)|1,stop,count=1000)
        if u.reg_read(UC_ARM_REG_PC)!=stop or u.reg_read(UC_ARM_REG_R0)!=int(accepted) or u.reg_read(UC_ARM_REG_SP)!=stack or any(u.reg_read(reg)!=0x13579000+n for n,reg in enumerate(preserved)):raise ValueError('CPU ABI/return')
        after=bytes(u.mem_read(state-4,STATE_BYTES+8))
        if after!=b'\xa7'*4+expected+b'\xa7'*4:raise ValueError(f'CPU state/bounds mismatch key={key}, before={before[:20].hex()}, got={after[4:24].hex()}, want={expected[:20].hex()}')
        counts['undo' if key is None else 'feed']+=1
        if not accepted:counts['rejected']+=1
    def press(c,key):
        before=encode_state(c);accepted=c.press(key);execute(before,encode_state(c),accepted,KEYS.index(key));return accepted
    def back(c):
        before=encode_state(c);accepted=c.backspace();execute(before,encode_state(c),accepted);return accepted
    print('tables emitted; starting full row/key CPU coverage',flush=True)
    # Every serialized row/key combination, including invalid ordering and
    # active partial initials. Empty-row and last-slot append rejection included.
    for rank in range(EMPTY_ROW+1):
        for key in KEYS:
            c=Composer(2);c.state=state_from_rank(rank);press(c,key)
        if rank%2800==0:print('row',rank,'of',EMPTY_ROW,flush=True)
    for li,l in enumerate(INITIALS):
        for vi,v in enumerate(MEDIALS):
            for ti,t in enumerate(FINALS):
                c=Composer(1);keys=[l,v]+([] if not t else list(FINAL_SPLIT.get(t,(t,))))
                for key in keys:
                    if not press(c,key):raise ValueError('syllable accepted path')
                if c.candidate()!=chr(0xac00+li*588+vi*28+ti):raise ValueError('reference syllable')
                while c.history:back(c)
                back(c)
                c.load(chr(0xac00+li*588+vi*28+ti))
                while back(c):pass
    for keys in ['ㄱㅜㄱㅇㅓ','ㄷㅏㄹㄱㅏ','ㄱㅏㄴㅏㄷㅏㄹㅏ','ㄲㅘㅣㄹㄱㅏ']:
        c=Composer(4)
        for key in keys:press(c,key)
        for key in KEYS:press(c,key)
        while c.history:back(c)
    # Inactive tail after deleting a later initial must not recompose the
    # preceding committed syllable (this needs the explicit active-tail flag).
    c=Composer(4);c.load('국어');back(c);back(c)
    for key in ['ㅏ','ㄴ','ㅏ']:press(c,key)
    for limit in range(1,9):
        c=Composer(limit);c.load('가'*limit)
        for key in KEYS:
            sample=Composer(limit);sample.load('가'*limit);press(sample,key)
        back(c);press(c,'ㄱ')
    base=encode_state(Composer(4))
    malformed=[]
    for offset,values in [(0,[9]),(1,[0,9,255]),(2,[65,255]),(3,[1,2,255])]:
        for value in values:
            bad=bytearray(base);bad[offset]=value;malformed.append(bytes(bad))
    bad=bytearray(base);bad[4:6]=b'\x00\x00';malformed.append(bytes(bad))
    c=Composer(4);c.load('가');good=encode_state(c)
    for rank in [11191,65535]:
        bad=bytearray(good);bad[4:6]=struct.pack('<H',rank);malformed.append(bytes(bad))
    for bad in malformed:
        execute(bad,bad,False,0);execute(bad,bad,False);counts['malformed']+=2
    c=Composer(4);c.press('ㄱ');history_sample=encode_state(c)
    for meta,prior in [(2,EMPTY),(0x200,EMPTY),(1,EMPTY),(0,0)]:
        bad=bytearray(history_sample);bad[20:24]=struct.pack('<HH',meta,prior);execute(bytes(bad),bytes(bad),False);counts['malformed']+=1
    bad=bytearray(history_sample);bad[2]=64;execute(bytes(bad),bytes(bad),False,0)
    bad=bytearray(base);bad[2]=1;execute(bytes(bad),bytes(bad),False,0);execute(bytes(bad),bytes(bad),False);counts['malformed']+=2
    for capacity in [0,275]:execute(base,base,False,0,capacity);execute(base,base,False,capacity=capacity)
    for key in [40,255,0xffffffff]:execute(base,base,False,key)
    (out/'feed.bin').write_bytes(feed);(out/'undo.bin').write_bytes(undo)
    report=dict(id='exe45.hangul-keyboard.native-composer.v1',passed=True,rom_integrated=False,state_bytes=STATE_BYTES,transition_rows=EMPTY_ROW+1,keys=40,transition_bytes=len(pairs),deletion_bytes=len(deletes),full_row_key_CPU_vectors=(EMPTY_ROW+1)*40,complete_syllable_paths=11172,counts=counts,machine_code=dict(feed=feed_isa,undo=undo_isa),artifacts={p.name:sha(p.read_bytes()) for p in [out/'feed.bin',out/'undo.bin',out/'transitions.bin',out/'deletions.bin']},tools={n:sha((ROOT/'tools'/n).read_bytes()) for n in ['hangul_keyboard_model.py','hangul_composer_thumb.py','bench_hangul_composer_thumb.py']},limits=['Isolated caller-owned aligned state/table memory; no game RAM reservation, native entry/return hook or keyboard mapping installed.','Finite table implements the host model, not independent human UX approval.','Whole row/key CPU domain and full syllable creation/deletion paths; malformed histories are not exhaustively covered.','Record marker/save compatibility, selection/rendering and actual persistence remain unresolved.'])
    (out/'report.json').write_text(json.dumps(report,indent=2),encoding='utf8');print('PASS native composer',counts,flush=True)

if __name__=='__main__':main()
