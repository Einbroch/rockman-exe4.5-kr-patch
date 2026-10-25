"""Bounded actual secondary-root selections and full75 static/CPU coverage."""
import json
import struct
import inspect
from build_visibility_poc import ROOT,sha,require_hash
from report_chip_library_runtime import read,require,bdf_cells
from report_fixedcell_runtime import verify_route
from tpl_literals import resolve_units
from archive_scripts import verify_untouched_scripts
import report_chip_mono_cannon_runtime as previous
from capture_secondary_chip_descriptions import SCRIPTS

def secondary_sentence(*args,**kwargs):
    code=inspect.getsource(previous.mono_sentence)
    require(code.count("'76937C'")==1,'mono secondary report binding')
    ns=dict(previous.__dict__)
    code=code.replace("'76937C'","'76BC60'")
    old="colors=read(ROOT/'analysis/exe45_chip_description_mono_pixels_v1.json')['role_colors'];seen=set()"
    require(code.count(old)==1,'palette observation anchor')
    measured='''colors={};seen=set()
    for cell,glyph in enumerate(expected):
        row,col=divmod(cell,10)
        if col>=9:continue
        for yy,pixels in enumerate(unpack_pixels(glyph)):
            for xx,role in enumerate(pixels):
                rgb=shot.getpixel((10+col*8+xx,88+row*16+yy))
                word=struct.unpack_from('<H',palette,0x240+role*2)[0]
                if str(role) not in colors:colors[str(role)]={'palette_bgr555':word,'rgb':list(rgb)}
                require(colors[str(role)]=={'palette_bgr555':word,'rgb':list(rgb)},'secondary role scanout inconsistent across glyph masks')
    '''
    code=code.replace(old,measured)
    code=code.replace("'pixel_masks_match':True}","'pixel_masks_match':True,'observed_role_colors':colors,'palette_check':'per-page observed palette and consistent scanout role masks; not Cannon color assumption'}")
    exec(compile(code,previous.__file__+' [secondary archive/per-page native palette]','exec'),ns)
    return ns['mono_sentence'](*args,**kwargs)

def prepare():
    stem='exe45_ko_development_chip_secondary_desc_v1';rom_path=ROOT/f'poc/output/{stem}.gba'
    m=read(rom_path.with_suffix('.json'));build=m['output_sha256'];require(m['translated_units']==646,'646 selected units')
    for suffix in ('','_repro'):require_hash(ROOT/f'poc/output/{stem}{suffix}.gba',build)
    source=ROOT/read(ROOT/'project.json')['source_profile']['filename'];require_hash(source,m['source_sha256']);native=source.read_bytes();rom=rom_path.read_bytes()
    for a in m['translation_assets']:require_hash(ROOT/a['path'],a['sha256'])
    require(m['final_diff_audited'] and m['header_unchanged'],'final diff/header')
    a=read(ROOT/'translations/chip_secondary_descriptions_ko.json');u=resolve_units(a);texts={int(x['id'].split(':')[1]):x['translation'] for x in u};require(len(texts)==75,'secondary75')
    ar=next(x for x in m['archives'] if x['archive']=='76BC60');payload=rom[ar['rom_offset']:ar['rom_offset']+ar['compiled_bytes']]
    require(sha(native[0x76BC60:0x76BC60+3255])==a['source_archive_sha256'],'source pool')
    require(ar['protected_controls_unchanged'] and ar['native_roundtrip'] and ar['semantic_roundtrip'] and ar['binary_roundtrip'],'secondary round trips')
    require(len(verify_untouched_scripts(native[0x76BC60:0x76BC60+3255],payload,113,set(texts)))==38,'38 native nonliteral slots')
    for ptr in ar['pointers']:require(struct.unpack_from('<I',rom,ptr)[0]==0x08000000+ar['rom_offset'],'secondary relocation')
    p=ROOT/'poc/runtime/chip-secondary-desc-v1-native-samples-r3';seen=set();route=verify_route(p,build,seen);e=read(p/'secondary_environment.json')
    require(e['passed'] and e['covered_scripts']==SCRIPTS and route['normal_play_checkpoint_eligible'] is False,'secondary native selection coverage')
    require_hash(ROOT/'tools/capture_secondary_chip_descriptions_r3.py',e['tool_sha256'])
    table={int(k,16):v for line in (ROOT/'external/textpet-plugins/exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines() if '=' in line for k,v in [line.split('=',1)] if len(k)==2}
    offsets={struct.unpack_from('<H',payload,i*2)[0]:i for i in SCRIPTS};pixels={};covered=set()
    for step in route['capture_steps']:
        calls=[c for c in read(p/f'step_{step:03d}_fixedcells.json')['calls'] if c['font']==0x08619EF8];require(calls,'secondary glyph call')
        i=offsets[calls[-1]['stream']-0x08000000-ar['rom_offset']]
        pixels[str(step)]=secondary_sentence(p,step,m,native,table,texts[i],i,rom_path);covered.add(i)
    require(covered==set(SCRIPTS),'seven held screenshot coverage')
    normal=ROOT/'poc/runtime/chip-secondary-desc-v1-normal-scroll';nr=verify_route(normal,build,seen)
    require(read(normal/'folder_qa_environment.json')['passed'],'normal primary folder regression')
    primary={int(x['id'].split(':')[1]):x['translation'] for x in resolve_units(read(ROOT/'translations/chip_descriptions_batch09_ko.json'))}
    regression={str(step):previous.mono_sentence(normal,step,m,native,table,primary[i],i,rom_path) for step,i in ((9,1),(12,4),(15,15),(16,15))}
    cpu=read(ROOT/'analysis/exe45_secondary_description_cpu_v1.json');require(cpu['rom_sha256']==build and cpu['vectors']==150,'all75 CPU parser vectors')
    saves={}
    for directory in seen:
        env=read(directory/'probe_environment.json')
        for name,before in env['files_before'].items():
            if name not in (stem+'.sav',stem+'.rtc'):require(env['files_after'].get(name)==before,'foreign save changed')
        saves[str(directory.relative_to(ROOT))]={'own_save':env['files_after'].get(stem+'.sav'),'own_rtc':env['files_after'].get(stem+'.rtc'),'other_saves_preserved':True}
    return {'rom_sha256':build,'policy':'development-draft; NON-DISTRIBUTION','status':'PASS bounded secondary description development build',
            'translated_units':646,'new_secondary_description_units':75,'secondary_scripts_with_screenshot_pixels':sorted(covered),'secondary_pixels':pixels,'normal_primary_description_regression':regression,'cpu_vectors':150,'reproducible':True,'saves':saves,
            'limits':['secondary source IDs selected by diagnostic descriptor aliases, not acquisition normal play','seven screenshot samples, not all75 runtime coverage','secondary98 names not integrated and remain Japanese on these screens','four pointer roots statically relocated; unobserved shared consumers still pending','all wording/presentation needs human review; full game/audio/hardware/release unverified']}

if __name__=='__main__':print(json.dumps(prepare(),ensure_ascii=False,indent=2))
