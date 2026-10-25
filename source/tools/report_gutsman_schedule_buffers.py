"""Fixed meal-ROM normal commit/query evidence; not an alarm-cause closure."""
import json,struct
from PIL import Image
from report_roll_pet import ROOT,read,sha,pixels,verify_route
from build_visibility_poc import require_hash,bdf_glyphs
from korean_codec import encode_hangul
STEM='exe45_ko_development_gutsman_alarm_meal_v1'
PREFIX='gutsman-event-buffer-native-v1-'
def main():
    rp=ROOT/f'poc/output/{STEM}.gba';m=read(rp.with_suffix('.json'));require_hash(rp,m['output_sha256']);rom=rp.read_bytes();rt=ROOT/'poc/runtime';cfg=read(ROOT/'project.json');require_hash(ROOT/cfg['source_profile']['filename'],m['source_sha256']);routes={}
    for route,parent in [('today','gutsman-alarm-meal-v1-select-gutsman'),('calendar','gutsman-alarm-meal-v1-select-gutsman'),('time',PREFIX+'calendar'),('meal-register',PREFIX+'time'),('meal-query',PREFIX+'meal-register')]:
        p=rt/(PREFIX+route);r=verify_route(p,m['output_sha256'],set());routes[route]=r
        if r['state_origin']!=str(rt/parent/'result.json') or r.get('normal_play_checkpoint_eligible') is False:raise ValueError('native ancestry')
        if any(x in (p/'segment.lua').read_text(encoding='utf8') for x in ['emu.write','setState','AliasReads']):raise ValueError('native intervention')
        if route in ['today','meal-query']:
            env=read(p/'schedule_buffers_environment.json')
            if not env['observer_only'] or not env['no_aliases'] or env['rom_sha256']!=m['output_sha256'] or env['self_sha256']!=sha((ROOT/'tools/capture_gutsman_schedule_buffers.py').read_bytes()) or env['pet_probe_sha256']!=sha((ROOT/'tools/capture_roll_pet.py').read_bytes()):raise ValueError('buffer observer identity')
    word='식사';body=encode_hangul(word)+b'\xe5';ar=next(a for a in m['archives'] if a['archive']=='6368E8');payload=rom[ar['rom_offset']:ar['rom_offset']+ar['compiled_bytes']];address=0x08000000+ar['rom_offset']+struct.unpack_from('<H',payload,62*2)[0]
    if rom[address-0x08000000:address-0x08000000+len(body)]!=body:raise ValueError('preset ROM body')
    reg=rt/(PREFIX+'meal-register');calls=read(reg/'step_007_preset_path.json')['calls'];copy=[c for c in calls if c['pc']==0x08032AC6 and c['registers'][:2]==[address,0x02026080]];commit=[c for c in calls if c['pc']==0x08032AC6 and c['registers'][:2]==[0x02026080,0x0200131A]]
    if len(copy)!=1 or len(commit)!=1:raise ValueError('preset lookup/native copy/record')
    ram=(reg/'step_007_gbaExtWorkRam.bin').read_bytes();record=ram[0x1310:0x1330]
    if record!=bytes.fromhex('03000001010602000002')+body+bytes(13):raise ValueError('meal committed record')
    q=rt/(PREFIX+'meal-query');ram=(q/'step_005_gbaExtWorkRam.bin').read_bytes();trace=read(q/'step_005_schedule_buffers.json');addresses=[0x02010C40,0x02010C44];draws=[d for d in trace['draws'] if d['stream'] in addresses]
    if ram[0x1310:0x1330]!=record or ram[0x10C40:0x10C49]!=body or [d['stream'] for d in draws]!=addresses or [d['offset'] for d in draws]!=[10796,10844]:raise ValueError('committed record/query name stream')
    actualreads=[r for r in trace['reads'] if 0x02010C40<=r['stream']<=0x02010C48]
    if not actualreads or {r['stream'] for r in actualreads}!={*addresses,0x02010C48} or actualreads[-1]['byte']!=0xE5 or any(r['byte']!=ram[r['stream']-0x02000000] for r in actualreads):raise ValueError('name native parser boundary')
    glyphs=bdf_glyphs(ROOT/cfg['development_dependencies']['font']['path'],set(word));font=m['extension'];expected={}
    for ch,d in zip(word,draws):
        index=font['legacy_index_view']+ord(ch)-0xAC00;g=rom[font['normal_font_offset']+index*96:font['normal_font_offset']+(index+1)*96]
        if d['glyph_index']!=index or g!=glyphs[ch]:raise ValueError('query Hangul glyph provider')
        expected[d['stream']]=dict(ch=ch,index=index,record=g,id='native-meal-query')
    # This observer did not log per-glyph color. Bind the pixel proof to the
    # captured active context color; do not invent a per-glyph trace value.
    colored=[dict(d,color=ram[0xFABC]) for d in draws]
    proof=pixels(q,5,colored,expected,rom,m,cursor_indices=())
    # The write watch covers AC0..AE0 (hour buffer) only; do not mislabel it
    # as event-name C40 producer tracing or proof of the invalid alarm cause.
    result=dict(passed=True,policy='fixed-baseline native observation; NON-DISTRIBUTION',release_eligible=False,rom_sha256=m['output_sha256'],new_translations=0,routes=list(routes),committed_record=record.hex(),native_copy_frame=copy[0]['frame'],commit_frame=commit[0]['frame'],name_buffer='02010C40',name_bytes=body.hex(),name_parser_reads=len(actualreads),color_evidence='active context snapshot 0200FABC; not per-glyph color trace',normal_name_pixels=proof,buffer_draw_addresses=[hex(d['stream']) for d in trace['draws']],screenshot_sha256=sha((q/'step_005.png').read_bytes()),limits=['Same-session preset meal registration/query; not alarm timing or TV/promise event selection.','Write observer AC0..AE0 covers hour only; C40 producer/selected-record read still needs direct tracing.','Earlier invalid alarm alias initialization cause unresolved; no fix/normal-game bug conclusion.','No arbitrary name editing, permanent reload or old-save compatibility proof.'])
    out=ROOT/'analysis/gutsman_event_buffer_native_v1';out.mkdir(parents=True,exist_ok=True);(out/'runtime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps({k:v for k,v in result.items() if k not in ['normal_name_pixels','limits']},ensure_ascii=False));return result
if __name__=='__main__':main()
