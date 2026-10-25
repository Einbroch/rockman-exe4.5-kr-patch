"""Individually authored Official preliminary/NPC117; source-bound draft."""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of

SOURCE='analysis/full_scope_v1/source_tpl/7AE0A0.tpl'
SOURCE_SHA='7cc50dfd9b0b5bcf06602b1717b6f8e9e8b1b9e0276b7ad9174dcfe95cdc39dd'
OUT='translations/official_prelim_draft_ko.json'
# None keeps existing quote-only source literals; never selects by whole script.
DRAFT={
0:['나는\n오피셜 토너먼트의\n시험관이다...','오피셜 토너먼트의\n예선 접수를 하고 있지','예선에 참가하겠나?','예  ','아니요','자네는...\n','...맞군...','미안하지만 지금의 자네는\n오피셜 토너먼트의\n예선을 볼 자격이 없네','우리는 사전에\n전국의 넷 배틀러에게\n적성 시험을 실시하고 있네','자네는 아직 적성 수준에\n도달하지 못했네','토너먼트에 나가고 싶다면,\n힘내서 적성 시험을\n통과하도록 하게...','눈치채지 못했을지 모르지만,\n자네가 견습 넷 배틀러가\n된 그날부터,','시험은 시작되어 있었네\n......','힘내 보게'],
1:['자네는...\n','...맞군...','음, 적성 시험인\n내비 6체 삭제를\n훌륭히 해냈군','적성은 충분하네','그럼, 예선 설명을\n시작하겠네','말하자면, 오피셜\n토너먼트의 예선이네','자네가 어떤 사건을\n해결해 주었으면 하네','조금 위험한 일을\n겪을 수도 있지만,\n도전하겠나?','예  ','아니요','마음의 준비가\n되면, 언제든 오게'],
2:['...인가...\n역시 왔군...','오피셜 토너먼트의\n예선을 보겠나?','예선에서는,\n자네가 어떤 사건을\n해결해 주었으면 하네','조금 위험한 일을\n겪을 수도 있지만,\n도전하겠나?','예  ','아니요','마음의 준비가\n되면, 언제든 오게'],
3:['그럼, 예선에 대해\n자세히 설명하겠네','이 앞의 인터넷12에\n트윈 록이라는\n보안 시스템이 있네','트윈 록은,\n언더인터넷 입구\n앞에 있으며,',None,'」,\n「','」,\n2개의 열쇠가 모여야','비로소 해제할 수 있는\n튼튼한 보안 시스템으로,','언더인터넷에서\n흉악한 내비와 바이러스가\n나오지 못하게 하고 있지','트윈 록 너머에는\n오피셜 토너먼트의\n참가 접수장이 있네','즉, 선택된 내비만\n들어갈 수 있도록 해 놓았지','그런데, 트윈 록을\n해제하는 열쇠 중 1개인\n「','」:','블랙워크스를 자칭하는\n집단에게 빼앗기고\n말았네','여기까지 설명하면\n이제 알겠지만,','블랙워크스를 소탕하고\n「','」:\n되찾아 주게','그것이, 토너먼트\n예선의 내용이네','블랙워크스 녀석들은\n인터넷10, 11에\n두 무리로 나뉘어 있을 걸세','녀석들이 숨은\n장소로 가려면 인터넷12를\n경유해야 하네',None,'」:\n되찾아 준다면',None,'」,\n「','」:','자네에게 주겠네\n그러면 참가 접수장까지\n갈 수 있지','그럼, 힘내 보게'],
4:['블랙워크스 녀석들은\n인터넷10, 11에\n두 무리로 나뉘어 있을 걸세','녀석들이 숨은\n장소로 가려면 인터넷12를\n경유해야 하네','조심하게...'],
5:['오, 이것은...','블랙워크스에게서\n「','」:\n되찾았군...','...좋아, 합격이다!',None,'」:\n그대로 가지고 있게','그리고, 이것을 자네에게\n주겠네',',\n「','」\n획득!!','그걸 가지고 인터넷12의\n트윈 록을 해제하면\n그곳이 참가 접수장이네','그 너머에 무엇이 기다릴지는\n내 입으로 말할 수 없지만,\n힘내 보게'],
6:['네트워크 사회의\n치안은 나빠져만 가는군','더 많은 훌륭한\n넷 배틀러를 육성해서','더 나은 네트워크 사회를\n만들어 가야 하네'],
7:['그런가...'],
10:['하아암...','앗, 안 되지, 안 돼!\n인터넷의 평화를\n지키는 것이','우리 오피셜의 임무!','약간의 졸음 따위는\n아무것도 아니지!!'],
11:['아, 보고서를\n오후까지 써야 하는데!','아, 제때 끝낼 수 있을까...'],
12:['왜 이 에어리어는\n이렇게 빙빙 도는 거야!?'],
13:['환영합니다!!\n여기는 인터넷9입니다!','여기부터는 오피셜이\n관리하는 에어리어입니다!'],
20:['무슨 일이시죠?\n뭔가 잃어버리기라도\n하셨나요?','...네, 아니라고요?','안 돼요,\n일을 방해하시면'],
21:['음음, 오늘도 평화로우니\n무엇보다 좋군!'],
22:['버그 조각도\n교환하고 왔으니','뭘 할까...'],
30:['이 경광등에\n맹세하고 이 에어리어의\n치안을 지키겠습니다!!'],
31:['어두워지면,\n이래저래 위험해지니\n제대로 순찰해야지!','오피셜이 있기만 해도\n범죄 발생률이\n줄어든다고 하니까!!'],
32:['이 앞 에어리어에\n인터넷 학원이\n있는데,','내비가 공부를 해 봐도\n...글쎄'],
40:['시민이 잠들어 있을 때\n일하는 것이 우리의 임무!'],
41:['드르렁...'],
50:['...음?','...꽤 능숙한\n실력자 같군...','나와 겨뤄 보지 않겠나?','그래  ','그만둘래','네 실력을\n보고 싶군...'],
51:['이 나를\n쓰러뜨리다니...','그 힘을, 올바르게\n쓰도록 해라...'],
52:['좀 더 잘할 줄 알았는데,\n내가 잘못 생각했나...'],
53:['번개여,\n내게 힘을!!','배틀 오퍼레이션, 세트!\n인!!'],
54:['...음?','이것 참 기묘하군...\n꿈인가 환상인가...','싸워 보면 알겠지...','덤벼  ','무리야!','싸울 것도 없겠군...'],
220:['나는 버그 조각\n교환상...','교환하시겠어요?\n','예  ','아니요'],
221:['또 오세요!'],
222:['유감이지만,\n품절입니다...']
}

