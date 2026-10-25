"""Actual emitted local counter and unchanged E5 copy; synthetic CPU, not gameplay."""
import json
from report_roll_pet import ROOT,read,sha
from build_visibility_poc import require_hash
from bench_chip_library import Uc,UC_ARCH_ARM,UC_MODE_THUMB,UC_HOOK_CODE,REGS
from unicorn.arm_const import UC_ARM_REG_CPSR,UC_CPU_ARM_TI925T
from calendar_presets import SITE,END
from korean_codec import encode_hangul
from run_calendar_presets import STEM
_ENGINES={}

def execute(blob,body,start,end):
    key=id(blob)
    if key not in _ENGINES:
        u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T);u.mem_map(0x08000000,(len(blob)+4095)&~4095);u.mem_write(0x08000000,blob);u.mem_map(0x02000000,0x40000);u.mem_map(0x03000000,0x8000);_ENGINES[key]=(blob,u)
    u=_ENGINES[key][1]
    buf=0x02026080;u.mem_write(buf,body+b'\xa7'*64);u.reg_write(UC_ARM_REG_CPSR,0xF00000F3)
    before=[0x12345600+i for i in range(15)];before[1]=before[2]=0;before[3]=buf;before[13]=0x03007F00;before[14]=0x08001235
    for reg,value in zip(REGS,before):u.reg_write(reg,value)
    reached=[]
    def stop(engine,address,size,user):
        if address==end:reached.append(address);engine.emu_stop()
    hook=u.hook_add(UC_HOOK_CODE,stop);u.emu_start((0x08000000+start)|1,0,count=1000);u.hook_del(hook)
    if reached!=[end]:raise ValueError('counter continuation')
    return [u.reg_read(r) for r in REGS],u.reg_read(UC_ARM_REG_CPSR),bytes(u.mem_read(buf,len(body)+64)),before

def main(stem=STEM):
    rp=ROOT/f'poc/output/{stem}.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();source=(ROOT/read(ROOT/'project.json')['source_profile']['filename']).read_bytes();native_count=0
    # All native single-byte character values and all E4 extension payloads;
    # no claim that these bytes are all active keyboard entries.
    for body in [bytes([v,0xE5]) for v in range(0xE4)]+[bytes([0xE4,v,0xE5]) for v in range(256)]+[b'\xe5',bytes.fromhex('cfb4cae5'),bytes.fromhex('d1e407a2e5')]:
        a,af,am,_=execute(source,body,SITE,0x08000000+END);b,bf,bm,_=execute(rom,body,SITE,0x08000000+END)
        if a!=b or af!=bf or am!=bm:raise ValueError('native counter ABI/effects regression')
        native_count+=1
    hangul_count=0
    for index in range(11172):
        body=b'\xf9\xfc'+index.to_bytes(2,'little')+b'\xe5';regs,flags,after,before=execute(rom,body,SITE,0x08000000+END)
        expected=list(before);expected[:3]=[0xE5,4,1]
        if regs!=expected or flags&0xF0000000!=0x60000000 or after!=body+b'\xa7'*64:raise ValueError('Hangul count ABI/no data writes')
        hangul_count+=1
    # The native byte-at-a-time copy is safe only for the two selected default
    # names. Reject embeddedE5 before selecting a name; do not generalize to input.
    copy_rows=[]
    for name in ['식사','학원']:
        body=encode_hangul(name)+b'\xe5';u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.mem_map(0x08000000,0x800000);u.mem_write(0x08000000,source);u.mem_map(0x02000000,0x40000);u.mem_map(0x03000000,0x8000);src=0x02026080;dst=0x0200131A;u.mem_write(src,body);u.mem_write(dst,b'\xa7'*22);u.reg_write(REGS[0],src);u.reg_write(REGS[1],dst);u.reg_write(REGS[14],0x08032AD7);u.emu_start(0x08032AC7,0x08032AD6,count=100)
        if bytes(u.mem_read(dst,22))!=body+b'\xa7'*(22-len(body)):raise ValueError('native copy field/canary')
        copy_rows.append({'name':name,'copied_bytes':len(body),'trailing_field_bytes_unchanged':22-len(body)})
    result={'passed':True,'policy':'synthetic CPU bench; not gameplay/persistence','release_eligible':False,'rom_sha256':m['output_sha256'],'native_compatibility_vectors':native_count,'full_F9FC_counter_vectors':hangul_count,'native_copy_vectors':copy_rows,'limit':'Local counter supports valid F9FC indices; rawE5 copy verified only for selected twoE5-safe defaults. No Hangul keyboard/save/load proof.'}
    out=ROOT/'analysis/calendar_presets_poc_v1';out.mkdir(parents=True,exist_ok=True);(out/'counter_bench.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print('preset counter bench',native_count,hangul_count);return result

if __name__=='__main__':main()
