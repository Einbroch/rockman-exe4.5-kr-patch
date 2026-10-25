"""Manual67 normal Napalm test/media/market candidates; no ROM writes."""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of
SOURCES={
'7BD4B0':('d18618b080c427d67475e35028f3cc3df13f0e34b35880423536c796391494e8',36,'translations/napalm_normal_passage_draft_ko.json'),
'7BDC90':('76c4909296c653d0ec597fed739964dc93208d2f61174a40f8b5a38678a0e0fd',5,'translations/stereo_program_draft_ko.json'),
'7BE0CC':('f32919eedf132dcbe462468e413312f64dae18487569bb6525c1ee7ec565671a',4,'translations/old_tv_program_draft_ko.json'),
'7BE518':('6e6c38740b54196e296be056d654d894722e681775d5db0b712a5099b6054e9b',22,'translations/black_market_draft_ko.json'),
}
DRAFT={
'7BD4B0':{
0:['...너,\n여기를 지나가고 싶은가!?','난 마음에 든 녀석에게만\n길을 열어 주는 주의다','여길 지나가고 싶다면\n내가 말한 대로 해서,\n내 마음에 들어 봐!!','어때, 하겠나?','예  ','아니요','헤헤헤, 뭘\n시켜 볼까...','그렇지...\n좋아, 이렇게 하자','인터넷1에\n지금부터 내가 바이러스를\n뿌릴 테니까','그 바이러스들을\n제한 시간 안에\n모두 날려 버려라','콰앙 하고 말이야!!','내 네이팜 프로그램을\n빌려주마...','그리고 1가지 더, 내가 뿌린\n바이러스를 모두\n날려 버릴 때까지,','절대로 플러그아웃하지 마라','바이러스가 무서워\n인터넷도 못 돌아다니는\n겁쟁이는 싫어하니까','한 번이라도 플러그아웃하면\n여길 지나가게 하지 않겠다','아무튼\n화끈하게 해 보라고!'],
1:['그런가, 그럼 다른 길을\n찾아보도록 해!'],
2:['뭐야? 뭘 해야 하는지\n벌써 잊었나?','할 수 없군, 다시\n말해 주마!','인터넷1에\n지금부터 내가 바이러스를\n뿌릴 테니까','그 바이러스들을\n제한 시간 안에\n모두 날려 버려라!','그리고 1가지 더, 내가 뿌린\n바이러스를 모두\n날려 버릴 때까지,','절대로 플러그아웃하지 마라','바이러스가 무서워\n인터넷도 못 돌아다니는\n겁쟁이는 싫어하니까','한 번이라도 플러그아웃하면\n여길 지나가게 하지 않겠다','아무튼\n화끈하게 해 보라고!'],
3:['인터넷1에서\n네가 바이러스를\n날려 버리는 걸 봤다','너, 제법 소질이\n있잖아!!','마음에 들었다...\n자, 지나가라!!'],
4:['뭐야, 실패했잖아\n그래서는 이 길을\n내줄 수 없다고!?','한 번 더 갔다 올 건가?','예  ','아니요','그럼 얼른 갔다 와라!!'],
5:['그런가, 그럼 다른 길을\n찾아보도록 해!'],
},
'7BDC90':{0:['오 예 베이비!!','나·는·말·이·야아아!!\n스·테·레·오·의','프로그램 오오오 예!','좋·은·소·리이이\n들려준다 예...','땡큐!']},
'7BE0CC':{0:['하와아...','있잖아,\n채널 바꾸는 거,\n엄청 귀찮지 않아?','뭐, 난 낡은 TV니까\n그 정도 말은 해도\n되는 거 아냐?','딱히 얇지도 않고오\n액정도 아니고오']},
'7BE518':{
221:['또 찾아와 줘...'],
222:['미안하지만,\n지금은 품절이야...'],
223:['어서 와,\n블랙마켓에...','난 어둠의 상인...','돈만 두둑이 내면,\n어떤 녀석과도\n장사하지...','잠깐 보고 갈래?\n','보기  ','안 보기'],
224:['어서 와,\n블랙마켓에...','난 어둠의 상인...','돈만 두둑이 내면,\n어떤 녀석과도\n장사하지...','특히 오늘은\n일주일에 한 번 있는\n레이디스 데이야...','아가씨들에겐 팍팍\n서비스해 주겠어!','잠깐 보고 갈래?\n','보기  ','안 보기'],
225:['어이, 블랙마켓에\n잘 왔어!!','너, 운이 좋군!\n오늘 난\n기분이 최고거든!','서비스해 줄 테니,\n잔뜩 사 가라고','평소에는 볼 수 없는\n좋은 물건 있어!?\n','보기  ','안 보기'],
},
}
def create(archive):
    digest,count,out=SOURCES[archive];source=f'analysis/full_scope_v1/source_tpl/{archive}.tpl'
    require_hash(ROOT/source,digest);original=(ROOT/source).read_text(encoding='utf-8-sig')
    values={f'{archive}:{s}:{i}':t for s,v in DRAFT[archive].items() for i,t in enumerate(v)}
    selected=[x for x in literals(original) if re.search(r'[\u3040-\u30ff\u3400-\u9fff]',x.text)]
    if len(selected)!=count or set(values)!={x.key for x in selected}:raise ValueError('media market scope '+archive)
    starts={int(m.group(1)):m.start() for m in re.finditer(r'^script (\d+) mmbn45',original,re.M)};units=[]
    for x in selected:
        s,i=map(int,x.key.split(':')[1:]);t=values[x.key]
        events=list(re.finditer(r'mugshotShow\s+mugshot = (\w+)|mugshotHide',original[starts[s]:x.start]));shown=[m.group(1) for m in events if m.group(1)]
        if not shown and not (archive=='7BE518' and s==221):raise ValueError('actor missing '+x.key)
        portrait=shown[-1] if shown else 'HeelNaviBlack';visibility=('visible' if events[-1].group(1) else 'hidden') if events else 'inherited-from-caller'
        choice=(archive=='7BD4B0' and ((s==0 and i in (4,5)) or (s==4 and i in (2,3)))) or (archive=='7BE518' and ((s==223 and i in (4,5)) or (s==224 and i in (6,7)) or (s==225 and i in (4,5))))
        if t.count('\n')!=x.text.count('\n') or t.endswith('\n')!=x.text.endswith('\n'):raise ValueError('media topology '+x.key)
        if re.findall(r'-?\d+|\[[^\]]+\]',t)!=re.findall(r'-?\d+|\[[^\]]+\]',x.text):raise ValueError('media tokens '+x.key)
        if x.text.endswith('  ') and not t.endswith('  '):raise ValueError('choice spacing '+x.key)
        units.append(dict(id=x.key,source=x.text,translation=t,state='needs_review',speaker='player-choice' if choice else portrait,origin_portrait=portrait,portrait_visibility=visibility,context='Normal NapalmMan passage test/reminder/success/failure/retry, stereo singing program, tired old-TV program or black-market merchant. All local branches read.',variable_context='Source numeral1 kept; no inserted names/items. Black market221 inherits HeelNaviBlack; visible shop options still player choices.'))
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));src=ROOT/cfg['source_profile']['filename'];require_hash(src,cfg['source_profile']['sha256']);require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==int(archive,16))
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION',archive=archive,source_sha256=cfg['source_profile']['sha256'],source_tpl=dict(path=source,sha256=digest),source_archive_sha256=sha(payload_of(src.read_bytes(),row)),consumer='normal-dialogue-choice-minigame-shop',context='All67 Japanese literals from4 archives, local dialogue/branches read.',voice='Rough NapalmMan, sung stereo English loanwords, tired casual TV and rough merchant separated; candidate voices not approved.',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),insertion_state='translation-first draft only; not selected by ROM builder',protected_policy='Keep flag6194/startNapalmManMinigame hard=false, Internet1/all viruses/time unspecified/any plugout failure; market shops4/14/global7=2/global6=1/weekday3/Navi1 and options unchanged.',semantic_review=['Normal test Internet1 is not hard-test UnderInternet2. Napalm program lending appears only in initial0, not reminder2; no added time number or changed test command.', 'Retry4 uses mugshotHide unlike hard-test visible retry; choices are hidden player choices. Success offers passage and failure refuses it.', 'Stereo interrupted singing literals remain three separate pages/fragments; punctuation and sound expansion are authored candidates, not inferred voice/audio assets.', 'TV explicitly old, not thin or LCD; casual tired register retained rather than default polite MrProgGreen. No remote-control repair quest invented.', 'Market stock14 may also be reached through global7/6 special conditions before weekday/Navi branch. No player-gender gate, discount amount or item additions inferred.', 'Static protection not normal-play test/plugout/clock/market purchase/save/screen verification; rhythm, names and service phrasing require human review.'],units=units)
def main():
    for a,(_,count,out) in SOURCES.items():
        asset=create(a);p=ROOT/out
        if p.exists():
            if json.loads(p.read_text(encoding='utf8'))!=asset:raise ValueError('preserve media draft '+out)
        else:p.write_text(json.dumps(asset,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        print(f'Authored {a} {count}; ROM unchanged')
if __name__=='__main__':main()
