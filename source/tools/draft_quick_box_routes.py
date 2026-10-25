"""Manually authored quick-box tournament, agenda and profile candidates; no ROM writes."""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of

SOURCES={
'65B74C':('6339b7ce278745240573925add86c3ea3786203c0acd0dfdc1b2cff4e817763b',12,'translations/quick_tournament_draft_ko.json'),
'65B8E4':('fec888301a89e5101620077435232a22d1d57b7fa52598a66ba37aee1ec2095c',6,'translations/quick_agenda_draft_ko.json'),
'65B9E8':('981a92fe315bc19feba70e721b1bd1a30beea5e6e30fbd434e233e6583febb03',136,'translations/quick_profile_questions_draft_ko.json'),
}
DRAFT={
'65B74C':{
1:['아쉬웠네...\n다시 단련해서\n한 번 더 도전하자!'],
2:['우승이야!\n',',\n해냈어!!'],
10:['참가 신청을 안 했어!\n','!'],
20:['드디어 시작이야!\n','!\n온 힘을 다해 힘내자!'],
21:['드디어 시작이야!\n','!\n온 힘을 다해 힘내자!'],
22:['드디어 시작이야!\n','!\n온 힘을 다해 힘내자!'],
23:['드디어 시작이야!\n','!\n온 힘을 다해 힘내자!'],
},
'65B8E4':{
1:['곧'],
3:[' 일정이 있어!'],
10:['오늘 등록된\n일정은...','아무것도 없어'],
11:[':',' ','부터\n','「','」'],
12:[' 일정이야!'],
},
'65B9E8':{
1:['있잖아,\n',',\n인터넷은','1명이 하는 것보다\n다 같이 하는 게\n더 재밌지!','예를 들면, 형제자매와\n함께 말이야!',',\n형이나 오빠가 있어?','있어  ','없어','그렇구나~,\n그럼, 이름은?'],
2:['흐음, 그렇구나...'],
3:['있잖아,\n',',\n인터넷은','1명이 하는 것보다\n다 같이 하는 게\n더 재밌지!','예를 들면, 형제자매와\n함께 말이야!','맞다...\n',',\n남동생... 있어?','있어  ','없어','그렇구나~,\n이름이 뭐야?'],
4:['흐음, 그렇구나...'],
5:['있잖아,\n',',\n인터넷은','1명이 하는 것보다\n다 같이 하는 게\n더 재밌지!','예를 들면, 형제자매와\n함께 말이야!',',\n누나나 언니가 있어?','있어  ','없어','그렇구나~,\n그럼, 이름을 알려 줘?'],
6:['흐음, 그렇구나...'],
7:['있잖아,\n',',\n인터넷은','1명이 하는 것보다\n다 같이 하는 게\n더 재밌지!','예를 들면, 형제자매와\n함께 말이야!',',\n여동생이 있어?','있어  ','없어','그렇구나~,\n그럼, 이름을 알려 줘?'],
8:['흐음, 그렇구나...'],
9:['넷배틀 하면\n역시, 친구가\n떠오르지!',',\n친하게 지내는 친구를\n알려 줘'],
11:['인터넷\n재밌었지!!','그런데, 조금 배가\n고파진 것 같아!','이럴 때\n먹고 싶어지는','좋아하는 음식은\n뭐야?'],
13:['데이터 라이브러리는\n보기만 해도 재밌지','칩을 모으는 게\n취미가\n될 것 같아','아, 맞다!\n',',\n취미를 알려 줘!'],
15:['토너먼트 우승은\n넷배틀러 모두의\n꿈이지!','그럼 말이야,\n네가 앞으로 이루고 싶은\n꿈을 알려 줘!','정말 궁금해'],
17:['역시, 좋아하는 사람에게서\n메일이 오면\n기쁘지!!',',\n좋아하는 여자아이는\n이름이 뭐야?','괜찮잖아!\n아무한테도 말 안 할게\n응! 부탁이야!'],
19:['역시, 좋아하는 사람에게서\n메일이 오면\n기쁘지!!',',\n좋아하는 남자아이는\n이름이 뭐야?','괜찮잖아!\n아무한테도 말 안 할게\n응! 부탁이야!'],
21:['칩을 많이\n갖고 있거나,','배틀을 잘하거나\n하면,','여러 사람에게\n존경받을 수도\n있을 것 같은데,',',\n존경하는 사람은 누구야?'],
23:['여러 사람에게서 메일이\n올 것 같은데,','이 사람에게서 오면\n조금 곤란하겠다\n싶은','불편한 사람을 알려 줘!'],
25:['넷배틀도\n재밌지만,\nTV도 재밌지!',',\n좋아하는 TV 프로그램은\n뭐야!?'],
27:['인터넷도 좋지만\n공부도 제대로\n하자!!','그런데 말이야,\n',',\n자신 있는 과목은 뭐야?'],
29:['인터넷도 좋지만\n공부도 제대로\n하자!!','그런데 말이야,\n',',\n어려워하는 과목은 뭐야?'],
31:['만약에 말이야?\n토너먼트에서\n우승하면','좋아하는 건 뭐든\n선물해 준다고 하면\n뭘 갖고 싶어?'],
32:['라이브러리에 있는\n칩처럼,','유치원도\n많이 있지?','그런데, 네가 다니는\n유치원 이름은\n뭐야?'],
33:['라이브러리에 있는\n칩처럼,\n학교도 많이 있지?','그런데, 네가 다니는\n학교 이름은\n뭐야?'],
34:['라이브러리에 있는\n칩처럼,\n회사도 많이 있지?','그런데, 네가 다니는\n회사 이름은\n뭐야?'],
40:['의\n형이나 오빠는,'],
41:['그 밖에는?\n\n','있어  ','없어'],
42:['흐음, 그렇구나...'],
43:['의\n남동생은,'],
44:['그 밖에는?\n\n','있어  ','없어'],
45:['흐음, 그렇구나...'],
46:['의\n누나나 언니는,'],
47:['그 밖에는?\n\n','있어  ','없어'],
48:['흐음, 그렇구나...'],
49:['의\n여동생은,'],
50:['그 밖에는?\n\n','있어  ','없어'],
51:['흐음, 그렇구나...'],
52:['의\n친구는,'],
53:['그 밖에는?\n\n','있어  ','없어'],
54:['흐음, 그렇구나...'],
55:['의\n취미는,'],
56:['그 밖에는?\n\n','있어  ','없어'],
57:['흐음, 그렇구나...'],
58:['의\n좋아하는 TV 프로그램은,'],
59:['그 밖에는?\n\n','있어  ','없어'],
60:['흐음, 그렇구나...'],
61:['의\n갖고 싶은 것은,'],
62:['그 밖에는?\n\n','있어  ','없어'],
63:['흐음, 그렇구나...'],
80:['형이나 오빠라...\n좋겠다!'],
81:['남동생이라...\n후훗! 좋겠다!'],
82:['누나나 언니는,\n다정해?'],
83:['여동생이라...\n잘 대해 줘야겠네'],
84:['친구는 소중히\n여겨야지!!'],
85:['이름만 들어도,\n배가 고파지네!'],
86:['꽤 좋은 취미를\n갖고 있네!!'],
87:['그 꿈을 이룰 수 있으면\n좋겠다!'],
88:['그렇구나~, 좋은 얘기를\n들었네!'],
89:['확실히, 그 사람은\n대단한 사람이야...'],
90:['그렇구나...'],
91:['그렇구나~,\n나도 한 번\n보고 싶어'],
92:['흐음, 그렇구나!'],
93:['극복할 수 있도록\n힘내야겠네!'],
94:['그렇구나, 역시 그랬네!'],
95:['그렇구나...\n기억해 둬야지!'],
}}
CHOICES={(1,5),(1,6),(3,6),(3,7),(5,5),(5,6),(7,5),(7,6)}
CHOICES|={(s,i) for s in (41,44,47,50,53,56,59,62) for i in (1,2)}

