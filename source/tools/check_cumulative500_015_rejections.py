"""In-memory corruption of the merged tutorial's retained/new contract."""
from copy import deepcopy
from build_visibility_poc import ROOT,sha
from cumulative_batch500 import read,frozen_write
from cumulative_batch500_015 import verify_product_lineage
def main():
    cfg=read('project.json');source=(ROOT/cfg['source_profile']['filename']).read_bytes()
    rp=ROOT/'poc/output/exe45_ko_development_pending500_015_v1.gba';rom=rp.read_bytes();meta=read(str(rp.with_suffix('.json').relative_to(ROOT)))
    verify_product_lineage(source,rom,meta);results=[]
    for case in ('lost_declared_unit','lost_carry_id','changed_carry_metrics','changed_retained_script','changed_new_script','changed_pointer_bytes'):
        m=deepcopy(meta);data=bytearray(rom);r=next(x for x in m['archives'] if x['archive']=='768800')
        if case=='lost_declared_unit':m['translated_units']-=1
        elif case=='lost_carry_id':r['layout']=[x for x in r['layout'] if x['id']!='768800:1:0']
        elif case=='changed_carry_metrics':next(x for x in r['layout'] if x['id']=='768800:1:0')['line_advance_pixels'][0]+=1
        elif case in ('changed_retained_script','changed_new_script'):
            script=1 if case=='changed_retained_script' else 2;at=r['rom_offset']+int.from_bytes(data[r['rom_offset']+script*2:r['rom_offset']+script*2+2],'little');data[at]^=1
        else:data[r['pointers'][0]:r['pointers'][0]+4]=b'\0'*4
        try:verify_product_lineage(source,bytes(data),m)
        except ValueError as exc:results.append(dict(case=case,rejected=True,reason=str(exc)))
        else:raise ValueError('Accepted merged tutorial defect '+case)
    frozen_write(ROOT/'analysis/pending500_015_v1/rejection_controls.json',dict(passed=True,rom_sha256=sha(rom),valid_artifact_accepted=True,in_memory_only=True,controls=results))
    print('PASS six carry/payload/pointer defects rejected')
if __name__=='__main__':main()
