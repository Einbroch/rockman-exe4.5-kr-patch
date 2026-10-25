"""Exact authored old-consumer reconstruction + new500 carry diagnostics, no ROM."""
from copy import deepcopy
from collections import defaultdict
from build_visibility_poc import ROOT,sha,require_hash,run_textpet
from cumulative_batch500 import read,frozen_write
from tpl_literals import resolve_units,literals,skeleton
from survey_aggregate_pet_033 import replace_exact
from canonical_literals_031 import canonical_literals
from verify_tpi_index import lz77_decompress
from compare_archive_payloads import payload_of
from archive_scripts import verify_untouched_scripts
from textpet_korean import command
from prepare_repartition500 import layout_records

SOURCE='analysis/pending_insertion_500_041_source_v7'


def ref(p):return dict(path=str(p.relative_to(ROOT)),sha256=sha(p.read_bytes()))


def main():
    s=read(SOURCE+'/selection.json');v=read(SOURCE+'/verification_v2.json');require_hash(ROOT/s['baseline_rom'],s['baseline_sha256']);rom=(ROOT/s['baseline_rom']).read_bytes();m=read(s['baseline_rom'].replace('.gba','.json'));cfg=read('project.json');require_hash(ROOT/cfg['source_profile']['filename'],s['source_sha256']);source=(ROOT/cfg['source_profile']['filename']).read_bytes()
    if not v['passed'] or v['units']!=500 or v['rom_written'] or v['existing_Korean_carry_merged']:raise ValueError('041 source-only500 prerequisite')
    for path,h in v['dependencies'].items():require_hash(ROOT/path,h)
    gs=defaultdict(list)
    for g in s['groups']:gs[g['archive']].append(g)
    out=ROOT/SOURCE/'carry_v1';out.mkdir(parents=True,exist_ok=False);common=command(ROOT/SOURCE/'compile_v2/plugins');records=[];carry=set();new=set()
    for r in v['archives']:
        arc=r['archive'];new.update(r['new_ids']);parents=r['current_consumer_carry_requirements'];native=payload_of(source,r['source_row']);require_hash(ROOT/r['source_tpl']['path'],r['source_tpl']['sha256']);original=(ROOT/r['source_tpl']['path']).read_text(encoding='utf-8-sig');raw={u.key:u.text for u in literals(original)};old=[];refs=[]
        if len(parents)>1:raise ValueError('041 multiple current consumer variants require explicit separate handling')
        if parents:
            parent=parents[0];required=set(parent['ids']);options=parent['authored_set_matches']
            if options:refs=[options[0]]
            else:refs=[dict(path=e['path'],sha256=e['sha256']) for e in m['translation_assets'] if e.get('archive')==arc]
            byid={}
            for link in refs:
                require_hash(ROOT/link['path'],link['sha256']);a=read(link['path'])
                if a.get('schema') not in (1,2) or a.get('source_sha256')!=sha(source):raise ValueError('041 authored carry source/policy')
                for u in resolve_units(a):
                    if u['id'] not in required or u['source']!=raw[u['id']]:raise ValueError('041 authored carry protected scope')
                    if u['id'] in byid and any(byid[u['id']][k]!=u[k] for k in ('source','translation','state')):raise ValueError('041 conflicting authored carry')
                    byid[u['id']]=deepcopy(u)
            if set(byid)!=required:raise ValueError('041 complete authored carry population')
            old=[byid[u.key] for u in literals(original) if u.key in byid];carry.update(required)
        units=old+deepcopy(r['units']);ids={u['id'] for u in units}
        if len(ids)!=len(units):raise ValueError('041 carry/new duplicate')
        f=out/arc;f.mkdir();target=replace_exact(original,{u['id']:u['translation'] for u in units});prior=replace_exact(original,{u['id']:u['translation'] for u in old})
        if skeleton(target)!=skeleton(original):raise ValueError('041 carry target protected controls')
        tp=f/'target.tpl';pp=f/'prior.tpl';bp=f/(arc+'.msg');np=f/(arc+'_prior.msg')
        for path,text in [(tp,target),(pp,prior)]:path.write_text(canonical_literals(text),encoding='utf8',newline='\n')
        def compile(x,y,log):run_textpet(common+['Read-Text-Archives',str(x),'--format','tpl','Write-Text-Archives',str(y),'--format','bin'],f/log)
        compile(pp,np,'prior.log');before=np.read_bytes()
        if parents:
            p=parents[0];physical=next(x for x in layout_records(m) if x.get('rom_offset')==p['rom_offset'] and x['archive']==arc);actual=lz77_decompress(rom,p['rom_offset'])[0] if physical.get('compression') else rom[p['rom_offset']:p['rom_offset']+p['compiled_bytes']]
            if before!=actual or sha(before)!=p['compiled_sha256']:raise ValueError('041 independently authored current carry bytes '+arc)
        elif before!=native:raise ValueError('041 unowned original')
        if not parents:
            require_hash(ROOT/r['new_only_compiled']['path'],r['new_only_compiled']['sha256']);payload=(ROOT/r['new_only_compiled']['path']).read_bytes();compiled=r['new_only_compiled']
        else:
            compile(tp,bp,'target.log');payload=bp.read_bytes();compiled=ref(bp)
        kept=verify_untouched_scripts(before,payload,r['script_count'],{g['script'] for g in gs[arc]})
        if len(payload)>65535:raise ValueError('041 cumulative u16 capacity')
        ap=f/'authored_combined_asset.json';asset=dict(schema=1,archive=arc,policy='development-draft; NON-DISTRIBUTION',source_sha256=sha(source),source_tpl=r['source_tpl'],source_archive_sha256=sha(native),units=units,new_ids=r['new_ids'],inherited_ids=[u['id'] for u in old],parent_authored_assets=refs,insertion_ready=False,review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False))
        frozen_write(ap,asset);records.append(dict(archive=arc,asset=ref(ap),target_tpl=ref(tp),compiled=compiled,new_ids=r['new_ids'],inherited_ids=[u['id'] for u in old],prior_authored_byte_reproduction_verified=True,current_unselected_scripts=kept,consumer_binding_admitted=False));print('PASS041 authored carry',arc,'new',len(r['new_ids']),'old',len(old),flush=True)
    if new!=set(s['selected_ids']) or len(new)!=500:raise ValueError('041 exact cumulative500 population')
    deps=[SOURCE+'/selection.json',SOURCE+'/verification_v2.json','tools/compile_carry500_041_v1.py']
    frozen_write(ROOT/SOURCE/'carry_verification_v1.json',dict(passed=True,status='041_SOURCE500_AND_AUTHORED_CARRY_REPRODUCED_NOT_ROM_OR_CONSUMER_ADMISSION',baseline_sha256=s['baseline_sha256'],source_sha256=sha(source),new_units=500,inherited_units=len(carry),archives=records,rom_written=False,product_admitted=False,runtime_tested=False,release_eligible=False,dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},limits=['No041 primary/repro ROM. Regenerated old consumer bytes and preserved current unselected scripts only.','Real loader/caller/default origin/selector native prefixes and positioned clearing remain unadmitted.','Combined target roundtrip/font/layout must enter the eventual primary gates; this does not replace those gates.']))
    print('PASS041 source500 + authored carry',len(carry),'NOT ROM/consumer admission')


if __name__=='__main__':main()
