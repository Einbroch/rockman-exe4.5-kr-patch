"""CPU edit-display conversion and native compact-wrapper integration fixtures."""
import json,struct
from build_visibility_poc import ROOT,sha,require_hash,bdf_glyphs,FONT_SHA256,LICENSE_SHA256
from bench_hangul_composer_thumb import *
from hangul_compact_state import CompactComposer
from hangul_editor_display import CODE,display,JAMO_BASE,JAMO_INDICES

def main():
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    blob,isa=assemble_verified(CODE,0x08004000,{})
    backend=ROOT/'analysis/hangul_keyboard_v1/cpu_composer';compact=ROOT/'analysis/hangul_keyboard_v1/cpu_compact'
    b= json.loads((backend/'report.json').read_text());c=json.loads((compact/'report.json').read_text())
    for directory,report in [(backend,b),(compact,c)]:
        if not report['passed'] or report['rom_integrated']:raise ValueError('dependency scope')
        for n,h in report['artifacts'].items():require_hash(directory/n,h)
        for n,h in report['tools'].items():require_hash(ROOT/'tools'/n,h)
    require_hash(backend/'report.json',c['dependency_report_sha256'])
    u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    u.mem_map(0x08000000,20480)
    for addr,path in [(0x08000000,backend/'feed.bin'),(0x08001000,backend/'undo.bin'),(0x08002000,compact/'wrapper.bin')]:u.mem_write(addr,path.read_bytes())
    u.mem_write(0x08004000,blob);u.mem_write(0x08003000,struct.pack('<4I',0x08000001,0x08001001,0x09000000,0x09200000))
    u.mem_protect(0x08000000,20480,UC_PROT_READ|UC_PROT_EXEC)
    for addr,n in [(0x09000000,'transitions.bin'),(0x09200000,'deletions.bin')]:
        data=(backend/n).read_bytes();size=(len(data)+4095)&~4095
        u.mem_map(addr,size);u.mem_write(addr,data);u.mem_protect(addr,size,UC_PROT_READ)
    u.mem_map(0x02000000,4096);u.mem_map(0x02002000,4096,UC_PROT_READ)
    u.mem_map(0x03007000,4096);u.mem_map(0x0ff00000,4096)
    src=0x02000101;dest=0x02000201;sp=0x03007f00;stop=0x0ff00000
    regs=[UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11]
    counts=dict(display=0,rejected=0,native_wrapper=0)
    def call(pc,args):
        u.reg_write(UC_ARM_REG_CPSR,0x30)
        for r,v in zip([UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3],args):u.reg_write(r,v)
        for i,r in enumerate(regs):u.reg_write(r,0x13579000+i)
        u.reg_write(UC_ARM_REG_SP,sp);u.reg_write(UC_ARM_REG_LR,stop|1)
        u.emu_start(pc|1,stop,count=100000)
        if u.reg_read(UC_ARM_REG_PC)!=stop or u.reg_read(UC_ARM_REG_SP)!=sp or any(u.reg_read(r)!=0x13579000+i for i,r in enumerate(regs)):raise ValueError('CPU return ABI')
        return u.reg_read(UC_ARM_REG_R0)
    def run(raw,mode=0,capacity=33,output=dest):
        try:expected=display(raw,mode)
        except ValueError:expected=None
        if expected and (capacity<len(expected) or src<output+len(expected) and output<src+64):expected=None
        u.mem_write(0x02000100,b'\xa7'*512);u.mem_write(src,raw)
        before=bytes(u.mem_read(0x02000100,512))
        actual=call(0x08004000,[src,output,capacity,mode])
        if actual!=(len(expected) if expected else 0):raise ValueError(f'status {raw[:20].hex()} mode{mode} got{actual}')
        after=bytearray(before)
        if expected:after[output-0x02000100:output-0x02000100+len(expected)]=expected
        if bytes(u.mem_read(0x02000100,512))!=bytes(after):raise ValueError('state/source/output bounds/atomic reject')
        counts['display']+=1;counts['rejected']+=expected is None
    def raw_words(words,limit=8,active=1):
        return bytes([len(words),limit,0,active if words else 0])+struct.pack('<8H',*(words+[EMPTY]*(8-len(words))))+bytes(44)
    print('display full uint16 rank domain at one cell',flush=True)
    for rank in range(65536):run(raw_words([rank]))
    for limit in [4,8]:
        for slot in range(limit):
            for rank in range(11172):
                words=[0]*limit;words[slot]=rank;run(raw_words(words,limit),1)
        print('complete syllable slots capacity',limit,flush=True)
    for limit in range(1,9):
        for count in range(1,limit+1):
            for li in range(19):
                raw=raw_words([11171]*(count-1)+[11172+li],limit)
                run(raw);run(raw,1);run(raw,capacity=count*4)
            raw=raw_words([11171]*count,limit)
            run(raw,capacity=count*4+1);run(raw,capacity=count*4)
            for offset in [-1,0,1,20,63]:run(raw,output=src+offset)
            run(raw,output=src+64)
    empty=raw_words([]);run(empty);run(empty,1);run(empty,capacity=0)
    for offset,values in [(0,[9]),(1,[0,9]),(2,[1,57]),(3,[1,2]),(4,[0]),(62,[57]),(63,[1])]:
        for value in values:
            bad=bytearray(empty);bad[offset]=value;run(bytes(bad))
    for mode in [2,255,0xffffffff]:run(empty,mode)
    for words,active in [([11172,0],1),([11172],0),([11191],1)]:run(raw_words(words,active=active))
    # Actual native replay output is consumed by emitted display code in the
    # same CPU fixture; host model only supplies the independent expected bytes.
    for baseline,keys in [('', 'ㄱㄱㅗㅏㅣㄹㄱㅏ'),('국어','ㄱㅏㄴㅏ'),('괙','ㅏㄴㅏ')]:
        model=CompactComposer(4,baseline);m=Composer(4);m.load(baseline);base=encode_state(m)[:20]
        u.mem_write(0x02002000,base)
        for action in [41]+[KEYS.index(k) for k in keys]+[40]*12+[41]:
            before=model.serialize();accepted=model.press(KEYS[action]) if action<40 else model.backspace() if action==40 else True
            u.mem_write(0x02000100,before)
            ret=call(0x08002000,[0x02000100,0x02002000,action,0x08003000])
            actual=bytes(u.mem_read(0x02000100,64))
            if ret!=int(accepted) or actual!=model.serialize():raise ValueError('native compose→display integration state')
            expected=display(model.serialize());u.mem_write(dest,b'\xa7'*40)
            if call(0x08004000,[0x02000100,dest,33,0])!=len(expected) or bytes(u.mem_read(dest,len(expected)))!=expected or bytes(u.mem_read(dest+len(expected),40-len(expected)))!=b'\xa7'*(40-len(expected)):raise ValueError('native compose→display integration bytes')
            counts['native_wrapper']+=1
    font=ROOT/'external/fonts/Galmuri11.bdf';license=ROOT/'external/fonts/LICENSE-Galmuri.txt'
    require_hash(font,FONT_SHA256);require_hash(license,LICENSE_SHA256)
    glyphs=bdf_glyphs(font,set(KEYS));bank=b''.join(glyphs[k] for k in KEYS)
    out=ROOT/'analysis/hangul_keyboard_v1/cpu_editor_display';out.mkdir(parents=True,exist_ok=True)
    (out/'helper.bin').write_bytes(blob);(out/'jamo_normal.bin').write_bytes(bank)
    report=dict(id='exe45.hangul-keyboard.editor-display.v1',passed=True,rom_integrated=False,mapping_adopted_in_ROM=False,counts=counts,full_uint16_rank_domain=65536,complete_syllable_slot_vectors=11172*12,native_compact_to_display_integration=True,output_max_bytes=33,source_bytes=64,source_precondition='canonical full replay state validated upstream; this helper checks display surface, not packed history',machine_code=isa,jamo_mapping=JAMO_INDICES,preserved_comma_index=11172,font=dict(path='external/fonts/Galmuri11.bdf',sha256=FONT_SHA256,license_sha256=LICENSE_SHA256,normal_record_bytes=96,normal_bank_bytes=len(bank)),artifacts={p.name:sha(p.read_bytes()) for p in [out/'helper.bin',out/'jamo_normal.bin']},tools={n:sha((ROOT/'tools'/n).read_bytes()) for n in ['hangul_editor_display.py','bench_hangul_editor_display.py','korean_codec.py','build_visibility_poc.py']},dependencies={str(p.relative_to(ROOT)).replace('\\','/'):sha(p.read_bytes()) for p in [backend/'report.json',compact/'report.json']},limits=['Proposed jamo index11173..11212 has no glyph supply in current ROM; never feed this output to it yet.','Caller-owned output capacity33 for eight cells; old descriptor0 is32 and cannot be reused unmodified.','No padding/cursor/highlight/cache lifetime/rendering hook or persistence claim.','Native CPU fixture integration, not emulator game interaction; human readability/arrangement approval pending.'])
    (out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    print('PASS edit-display CPU',counts,'jamo bank',len(bank),flush=True)

if __name__=='__main__':main()
