"""Conditional native calendar title classes and actual030 suffix execution.

Only existing legacy editors and two exact F9FC presets. Not new Hangul input,
imported/corrupt records, all writers or a product admission gate.
"""
import struct
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from bench_chip_library import REGS
from extended_dialogue import Cs,Ks,CS_ARCH_ARM,CS_MODE_THUMB,KS_ARCH_ARM,KS_MODE_THUMB
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_PROT_READ,UC_PROT_EXEC
from unicorn.arm_const import UC_ARM_REG_PC,UC_ARM_REG_CPSR,UC_CPU_ARM_TI925T
from bench_event_buffers_031 import BASE,OUT as EVENT_CPU
from korean_codec import encode_hangul

OUT='analysis/pending_insertion_500_031_event_title_bounds_v1/cpu.json'


def main():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    meta=read(BASE.replace('.gba','.json'));require_hash(ROOT/BASE,meta['output_sha256']);rom=(ROOT/BASE).read_bytes();prior=read(EVENT_CPU)
    if not prior['passed'] or prior['baseline_sha256']!=sha(rom):raise ValueError('031 event provider baseline')
    for p,h in prior['dependencies'].items():require_hash(ROOT/p,h)
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB);ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB);regions=[]
    for a,b in [(0x30E18,0x30E6C),(0x30EAA,0x30F02),(0x3100A,0x31060),(0x33020,0x3303C),(0x32AA8,0x32AD8)]:
        raw=source[a:b];ins=list(cs.disasm(raw,0x08000000+a))
        if sum(i.size for i in ins)!=len(raw) or rom[a:b]!=raw:raise ValueError('031 native title scope')
        for i in ins:
            if i.size not in (2,4) or i.size==4 and i.mnemonic!='bl' or bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+i.mnemonic+' '+i.op_str,i.address)[0])!=i.bytes:raise ValueError('031 title ARMv4T roundtrip')
        regions.append(dict(offset=a,bytes=b-a,sha256=sha(raw)))
    for a,n in [(0x30F04,8),(0x31060,8),(0x33064,4)]:
        if source[a:a+n]!=rom[a:a+n]:raise ValueError('031 title literal drift')
        regions.append(dict(offset=a,bytes=n,sha256=sha(source[a:a+n])))
    if struct.unpack_from('<I',source,0x33064)[0]!=0x02026080 or source[0x31012:0x31016]!=bytes.fromhex('0a202721'):raise ValueError('031 custom title cap10')
    native_widths=struct.unpack_from('<441I',source,0x5290C)
    if max(native_widths)!=11:raise ValueError('031 source native maximum width')
    if any(struct.unpack_from('<I',rom,meta['extension']['advance_offset']+i*4)[0]!=v for i,v in enumerate(native_widths)):raise ValueError('031 actual native metric drift')
    cases=[];classes=[];presets=[]
    for label,image in [('source',source),('030',rom)]:
        u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T);extent=(len(image)+4095)&~4095
        u.mem_map(0x08000000,extent);u.mem_write(0x08000000,image);u.mem_protect(0x08000000,extent,UC_PROT_READ|UC_PROT_EXEC);u.mem_map(0x02000000,0x40000);u.mem_map(0x03000000,0x8000)
        writes=[];stops=(0x08030E3E,0x0803303C);u.hook_add(UC_HOOK_MEM_WRITE,lambda uc,t,a,n,v,d:writes.append((a,n)))
        def hook(uc,a,n,d):
            if a in stops:uc.emu_stop()
        u.hook_add(UC_HOOK_CODE,hook)
        def run(entry,regs,stop):
            before=[0x1000+i*0x101 for i in range(15)];before[13]=0x03007F00;before[14]=0x080000C1
            for k,v in regs.items():before[k]=v
            u.reg_write(UC_ARM_REG_CPSR,0xF0000033)
            for r,v in zip(REGS,before):u.reg_write(r,v)
            u.mem_write(0x03007E00,b'\xA7'*256);writes.clear();u.emu_start(entry|1,0,count=2000)
            if u.reg_read(UC_ARM_REG_PC)!=stop or u.reg_read(REGS[13])!=before[13]:raise ValueError('031 scoped block stop/stack')
            if bytes(u.mem_read(0x03007E00,128))!=b'\xA7'*128:raise ValueError('031 title stack canary')
            if any(u.reg_read(REGS[i])!=before[i] for i in range(5,13)):raise ValueError('031 scoped preserved registers')
        for selection,cap,heading in [(1,8,35),(3,8,37),(4,6,38)]:
            run(0x08030E18,{0:selection},0x08030E3E)
            if (u.reg_read(REGS[0]),u.reg_read(REGS[1]))!=(cap,heading) or writes:raise ValueError('031 native title selector')
            classes.append(dict(image=label,selector=selection,editor_cap=cap,heading_script=heading))
        pool=struct.unpack_from('<I',image,0x32AD8)[0]
        def script_body(index):
            a=pool+struct.unpack_from('<H',image,pool-0x08000000+index*2)[0];p=a-0x08000000;e=image.index(b'\xE5',p,p+32)+1;return a,image[p:e]
        address,suffix=script_body(69)
        if suffix!=bytes.fromhex('aee463e469e5'):raise ValueError('031 actual unchanged friend suffix')
        for token in (b'\x9B',b'\xE4\x06'):
            for length in range(7):
                initial=token*length+b'\xE5';expected=initial[:-1]+suffix;u.mem_write(0x0202607C,b'\xA6'*49);u.mem_write(0x02026080,initial)
                run(0x0803302A,{},0x0803303C)
                if bytes(u.mem_read(0x02026080,41))!=expected+b'\xA6'*(41-len(expected)) or bytes(u.mem_read(0x0202607C,4))+bytes(u.mem_read(0x020260A9,4))!=b'\xA6'*8:raise ValueError('031 native suffix append exact bytes/canaries')
                if any(not(0x02026080<=a and a+n<=0x02026080+len(expected) or 0x03007E80<=a and a+n<=0x03007F00) for a,n in writes):raise ValueError('031 suffix unexpected write')
                cases.append(dict(image=label,native_token=token.hex(),person_glyphs=length,title_glyphs=length+3,title_bytes=len(expected),maximum_width=(length+3)*11))
        for index,name in ((62,'식사'),(63,'학원')):
            at,body=script_body(index)
            if label=='030' and body!=encode_hangul(name)+b'\xE5':raise ValueError('031 current preset identity')
            presets.append(dict(image=label,script=index,address=at,bytes=len(body),raw_hex=body.hex(),width=24 if label=='030' else 33))
    deps=[EVENT_CPU,'analysis/pending_insertion_500_031_event_runtime_v1/verification.json','tools/bench_event_title_bounds_031.py']
    frozen_write(ROOT/OUT,dict(schema=1,passed=True,source_sha256=sha(source),baseline_rom=BASE,baseline_sha256=sha(rom),native_ranges=regions,selector_cases=classes,suffix_cases=cases,actual_presets=presets,native_maximum_glyph_width=11,conditional_valid_legacy_title_bound=110,conditional_title_field_bytes=22,conditional_title_classes={'TV-native8':88,'manual-native8':88,'friend-native6-plus-source3':99,'custom-native10':110,'actual-two-Hangul-presets':24},dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},product_admitted=False,rom_written=False,release_eligible=False,limits=['Scoped selector and suffix blocks execute unchanged source/030, not full UI/default/import/persistence acquisition.','110px is conditional on these valid existing native editor classes or two exact presets, NOT arbitrary22byte records, unknown producers or new Hangul input.','Direct anniversary and imported/save-derived records require their own provider applicability; not proved by this experiment.','Do not use this as blanket admission for203event scripts or native GBA max-name rendering.']))
    print('031 native title selectors6/suffix28/actual presets4 PASS; conditional110px; no ROM',flush=True)


if __name__=='__main__':main()
