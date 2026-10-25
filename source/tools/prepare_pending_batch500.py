"""Read-only, source-bound 500-unit insertion preflight. No prose or ROM edits."""
import argparse,json,re,struct
from build_visibility_poc import ROOT,sha,require_hash,run_textpet,bdf_glyphs
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of
from tpl_literals import literals,replace_literals,skeleton
from textpet_korean import prepare_plugins,command
from archive_scripts import verify_untouched_scripts
from korean_codec import encode_character

BASE='poc/output/exe45_ko_development_mission_mail_header_v1.gba'
BASE_SHA='21565ad0db0cbdd25be1326cbed047febf25eb50a1873535833928d34326f389'
PLAN=[
 ('translations/batch500_045_navi_mail_npcs_6DD718_draft_ko.json',None,16),
 ('translations/batch500_045_navi_mail_npcs_6DD798_draft_ko.json',None,10),
 ('translations/batch500_045_navi_mail_npcs_6DD804_draft_ko.json',None,10),
 ('translations/batch500_045_navi_mail_npcs_6DD91C_draft_ko.json',None,32),
 ('translations/protoman_missions_draft_ko.json',None,253),
 ('translations/batch500_016_military_6DF988_draft_ko.json',None,153),
 ('translations/batch500_016_destruction_6E01AC_draft_ko.json',[38,39,40],26),
]

ARROW_LAYOUT='translations/pending_insertion_500_arrow_layout.json'
ARROW_IDS={'6DE3E0:61:1','6DE3E0:63:1','6DF988:34:2','6DF988:35:1','6DF988:37:1','6DF988:38:6','6DF988:42:5','6DF988:51:4'}

def arrow_layouts():
    d=json.loads((ROOT/ARROW_LAYOUT).read_text(encoding='utf8'))
    if d['release_eligible'] is not False or set(d['layouts'])!=ARROW_IDS:raise ValueError('individual arrow layout population')
    return d['layouts']

def same_layout_words(key,value,prior):
    if key=='6DE3E0:61:1':return re.sub(r'\s','',value)==re.sub(r'\s','',prior) and value.count('\n')==prior.count('\n')
    return value.replace('\n',' ')==prior.replace('\n',' ') and value.count('\n')==prior.count('\n')

