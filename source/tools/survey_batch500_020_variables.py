"""Current019 variable census with explicit native-provider applicability checks."""
import re,struct
from collections import defaultdict,Counter
from dataclasses import replace
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from nickname_capacity import native_bound,CPU
from survey_batch500_019_variables import inspect_template
from tpl_literals import literals

SURVEY='analysis/pending_insertion_500_020_survey_v1/survey.json'
OUT='analysis/pending_insertion_500_020_variable_survey_v1/survey.json'

def applicability(source,rom,cpu):
    for r in cpu['native_code']:
        a=r['offset'];b=a+r['bytes']
        if sha(source[a:b])!=r['sha256'] or rom[a:b]!=source[a:b]:raise ValueError('019 native provider code changed')
    for address,value in cpu['literals'].items():
        a=int(address,16)
        if struct.unpack_from('<I',source,a)[0]!=int(value,16) or rom[a:a+4]!=source[a:a+4]:raise ValueError('019 native provider literal changed')
    for a,b in ((0x526D8,0x526E0),(0x5290C,0x5290C+441*4)):
        if rom[a:b]!=source[a:b]:raise ValueError('019 descriptor/metric path changed')
    for index,expected in enumerate(cpu['suffix_hex']):
        a=0x63720C+index*2
        if rom[a:a+2]!=source[a:a+2]:raise ValueError('019 suffix lookup changed')
        at=0x63720C+struct.unpack_from('<H',source,a)[0];raw=bytes.fromhex(expected)
        if source[at:at+len(raw)]!=raw or rom[at:at+len(raw)]!=raw:raise ValueError('019 suffix record changed')
    return native_bound(source)

def main():
    s=read(SURVEY);rp=ROOT/s['baseline_rom'];require_hash(rp,s['baseline_sha256']);rom=rp.read_bytes();cfg=read('project.json');sp=ROOT/cfg['source_profile']['filename'];require_hash(sp,s['source_sha256']);source=sp.read_bytes()
    proof=read('analysis/pending500_019_v1/integration.json');runtime=read('analysis/pending500_019_v1/name_display_runtime.json')
    if not proof['passed'] or not runtime['passed'] or any(x['rom_sha256']!=s['baseline_sha256'] for x in (proof,runtime)) or s['pinned_changed_inputs']:raise ValueError('019 baseline evidence')
    bound=applicability(source,rom,read(CPU))
    if bound!=99 or any(p['nickname_advance']!=bound for p in runtime['pages']):raise ValueError('019 native observed aggregate')
    require_hash(ROOT/s['pinned_coverage']['path'],s['pinned_coverage']['sha256']);coverage=read(s['pinned_coverage']['path']);pool=defaultdict(list)
    for path,digest in coverage['draft_asset_hashes'].items():
        require_hash(ROOT/path,digest)
        for u in read(path)['units']:pool[u['id']].append((path,digest,u))
    candidates=[];rejected=[];types=Counter();tpls={}
    for g in s['unresolved_groups']:
        if g['reasons']!=['variable_insertion']:continue
        arc=g['archive'];ref=read(pool[g['ids'][0]][0][0])['source_tpl'];require_hash(ROOT/ref['path'],ref['sha256'])
        tpl=tpls.setdefault(arc,(ROOT/ref['path']).read_text(encoding='utf-8-sig'));section=re.search(r'^script '+str(g['script'])+r'\s+\w+\s*\{[\s\S]*?(?=^script\s|\Z)',tpl,re.M).group()
        commands=tuple(re.findall(r'^\t(print\w+)\b',section,re.M));types[commands]+=1;us={};refs=[]
        for key in g['ids']:
            options=pool[key]
            if len({(u['source'],u['translation'],u['state']) for _,_,u in options})!=1:raise ValueError('Conflicting pinned wording '+key)
            path,digest,u=options[0];us[key]=u;refs.append(dict(id=key,path=path,sha256=digest))
        items=literals('@archive '+arc+'\n'+section)
        if any(us[i.key]['source']!=i.text for i in items if i.key in us):raise ValueError('Protected source identity')
        header=len('@archive '+arc+'\n');template,reason=inspect_template(section,[replace(i,start=i.start-header,end=i.end-header) for i in items],us,bound,True)
        if reason:rejected.append(dict(archive=arc,script=g['script'],ids=g['ids'],commands=list(commands),reason=reason));continue
        candidates.append(dict(archive=arc,script=g['script'],units=len(g['ids']),ids=g['ids'],drafts=refs,source_tpl=ref,template=template))
    deps=[SURVEY,CPU,'analysis/pending500_019_v1/integration.json','analysis/pending500_019_v1/name_display_runtime.json']
    result=dict(schema=1,baseline_rom=s['baseline_rom'],baseline_sha256=s['baseline_sha256'],source_sha256=s['source_sha256'],dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},native_provider_source_byte_identical=True,native_advance_bound=bound,current_runtime_samples_bound=True,cpu_execution_rerun=False,variable_only_groups=sum(types.values()),variable_only_units=sum(len(g['ids']) for g in s['unresolved_groups'] if g['reasons']==['variable_insertion']),command_populations=[dict(commands=list(k),groups=v) for k,v in types.most_common()],nickname_template_candidates=candidates,candidate_units=sum(g['units'] for g in candidates),rejections=rejected,rejection_group_counts=dict(Counter(g['reason'] for g in rejected)),rom_written=False,prose_changed=False,release_eligible=False,limits='Actual019 native-code/literal/descriptor/441metrics/42suffix applicability plus two own019 diagnostic samples. Donor bounded CPU evidence is not rerun; samples do not prove all native inputs/Navi/routes/save. Conditional candidate census only, not consumer admission, compile, new500 or complete remaining population.')
    frozen_write(ROOT/OUT,result)
    print('019 variable-only',result['variable_only_groups'],result['variable_only_units'],'conditional nickname candidates',len(candidates),result['candidate_units']);print(result['rejection_group_counts']);print(result['command_populations'][:8])

if __name__=='__main__':main()
