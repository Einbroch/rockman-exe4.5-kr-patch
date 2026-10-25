"""Bounded native save, cold-process reload and list redisplay of school default."""
import json
from pathlib import Path
from build_visibility_poc import ROOT, sha, require_hash
from report_roll_pet import read
from report_fixedcell_runtime import verify_route
from korean_codec import encode_hangul
from fixedcell_font import bdf_cells

STEM='exe45_ko_development_calendar_presets_poc_v1'
PREFIX='calendar-presets-persist-v1-'

def main():
    m=read(ROOT/f'poc/output/{STEM}.json');rp=ROOT/f'poc/output/{STEM}.gba'
    require_hash(rp,m['output_sha256']);rom=rp.read_bytes()
    cfg=read(ROOT/'project.json');require_hash(ROOT/cfg['source_profile']['filename'],m['source_sha256'])
    rt=ROOT/'poc/runtime';commit=rt/(PREFIX+'save-commit');boot=rt/(PREFIX+'reboot');view=rt/(PREFIX+'reload-final-query')
    ce=read(commit/'save_environment.json');be=read(boot/'probe_environment.json')
    sav=STEM+'.sav';rtc=STEM+'.rtc'
    if ce['build_sha256']!=m['output_sha256']:raise ValueError('save artifact')
    before=ce['files_before'][sav];after=ce['files_after'][sav]
    if before!={'bytes':65536,'sha256':sha(bytes([255])*65536)} or after['bytes']!=65536 or after==before:raise ValueError('actual native save disk edge')
    require_hash(commit/'persistent_files_after'/sav,after['sha256'])
    for name in set(ce['files_before'])|set(ce['files_after']):
        if name not in (sav,rtc) and ce['files_before'].get(name)!=ce['files_after'].get(name):raise ValueError('unrelated save changed')
    if read(boot/'result.json')['state_origin'] is not None or be['files_before'][sav]!=after or be['files_after'][sav]!=after:raise ValueError('not a fresh process/disk reload')
    chain=[boot,rt/(PREFIX+'reload-direct'),rt/(PREFIX+'reload-calendar3'),view]
    for i,p in enumerate(chain):
        verify_route(p,m['output_sha256'],set())
        r=read(p/'result.json')
        if i and Path(r['state_origin']).resolve()!=(chain[i-1]/'result.json').resolve():raise ValueError('reload descendant chain')
        e=read(p/'probe_environment.json')
        if e['files_before'][sav]!=after or e['files_after'][sav]!=after:raise ValueError('disk identity drift')
    body=encode_hangul('학원')+b'\xe5'
    expected=bytes.fromhex('03000001010602000003')+body+bytes(13)
    prior=(rt/'calendar-presets-poc-v1-school-query/final_gbaExtWorkRam.bin').read_bytes()
    if prior[0x1310:0x1330]!=expected:raise ValueError('original registration')
    for p in chain:
        ram=(p/'final_gbaExtWorkRam.bin').read_bytes()
        if ram[0x1310:0x1330]!=expected:raise ValueError('persistent canonical name/header/field')
    cp='step_011';fc=m['fixedcell_extension']['mono_provider'];calls=read(view/(cp+'_fixedcells.json'))['calls']
    chosen=[c for c in calls if c['target']==0x0600A400 and [g['index'] for g in c['glyphs'][:2]]==[ord(ch)-0xAC00 for ch in '학원']]
    if len(chosen)!=1:raise ValueError('list actual Hangul consumer')
    c=chosen[0];provider=0x08000000+fc['font_offset'];glyphs=bdf_cells(ROOT/fc['font']['path'],set('학원'),fc['raster'])
    stage=(view/f"fixed_{c['id']:04}_stage.bin").read_bytes();records=[]
    for i,g in enumerate(c['glyphs']):
        off=g['font']-0x08000000+g['index']*64;record=rom[off:off+64];records.append(record)
        if i<2 and (g['font']!=provider or record!=glyphs['학원'[i]]):raise ValueError('list BDF/provider mismatch')
    vram=(view/(cp+'_gbaVideoRam.bin')).read_bytes()
    if stage!=b''.join(records) or vram[0xA400:0xA400+len(stage)]!=stage:raise ValueError('list staging/upload')
    out=ROOT/'analysis/calendar_presets_poc_v1';result={
        'passed':True,'policy':'functional-poc; NON-DISTRIBUTION','release_eligible':False,
        'rom_sha256':m['output_sha256'],'name':'학원','native_save_before':before,'native_save_after':after,
        'cold_boot_state_origin':None,'canonical_record_hex':expected.hex(),'normal_reload_chain':[str(p.relative_to(ROOT)) for p in chain],
        'list_glyph_provider_stage_vram':True,'list_screenshot':str((view/(cp+'.png')).relative_to(ROOT)),
        'visual_review':'Primary agent directly viewed 1 January list: 학원 at 2:00 AM. This is a fixed-cell list, not the normal-font detail dialogue.',
        'tool_sha256':sha(Path(__file__).read_bytes()),
        'limits':['Only the selected school default record; meal persistent reload pending.','No Hangul keyboard/editing, old-save compatibility, other names, full-game, RTC/alarm, audio/hardware or release approval.','Failed navigation captures retained, excluded from success chain.','This strengthens the named presets ROM only; later ROMs require their own runtime verification.']}
    (out/'persistence_runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print('school default native save/cold reload/list: PASS');return result

if __name__=='__main__':main()