def prepare(out):
    if out.exists():raise ValueError('preserve prior batch artifacts')
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'))
    source_path=ROOT/cfg['source_profile']['filename'];require_hash(source_path,cfg['source_profile']['sha256'])
    source=source_path.read_bytes();require_hash(ROOT/BASE,BASE_SHA)
    baseline=json.loads((ROOT/BASE).with_suffix('.json').read_text(encoding='utf8'))
    applied={r['archive'] for r in baseline['archives']}
    require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    rows=parse_tpi(ROOT/cfg['text_catalog']['path']);entries=[];ids=set();wanted=set()
    layout_path=ROOT/'translations/pending_insertion_500_001_layout.json'
    layout_spec=json.loads(layout_path.read_text(encoding='utf8'))
    if layout_spec['release_eligible'] is not False or set(layout_spec['layouts'])!={'6DF988:42:4'}:raise ValueError('individual batch layout population')
    combined_layout=dict(layout_spec['layouts'],**arrow_layouts())
    for path,scripts,count in PLAN:
        d=json.loads((ROOT/path).read_text(encoding='utf8'));a=d['archive']
        if a in applied or d['source_sha256']!=sha(source) or d['review']['release_eligible'] is not False:raise ValueError('batch applied/source/policy')
        require_hash(ROOT/d['source_tpl']['path'],d['source_tpl']['sha256'])
        tpl=(ROOT/d['source_tpl']['path']).read_text(encoding='utf-8-sig')
        u=[dict(x) for x in d['units'] if scripts is None or int(x['id'].split(':')[1]) in scripts]
        for x in u:
            if x['id'] in combined_layout:
                value=combined_layout[x['id']]
                if not same_layout_words(x['id'],value,x['translation']):raise ValueError('layout changes wording/topology')
                x['translation']=value
        originals={x.key:x.text for x in literals(tpl)}
        if len(u)!=count or any(x['id'] in ids or originals.get(x['id'])!=x['source'] or x['state']!='needs_review' for x in u):raise ValueError('batch IDs/protected source/state')
        scripts=sorted({int(x['id'].split(':')[1]) for x in u})
        # Every selected script's Japanese literal population is complete.
        expected={x.key for x in literals(tpl) if int(x.key.split(':')[1]) in scripts and re.search(r'[\u3040-\u30ff\u3400-\u9fff]',x.text)}
        if expected!={x['id'] for x in u}:raise ValueError('batch cuts a source Japanese script')
        row=next(r for r in rows if r['offset']==int(a,16));native=payload_of(source,row)
        if sha(native)!=d['source_archive_sha256']:raise ValueError('native source archive differs')
        for x in u:
            if re.findall(r'\d+',x['source'])!=re.findall(r'\d+',x['translation']):raise ValueError('numeric literal changed '+x['id'])
            ids.add(x['id']);wanted.update(ch for ch in x['translation'] if '\uac00'<=ch<='\ud7a3')
        language='mmbn45s' if a.startswith('6DD') else 'mmbn45'
        translated=replace_literals(tpl,u,language=language)
        entries.append((path,d,u,row,native,tpl,translated,scripts,language))
    if len(ids)!=500:raise ValueError('500-unit batch denominator')
    out.mkdir(parents=True)
    plugins=out/'plugins';plugin=prepare_plugins(plugins,{','})
    codes={}
    for line in (plugins/'exe45-utf8.tbl').read_text(encoding='utf-8-sig').splitlines():
        if '=' in line:
            k,v=line.split('=',1)
            if len(v)==1:codes[v]=bytes.fromhex(k)
    font=cfg['development_dependencies']['font'];require_hash(ROOT/font['path'],font['sha256'])
    glyphs=bdf_glyphs(ROOT/font['path'],wanted)
    records=[];layout_candidates=[];common=command(plugins)
    for path,d,u,row,native,tpl,translated,scripts,language in entries:
        a=d['archive'];work=out/a;work.mkdir()
        original=work/'source.tpl';original.write_text(tpl,encoding='utf8')
        target=work/'translated.tpl';target.write_text(translated,encoding='utf8')
        (work/'compiled').mkdir()
        source_bin=work/'source.msg';compiled=work/'compiled'/f'{a}.msg';reverse=work/'reverse.tpl';rebuilt=work/'rebuilt.msg'
        run_textpet(common+['Read-Text-Archives',str(original),'--format','tpl','Write-Text-Archives',str(source_bin),'--format','bin'],work/'source_compile.log')
        if source_bin.read_bytes()!=native:raise ValueError('source native roundtrip '+a)
        layout=[]
        for x in u:
            widths=[]
            for line in x['translation'].split('\n'):
                width=0
                for ch in line:
                    if ch not in codes:raise ValueError('unmapped character '+x['id']+repr(ch))
                    if '\uac00'<=ch<='\ud7a3' and codes[ch]!=encode_character(ch):raise ValueError('Hangul mapping mismatch')
                    width+=8 if language=='mmbn45s' else 12 if '\uac00'<=ch<='\ud7a3' or ch==',' else 8 if ch==' ' else 11
                widths.append(width)
            layout.append(dict(id=x['id'],line_advance_pixels=widths))
            limit=88 if language=='mmbn45s' else 152
            if len(widths)>(1 if language=='mmbn45s' else 3) or max(widths)>limit or language=='mmbn45' and len(widths)==3 and widths[2]>132:
                layout_candidates.append(dict(id=x['id'],widths=widths,comparison_pixels=limit,classification='insertion-layout candidate; no prose edit or runtime capacity claim'))
        run_textpet(common+['Read-Text-Archives',str(target),'--format','tpl','Write-Text-Archives',str(compiled),'--format','bin'],work/'compile.log')
        raw=compiled.read_bytes();run_textpet(common+['Read-Text-Archives',str(compiled),'--format','bin','Write-Text-Archives',str(reverse),'--format','tpl'],work/'reverse.log')
        back=reverse.read_text(encoding='utf-8-sig')
        if skeleton(tpl)!=skeleton(translated) or skeleton(back)!=skeleton(translated) or [(x.key,x.text) for x in literals(back)]!=[(x.key,x.text) for x in literals(translated)]:raise ValueError('semantic/protected command roundtrip '+a)
        run_textpet(common+['Read-Text-Archives',str(reverse),'--format','tpl','Write-Text-Archives',str(rebuilt),'--format','bin'],work/'rebuild.log')
        if rebuilt.read_bytes()!=raw:raise ValueError('binary roundtrip '+a)
        count=int(re.search(r'^@size\s+(\d+)',tpl,re.M).group(1))
        verify_untouched_scripts(native,raw,count,set(scripts))
        if len(raw)>0xffff:raise ValueError('16-bit archive extent')
        records.append(dict(archive=a,draft_path=path,draft_sha256=sha((ROOT/path).read_bytes()),source_tpl=d['source_tpl'],selected_ids=[x['id'] for x in u],selected_units=len(u),scripts=scripts,source_payload_sha256=sha(native),source_bytes=len(native),compiled_bytes=len(raw),compiled_sha256=sha(raw),source_pointers=row['pointers'],script_count=count,source_native_roundtrip=True,protected_controls_unchanged=True,semantic_roundtrip=True,binary_roundtrip=True,unselected_scripts_unchanged=True,layout=layout,ram_payload_exceeds_common_mail_8192_comparison=len(raw)>8192 if language=='mmbn45' else False,variable_widths_verified=False))
        print('Preflight',a,len(u),'native',len(native),'compiled',len(raw),flush=True)
    require_hash(ROOT/BASE,BASE_SHA);require_hash(source_path,cfg['source_profile']['sha256'])
    report=dict(schema=1,batch_id='pending-insertion-500-001',policy='development-draft; NON-DISTRIBUTION',source_sha256=sha(source),baseline_rom=BASE,baseline_sha256=BASE_SHA,total_units=500,unique_ids=500,archives=records,existing_drafts_reused_without_wording_changes=True,newly_translated_units=0,individual_layout=dict(path=str(layout_path.relative_to(ROOT)),sha256=sha(layout_path.read_bytes()),affected_ids=list(layout_spec['layouts'])),protected_information_passed=True,font_glyphs=len(glyphs),font_source=font,hangul_mapping_complete=True,plugin=plugin,layout_candidates=layout_candidates,rom_written=False,runtime_tested=False,release_eligible=False,stage='source/encoding/compile preflight complete; geometry, variables, loader capacities and integration pending')
    report['artifacts']={str(p.relative_to(out)):sha(p.read_bytes()) for p in sorted(out.rglob('*')) if p.is_file()}
    report['arrow_layout']=dict(path=ARROW_LAYOUT,sha256=sha((ROOT/ARROW_LAYOUT).read_bytes()),affected_ids=sorted(ARROW_IDS),row3_limit_pixels=132)
    (out/'preflight.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('500 preflight complete; layout candidates',len(layout_candidates),'ROM unchanged')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',default='analysis/pending_insertion_500_001');a=p.parse_args();prepare(ROOT/a.out)
