"""Five actual changed-archive defects, including new line metrics, in memory."""
from copy import deepcopy
from build_visibility_poc import ROOT,sha
from cumulative_batch500 import read,frozen_write
from cumulative_batch500_017 import verify_product_lineage
def main():
    cfg=read('project.json');source=(ROOT/cfg['source_profile']['filename']).read_bytes();stem='exe45_ko_development_pending500_017_v1';rom=(ROOT/f'poc/output/{stem}.gba').read_bytes();meta=read(f'poc/output/{stem}.json')
    verify_product_lineage(source,rom,meta);controls=[]
    for case in ('changed_payload_corrupt','new_id_lost','new_metrics_changed','pointer_bytes_corrupt','native_source_storage_changed'):
        m=deepcopy(meta);data=bytearray(rom);r=next(r for r in m['archives'] if r['archive']=='716DE4')
        if case=='changed_payload_corrupt':data[r['rom_offset']+int.from_bytes(data[r['rom_offset']:r['rom_offset']+2],'little')]^=1
        elif case=='new_id_lost':r['layout']=[u for u in r['layout'] if u['id']!='716DE4:14:0']
        elif case=='new_metrics_changed':next(u for u in r['layout'] if u['id']=='716DE4:14:0')['line_advance_pixels'][0]+=1
        elif case=='pointer_bytes_corrupt':data[r['pointers'][0]:r['pointers'][0]+4]=b'\0'*4
        else:data[0x716DE4]^=1
        try:verify_product_lineage(source,bytes(data),m)
        except ValueError as exc:controls.append(dict(case=case,rejected=True,reason=str(exc)))
        else:raise ValueError('Accepted changed-archive defect '+case)
    frozen_write(ROOT/'analysis/pending500_017_v1/changed_archive_controls.json',dict(passed=True,rom_sha256=sha(rom),valid_artifact_accepted=True,in_memory_only=True,controls=controls))
    print('PASS five changed-archive defects rejected')
if __name__=='__main__':main()
