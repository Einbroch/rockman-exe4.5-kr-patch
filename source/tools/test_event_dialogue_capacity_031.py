"""Controlled event-page acceptance/refusal and current conditional geometry."""
from copy import deepcopy
from build_visibility_poc import ROOT,sha,require_hash
from cumulative_batch500 import read,frozen_write
from event_dialogue_capacity_031 import validate,PREFIX
from nickname_capacity import ARGS
from tpl_literals import serialize
from survey_pet_quick_reflow_024 import replace_for_analysis

OUT='analysis/pending_insertion_500_031_event_models_v1/result.json'


def main():
    prefix=''.join('\t'+n+'\n'+a for n,a in PREFIX)
    body='\tcallBufferEventName\n\t"「"\n\tprintScheduleBuffer\n'+ARGS+'\t"」"\n\tkeyWait\n\t\tany = false\n\tclearMsg\n\twaitHold\n'
    def wrap(b=body,p=prefix):return '@archive ABCDEF\n@size 1\nscript 0 mmbn45 {\n'+p+b+'}\n'
    fixtures=[]
    def test(name,src,dst,accepted):
        try:validate(src,dst,[0],{'ABCDEF:0:0','ABCDEF:0:1'},99);actual=True
        except ValueError:actual=False
        if actual!=accepted:raise ValueError('031 event model fixture '+name)
        fixtures.append(dict(name=name,accepted=actual))
    base=wrap();test('PET-name-two-quotes-exact132',base,base,True)
    normal=wrap(p='\tmugshotShow\n\t\tmugshot = Rockman\n\tmsgOpen\n');test('normal-explicit-portrait',normal,normal,True)
    guard=wrap(body.replace('\twaitHold','\tcallCheckNowEvent\n\t\tjumpIfExists = 3\n\t\tjumpIfNone = continue\n\tflagClear\n\t\tflag = 3658\n\twaitHold'));test('cleared-conditional-preserved',guard,guard,True)
    for name,value in [
        ('aggregate133plus',wrap(body.replace('\t"」"','\t"」!"'))),
        ('missing-producer',wrap(body.replace('\tcallBufferEventName\n',''))),
        ('unknown-overwrite',wrap(body.replace('\t"「"','\tcallBufferEventFrequency\n\t"「"'))),
        ('reversed-wait-clear',wrap(body.replace('\tkeyWait\n\t\tany = false\n\tclearMsg','\tclearMsg\n\tkeyWait\n\t\tany = false'))),
        ('bad-arguments',wrap(body.replace('printN = false','printN = true'))),
        ('unprepared-numeric',wrap(body.replace('\tprintScheduleBuffer\n'+ARGS,'\tprintBuffer\n\t\tbuffer = 1\n\t\tminLength = 2\n\t\tpadZeros = true\n\t\tpadLeft = true\n'))),
        ('caller-inherited-box',wrap(p='')),
        ('unknown-box-origin',wrap(p=prefix.replace('left = 92','left = 91'))),
        ('unknown-choice',wrap(body.replace('\tkeyWait','\tpositionOptionHorizontal\n\t\twidth = 8\n\tkeyWait'))),
        ('producer-after-wait',wrap(body.replace('\tclearMsg','\tcallBufferEventName\n\tclearMsg'))),
        ('unknown-caller-guard',wrap(body.replace('\twaitHold','\tcallFindSoonEvent\n\t\tjumpIfExists = 2\n\t\tjumpIfNone = 3\n'))),
        ('missing-terminal',wrap(body.replace('\twaitHold\n',''))),
    ]:test(name,value,value,False)
    test('protected-origin-change',base,base.replace('left = 92','left = 93'),False)
    text=serialize('가\n나\n다\n라');four=wrap(body.replace('"」"',text));test('fourrows',four,four,False)
    survey_path='analysis/pending_insertion_500_031_event_layout_v1/survey.json';survey=read(survey_path);count=0;groups=0
    for g in survey['candidate_groups']:
        if g['profile']!='event-pages':continue
        ref=g['source_tpl'];require_hash(ROOT/ref['path'],ref['sha256']);src=(ROOT/ref['path']).read_text(encoding='utf-8-sig');units=[]
        for link in g['drafts']:
            require_hash(ROOT/link['path'],link['sha256']);u=deepcopy(next(u for u in read(link['path'])['units'] if u['id']==link['id']));u['translation']=g['explicit_layouts'].get(u['id'],u['translation']);units.append(u)
        if validate(src,replace_for_analysis(src,units),[g['script']],set(g['ids']),survey['native_nickname_bound'])!=g['geometry']:raise ValueError('031 frozen event geometry')
        count+=len(units);groups+=1
    deps=[survey_path,'tools/test_event_dialogue_capacity_031.py','tools/event_dialogue_capacity_031.py']
    frozen_write(ROOT/OUT,dict(schema=1,passed=True,fixtures=fixtures,conditional_candidate_units=count,conditional_candidate_scripts=groups,dependencies={p:sha((ROOT/p).read_bytes()) for p in deps},product_admitted=False,rom_written=False,release_eligible=False,limits=['Controlled model tests and current205 geometry only; native guards/time formatting/all title origins/GBA maximum name still separate prerequisites.']))
    print('031 event geometry PASS',len(fixtures),'fixtures',count,'conditional units',groups,'scripts',flush=True)


if __name__=='__main__':main()
