"""Bounded native nickname producer/descriptor CPU experiment; no ROM writes.

The Navi query is modeled, not its normal caller. Native string copies execute.
This does not admit translations or prove Hangul keyboard/save support.
"""
import argparse, json, struct, sys
from pathlib import Path
from build_visibility_poc import ROOT, sha, require_hash
from extended_dialogue import Cs, Ks, CS_ARCH_ARM, CS_MODE_THUMB, KS_ARCH_ARM, KS_MODE_THUMB
sys.path.insert(0, str(ROOT/'external/arm_bench_python'))
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB, UC_PROT_READ, UC_PROT_EXEC, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--rom', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args=parser.parse_args()
    profile=json.loads((ROOT/'project.json').read_text(encoding='utf8'))['source_profile']
    source=ROOT/profile['filename']; require_hash(source,profile['sha256'])
    product=json.loads(args.rom.with_suffix('.json').read_text(encoding='utf8'))
    require_hash(args.rom,product['output_sha256'])
    native=source.read_bytes(); current=args.rom.read_bytes()
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    cs=Cs(CS_ARCH_ARM,CS_MODE_THUMB); ks=Ks(KS_ARCH_ARM,KS_MODE_THUMB)
    ranges=[(0x38F60,0x38F84),(0x35E62,0x35E68),(0x32AB6,0x32AD8),(0x517D0,0x5181C),(0x94C,0x956),(0x39E2C,0x39E66)]
    code=[]
    for a,b in ranges:
        raw=native[a:b]
        if current[a:b]!=raw: raise ValueError('native code changed')
        ins=list(cs.disasm(raw,a+0x08000000))
        if sum(i.size for i in ins)!=len(raw): raise ValueError('instruction extent')
        for i in ins:
            assembled=bytes(ks.asm('.syntax unified\n.cpu arm7tdmi\n.thumb\n'+i.mnemonic+' '+i.op_str,i.address)[0])
            if i.size not in (2,4) or i.size==4 and i.mnemonic!='bl' or assembled!=i.bytes: raise ValueError('ISA roundtrip')
        code.append(dict(offset=a,bytes=b-a,sha256=sha(raw)))
    literals={0x38F84:0x0863720C,0x38F88:0x02000E50,0x38F8C:0x02000E5E,0x35EA4:0x02000950,0x5181C:0x080526D0,0x518F8:0x02010AC0,0x39E68:0x02000E50}
    for a,v in literals.items():
        if struct.unpack_from('<I',native,a)[0]!=v or current[a:a+4]!=native[a:a+4]: raise ValueError('literal identity')
    if struct.unpack_from('<II',native,0x526D8)!=(0x02000E5F,21) or current[0x526D8:0x526E0]!=native[0x526D8:0x526E0]: raise ValueError('nickname descriptor')
    table=0x63720C
    suffixes=[]
    for index in range(42):
        at=table+struct.unpack_from('<H',native,table+index*2)[0]
        end=native.index(0xE5,at)+1; data=native[at:end]
        if current[at:end]!=data or current[table+index*2:table+index*2+2]!=native[table+index*2:table+index*2+2]: raise ValueError('suffix identity')
        suffixes.append(data)
    widths=struct.unpack_from('<442I',native,0x5290C)
    # The existing extension preserves the legacy view. Index441 is reserved,
    # not part of the declared441 source glyph population.
    width_at=product['extension']['advance_offset']
    if current[width_at:width_at+441*4]!=native[0x5290C:0x5290C+441*4]: raise ValueError('legacy metric identity')
    def glyphs(data):
        result=[]; at=0
        while at<len(data):
            value=data[at]; at+=1
            if value==0xE5:
                if at!=len(data): raise ValueError('text trailing bytes')
                return result
            if value==0xE4:
                if at==len(data): raise ValueError('truncated native glyph')
                # Native E4 continuation adds228, not256. Normal runtime
                # E406 -> glyph234 at the renderer established this boundary.
                value=228+data[at]; at+=1
            if value>=442: raise ValueError('unsupported native fixture')
            result.append(value)
        raise ValueError('unterminated native fixture')
    rows=[]; counts=dict(writer=0,reader=0)
    for variant,image in [('source',native),('product',current)]:
        u=Uc(UC_ARCH_ARM,UC_MODE_THUMB); u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
        extent=(len(image)+4095)&~4095
        u.mem_map(0x08000000,extent); u.mem_write(0x08000000,image); u.mem_protect(0x08000000,extent,UC_PROT_READ|UC_PROT_EXEC)
        u.mem_map(0x02000000,0x40000); u.mem_map(0x03007000,4096); u.mem_map(0x0FF00000,4096)
        writes=[]; queried=[]; navi=0
        def services(cpu,pc,size,user):
            if pc==0x08000CEC:
                queried.append(navi); cpu.reg_write(UC_ARM_REG_R0,navi); cpu.reg_write(UC_ARM_REG_PC,cpu.reg_read(UC_ARM_REG_LR)|1)
        u.hook_add(UC_HOOK_CODE,services)
        u.hook_add(UC_HOOK_MEM_WRITE,lambda cpu,access,a,n,v,user:writes.append((a,n)))
        def execute(pc,allowed):
            u.reg_write(UC_ARM_REG_CPSR,0x30); u.reg_write(UC_ARM_REG_SP,0x03007F00); u.reg_write(UC_ARM_REG_LR,0x0FF00001)
            writes.clear(); u.emu_start(pc|1,0x0FF00000,count=10000)
            if u.reg_read(UC_ARM_REG_PC)!=0x0FF00000 or u.reg_read(UC_ARM_REG_SP)!=0x03007F00: raise ValueError('return/stack')
            if any(not(0x03007EF0<=a and a+n<=0x03007F00 or any(s<=a and a+n<=e for s,e in allowed)) for a,n in writes): raise ValueError('write extent')
        for navi in range(21):
            for gender in range(2):
                suffix=suffixes[navi*2+gender]
                for encoded in (b'\x9B',b'\xE4\x06'):
                    for length in range(7):
                        owner=encoded*length+b'\xE5'; expected=owner[:-1]+suffix
                        u.mem_write(0x02000000,b'\xA7'*0x40000)
                        u.mem_write(0x02000952,bytes([gender])); u.mem_write(0x02000E50,b'\x01'+owner)
                        before=bytes(u.mem_read(0x02000000,0x40000)); queried.clear()
                        execute(0x08038F60,[(0x02000E5E,0x02000E5F+len(expected))])
                        wanted=bytearray(before); wanted[0xE5E:0xE5F+len(expected)]=b'\x01'+expected
                        if bytes(u.mem_read(0x02000000,0x40000))!=wanted or queried!=[navi]: raise ValueError('nickname producer')
                        counts['writer']+=1
                        ctx=0x0200FA20; stream=0x02020000; buffer=0x02010AC0
                        u.mem_write(ctx,bytes(128)); u.mem_write(stream,bytes.fromhex('F90C01'))
                        u.reg_write(UC_ARM_REG_R4,stream); u.reg_write(UC_ARM_REG_R5,ctx)
                        before=bytes(u.mem_read(0x02000000,0x40000))
                        execute(0x080517D0,[(ctx,ctx+128),(buffer,buffer+21)])
                        wanted=bytearray(before); wanted[buffer-0x02000000:buffer-0x02000000+21]=before[0xE5F:0xE5F+21]
                        wanted[ctx-0x02000000+5]=1
                        for offset,value,fmt in [(0x64,1,'<H'),(0x2C,buffer,'<I'),(0x44,stream+3,'<I')]: struct.pack_into(fmt,wanted,ctx-0x02000000+offset,value)
                        if bytes(u.mem_read(0x02000000,0x40000))!=wanted or u.reg_read(UC_ARM_REG_R4)!=buffer or u.reg_read(UC_ARM_REG_R0)!=1: raise ValueError('nickname descriptor consumer')
                        counts['reader']+=1
                        if variant=='source': rows.append(dict(navi_fixture=navi,gender_fixture=gender,logical_length=length,owner_hex=owner.hex(),nickname_hex=expected.hex(),glyph_indices=glyphs(expected),advance=sum(widths[i] for i in glyphs(expected))))
    suffix_max=max(sum(widths[i] for i in glyphs(s)) for s in suffixes)
    conditional_bound=6*max(widths[:441])+suffix_max
    report=dict(schema=1,id='exe45.pending019.native-nickname.v1',status='BOUNDED_CPU_ANALYSIS_NOT_INSERTION_APPROVAL',source_sha256=profile['sha256'],rom_sha256=product['output_sha256'],tool_sha256=sha(Path(__file__).read_bytes()),counts=counts,native_code=code,literals={hex(a):hex(v) for a,v in literals.items()},suffix_hex=[s.hex() for s in suffixes],rows=rows,max_fixture_advance=max(r['advance'] for r in rows),descriptor_bytes=21,owner_initializer_logical_limit=6,conditional_native_bound=dict(glyph_population=441,max_glyph_advance=max(widths[:441]),max_suffix_advance=suffix_max,owner_six_glyphs_plus_suffix=conditional_bound,plus_current_comma=conditional_bound+12,conditions=['At most6 complete source glyphs, each index0..440.','Selected suffix index0..41, exact source table.','Native provider and metric path, not Hangul input or arbitrary save bytes.']),limits=['Navi query modeled with indices0..20, gender fixture0..1; normal selection/caller/save not exercised.','Only two native owner glyphs and lengths0..6 plus42 suffix selections. No full input repertoire/max-width claim.','Native name initializer contains limit6; initializer not executed in this experiment.','Native E4 glyph is two bytes/one glyph. Buffer byte width is not glyph width.','No aggregate translated page rendering, automatic Hangul input, storage/save/redisplay, new translation selection or product change.'])
    args.out.parent.mkdir(parents=True,exist_ok=True); args.out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    require_hash(source,profile['sha256']); require_hash(args.rom,product['output_sha256'])
    print('PASS bounded native nickname',counts,'max fixture advance',report['max_fixture_advance'])

if __name__=='__main__': main()
