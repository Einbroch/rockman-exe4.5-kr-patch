"""Static literal reader candidates for all three description root words.

Raw opcode candidates do not establish executable code or full reachability.
"""
import json
import struct
from build_visibility_poc import ROOT,sha,require_hash
from report_chip_library_runtime import read,require


def analyze(blob,offset):
    target=0x08000000+offset;readers=[]
    for at in range(max(0,offset-4096),min(len(blob)-3,offset+4096),2):
        h=struct.unpack_from('<H',blob,at)[0];pc=(0x08000000+at+4)&~3
        if h&0xF800 in (0x4800,0xA000) and pc+(h&255)*4==target:
            readers.append({'address':0x08000000+at,'mode':'Thumb','kind':'LDR literal' if h&0xF800==0x4800 else 'ADR','hex':blob[at:at+2].hex()})
        if at%4==0:
            w=struct.unpack_from('<I',blob,at)[0]
            if w&0x0E500000==0x04100000 and (w>>16)&15==15 and w&(1<<24):
                pc=0x08000000+at+8;address=pc+(w&4095)*(1 if w&(1<<23) else -1)
                if address==target: readers.append({'address':0x08000000+at,'mode':'ARM','kind':'LDR literal candidate','hex':blob[at:at+4].hex()})
    pointers=[0x08000000+at for at in range(0,len(blob)-3,4) if struct.unpack_from('<I',blob,at)[0] in (target,target|1)]
    return {'root_offset':offset,'root_address':target,'source_value':struct.unpack_from('<I',blob,offset)[0],'direct_reader_candidates':readers,'aligned_exact_address_word_references':pointers}


def main():
    project=read(ROOT/'project.json');path=ROOT/project['source_profile']['filename'];require_hash(path,project['source_profile']['sha256']);blob=path.read_bytes()
    roots=[analyze(blob,offset) for offset in (0x2165C,0xD2B58,0xD4D0C)]
    require(all(r['source_value']==0x0876937C for r in roots),'description source root drift')
    out=ROOT/'analysis/exe45_description_roots_static_v2.json';require(not out.exists(),'refuse report overwrite')
    out.write_text(json.dumps({'source_sha256':sha(blob),'tool_sha256':sha((ROOT/'tools/analyze_description_roots_v2.py').read_bytes()),'roots':roots,
        'scope':'All possible local Thumb literal/ADR and ARM immediate PC word-load candidates, plus full-ROM aligned exact-address word references',
        'limits':['opcode candidates may be data, not executed code','no direct reader is not proof of no computed/register-base read or unreachable code','D2B58 runtime unresolved; 2165C/D4D0C separately observed on129-unit ROM']},indent=2),encoding='utf-8')
    print([(hex(r['root_address']),len(r['direct_reader_candidates']),len(r['aligned_exact_address_word_references'])) for r in roots])


if __name__=='__main__': main()