def create(archive):
    digest,count,out=SOURCES[archive];source=f'analysis/full_scope_v1/source_tpl/{archive}.tpl'
    require_hash(ROOT/source,digest);original=(ROOT/source).read_text(encoding='utf-8-sig')
    all_values={f'{archive}:{s}:{i}':t for s,v in DRAFT[archive].items() for i,t in enumerate(v)}
    selected=[x for x in literals(original) if re.search(r'[\u3040-\u30ff\u3400-\u9fff]',x.text)]
    values={x.key:all_values[x.key] for x in selected}
    if len(selected)!=count:raise ValueError('quick-box scope '+archive)
    units=[]
    for x in selected:
        s,i=map(int,x.key.split(':')[1:]);t=values[x.key]
        if t.count('\n')!=x.text.count('\n') or t.startswith('\n')!=x.text.startswith('\n') or t.endswith('\n')!=x.text.endswith('\n'):raise ValueError('quick-box topology '+x.key)
        if re.findall(r'-?\d+|\[[^\]]+\]',t)!=re.findall(r'-?\d+|\[[^\]]+\]',x.text):raise ValueError('quick-box tokens '+x.key)
        if len(x.text)-len(x.text.rstrip(' '))!=len(t)-len(t.rstrip(' ')):raise ValueError('quick-box padding '+x.key)
        choice=archive=='65B9E8' and (s,i) in CHOICES
        units.append(dict(id=x.key,source=x.text,translation=t,state='needs_review',
            speaker='player-choice' if choice else 'unshown-quick-box-voice',
            origin_portrait=None,portrait_visibility='not-shown-in-script',
            context={'65B74C':'Tournament loss/win/not-entered/start notification, source actor not shown.',
                     '65B8E4':'Upcoming event list and today agenda; hour/minute/AMPM/name buffers preserved.',
                     '65B9E8':'Profile questions1..34; existing-entry/additional-entry choices40..63; reactions80..95.'}[archive],
            variable_context='Nickname/schedule/profile buffers retain position and arguments; no fixed 이/가/아/야 particle attached to user value. Actor/caller, input persistence, maximum width remain unverified.'))
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'));src=ROOT/cfg['source_profile']['filename']
    require_hash(src,cfg['source_profile']['sha256']);require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==int(archive,16))
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION',archive=archive,
        source_sha256=cfg['source_profile']['sha256'],source_tpl=dict(path=source,sha256=digest),
        source_archive_sha256=sha(payload_of(src.read_bytes(),row)),consumer='quick-box-tournament-agenda-profile',
        context=units[0]['context'],voice='Friendly plain source voice; no named Navi asserted without mugshot or caller proof; not human approved.',
        review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),
        insertion_state='translation-first draft only; not selected by ROM builder',
        protected_policy='Keep all commands/flags/branches/variables/name buffers, source literals not selected, original newlines and choice two-space padding; no edits to source archive or ROM.',
        semantic_review={
            '65B74C':['Loss encouragement, championship, lack of entry, approaching start are distinct; no false successful registration.',
                      'Nickname stays between text fragments; punctuation ! remains source. callCancelMenuTransition in10 and flag3603 in20..23 retained. No live competition verification.'],
            '65B8E4':['Quote characters/colon/blank literals are unselected source, not drafting count. Upcoming suffix 일정이 있어 and today suffix 일정이야 attach after quoted event names without final-consonant particle.',
                      'Hour/minute buffer1 formatting and AMPM buffer order unchanged. Time suffix부터 retains start-time meaning, not duration. AMPM output text translation and actual consumer width not proved by this batch.',
                      'Soon-event loop2 and today loop11 preserved, including source first soon-event jumpIfNone=2. No inferred branch repair or agenda/calendar runtime verification.'],
            '65B9E8':['Sibling candidates 형이나 오빠/누나나 언니 avoid inferring operator gender; younger brother/sister distinct. Same broader labels remain candidates, not bulk rewritten.',
                      'Source17/19 explicitly distinguish female/male liked person via global22 branch; preserved 여자아이/남자아이, not normalized to gender-neutral label.',
                      'School/company/kindergarten routing preserves global23 values1..5 to33,6..9 to34, otherwise32. No inferred age values or branch rewrite.',
                      'Nickname direct address uses comma and ownership uses 의, both avoid dependent allomorphs. Existing profile strings1/2/3 and global5 record-count routes unchanged.',
                      'ニガテな人 candidate 불편한 사람 matches new manager candidate; older 싫어하는 사람 remains unreconciled. No independent wording approval or input persistence/screen verification.']
        }[archive],units=units)

def main():
    for a,(_,count,out) in SOURCES.items():
        asset=create(a);p=ROOT/out
        if p.exists():
            if json.loads(p.read_text(encoding='utf8'))!=asset:raise ValueError('preserve quick-box draft '+out)
        else:p.write_text(json.dumps(asset,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        print(f'Authored {a} {count}; ROM unchanged')
if __name__=='__main__':main()
