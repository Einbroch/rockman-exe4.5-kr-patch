"""Compile old and merged source-based assets; prove carry script identity."""
import json
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import derive,prepare,read,frozen_write,PROFILE007
from build_development_patch import compile_archive,selected_scope
from textpet_korean import prepare_plugins,command
from korean_codec import EXTRA_CHARACTER_INDICES
from archive_scripts import verify_untouched_scripts
from verify_pending500_002_rom import read_payload
from tpl_literals import resolve_units

def main(profile=PROFILE007):
    BASE,BASE_SHA,OUT,BATCH_ID,SOURCE_PREFLIGHT=(profile[k] for k in ('base','base_sha','out','batch_id','source_preflight'))
    PREFLIGHT=OUT+'/preflight.json'
    out=ROOT/OUT
    if (ROOT/PREFLIGHT).exists():raise ValueError('Preserve cumulative preflight')
    cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,cfg['source_profile']['sha256']);source=sp.read_bytes()
    prepare(profile);derived=derive(source,profile)
    extra={ch for _,_,a,_,_,_,_,_ in derived for u in resolve_units(a) for ch in u['translation'] if ch in EXTRA_CHARACTER_INDICES}
    plugins=out/'plugins';prepare_plugins(plugins,extra);common=command(plugins)
    base=(ROOT/BASE).read_bytes();results=[]
    for path,row,asset,scope,r,native,parent,old_record in derived:
        a=asset['archive']
        # Recompile exact parent under its existing scope before admitting carry.
        if parent is None:old_raw=native
        else:
            carry=read(parent['path']);old_scope=dict(scope,literal_scripts=[s for s in scope['literal_scripts'] if s not in r['scripts']],literal_ids=[u['id'] for u in carry['units']],literal_profiles=scope['literal_profiles'][:-1],protected_numeral_ids=[k for k in scope['protected_numeral_ids'] if k not in r['selected_ids']])
            if scope.get('nickname_capacity_profiles'):
                old_scope['nickname_capacity_profiles']=[p for p in scope['nickname_capacity_profiles'] if p['script'] in old_scope['literal_scripts']]
            if scope.get('fullbox_capacity_profiles'):
                old_scope['fullbox_capacity_profiles']=[p for p in scope['fullbox_capacity_profiles'] if p['script'] in old_scope['literal_scripts']]
            old_raw,old_proof=compile_archive(source,row,carry,old_scope,common,plugins,out/(a+'_carry'))
            if old_raw!=read_payload(base,old_record):raise ValueError('Parent does not reproduce actual baseline '+a)
        raw,proof=compile_archive(source,row,asset,scope,common,plugins,out/(a+'_merged'))
        preserved=verify_untouched_scripts(old_raw,raw,scope['script_count'],set(r['scripts']))
        result=dict(archive=a,asset_path=path,asset_sha256=sha((ROOT/path).read_bytes()),parent=parent,scope=scope,new_ids=r['selected_ids'],selected_ids=[u['id'] for u in asset['units']],translated_units=len(asset['units']),new_units=len(r['selected_ids']),compiled_sha256=sha(raw),compiled_bytes=len(raw),parent_compiled_sha256=sha(old_raw),carry_scripts_byte_identical=preserved,proof=proof)
        results.append(result);print('Merged',a,result['translated_units'],'new',result['new_units'],'carry scripts PASS',flush=True)
    report=dict(schema=1,batch_id=BATCH_ID,policy='development-draft; NON-DISTRIBUTION',source_sha256=sha(source),baseline_rom=BASE,baseline_sha256=BASE_SHA,source_preflight_sha256=sha((ROOT/SOURCE_PREFLIGHT).read_bytes()),new_units=sum(r['new_units'] for r in results),archives=results,rom_written=False,runtime_tested=False,release_eligible=False)
    frozen_write(ROOT/PREFLIGHT,report)
    print('PASS cumulative500 preflight; old scripts and consumer profiles retained')
if __name__=='__main__':main()
