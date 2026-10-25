"""037 strict source/target archive identity compiler; no product writer."""
from prepare_source500_037_v2 import *


def main():
    cfg,source,rom,m=baseline();s=read(OUT+'/selection.json')
    for p,h in s['dependencies'].items():require_hash(ROOT/p,h)
    out=ROOT/OUT/'compile_v1';out.mkdir(parents=True,exist_ok=False)
    plugin=prepare_plugins(out/'plugins',set(EXTRA_CHARACTER_INDICES));common=command(out/'plugins')
    grouped=defaultdict(list)
    for g in s['groups']:grouped[g['archive']].append(g)
    records=[];seen=set();chars=set();validators=dict(VALIDATORS)
    for arc,groups in sorted(grouped.items()):
        sr=groups[0]['source_tpl'];require_hash(ROOT/sr['path'],sr['sha256']);original=(ROOT/sr['path']).read_text(encoding='utf-8-sig');row=groups[0]['source_row']
        native=payload_of(source,row);need(payload_of(rom,row)==native,'Current native source retained')
        need(all(rom[p:p+4]==source[p:p+4] for p in row['pointers'] if p),'Current source pointers retained')
        units=[];values={};source_lits={u.key:u.text for u in literals(original)}
        for g in groups:
            subset={}
            for d in g['drafts']:
                require_hash(ROOT/d['path'],d['sha256']);a=read(d['path']);u=deepcopy(next(u for u in a['units'] if u['id']==d['id']))
                v=g['explicit_layouts'].get(u['id'],u['translation'])
                need(u['id'] not in seen and u['source']==source_lits[u['id']] and u['state']=='needs_review' and v.replace('\n',' ')==u['translation'].replace('\n',' ') and protected_edges(u['source'],v),'Compile source/wording ownership')
                u['translation']=v;units.append(u);values[u['id']]=v;subset[u['id']]=v;seen.add(u['id']);chars.update(v)
            need(validators[g['profile']](original,replace_exact(original,subset),[g['script']],set(g['geometry_ids']),99)==g['geometry'],'Compile geometry replay')
        validate_literal_numerals(units,dict(preserve_literal_numerals=True))
        target=replace_exact(original,values);need(skeleton(original)==skeleton(target),'Protected original topology')
        f=out/arc;f.mkdir();a=f/'source.tpl';b=f/'target.tpl'
        a.write_text(canonical_literals(original),encoding='utf8',newline='\n');b.write_text(canonical_literals(target),encoding='utf8',newline='\n')
        def convert(x,xf,y,yf,log):run_textpet(common+['Read-Text-Archives',str(x),'--format',xf,'Write-Text-Archives',str(y),'--format',yf],f/log)
        n=f/(arc+'_native.msg');p=f/(arc+'.msg');r=f/'reverse.tpl';again=f/(arc+'_rebuilt.msg')
        convert(a,'tpl',n,'bin','native.log');need(n.read_bytes()==native,'Complete source byte roundtrip')
        convert(b,'tpl',p,'bin','compile.log');payload=p.read_bytes();need(len(payload)<=65535,'16-bit script offset capacity')
        convert(p,'bin',r,'tpl','reverse.log');convert(r,'tpl',again,'bin','rebuild.log')
        exported=r.read_text(encoding='utf-8-sig')
        need(skeleton(original)==skeleton(exported) and [(u.key,u.language,u.text) for u in literals(target)]==[(u.key,u.language,u.text) for u in literals(exported)] and again.read_bytes()==payload,'Target semantic/control/binary roundtrip')
        count=int(re.search(r'^@size (\d+)$',original,re.M)[1]);kept=verify_untouched_scripts(native,payload,count,{g['script'] for g in groups})
        records.append(dict(archive=arc,source_tpl=sr,source_payload_sha256=sha(native),native_bytes=len(native),compiled_bytes=len(payload),script_count=count,target_tpl=ref(b),compiled=ref(p),units=units,unselected_scripts=kept,controls_unchanged=True,roundtrip=True,product_admitted=False))
        print('PASS source037',arc,len(units),'units',flush=True)
    need(seen==set(s['selected_ids']) and len(seen)==500,'Exact500 compile population')
    wanted={c for c in chars if '\uac00'<=c<='\ud7a3'};extra=chars&EXTRA_CHARACTER_INDICES.keys();fp=ROOT/cfg['development_dependencies']['font']['path'];require_hash(fp,cfg['development_dependencies']['font']['sha256'])
    glyphs=bdf_glyphs(fp,wanted);glyphs.update(bdf_glyphs(fp,extra,{c:EXTRA_CHARACTER_METRICS[c]['vertical_shift'] for c in extra}))
    for c,glyph in glyphs.items():
        i=m['extension']['legacy_index_view']+(ord(c)-0xAC00 if c in wanted else EXTRA_CHARACTER_INDICES[c]);at=m['extension']['normal_font_offset']+i*96
        need(rom[at:at+96]==glyph,'Actual036 glyph supply '+c)
    require_hash(ROOT/BASE,BASE_SHA)
    frozen_write(ROOT/OUT/'verification_v1.json',dict(schema=1,status='EXACT500_SOURCE_COMPILE_FONT_GEOMETRY_PASS_NOT_ROM_ADMISSION',passed=True,baseline_rom=BASE,baseline_sha256=BASE_SHA,source_sha256=sha(source),selection=ref(ROOT/OUT/'selection.json'),units=500,archive_count=len(records),extended_glyphs_checked=len(glyphs),archives=records,plugin=plugin,tools=[ref(ROOT/'tools/compile_source500_037_v2.py'),ref(ROOT/'tools/prepare_source500_037_v2.py')],wording_changed=False,rom_written=False,new_units_applied=0,insertion_ready=False,product_integrated=False,runtime_tested=False,release_eligible=False,limits=s['limits']+['Native loader/root lifetime for additional storage classes, cumulative writer/ownership/independent product build and runtime verification still required.'],preparation_scope='Independent037 source-only compile; prior036 filename failure is not a037 attempt'))
    print('PASS source037 exact500,',len(records),'archives,',len(glyphs),'current-ROM glyphs; NO ROM')


if __name__=='__main__':main()
