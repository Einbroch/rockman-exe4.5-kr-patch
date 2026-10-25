"""Read-only source-pinned F9/0C descriptor investigation, NOT runtime proof."""
import json,struct
from report_roll_pet import ROOT,read,sha,require_hash
from run_gutsman_answers import STEM

def main():
    m=read(ROOT/f'poc/output/{STEM}.json');rp=ROOT/f'poc/output/{STEM}.gba';require_hash(rp,m['output_sha256']);rom=rp.read_bytes()
    sp=ROOT/read(ROOT/'project.json')['source_profile']['filename'];require_hash(sp,m['source_sha256']);source=sp.read_bytes()
    def word(at):return struct.unpack_from('<I',source,at)[0]
    if word(0x500e8)!=0x08051575 or word(0x51584)!=0x08051588 or word(0x51588+12*4)!=0x080517d1 or word(0x5181c)!=0x080526d0 or word(0x518f8)!=0x02010ac0:raise ValueError('source-pinned F9/0C dispatch chain')
    wrapper=m['extension']['machine_code'][0];at=wrapper['address']-0x08000000
    if struct.unpack_from('<I',rom,0x500e8)[0]!=wrapper['address']|1 or rom[at:at+10]!=bytes.fromhex('6178fc2901d01a4f3847') or struct.unpack_from('<I',rom,at+wrapper['literal_offset'])[0]!=0x08051575:raise ValueError('installed F9 wrapper must forward nonFC commands to native handler')
    # F9 slot intentionally points to the existing Korean wrapper; do NOT
    # incorrectly demand the original pointer and call the installed hook drift.
    regions=[(0x51574,0x51584,'F9 dispatcher CODE'),(0x51584,0x51588+13*4,'pointer literal and dispatch table DATA'),(0x517d0,0x5181c,'0C command consumer CODE'),(0x5181c,0x51820,'descriptor-table pointer DATA'),(0x518f8,0x518fc,'display-output pointer DATA'),(0x526d0+28*8,0x526d0+31*8,'string descriptors DATA'),(0x94c,0x956,'reverse byte-copy helper CODE')]
    guards=[]
    guards.append(dict(start=0x500e8,end=0x500ec,classification='installed Korean F9 wrapper pointer DATA',unchanged_in_product=False,final_pointer=wrapper['address']|1,nonFC_forward_to_original_verified=True,wrapper_first10_sha256=sha(rom[at:at+10])))
    for a,b,kind in regions:
        if source[a:b]!=rom[a:b]:raise ValueError('answer-buffer native region drift')
        guards.append(dict(start=a,end=b,classification=kind,sha256=sha(source[a:b]),unchanged_in_product=True))
    slots=[dict(command='printStringBuffer'+str(i-27),bytes_hex='f90c'+format(i,'02x'),descriptor=0x080526d0+i*8,source_pointer=word(0x526d0+i*8),r2_argument=word(0x526d0+i*8+4)) for i in (28,29,30)]
    result=dict(policy='development analysis; NON-DISTRIBUTION',release_eligible=False,source_sha256=m['source_sha256'],rom_sha256=m['output_sha256'],native_guards=guards,static_dispatch_chain=['080500E8 F9 slot ->08051575 Thumb dispatcher','08051584 literal ->08051588 dispatch table; index0C ->080517D1 Thumb consumer','080517E8 descriptor-table literal ->080526D0; index28/29/30, stride8','080517EE loads descriptor+4 into r2; 080517F0 loads source pointer into r0','080517F6 loads context+64 halfword, shifts left7; adds02010AC0 into copy destination r1','08051800 calls0800094C reverse byte-copy helper; context+64 increment; context+2C replaced with copied-output pointer'],descriptors=slots,writer_provenance_verified=False,runtime_consumer_verified=False,typed_hangul_commit_or_persistence_verified=False,limits=['Static descriptor addresses are NOT proof that data originated from committed player answers. Writer, field identity and save/reload ancestry remain unresolved.','r2=512 is recorded literally; do not reinterpret overlapping descriptor ranges as independent permanent records or infer safe Korean storage capacity.','The existing schedule observer uses02010AC0 too; shared transient output is not proof of the same producer. No buffer RAM was fabricated.'])
    out=ROOT/'analysis/gutsman_answers_v1/answer_buffer_static.json';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(json.dumps(slots,indent=2));return result

if __name__=='__main__':main()
