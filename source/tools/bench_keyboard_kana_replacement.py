"""Execute two-page selectors across page changes; CPU fixtures, not ROM QA."""
import json
import struct
from build_visibility_poc import ROOT, sha, require_hash
from report_fixedcell_runtime import read
from bench_hangul_composer_thumb import *
from unicorn import UC_HOOK_MEM_WRITE
from extended_dialogue import Ks, Cs, KS_ARCH_ARM, KS_MODE_THUMB, CS_ARCH_ARM, CS_MODE_THUMB
from prepare_keyboard_kana_replacement import assemble
from hangul_mixed_replay_state import MixedReplay, KEYS, apply
from hangul_mixed_editor_init import initialize
from hangul_keyboard_model import INITIALS, MEDIALS, FINALS, FINAL_SPLIT


def main():
    base = ROOT/'analysis/hangul_keyboard_v1'
    deps = {}
    for name in ('cpu_keyboard_actions','kana_replacement','cpu_composer'):
        p = base/name/'report.json'; d = read(p)
        if not d['passed'] or d.get('rom_integrated', False): raise ValueError('dependency scope')
        for n,h in d.get('tools',{}).items(): require_hash(ROOT/'tools'/n,h)
        for n,h in d.get('artifacts',{}).items(): require_hash(p.parent/n,h)
        deps[name+'/report.json'] = sha(p.read_bytes())
    profile = read(ROOT/'project.json')['source_profile']
    source = ROOT/profile['filename']; require_hash(source,profile['sha256']); rom = source.read_bytes()
    report = read(base/'cpu_keyboard_actions/report.json'); site = report['native_caller']
    pc, target = 0x08000000+site['offset'], 0x08303000
    if rom[site['offset']:site['offset']+6].hex() != site['expected_hex']: raise ValueError('native caller')
    ks = Ks(KS_ARCH_ARM,KS_MODE_THUMB); cs = Cs(CS_ARCH_ARM,CS_MODE_THUMB)
    patch = bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\nbl #0x08303000',pc)[0])
    decoded = list(cs.disasm(patch,pc))
    if len(patch)!=4 or len(decoded)!=1 or decoded[0].mnemonic!='bl' or decoded[0].op_str!='#0x8303000':
        raise ValueError('final BL boundary/target')
    if bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+decoded[0].mnemonic+' '+decoded[0].op_str,pc)[0])!=patch:
        raise ValueError('final BL semantic roundtrip')
    patch_isa = dict(isa='ARM7TDMI ARMv4T Thumb-1 BL',address=pc,target=target,hex=patch.hex(),roundtrip=True)
    blob, isa = assemble(); require_hash(base/'kana_replacement/shim.bin',sha(blob))
    selectors = (base/'kana_replacement/selectors.bin').read_bytes()
    u = Uc(UC_ARCH_ARM,UC_MODE_THUMB); u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    u.mem_map(0x08000000,len(rom)); u.mem_write(0x08000000,rom)
    u.mem_write(pc,patch); u.mem_write(target,blob)
    u.mem_protect(0x08000000,len(rom),UC_PROT_READ|UC_PROT_EXEC)
    for at,n in ((0x08F0D000,'dispatch.bin'),(0x08F0E000,'keyedit.bin'),(0x08F0F000,'rebase.bin')):
        u.mem_map(at,4096); u.mem_write(at,(base/'cpu_keyboard_actions'/n).read_bytes())
        u.mem_protect(at,4096,UC_PROT_READ|UC_PROT_EXEC)
    for at,n in ((0x09000000,'transitions.bin'),(0x09200000,'deletions.bin')):
        b = (base/'cpu_composer'/n).read_bytes(); size = (len(b)+4095)&~4095
        u.mem_map(at,size); u.mem_write(at,b); u.mem_protect(at,size,UC_PROT_READ)
    u.mem_map(0x09300000,8192)
    u.mem_write(0x09300000,struct.pack('<4I',0x09000000,0x09200000,0x08F0E001,0x08F0F001))
    u.mem_write(0x09301000,selectors); u.mem_protect(0x09300000,8192,UC_PROT_READ)
    u.mem_map(0x02000000,0x40000); u.mem_map(0x03007000,4096)
    ed,glob,keys,sp = 0x0200FC40,0x02000200,0x02000300,0x03007F00
    regs = [UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,
            UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11]
    writes = []; u.hook_add(UC_HOOK_MEM_WRITE,lambda cpu,access,a,n,v,user:writes.append((a,n)))
    counts = dict(calls=0,accepted=0,rejected_consumed=0,unhandled=0,
                  same_page_syllables=0,cross_page_syllables=0,invalid_cases=0)
    seed = bytes(range(256))*1024
    def step(raw,col,row,page,mask=1,continuing=False,cap=None):
        if not continuing:
            u.mem_write(0x02000000,seed)
            u.mem_write(ed,initialize(struct.pack('<4I',raw[0]&15,33,0x020010A6,0))[:20]+raw)
        elif bytes(u.mem_read(ed+20,76)) != raw: raise ValueError('uninterrupted state drift')
        u.mem_write(ed+6,bytes((col,row,page))); u.mem_write(glob+4,struct.pack('<I',keys))
        u.mem_write(keys+2,struct.pack('<H',mask))
        if cap is not None: u.mem_write(ed+4,bytes([cap]))
        action = None; consumed = bool(mask&3); wanted = raw; accepted = False
        if consumed and cap is None:
            if mask&2: action = ('backspace',None)
            elif col==15 and row in (2,3): action = ('move',1 if row==2 else -1)
            elif page in (0,1) and col<15 and row<6:
                v = selectors[row*15+col]
                if v<40: action = ('jamo',KEYS[v])
        if action:
            try: accepted,wanted = apply(raw,*action)
            except ValueError: pass
        expected = bytearray(u.mem_read(0x02000000,0x40000))
        expected[ed+20-0x02000000:ed+96-0x02000000] = wanted
        u.mem_write(sp-212,b'\x5A'*212); u.reg_write(UC_ARM_REG_CPSR,0x30)
        saved = [ed if r==UC_ARM_REG_R5 else glob if r==UC_ARM_REG_R10 else 0x13579000+i
                 for i,r in enumerate(regs)]
        for r,v in zip(regs,saved): u.reg_write(r,v)
        u.reg_write(UC_ARM_REG_SP,sp); writes.clear()
        dest = 0x08034F66 if consumed else pc+6
        u.emu_start(pc|1,dest,count=40000)
        if u.reg_read(UC_ARM_REG_PC)!=dest or u.reg_read(UC_ARM_REG_R0)!=int(consumed) or bool(u.reg_read(UC_ARM_REG_CPSR)&0x40000000)==consumed:
            raise ValueError('handled/native branch contract')
        if u.reg_read(UC_ARM_REG_SP)!=sp or any(u.reg_read(r)!=v for r,v in zip(regs,saved)) or bytes(u.mem_read(sp-212,4))!=b'\x5A'*4:
            raise ValueError('ABI/stack guard')
        if bytes(u.mem_read(0x02000000,0x40000))!=expected: raise ValueError('whole EWRAM atomicity')
        if any(not (sp-208<=a and a+n<=sp or accepted and ed+20<=a and a+n<=ed+96) for a,n in writes):
            raise ValueError('write extent')
        counts['calls']+=1; counts['accepted']+=accepted
        counts['rejected_consumed']+=consumed and not accepted; counts['unhandled']+=not consumed
        return wanted
    empty = MixedReplay(4).serialize(); partial = MixedReplay(4)
    for k in 'ㄱㅗㅏㄹㄱ': partial.press(k)
    loaded = MixedReplay(4); loaded.load((229,0x809B,11171))
    for raw in (empty,partial.serialize(),loaded.serialize()):
        for page in range(3):
            for row in range(6):
                for col in range(16): step(raw,col,row,page)
        for page in (0,1):
            for mask in range(1024): step(raw,0,0,page,mask)
        for col,row,page in ((16,0,0),(255,0,1),(0,6,0),(0,255,1),(0,0,255)):
            step(raw,col,row,page); counts['invalid_cases']+=1
        for cap in (0,1,10,255): step(raw,0,0,1,cap=cap); counts['invalid_cases']+=1
    positions = {KEYS[v]:(i%15,i//15) for i,v in enumerate(selectors) if v<40}
    # All syllables on each page AND mixed-page input. Between key presses,
    # only UI page/cell/key-state fixtures change; compact composition is untouched.
    for rank in range(11172):
        l = INITIALS[rank//588]; v = MEDIALS[rank//28%21]; t = FINALS[rank%28]
        path = [l,v]+([] if not t else list(FINAL_SPLIT.get(t,(t,))))
        for mode in (0,1,2):
            raw = empty
            for n,k in enumerate(path):
                col,row = positions[k]; page = n%2 if mode==2 else mode
                raw = step(raw,col,row,page,continuing=n>0)
            if MixedReplay.restore(raw).model.state.cells!=(rank,): raise ValueError('canonical syllable mismatch')
            for n in range(len(path)): raw = step(raw,0,0,n%2,mask=3,continuing=True)
            if raw != empty: raise ValueError('cross-page key-history undo')
            counts['cross_page_syllables' if mode==2 else 'same_page_syllables']+=1
        if rank%2048==0: print('two-page syllable',rank,flush=True)
    out = base/'cpu_kana_replacement'; out.mkdir(exist_ok=True)
    result = dict(passed=True,rom_integrated=False,counts=counts,source_sha256=profile['sha256'],
        dependencies=deps,nested_stack_bytes=208,ISA=isa,caller_ISA=patch_isa,
        compact_state_HOST_rewritten_between_keys=False,
        tools={n:sha((ROOT/'tools'/n).read_bytes()) for n in
            ('bench_keyboard_kana_replacement.py','prepare_keyboard_kana_replacement.py')},
        limits=['CPU fixtures execute native BL/BNE and emitted action/dispatch/keyedit/rebase code, not natural gamepad input.',
            'Cell/page positions supplied by host; page-switch controller, full navigation and renderer not exercised.',
            'No ROM installation, screen approval, commit/save/reset/fresh-load claim.'])
    (out/'report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
    require_hash(source,profile['sha256']); print('PASS two-page kana replacement CPU',counts,flush=True)


if __name__=='__main__': main()
