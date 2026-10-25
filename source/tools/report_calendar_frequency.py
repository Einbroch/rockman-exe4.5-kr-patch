"""Bind the native frequency loader, exact decoded output, OBJ selection and pixels."""
import json,struct
from pathlib import Path
from PIL import Image
from build_visibility_poc import ROOT,sha,require_hash
from report_fixedcell_runtime import verify_route
from calendar_frequency_graphics import BASE,STORED,construct,decode,WORDS
from verify_tpi_index import lz77_decompress
from run_calendar_frequency import STEM,PREFIX

def main():
    rp=ROOT/f'poc/output/{STEM}.gba';m=json.loads(rp.with_suffix('.json').read_text());require_hash(rp,m['output_sha256']);rom=rp.read_bytes()
    source=(ROOT/json.loads((ROOT/'project.json').read_text())['source_profile']['filename']).read_bytes()
    asset=json.loads((ROOT/'translations/calendar_frequency_graphics_ko.json').read_text(encoding='utf-8'));stored,payload,prepared=construct(source,asset)
    if rom[BASE:BASE+STORED]!=stored:raise ValueError('ROM asset')
    baseline=ROOT/'poc/output/exe45_ko_development_calendar_date_v1.gba';require_hash(baseline,'afc8a779872ad6e81db8a6b29f96af9423540ed14062e2940953afebd78bf7c1');old=baseline.read_bytes()
    if old[:BASE]!=rom[:BASE] or old[BASE+STORED:]!=rom[BASE+STORED:]:raise ValueError('unrelated ROM difference')
    require_hash(ROOT/f'poc/output/{STEM}_repro.gba',m['output_sha256'])
    p=ROOT/'poc/runtime'/(PREFIX+'selector');route=verify_route(p,m['output_sha256'],set());env=json.loads((p/'frequency_upload_environment.json').read_text())
    if not env['observer_only'] or env['self_sha256']!=sha((ROOT/'tools/capture_frequency_upload.py').read_bytes()) or env['runner_sha256']!=sha((ROOT/'tools/run_mesen_segment.py').read_bytes()):raise ValueError('observer drift')
    loads=json.loads((p/'step_013_frequency_loads.json').read_text())['loads']
    if len(loads)!=1:raise ValueError('loader population')
    load=loads[0]
    if any(load[k]!=v for k,v in {'source':0x0863673C,'stage':0x0201B800,'table':0x080327D0,'targets':0x080327FC,'index':16,'copy_source':0x0201B804,'copy_target':0x06013800,'bytes':1280}.items()):raise ValueError('native selector loader')
    if (p/'frequency_0001_decompressed.bin').read_bytes()!=payload:raise ValueError('native decompression')
    control=ROOT/'poc/runtime/calendar-frequency-upload-v3'
    verify_route(control,'903858514f23de53ce5ce5def2c07527ff3461d216e3fa6a06d47ef92eb6e883',set())
    if (control/'frequency_0001_decompressed.bin').read_bytes()!=lz77_decompress(source,BASE)[0]:raise ValueError('native original codec output')
    samples=[];sheet=Image.new('RGB',(240*5,160))
    for i,step in enumerate([6,7,9,11,13]):
        cp=f'step_{step:03}';v=(p/(cp+'_gbaVideoRam.bin')).read_bytes();o=(p/(cp+'_gbaSpriteRam.bin')).read_bytes();im=Image.open(p/(cp+'.png')).convert('RGB')
        if v[0x13800:0x13D00]!=payload[4:]:raise ValueError('all five resident tiles')
        a,b,c=struct.unpack_from('<HHH',o,16*8)
        if (a,b,c)!=(0x4043,0x8067,0x45C0+i*8):raise ValueError('native frequency selection/OAM')
        rows=decode(payload[4+i*256:4+(i+1)*256]);colors={}
        for role in (0,3,9):
            colors[role]={im.getpixel((103+x,67+y)) for y,row in enumerate(rows) for x,v in enumerate(row) if v==role}
            if len(colors[role])!=1:raise ValueError(f'visible frequency role mismatch {step}/{role}')
        if len({next(iter(v)) for v in colors.values()})!=3:raise ValueError('invisible glyph/shadow')
        samples.append({'step':step,'translation':WORDS[i],'oam':[a,b,c],'all_canvas_pixels_match_three_role_masks':True,'colors':{k:list(next(iter(v))) for k,v in colors.items()},'screenshot_sha256':sha((p/(cp+'.png')).read_bytes())});sheet.paste(im,(i*240,0))
    out=ROOT/'analysis/calendar_frequency_v1';out.mkdir(parents=True,exist_ok=True);sheet.save(out/'selector_contact_sheet.png')
    result={'passed':True,'policy':'development-draft; NON-DISTRIBUTION','release_eligible':False,'rom_sha256':m['output_sha256'],'translated_text_units':m['translated_units'],'added_graphic_labels':5,'byte_identical_rebuild':True,'only_frequency_slot_differs_from_calendar_date':True,'source_sha256':sha(source),'tool_sha256':sha(Path(__file__).read_bytes()),'prepared':prepared,'native_loader':load,'native_decompressed_output_exact':True,'source_decompressed_output_exact':True,'normal_route':route['steps_captured'],'samples':samples,'limits':['Five-choice selector only; four source references are shared, other loader/registration/query paths require distinct runtime verification.','Basic names/keyboard/user-string storage/save/reload remain native and unresolved.','Not full-game, hardware, audio, RTC or release verification.']}
    (out/'frequency_runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print('normal five frequency graphics QA: PASS');return result

if __name__=='__main__':main()
