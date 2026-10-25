"""New-archive checker controls; byte/ID/lookup corruption in memory only."""
from copy import deepcopy
from build_visibility_poc import ROOT,sha
from cumulative_batch500 import read,frozen_write
from cumulative_batch500_010 import verify_product_lineage
STEM='exe45_ko_development_pending500_010_v1'
ARCHIVE='6989B0'
OUT='analysis/pending500_010_v1/new_archive_controls.json'
def main():
    cfg=read('project.json');source=(ROOT/cfg['source_profile']['filename']).read_bytes();rp=ROOT/f'poc/output/{STEM}.gba';rom=rp.read_bytes();meta=read(str(rp.with_suffix('.json').relative_to(ROOT)))
    verify_product_lineage(source,rom,meta);controls=[]
    for case in ('new_payload_corrupt','new_source_id_lost','new_pointers_changed','new_pointer_bytes_corrupt','native_source_storage_changed'):
        m=deepcopy(meta);data=bytearray(rom);record=next(r for r in m['archives'] if r['archive']==ARCHIVE)
        if case=='new_payload_corrupt':data[record['rom_offset']+int.from_bytes(data[record['rom_offset']:record['rom_offset']+2],'little')]^=1
        elif case=='new_source_id_lost':record['layout']=record['layout'][1:]
        elif case=='new_pointers_changed':record['pointers']=[]
        elif case=='new_pointer_bytes_corrupt':data[record['pointers'][0]:record['pointers'][0]+4]=b'\0'*4
        else:data[int(ARCHIVE,16)]^=1
        try:verify_product_lineage(source,bytes(data),m)
        except ValueError as exc:controls.append(dict(case=case,rejected=True,reason=str(exc)))
        else:raise ValueError('Accepted new-archive defect '+case)
    out=ROOT/OUT
    if out.exists():raise ValueError('Preserve controls')
    frozen_write(out,dict(passed=True,rom_sha256=sha(rom),valid_artifact_accepted=True,in_memory_only=True,controls=controls))
    print('PASS five new-archive defects rejected')
if __name__=='__main__':main()