def create():
    require_hash(ROOT/SOURCE,SOURCE_SHA);original=(ROOT/SOURCE).read_text(encoding='utf-8-sig')
    values={f'7AE0A0:{s}:{i}':t for s,rows in DRAFT.items() for i,t in enumerate(rows) if t is not None}
    selected=[x for x in literals(original) if re.search(r'[\u3040-\u30ff\u3400-\u9fff]',x.text)]
    if len(selected)!=117 or set(values)!={x.key for x in selected}:raise ValueError('prelim117 scope '+str(set(values)^{x.key for x in selected}))
    blocks={int(m.group(1)):(m.start(),m.group(0)) for m in re.finditer(r'script (\d+) mmbn45 \{(.*?)(?=\nscript |\Z)',original,re.S)}
    units=[]
    for x in selected:
        s,i=map(int,x.key.split(':')[1:]);t=values[x.key];start,block=blocks[s]
        events=list(re.finditer(r'mugshotShow\s+mugshot = (\w+)|mugshotHide',original[start:x.start]))
        if s==221:portrait='NormalNaviPink';speaker=portrait;visibility='inherited from native220 exchange-shop caller'
        elif not events:raise ValueError('unresolved speaker '+x.key)
        else:
            shown=[m.group(1) for m in events if m.group(1)]
            if not shown:raise ValueError('unresolved portrait '+x.key)
            portrait=shown[-1];visibility='visible' if events[-1].group(1) else 'hidden'
            speaker=portrait if visibility=='visible' else 'system-reward' if s==5 and i in (7,8) else 'player-choice'
        if t.count('\n')!=x.text.count('\n') or t.endswith('\n')!=x.text.endswith('\n'):raise ValueError('source row topology '+x.key)
        if re.findall(r'-?\d+|\[[^\]]+\]',t)!=re.findall(r'-?\d+|\[[^\]]+\]',x.text):raise ValueError('source numbers/tokens '+x.key)
        units.append(dict(id=x.key,source=x.text,translation=t,state='needs_review',speaker=speaker,origin_portrait=portrait,portrait_visibility=visibility,context='Official aptitude/preliminary qualification, two-key theft/recovery, Internet9 nearby NPCs, ThunderMan normal/self-Navi challenge and bugfrag shop',variable_context='printCurrentNavi/item10/item11 and key order unchanged; invariant colon/comma/list construction avoids name-dependent particles. Hidden options/reward distinguished; actual variable width/caller review pending.'))
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));src=ROOT/cfg['source_profile']['filename'];require_hash(src,cfg['source_profile']['sha256']);require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==0x7AE0A0)
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION',source_sha256=cfg['source_profile']['sha256'],archive='7AE0A0',source_tpl=dict(path=SOURCE,sha256=SOURCE_SHA),source_archive_sha256=sha(payload_of(src.read_bytes(),row)),consumer='normal-dialogue-and-choice',context='All117 unselected Japanese literals in255-slot Official preliminary/NPC archive. Source body, flags2491/1808, keys10/11, grant10 and ThunderMan checkNavi6 branches read together. Source-only quote literals kept unselected.',voice='NormalNaviBrown examiner commanding register, Official NPC/patrol and polite shop separated; ThunderMan solemn challenge source voice reused as candidate, no new approvals.',review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),insertion_state='translation-first draft only; not selected by ROM builder',protected_policy='Keep source IDs, numeric6/2/1/10/11/12/9, selected/cancel defaults and widths, flag progression, item10/11 variables and grant order, hidden portrait choices, ThunderMan battle setup and shop stock logic. No ROM/gameplay/save mutation.',semantic_review=['Source ツインロック candidate 트윈 록 follows existing keyitem_full_rom_ko.json. 블랙워크스/경광등/인터넷 학원 remain source-backed candidates, not human-approved new terms.', 'Narrative gives stolen key11, recovery via groups inInternet10/11 reached throughInternet12, keeps stolen key and grants key10. No item variable hardcoded to guessed display name.', 'Key-bearing fragments use colon/comma noun labels; meanings retained but final prose/presentation requires review, no automatic particle choice assumed.', 'Visible source portrait0..7 examiner vs hidden player choices and reward5 distinguished. Shop221 inherits source220 NormalNaviPink; no unrelated actor invented.', 'CheckNavi6/self-match54, challenge acceptance53, win51/loss52 and shop220..222 stay separate. Normal gameplay and all selected branches unverified.'],units=units)

def main():
    a=create();path=ROOT/OUT
    if path.exists():
        if json.loads(path.read_text(encoding='utf8'))!=a:raise ValueError('preserve prior translation')
    else:path.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print('Authored Official preliminary117 draft only; ROM unchanged')

if __name__=='__main__':main()
