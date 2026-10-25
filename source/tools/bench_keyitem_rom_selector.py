"""Analysis CPU experiment; no GBA ROM output and no renderer/runtime claim."""
import argparse,json,struct
from collections import Counter
from build_visibility_poc import ROOT,sha,require_hash
from verify_tpi_index import lz77_decompress
from archive_scripts import script_spans
from keyitem_empty import resolved
from keyitem_rom_selector_probe import construct,CALLERS,INSTALL,EXPECTED
from bench_chip_library import REGS
import unicorn
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_PC,UC_ARM_REG_CPSR

STEM='exe45_ko_development_possessions_statistics_v1'
DRAFT_SHA='a83c2de2991efc47028ec07a784a9c9a53ea547469b376dcba74944e5b535da0'
FULL_SHA='85452fd9d03dc22a89f322ec472e19e11d09ecf6c0058cd63ad0c015016738c8'

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='analysis/keyitem_rom_selector_probe_v1');ap.add_argument('--stem',default=STEM);ap.add_argument('--integrated',action='store_true');args=ap.parse_args()
    out=ROOT/args.out
    if out.exists():raise ValueError('preserve CPU experiment evidence')
    rp=ROOT/f'poc/output/{args.stem}.gba';m=json.loads(rp.with_suffix('.json').read_text(encoding='utf8'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes()
    original=ROOT/'Rockman EXE 4.5 Real Operation (J)(Independent).gba';require_hash(original,m['source_sha256']);source=original.read_bytes()
    require_hash(ROOT/'analysis/keyitem_translation_draft_v1/draft.json',DRAFT_SHA)
    full=ROOT/'analysis/keyitem_translation_draft_v1/bench/full-draft/709408.msg';require_hash(full,FULL_SHA);payload=full.read_bytes();spans=resolved(payload)
    if len(payload)!=2477 or source[INSTALL:INSTALL+12]!=EXPECTED or (not args.integrated and rom[INSTALL:INSTALL+12]!=EXPECTED):raise ValueError('full draft/source reader')
    keyroot=struct.unpack_from('<I',rom,0x4c5e8)[0];active,_=lz77_decompress(rom,keyroot-0x08000000);alt,_=lz77_decompress(source,0x709704)
    if len(active)!=1273 or struct.unpack_from('<H',alt)[0]!=90 or active[:16]!=lz77_decompress(source,0x709408)[0][:16]:raise ValueError('active/alternate archive identity')
    if args.integrated:
        from keyitem_rom_data import verify_final
        verify_final(source,rom,m['keyitem_rom'])
        clone=0x08000000+m['keyitem_rom']['rom_offset'];hook=m['keyitem_rom']['hook_address']
        if rom[clone-0x08000000:clone-0x08000000+len(payload)]!=payload:raise ValueError('integrated39 selected wording identity')
    else:clone=(0x08000000+len(rom)+3)&~3;hook=(clone+len(payload)+3)&~3
    stub,code,meta=construct(source,active[:16],clone,hook)
    require_hash(ROOT/'external/arm_bench_python/unicorn/lib/unicorn.dll','010d85dce84b8f6ffaec3d5420f1b5f7768f859eb831be574c7da23e656ee8f1')
    require_hash(ROOT/'external/arm_bench_python/unicorn/unicorn_py3/unicorn.py','b4de7d560790a587157b17edd71c83b4f2d2bade2447d1a5433c497468ac8aeb')
    if unicorn.__version__!='2.1.4':raise ValueError('CPU version drift')
    u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    u.mem_map(0x08000000,(max(0x08000000+len(rom),hook+len(code))-0x08000000+4095)&~4095);u.mem_write(0x08000000,rom);u.mem_write(clone,payload);u.mem_write(hook,code)
    u.mem_map(0x02000000,0x40000);u.mem_map(0x03000000,0x8000)
    writes=[];clears=[];stop=0x0804FB90;context=0x0200FA20;global_context=0x02000100;stack=0x03007F00
    def callback(uc,address,size,user):
        if address==stop:uc.emu_stop()
        elif address==0x0800090C:
            # Only native bulk-zero helper is substituted by its bounded
            # contract. Native prologue, context restoration and lookup run.
            at=uc.reg_read(REGS[0]);n=uc.reg_read(REGS[1]);clears.append((at,n))
            if (at,n)!=(context,216):raise ValueError('unexpected zero-helper contract')
            uc.mem_write(at,bytes(n));uc.reg_write(UC_ARM_REG_PC,uc.reg_read(REGS[14]))
    u.hook_add(UC_HOOK_CODE,callback)
    u.hook_add(UC_HOOK_MEM_WRITE,lambda uc,a,address,size,value,user:writes.append((address,size)))
    cases=[]
    def execute(root,script,caller,blob,patched):
        u.mem_write(0x08000000+INSTALL,stub if patched else EXPECTED)
        u.ctl_remove_cache(0x08000000+INSTALL,0x08000000+INSTALL+12)
        u.mem_write(root,blob);u.mem_write(global_context+44,struct.pack('<I',context));u.mem_write(context,bytes([0xA7])*216)
        u.mem_write(context+76,struct.pack('<4I',0x12345678,0x23456789,0x3456789A,0x456789AB));u.mem_write(stack-128,bytes([0xCC])*128)
        before=[0x1000+i*0x101 for i in range(15)];before[0]=root;before[1]=script;before[10]=global_context;before[13]=stack;before[14]=caller
        for reg,value in zip(REGS,before):u.reg_write(reg,value)
        u.reg_write(UC_ARM_REG_CPSR,0xF0000033);writes.clear();clears.clear();u.emu_start(0x08000000+INSTALL+1,0,count=1000)
        after=[u.reg_read(reg) for reg in REGS]
        if u.reg_read(UC_ARM_REG_PC)!=stop or clears!=[(context,216)]:raise ValueError('native continuation/zero-helper')
        if any(not (context<=a and a+n<=context+216 or stack-64<=a and a+n<=stack) for a,n in writes):raise ValueError('write escaped original context/stack')
        if bytes(u.mem_read(root,len(blob)))!=blob or bytes(u.mem_read(clone,len(payload)))!=payload:raise ValueError('text-RAM/ROM clone mutated')
        return after,bytes(u.mem_read(context,216)),u.reg_read(UC_ARM_REG_CPSR),list(writes)
    def case(kind,root,script,caller,blob,translated):
        native,nram,nflags,_=execute(root,script,caller,blob,False)
        patched,pram,pflags,wr=execute(root,script,caller,blob,True)
        chosen=clone if translated else root
        table=payload if translated else blob
        offset=struct.unpack_from('<H',table,script*2)[0]
        expected=native.copy();expected[1]=offset
        comparison=bytearray(nram);struct.pack_into('<I',comparison,0x30,chosen);struct.pack_into('<I',comparison,0x2c,chosen+offset);struct.pack_into('<I',comparison,0x34,chosen+offset)
        if patched!=expected or pram!=bytes(comparison) or pflags!=nflags:
            raise ValueError(f'ABI/context/flags failed:{kind}/{hex(root)}/{script}/{hex(caller)} registers={[(i,hex(a),hex(b)) for i,(a,b) in enumerate(zip(patched,expected)) if a!=b]} context_bytes={[i for i,(a,b) in enumerate(zip(pram,comparison)) if a!=b]} flags={hex(pflags)}/{hex(nflags)}')
        if translated and bytes(u.mem_read(chosen+offset,len(spans[script])))!=spans[script]:raise ValueError('all49 native script starts')
        cases.append(dict(kind=kind,root=root,script=script,caller=caller,translated=translated,chosen_root=chosen,native_stream=chosen+offset,registers_and_flags_preserved_except_declared_offset=True,context_only_declared_root_stream_fields_differ=True,writes_original_context_and_stack_only=True))
    for root,callers in CALLERS.items():
        for caller in callers:
            for script in range(49):case('keyitem',root,script,caller,active,True)
            for script in range(45):case('alternate709704',root,script,caller,alt,False)
            for byte in range(16):
                changed=bytearray(active);changed[byte]^=1
                for script in [0,32,48]:case('changed-header',root,script,caller,bytes(changed),False)
            # Invalid native scriptIDs must preserve the original reader;
            # bytes beyond the49-word table remain source bytes, not a table.
            for script in [49,50,127,128,255]:case('out-of-scope-script',root,script,caller,active,False)
    for root in [0x02020800,0x02031000,0x02038000]:
        for caller in [0x08012345,0x0803497D,0x0804CC33]:
            for script in [0,6,32,48]:case('unknown-caller-or-root',root,script,caller,active,False)
    result=dict(passed=True,scope='Analysis-only synthetic CPU execution; native bulk-zero helper substituted; NOT GBA runtime/render/timing or product build.',
        source_sha256=sha(source),baseline_rom_sha256=sha(rom),draft_sha256=DRAFT_SHA,compiled_full_draft_sha256=sha(payload),compiled_full_draft_bytes=len(payload),rom_file_modified=False,new_translation_units_applied=0,
        vectors=len(cases),case_counts=dict(Counter(x['kind'] for x in cases)),selector=meta,cases=cases,integrated_artifact_final_bytes_checked=args.integrated,
        rejected_choices=['Do not grow either decompression beyond original1291 without a lifetime proof.','Do not replace both02031000 roots unconditionally: loader selects709408 or709704.','Do not interpret table/graphics literals as executable instructions or dialogue-root evidence.'],
        limits=['No primary-builder integration or changed-ROM runtime yet.','Other02031000 consumer not reached by the normal navigation attempts; shop/inventory interpretation remains a hypothesis.','All39 wording/glossary and quantity bounds/layout need contextual checks; no release eligibility.','Global Hangul input/commit/all redisplays/fresh persistence/old-save compatibility remain open.'])
    out.mkdir(parents=True);(out/'selector.bin').write_bytes(code);(out/'entry_stub.bin').write_bytes(stub);(out/'report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps({k:result[k] for k in ['passed','vectors','case_counts','compiled_full_draft_bytes','rom_file_modified','new_translation_units_applied']},indent=2))
if __name__=='__main__':main()
