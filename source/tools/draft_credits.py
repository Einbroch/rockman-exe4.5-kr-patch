"""Manual71 credits candidates; no ROM writes."""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of

SOURCES={
'7CE5C8':('f414a6099a1d889e001d8776face934959fdc2787d8c55161adfc75148be2270',71,'translations/credits_draft_ko.json'),
}
DRAFT={
'7CE5C8':{
0:['기획'],
1:['        야스마 마사히로'],
2:['        오자키 코헤이'],
3:['시나리오'],
4:['        에구치 마사카즈'],
5:['캐릭터 디자인'],
6:['        이시하라 유지'],
7:['          카지 하야토'],
8:['레이저맨 디자인'],
9:['        노나카 요시히토'],
10:['켄도맨 디자인'],
11:['         코이도 유타'],
12:['비디오맨 디자인'],
13:['        시미즈 요스케'],
14:['오브젝트'],
15:['        사토 카즈타카'],
16:['        나카야마 이쿠오'],
17:['        아리마 쿄코'],
18:['        나카시마 토키코'],
19:['        요시오카 마유미'],
20:['스크롤'],
21:['          키지마 미키'],
22:['       후지사키 준코'],
23:['        류고 치에코'],
24:['프로그램'],
25:['        마츠다 코에츠'],
26:['       신가키 히데카즈'],
27:['        사카노 미츠노리'],
28:['        아나이 토시히데'],
29:['         이쿠타 신야'],
30:['        니시야마 나오코'],
31:['        이토 소이치'],
32:['음악'],
33:['       호리야마 토시히코'],
34:['         카이다 아카리'],
35:['효과음'],
36:['        아마기시 신지'],
37:['공식 일러스트'],
38:['        코마키 신스케'],
39:['플러그인 효과'],
40:['        히키타 히로카즈'],
41:['설명서 제작'],
42:['        이와사키 아케미'],
43:['버그 검사 총괄'],
44:['         난바 마사토'],
45:['특별히 감사드립니다!'],
46:['        야마시타 히로시'],
47:['        시모가와 테루히로'],
48:['        나카무라 히로코'],
49:['        초야 카즈오'],
50:['        후나하라 쿠니오'],
51:['         우카이 사토시'],
53:['         야스다 유코'],
54:['        키타하라 타카시'],
55:['        미나미데 나오토'],
56:['          타나카 사라'],
57:['  코나미JPN 코지마 히데오'],
58:[' 코나미JPN 히나미 마사히로'],
59:['    록맨 클럽 여러분'],
60:['    두 번째 개발부 여러분'],
61:['        캡콤 여러분'],
62:['프로듀서'],
63:['        이나후네 케이지'],
64:['클리어 시간     ',None],
65:['데이터 라이브러리 S  ','장'],
66:[None,'장'],
67:[None,'장'],
68:['록맨 에그제4.5'],
69:['리얼 오퍼레이션'],
70:['스태프'],
},
}

def create(archive):
    digest,count,out=SOURCES[archive];source=f'analysis/full_scope_v1/source_tpl/{archive}.tpl'
    require_hash(ROOT/source,digest);original=(ROOT/source).read_text(encoding='utf-8-sig')
    values={f'{archive}:{s}:{i}':t for s,v in DRAFT[archive].items() for i,t in enumerate(v) if t is not None}
    selected=[x for x in literals(original) if re.search(r'[\u3040-\u30ff\u3400-\u9fff]',x.text)]
    if len(selected)!=count or set(values)!={x.key for x in selected}:raise ValueError('laserman scope '+archive)
    starts={int(m.group(1)):m.start() for m in re.finditer(r'^script (\d+) mmbn45',original,re.M)};units=[]
    for x in selected:
        s,i=map(int,x.key.split(':')[1:]);t=values[x.key]
        portrait=None;visibility='not-shown-in-script'
        if len(t)-len(t.lstrip(' '))!=len(x.text)-len(x.text.lstrip(' ')):raise ValueError('credits leading alignment '+x.key)
        if len(t)-len(t.rstrip(' '))!=len(x.text)-len(x.text.rstrip(' ')):raise ValueError('credits trailing alignment '+x.key)
        if t.count('\n')!=x.text.count('\n') or t.endswith('\n')!=x.text.endswith('\n'):raise ValueError('laserman topology '+x.key)
        if re.findall(r'-?\d+|\[[^\]]+\]',t)!=re.findall(r'-?\d+|\[[^\]]+\]',x.text):raise ValueError('laserman tokens '+x.key)
        if x.text.endswith('  ') and not t.endswith('  '):raise ValueError('choice spacing '+x.key)
        units.append(dict(id=x.key,source=x.text,translation=t,state='needs_review',speaker="credits-label" if s>=64 else "credits-entry",origin_portrait=portrait,portrait_visibility=visibility,context='Staff credits and end-result labels; kana names transliterated as candidates, no speaker portrait.',variable_context='64 buffers0/1 padded2 time;65..67 buffer0 padded3 chip counts, S/M/G prefixes and colon preserved. Leading/trailing ASCII spaces preserved exactly.'))
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));src=ROOT/cfg['source_profile']['filename'];require_hash(src,cfg['source_profile']['sha256']);require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==int(archive,16))
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION',archive=archive,source_sha256=cfg['source_profile']['sha256'],source_tpl=dict(path=source,sha256=digest),source_archive_sha256=sha(payload_of(src.read_bytes(),row)),consumer='staff-credits-and-clear-result-labels',context='All71 Japanese literals in credits archive; absent script52 not fabricated, non-Japanese S/M/G/time separators preserved.',voice='Credit role labels and kana-based staff-name transcription candidates; not human approved.',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),insertion_state='translation-first draft only; not selected by ROM builder',protected_policy='Preserve every original leading/trailing ASCII space, source role/name links/order, script gaps, printBuffer indices/padding/minLength and nonselected colon/M/G prefixes.',semantic_review=['People names transcribed from kana actually present; no external spelling/kanji inferred or identification approved. Role/person relationships and KonamiJPN attribution retained.', 'Roles オブジェクト/スクロール/プラグインエフェクト remain literal labels; no task responsibility expansion invented.', '第2 development division source spelled kana without ASCII digit; draft must not invent a numeric token, use descriptive 두 번째 개발부 candidate without new ASCII numeric token.', 'Credit spacing is preserved source alignment, not confirmed Korean centering or capacity. Actual ending font/renderer/scroll layout remains unverified.', 'Standard/Mega/Giga library counters preserve S/M/G and dynamic3digit width; count suffix枚 drafted 장. Time HH:MM buffer order/zero padding unchanged.', 'Game-title4.5 and Real Operation subtitle remain candidates consistent with project title; no branding exclusion or distribution approval.', 'No actual ending/credits/clear-result runtime screenshot or save verification; static checks not human or runtime approval.'],units=units)

def main():
    for a,(_,count,out) in SOURCES.items():
        asset=create(a);p=ROOT/out
        if p.exists():
            if json.loads(p.read_text(encoding='utf8'))!=asset:raise ValueError('preserve laserman draft '+out)
        else:p.write_text(json.dumps(asset,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        print(f'Authored {a} {count}; ROM unchanged')
if __name__=='__main__':main()
