"""Native five-frequency lookup/F90C slots0..4 and calendar initializer facts.

Controlled CPU, no substituted native helper/BIOS and no product admission.
"""
import struct
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from bench_chip_library import REGS
from extended_dialogue import Cs,Ks,CS_ARCH_ARM,CS_MODE_THUMB,KS_ARCH_ARM,KS_MODE_THUMB
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_PROT_READ,UC_PROT_EXEC
from unicorn.arm_const import UC_ARM_REG_PC,UC_ARM_REG_CPSR,UC_CPU_ARM_TI925T
from bench_event_buffers_031 import BASE
from keyitem_rom_data_024 import verify_final

OUT='analysis/pending_insertion_500_031_frequency_cpu_v1/cpu.json'


def main():
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes();m=read(BASE.replace('.gba','.json'));require_hash(ROOT/BASE,m['output_sha256']);rom=(ROOT/BASE).read_bytes()
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB);ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB);ranges=[]
    # The existing composed key-item/mail selector owns4FB4C..58. Verify that
    # adopted selector and its native replay instead of claiming byte identity.
    verify_final(source,rom,m['keyitem_rom'])
    for a,b in [(0x3410E,0x34122),(0x32AA8,0x32AD8),(0x51E5C,0x51E72),(0x517D0,0x5181C),(0x94C,0x956),(0x322A8,0x322BE),(0x4F7B6,0x4F7CC),(0x4FB58,0x4FC20),(0x50338,0x5034A),(0x51E8C,0x51E9A)]:
        raw=source[a:b];ins=list(cs.disasm(raw,0x08000000+a))
        if sum(i.size for i in ins)!=len(raw) or rom[a:b]!=raw:raise ValueError('031 frequency/init source scope')
        for i in ins:
            if i.size not in (2,4) or i.size==4 and i.mnemonic!='bl' or bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+i.mnemonic+' '+i.op_str,i.address)[0])!=i.bytes:raise ValueError('031 frequency/init ARMv4T roundtrip')
        ranges.append(dict(offset=a,bytes=b-a,sha256=sha(raw),kind='code'))
    for a,n in [(0x34134,12),(0x51E74,4),(0x5263C,4),(0x526D0+67*8,8),(0x5181C,4),(0x518F8,4),(0x322D8,4),(0x5034C,4),(0x51E9C,4),(0x51C80,4),(0x50278,4)]:
        if source[a:a+n]!=rom[a:a+n]:raise ValueError('031 frequency/init literal drift')
        ranges.append(dict(offset=a,bytes=n,sha256=sha(source[a:a+n]),kind='data'))
    if struct.unpack_from('<I',source,0x5263C)[0]!=0x0803410F or struct.unpack_from('<I',source,0x322D8)[0]!=0x080322DC or struct.unpack_from('<II',source,0x526D0+67*8)!=(0x02014E54,32):raise ValueError('031 native dispatch/descriptor')
    roots=[]
    for index in range(23):
        at=0x322DC+index*4;native=struct.unpack_from('<I',source,at)[0];arc=f'{native-0x08000000:X}';current=next(a for a in m['archives'] if a['archive']==arc)
        if struct.unpack_from('<I',rom,at)[0]!=0x08000000+current['rom_offset']:raise ValueError('031 actual calendar root pointer')
        roots.append(dict(index=index,source_archive=arc,pointer_offset=at,current_pointer=0x08000000+current['rom_offset']))
    cases=[];bodies=[]
    for label,image in [('source',source),('030',rom)]:
        u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T);extent=(len(image)+4095)&~4095;u.mem_map(0x08000000,extent);u.mem_write(0x08000000,image);u.mem_protect(0x08000000,extent,UC_PROT_READ|UC_PROT_EXEC);u.mem_map(0x02000000,0x40000);u.mem_map(0x03000000,0x8000)
        writes=[];stop,stack,ctx,stream,record,buffer=0x080000C0,0x03007F00,0x0200FA20,0x02020000,0x02001310,0x02014E54
        u.hook_add(UC_HOOK_CODE,lambda uc,a,n,d:uc.emu_stop(),begin=stop,end=stop);u.hook_add(UC_HOOK_MEM_WRITE,lambda uc,t,a,n,v,d:writes.append((a,n)))
        def run(entry,allowed):
            before=[0x1000+i*0x101 for i in range(15)];before[4]=stream;before[5]=ctx;before[13]=stack;before[14]=stop|1
            u.reg_write(UC_ARM_REG_CPSR,0xF0000033)
            for r,v in zip(REGS,before):u.reg_write(r,v)
            u.mem_write(stack-256,b'\xA7'*256);writes.clear();u.emu_start(entry|1,0,count=3000)
            if u.reg_read(UC_ARM_REG_PC)!=stop or u.reg_read(REGS[13])!=stack or any(u.reg_read(REGS[i])!=before[i] for i in (5,6,8,9,10,11,12)):raise ValueError('031 frequency return/ABI')
            if bytes(u.mem_read(stack-256,128))!=b'\xA7'*128 or any(not(stack-128<=a and a+n<=stack or any(lo<=a and a+n<=hi for lo,hi in allowed)) for a,n in writes):raise ValueError('031 frequency allowed writes/canary')
        pool=struct.unpack_from('<I',image,0x32AD8)[0]
        for frequency in range(5):
            at=pool+struct.unpack_from('<H',image,pool-0x08000000+(119+frequency)*2)[0];off=at-0x08000000;end=image.index(b'\xE5',off,off+32)+1;body=image[off:end];glyphs=[];width=0;pos=0
            while pos<len(body)-1:
                x=body[pos];pos+=1
                if x==0xE4:x=228+body[pos];pos+=1
                elif x==0xF9:
                    if body[pos]!=0xFC:raise ValueError('031 frequency unexpected command')
                    x=m['extension']['legacy_index_view']+int.from_bytes(body[pos+1:pos+3],'little');pos+=3
                if x>=441 and label=='source':raise ValueError('031 source frequency glyph')
                width+=struct.unpack_from('<I',image,(0x5290C if label=='source' else m['extension']['advance_offset'])+x*4)[0];glyphs.append(x)
            if pos!=len(body)-1:raise ValueError('031 frequency complete glyph boundaries')
            bodies.append(dict(image=label,frequency=frequency,script=119+frequency,address=at,raw_hex=body.hex(),glyphs=glyphs,width=width))
            u.mem_write(0x02010ABC,b'\xA6'*(5*128+8));expected=bytearray(b'\xA6'*(5*128));u.mem_write(record,bytes(8)+bytes([frequency])+bytes(23));u.mem_write(0x02014DFC,struct.pack('<I',record))
            for slot in range(5):
                u.mem_write(ctx,bytes(216));u.mem_write(stream,bytes([0xFC,3,44,0]));u.mem_write(buffer-4,b'\xA6'*40);run(0x08051E5C,[(buffer,buffer+32)])
                if bytes(u.mem_read(buffer,32))!=body+b'\xA6'*(32-len(body)) or bytes(u.mem_read(buffer-4,4))+bytes(u.mem_read(buffer+32,4))!=b'\xA6'*8 or u.reg_read(REGS[4])!=stream+4:raise ValueError('031 frequency producer')
                u.mem_write(stream,bytes([0xF9,12,67]));u.mem_write(ctx+100,struct.pack('<H',slot));dest=0x02010AC0+slot*128;run(0x080517D0,[(ctx,ctx+216),(dest,dest+32)])
                expected[slot*128:slot*128+32]=body+b'\xA6'*(32-len(body))
                if bytes(u.mem_read(0x02010AC0,5*128))!=expected or bytes(u.mem_read(0x02010ABC,4))+bytes(u.mem_read(0x02010D40,4))!=b'\xA6'*8:raise ValueError('031 frequency all five slots retention')
                state=bytes(u.mem_read(ctx,216))
                if u.reg_read(REGS[4])!=dest or struct.unpack_from('<I',state,0x44)[0]!=stream+3 or struct.unpack_from('<H',state,100)[0]!=slot+1:raise ValueError('031 frequency continuation')
                cases.append(dict(image=label,frequency=frequency,slot=slot,prior_scratch_slots_preserved=True))
    deps=['tools/bench_event_frequency_031.py','tools/keyitem_rom_data_024.py']
    result=dict(schema=1,passed=True,source_sha256=sha(source),baseline_rom=BASE,baseline_sha256=sha(rom),cases=cases,case_count=len(cases),bodies=bodies,maximum_current_frequency_width=max(b['width'] for b in bodies if b['image']=='030'),native_ranges=ranges,calendar_roots=roots,default_context_origin=[52,110],default_origin_code=[0x4FBB4,0x4FBB8],composed_initializer_selector_verified=True,dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},rom_written=False,release_eligible=False,limits=['Five valid frequency values and native F90C slots0..4 in CPU, not arbitrary descriptor contents or date formatting.','Calendar table/entry/default origin and fullquick/skip opcode bytes statically bound; fullquick GBA route is separate.','No new translations applied, title producer universality, choice outcomes, Hangul input or persistence claim.'])
    frozen_write(ROOT/OUT,result);print('031 frequency PASS',len(cases),'source/030 cases; max current',result['maximum_current_frequency_width'],'px; no ROM',flush=True)


if __name__=='__main__':main()
