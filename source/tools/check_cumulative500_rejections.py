"""Artifact checker negative controls, never mutate an on-disk ROM or asset."""
from copy import deepcopy
from build_visibility_poc import ROOT
from cumulative_batch500 import read,verify_product_lineage,frozen_write
STEM='exe45_ko_development_pending500_007_v1'
OUT='analysis/pending500_007_v1/rejection_controls.json'
VERIFY=verify_product_lineage

def main():
    cfg=read('project.json');source=(ROOT/cfg['source_profile']['filename']).read_bytes()
    rp=ROOT/f'poc/output/{STEM}.gba';rom=rp.read_bytes();meta=read(str(rp.with_suffix('.json').relative_to(ROOT)))
    VERIFY(source,rom,meta);controls=[]
    for case in ('lost_declared_unit','lost_carry_id','changed_carry_metrics','changed_retained_script'):
        altered=deepcopy(meta);data=rom;r=next(r for r in altered['archives'] if r['archive']=='6DA21C')
        if case=='lost_declared_unit':altered['translated_units']-=1
        elif case=='lost_carry_id':r['layout']=[x for x in r['layout'] if x['id']!='6DA21C:0:0']
        elif case=='changed_carry_metrics':next(x for x in r['layout'] if x['id']=='6DA21C:0:0')['line_advance_pixels'][0]+=1
        else:
            data=bytearray(rom);at=r['rom_offset']+int.from_bytes(rom[r['rom_offset']:r['rom_offset']+2],'little');data[at]^=1;data=bytes(data)
        try:VERIFY(source,data,altered)
        except ValueError as exc:controls.append(dict(case=case,rejected=True,reason=str(exc)))
        else:raise ValueError('Checker accepted defect: '+case)
    out=ROOT/OUT
    if out.exists():raise ValueError('Preserve controls')
    frozen_write(out,dict(passed=True,valid_product_accepted=True,in_memory_only=True,controls=controls))
    print('PASS valid artifact accepted; four carry/population defects rejected')
if __name__=='__main__':main()
