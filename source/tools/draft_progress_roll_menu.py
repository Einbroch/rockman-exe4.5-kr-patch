"""Manual progress hints and remaining Roll menu drafts; no ROM writes."""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of
SOURCES={
'65E8B8':('1f9361c075c7e4d06b6fd72cdeffa5e6609c5cb764e0609e711d960ec8fc93f3',31,'translations/quick_progress_hints_draft_ko.json'),
'65F11C':('325e00b29edbe2174124bd45ef40fd118786b80bb2b48779bd9bce8d5a1b4033',51,'translations/roll_menu_remaining_draft_ko.json'),
}
DRAFT={
'65E8B8':{
'10:0':'인터넷을 더\n탐색해 보자!',
'11:0':'견습 라이선스 시험을\n보러 가자!',
'12:0':'견습 라이선스 시험\n힘내자!!',
'13:1':'」 칩을\n구하러 가자!',
'14:0':'견습 라이선스를\n받으러 가자!',
'15:0':'견습 라이선스 시험\n수고했어!\n잠깐 쉴까?',
'16:0':'인터넷3에서\n벌어진 사건이\n신경 쓰이네...',
'17:0':'아까 쓰러뜨린 내비가\n사건의 범인이었던\n것 같네...',
'17:1':'피곤하지,\n한 번 플러그아웃\n할까?',
'18:0':'인터넷5에서\n벌어진 사건이\n신경 쓰이네...',
'19:0':'인터넷7에서\n벌어진 사건이\n신경 쓰이네...',
'20:0':'인터넷9에서\n벌어진 사건이\n신경 쓰이네...',
'21:0':'인터넷10에서\n벌어진 사건이\n신경 쓰이네...',
'22:0':'인터넷12에서\n벌어진 사건이\n신경 쓰이네...',
'23:0':'블랙워크스에게서\n「마이너스키」를\n되찾자!!',
'24:0':'「마이너스키」는,\n다른 내비 1명이 갖고\n있는 것 같네!!',
'25:0':'「마이너스키」를\n인터넷9에 있는\n내비에게 전해 주자!',
'26:0':'오피셜\n토너먼트의\n참가 접수장에',
'26:1':'가 보자!',
'27:0':'언더인터넷으로\n가자!',
'27:1':'흉악범을 찾을\n표식은\n관이었지',
'28:0':',\n오피셜\n토너먼트에',
'28:1':'참가 신청하러 가자!',
'29:0':'주말에 열리는\n오피셜 토너먼트\n힘내자!!',
'30:0':'오피셜 토너먼트\n우승...\n넷배틀러의 꿈이지',
'31:0':'인터넷에는\n아직 비밀이 더\n있을지도 몰라!',
'31:1':'좀 더 탐색해\n보자',
'32:1':'오피셜\n토너먼트 예선을\n보러 가자!',
'33:0':'있잖아, 아까 도착한\n메일을 읽어 보자!',
'34:0':'다음 주가 되면,\n오피셜\n토너먼트의',
'34:1':'참가 접수장에\n가자',
},
'65F11C':{
'3:0':'그날은 이미 지났는데?',
'4:0':'더는 등록할 수 없어',
'4:1':'새로 등록하려면,\n이미 등록된\n일정을 삭제해 줘',
'5:0':'무엇을 삭제할 거야?\n','5:1':'일정\n','5:2':'기념일',
'6:0':'어느 날의 일정을 볼 거야?',
'7:0':'무엇을 등록할 거야?\n','7:1':'일정\n','7:2':'기념일',
'8:0':'무엇을 삭제할 거야?\n','8:1':'일정\n','8:2':'기념일',
'10:0':'이건:','10:1':'의\n소지품이야!\n','10:2':'키 아이템 확인',
'25:0':'이런!\n','25:1':',\n같은 시간에 일정이 있어!',
'30:0':'덮어쓰게 되는데,\n괜찮아?\n','30:1':'예  ','30:2':'아니요',
'31:0':'어떤 기념일이야?\n','32:0':'어디에 등록할 거야?\n',
'33:0':'이대로 괜찮아?\n\n','33:1':'예  ','33:2':'아니요',
'40:0':'나에게 서브칩을\n전송할 수\n있어!',
'41:0':'내 장비를\n바꿀 수 있어!',
'42:0':'데이터 라이브러리를\n확인할 수 있어!',
'43:0':'메일을\n확인할 수 있어!',
'44:0':'키 아이템을\n확인할 수\n있어!',
'45:0':'지금까지의 데이터를\n저장할 수 있어!',
'50:5':'」\n일정을 삭제할 거야','50:6':'삭제해도 괜찮아?\n\n','50:7':'예  ','50:8':'아니요',
'51:6':'」\n기념일을 삭제할 거야','51:7':'삭제해도 괜찮아?\n\n','51:8':'예  ','51:9':'아니요',
'52:3':'」\n기념일을 삭제할 거야','52:4':'삭제해도 괜찮아?\n\n','52:5':'예  ','52:6':'아니요',
'60:0':'계산 문제집에\n도전할래?\n','60:1':'예  ','60:2':'아니요',
'61:0':'얼음 편지를\n읽어 볼래?\n','61:1':'예  ','61:2':'아니요',
'63:0':'......\n지금은 안 되나 봐',
}}
CHOICES={(s,i) for s in (5,7,8,30,33,60,61) for i in (1,2)}
CHOICES|={(10,2),(50,7),(50,8),(51,8),(51,9),(52,5),(52,6)}
def create(archive):
    digest,count,out=SOURCES[archive];source=f'analysis/full_scope_v1/source_tpl/{archive}.tpl'
    require_hash(ROOT/source,digest);original=(ROOT/source).read_text(encoding='utf-8-sig')
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'))
    plan=json.loads((ROOT/'translations/full_translation_first_plan.json').read_text(encoding='utf8'))
    require_hash(ROOT/plan['source_inventory']['path'],plan['source_inventory']['sha256'])
    catalog=json.loads((ROOT/plan['source_inventory']['path']).read_text(encoding='utf8'))
    ids={u['id'] for u in catalog['units'] if u['archive']==archive and u['status']=='unselected_japanese'}
    values={archive+':'+k:v for k,v in DRAFT[archive].items()}
    selected=[x for x in literals(original) if x.key in ids]
    if len(selected)!=count or set(values)!=ids:raise ValueError('hint/menu scope '+archive)
    units=[]
    for x in selected:
        s,i=map(int,x.key.split(':')[1:]);t=values[x.key]
        if t.count('\n')!=x.text.count('\n') or t.startswith('\n')!=x.text.startswith('\n') or t.endswith('\n')!=x.text.endswith('\n'):raise ValueError('hint/menu topology '+x.key)
        if re.findall(r'-?\d+|\[[^\]]+\]',t)!=re.findall(r'-?\d+|\[[^\]]+\]',x.text):raise ValueError('hint/menu tokens '+x.key)
        if len(x.text)-len(x.text.rstrip(' '))!=len(t)-len(t.rstrip(' ')):raise ValueError('hint/menu padding '+x.key)
        roll=archive=='65F11C';choice=roll and (s,i) in CHOICES
        units.append(dict(id=x.key,source=x.text,translation=t,state='needs_review',
            speaker='player-choice' if choice else 'Roll' if roll else 'unshown-progress-hint-voice',
            origin_portrait='Roll' if roll else None,portrait_visibility='visible' if choice else 'shown' if roll else 'not-shown-in-script',
            context='Roll calendar/delete/overwrite/menu guidance with explicit portrait; source-selected literals excluded.' if roll else 'Progress-priority hints routed by source10 flags, items and tournament state; source no mugshot.',
            variable_context='Nickname/chip/event buffers retain arguments and ordering. Ownership 의 or quoted name + category avoids dependent particle. Capacity/input persistence and caller still need runtime checks.'))
    src=ROOT/cfg['source_profile']['filename'];require_hash(src,cfg['source_profile']['sha256'])
    require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==int(archive,16))
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION',archive=archive,
        source_sha256=cfg['source_profile']['sha256'],source_tpl=dict(path=source,sha256=digest),
        source_archive_sha256=sha(payload_of(src.read_bytes(),row)),
        consumer='roll-menu-remaining' if archive=='65F11C' else 'quick-progress-hints',
        context=units[0]['context'],voice='Friendly plain source; explicit Roll menu only; no assigned Navi for quick hints; not human approved.',
        review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),
        insertion_state='translation-first draft only; not selected by ROM builder',
        protected_policy='Keep current-ROM selection, source hashes/commands/flags/items/tournament/date branches/variable order, newline/choice padding, portraits and option dimensions. No menu action/save/ROM writes.',
        semantic_review=(
            ['Source10 priority dispatch unchanged, including flags2/8904..8910, navi flags, item1/11, tournament bitmask4; no new progression claim.',
             'Areas3/5/7/9/10/12, chip104 buffer0, minus-key retrieval and delivery internet9 retain destination and numeral meaning.',
             'Defeated Navi suspected culprit, other Navi1 has key: conjecture preserved, not certain attribution. Coffin marker retained without naming criminal.',
             'Weekday0/6 branches34/30 and unread-mail branches9416..9422 to33 unchanged; no inferred current date or weekday consumer verification.',
             'No live progression/hint priority/quest/tournament/mail/portrait/runtime evidence; candidate terminology 내비 vs previous 나비 variants remains review.']
            if archive=='65E8B8' else
            ['Only51 source-unselected entries drafted; previously selected date/register/type/time/confirmation literals remain untouched.',
             'Delete50 schedule and51/52 anniversary categories come from source frequency/year/date buffers and prior register branches; quoted name avoids fixed 을/를. Consumer/persistence still needs runtime.',
             'Overwrite30 is separate from delete50..52 and final confirmation33; no erased or overwritten schedule in this turn.',
             '21 player-choice literals retain visible Roll, two spaces or newline, width7/8 and defaults0/1/BSeparate; actor is explicit not inferred.',
             'Calculation drill drafted 계산 문제집; ice letter 얼음 편지 candidate pending terminology review; cannot-play63 not failure/success.',
             'All wording/layout/input limit and actual date/frequency/AMPM rendering remain needs_review; static checks do not establish runtime or approval.']
        ),units=units)
def main():
    for a,(_,count,out) in SOURCES.items():
        asset=create(a);p=ROOT/out
        if p.exists():
            if json.loads(p.read_text(encoding='utf8'))!=asset:raise ValueError('preserve hint/menu draft '+out)
        else:p.write_text(json.dumps(asset,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        print(f'Authored {a} {count}; ROM unchanged')
if __name__=='__main__':main()
