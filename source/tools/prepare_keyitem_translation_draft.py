"""Source-pinned translation preparation; deliberately not a ROM build input."""
import json
from build_visibility_poc import ROOT, sha, require_hash
from tpl_literals import literals, replace_literals, skeleton

TEXT = {
0: ['견습 라이선스 시험에\n응시하기 위한\n수험표'],
1: ['견습 넷배틀러임을\n증명하는\n라이선스'],
2: ['실버 토너먼트에서\n우승한 내비에게\n수여하는 라이선스'],
3: ['골드 토너먼트에서\n우승한 내비에게\n수여하는 라이선스'],
4: ['오피셜 토너먼트에서\n우승한 선수에게\n수여하는 트로피'],
5: ['인터넷2와 3을\n잇는 통로를 막는\n문을 여는 열쇠'],
6: ['전뇌 식물의 씨앗\n(×', '개)'],
7: ['전뇌 세계의 전기를\n다스리는 신을\n본뜬 조각상(×', '개)'],
8: ['통행증'],
9: ['커트 키2'],
10: ['인터넷12의\n트윈 록을 해제하는\n열쇠 역할의 데이터'],
11: ['인터넷12의\n트윈 록을 해제하는\n열쇠 역할의 데이터'],
12: ['스피드 테스트를\n통과했다는 증표'],
13: ['테크닉 테스트를\n통과했다는 증표'],
14: ['칩 획득 테스트를\n통과했다는 증표'],
15: ['번역'],
16: ['산수 문제가\n많이 담긴\n교육 프로그램(×', '개)'],
17: ['얼어붙은 바이러스를\n찾아내기 위한\n검색 소프트웨어(×', '개)'],
18: ['샤로 군에서 보낸\n저격 훈련 초대장\n(×', '개)'],
19: ['에브리데이 토너먼트\n우승자에게\n수여하는 티켓'],
20: ['에브리데이 토너먼트\n우승자에게\n수여하는 티켓'],
32: ['키 아이템이\n1개도 없다・・・'],
33: ['HP 메모리'],
34: ['확장 메모리'],
35: ['레귤러UP1'],
36: ['레귤러UP2'],
37: ['레귤러UP3'],
38: ['서브 메모리'],
39: ['HP를 50 회복!'],
40: ['HP를 최대치까지\n회복!'],
41: ['잠시 동안\n약한 바이러스와\n마주치지 않게 된다'],
42: ['미스터리 데이터의\n함정을 해제한다'],
43: ['바로 전에 만난\n적과 다시\n마주치기 쉬워진다'],
44: ['보안이 걸린\n미스터리 데이터를\n해석한다'],
}

def prepare():
    source_path=ROOT/'analysis/full_scope_v1/source_tpl/709408.tpl'
    require_hash(source_path,'5cffb36f931ce04b2eaaa9861adabbe22b279b5f5eb565e9910ca436ba4cccdb')
    original=source_path.read_text(encoding='utf-8-sig')
    items=literals(original)
    expected={f'709408:{s}:{i}' for s, texts in TEXT.items() for i in range(len(texts))}
    if {x.key for x in items}!=expected:
        raise ValueError('keyitem source literal inventory changed')
    units=[]
    for x in items:
        _,script,ordinal=x.key.split(':')
        target=TEXT[int(script)][int(ordinal)]
        if target.count('\n')!=x.text.count('\n'):
            raise ValueError('keyitem row structure changed: '+x.key)
        units.append(dict(id=x.key,source=x.text,translation=target,state='needs_review'))
    translated=replace_literals(original,units)
    if skeleton(original)!=skeleton(translated):
        raise ValueError('keyitem command structure changed')
    for s in [6,7,16,17,18]:
        if TEXT[s][-1]!='개)' or not TEXT[s][0].endswith('(×'):
            raise ValueError('keyitem quantity insertion boundaries changed')
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION; NOT BUILD INPUT',
        archive='709408',source_tpl_sha256=sha(source_path.read_bytes()),
        rom_applied=False,release_eligible=False,
        review=dict(wording='needs_review',layout='needs_runtime_review',
                    glossary='pending contextual reconciliation'),
        unresolved=['Both native decompression consumers need proven capacity/lifetime.',
                    'Quantity-buffer aggregate geometry and glossary need verification.',
                    'No new ROM or translated runtime-screen claim.'],
        units=units),translated

def main():
    asset,target=prepare()
    out=ROOT/'analysis/keyitem_translation_draft_v1'
    out.mkdir(exist_ok=True)
    files={out/'draft.json':json.dumps(asset,ensure_ascii=False,indent=2)+'\n',
           out/'709408.ko.draft.tpl':target}
    for path,text in files.items():
        if path.exists() and path.read_text(encoding='utf8')!=text:
            raise ValueError('preserve existing draft evidence: '+str(path))
        if not path.exists():path.write_text(text,encoding='utf8')
    print(json.dumps(dict(units=len(asset['units']),source_literals_preserved=True,
        command_skeleton_unchanged=True,rom_applied=False,release_eligible=False)))

if __name__=='__main__':main()
