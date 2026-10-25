"""Batch500-007: manually authored schedule477/mail14/Aqua greeting9; no ROM writes."""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of
from draft_batch500_006 import COMMON,CHOICES
SOURCES={
'67BCF4':('f9181b169226a06312e74f1f9304ac65d5f8f7cd58dfff726a0ed457a4083618',57,'translations/batch500_007_schedule_67BCF4_draft_ko.json'),
'68CBFC':('647032d8a3d47f5c34c00ac17020d438c7383cfa77c3f3e9c0f63b9564f699b9',57,'translations/batch500_007_schedule_68CBFC_draft_ko.json'),
'692874':('509fbfc6904a767c3e0d97956371763e7ad1fa064ee270133c98b043409bbce4',57,'translations/batch500_007_schedule_692874_draft_ko.json'),
'69D8D4':('a0d0716da4282a903657ecd91a059923851b842dae9efaaff63fd49ab30e1c8d',57,'translations/batch500_007_schedule_69D8D4_draft_ko.json'),
'6B525C':('d1a3f461ce625915cd4e8878d82ffb0a48a62a89003b93cafb53d99961a04147',57,'translations/batch500_007_schedule_6B525C_draft_ko.json'),
'6811F0':('6745443096ccb01da34cdcd5827c048e17294d0913c2193689fcfe7ac3ab05f6',64,'translations/batch500_007_schedule_6811F0_draft_ko.json'),
'6A2FBC':('6465a56fce26782c78d5411a29896e7246a5a9fbd09eecb1b0c00406fe60eb2d',64,'translations/batch500_007_schedule_6A2FBC_draft_ko.json'),
'6C6828':('65b693b7a10224f0aaac51a17fe56285f6438350ffb5bc3b1532f6ba77d4aad3',64,'translations/batch500_007_schedule_6C6828_draft_ko.json'),
'6C2660':('36121b42f7699e25975be5bbcd7d3d5c0a47ad7359491d8bb53b7c49cec58d65',14,'translations/batch500_007_mail_6C2660_draft_ko.json'),
'698424':('258e433337e34d34d49c132a4ed282ac73b0844c2c702ed64de4d85350dac4aa',9,'translations/batch500_007_greeting_698424_draft_ko.json'),
}
ACTORS={'67BCF4':'ThunderMan','68CBFC':'MetalMan','692874':'JunkMan','69D8D4':'WoodMan','6B525C':'KnightMan','6811F0':'ProtoMan','6A2FBC':'StarMan','6C6828':'ElecMan'}
TRAINING={'6811F0':(60,61),'6A2FBC':(60,61),'6C6828':(60,62)}
# All prose below is authored per stable source ID, not source-string rules.
DRAFT={
'67BCF4':{
'0:2':'일이다\n무엇을 할 건가...',
'1:0':'어느 날의 일정을\n입력할 건가?',
'2:0':'무엇을 등록할 건가?\n','3:0':'그날은 이미 지났네...',
'4:0':'더 이상\n등록할 수 없네...',
'4:1':'새로 등록하려면,\n이미 등록된\n일정을 삭제해 주게',
'5:0':'무엇을 삭제할 건가?\n','6:0':'어느 날의 일정을 볼 건가?',
'7:0':'무엇을 등록할 건가?\n','8:0':'무엇을 삭제할 건가?\n',
'10:1':'의\n소지품이다...\n',
'20:0':'몇 시부터 시작하나?','21:0':'어느 종류인가?','22:0':'어떤 내용인가?','23:0':'누구와의 약속인가?',
'24:0':'이대로 하면 되겠나?\n\n',
'25:0':',\n같은 시간에 일정이 있네',
'30:0':'덮어쓰게 되는데,\n괜찮겠나?\n',
'31:0':'어떤 기념일인가?\n','32:0':'어디에 등록할 건가?\n','33:0':'이대로 하면 되겠나?\n\n',
'40:0':'내게 서브칩을\n전송할 수\n있네...',
'41:0':'내 장비를\n변경할 수 있네...',
'42:0':'데이터 라이브러리를\n확인할 수 있네...',
'43:0':'메일을 확인할 수\n있네',
'44:0':'키 아이템을\n확인할 수\n있네...',
'45:0':'지금까지의 데이터를\n저장할 수 있네...',
'50:5':'」\n일정을 삭제하겠네...','50:6':'괜찮겠나?\n\n',
'51:6':'」\n기념일을 삭제하겠네...','51:7':'괜찮겠나?\n\n',
'52:3':'」\n기념일을 삭제하겠네...','52:4':'괜찮겠나?\n\n'},
'68CBFC':{
'0:2':'일이다\n뭘 할 거냐...',
'1:0':'어느 날의 일정을\n입력할 거냐?',
'2:0':'뭘 등록할 거냐?\n','3:0':'그날은 이미 지났다...',
'4:0':'더 이상\n등록할 수 없다...',
'4:1':'새로 등록하려면,\n이미 등록된\n일정을 삭제해 줘',
'5:0':'뭘 삭제할 거냐?\n','6:0':'어느 날의 일정을 볼 거냐?',
'7:0':'뭘 등록할 거냐?\n','8:0':'뭘 삭제할 거냐?\n',
'10:1':'의\n소지품이다...\n',
'20:0':'몇 시부터 시작하냐?','21:0':'어느 종류냐?','22:0':'어떤 내용이냐?','23:0':'누구와의 약속이냐?',
'24:0':'이대로 하면 되겠지?\n\n',
'25:0':',\n같은 시간에 일정이 있다',
'30:0':'덮어쓰게 되는데,\n괜찮겠지?\n',
'31:0':'어떤 기념일이냐?\n','32:0':'어디에 등록할 거냐?\n','33:0':'이대로 하면 되겠지?\n\n',
'40:0':'나한테 서브칩을\n전송할 수\n있다...',
'41:0':'내 장비를\n변경할 수 있다...',
'42:0':'데이터 라이브러리를\n확인할 수 있다...',
'43:0':'메일을 확인할 수\n있다',
'44:0':'키 아이템을\n확인할 수\n있다...',
'45:0':'지금까지의 데이터를\n저장할 수 있다...',
'50:5':'」\n일정을 삭제하겠다','50:6':'괜찮겠지?\n\n',
'51:6':'」\n기념일을 삭제하겠다','51:7':'괜찮겠지?\n\n',
'52:3':'」\n기념일을 삭제하겠다','52:4':'괜찮겠지?\n\n'},
'692874':{
'0:0':'오늘은,\n','0:1':'월','0:2':'일이다\n뭐, 뭘 할 거냐?',
'1:0':'어느 날의 일정을\n입력할 거냐?',
'2:0':'뭘 등록할 거냐?\n','3:0':'그, 그날은,\n이미 지났다...',
'4:0':'더, 더 이상\n등록할 수 없다...',
'4:1':'새로 등록하려면,\n이미 등록된\n일정을 삭제해 줘',
'5:0':'뭘 삭제할 거냐?\n','6:0':'어느 날의 일정을\n볼 거냐?',
'7:0':'뭘 등록할 거냐?\n','8:0':'뭘 삭제할 거냐?\n',
'10:1':'의\n소지품이다...\n',
'20:0':'며, 몇 시부터냐?','21:0':'어느 종류냐?','22:0':'어, 어떤 내용이냐?','23:0':'누구와의 약속이냐?',
'24:0':'이대로 해도 되냐?\n\n',
'25:0':',\n같은 시간에\n다른 일정이 있다...',
'30:0':'덮어쓰게 되는데,\n괜찮냐?\n',
'31:0':'어, 어떤 기념일이냐?\n','32:0':'어디에 등록할 거냐?\n','33:0':'이대로 해도 되냐?\n\n',
'40:0':'나한테 서브칩을\n전송할 수\n있다',
'41:0':'내 장비를\n변경할 수 있다',
'42:0':'데이터 라이브러리를\n확인할 수 있다',
'43:0':'메일을 확인할 수\n있다',
'44:0':'키 아이템을\n확인할 수\n있다...',
'45:0':'지금까지의 데이터를\n저장할 수 있다',
'50:5':'」\n일정을 삭제하겠다','50:6':'괜찮냐?\n\n',
'51:6':'」\n기념일을 삭제하겠다','51:7':'괜찮냐?\n\n',
'52:3':'」\n기념일을 삭제하겠다','52:4':'괜찮냐?\n\n'},
'69D8D4':{
'0:2':'일이다\n무엇을 할까?',
'1:0':'어느 날의 일정을\n입력할까?',
'2:0':'무엇을 등록할까?\n','3:0':'그날은 이미 지났다',
'4:0':'더 이상\n등록할 수 없겠군...',
'4:1':'새로 등록하려면,\n이미 등록된\n일정을 삭제해 줘',
'5:0':'무엇을 삭제할까?\n','6:0':'어느 날의 일정을 볼까?',
'7:0':'무엇을 등록할까?\n','8:0':'무엇을 삭제할까?\n',
'10:1':'의\n소지품이다\n',
'20:0':'몇 시부터 시작하나?','21:0':'어느 종류인가?','22:0':'어떤 내용인가?','23:0':'누구와의 약속인가?',
'24:0':'이대로 하면 되겠지?\n\n',
'25:0':',\n같은 시간에 일정이 있다',
'30:0':'덮어쓰게 되는데,\n괜찮겠지?\n',
'31:0':'어떤 기념일인가?\n','32:0':'어디에 등록할까?\n','33:0':'이대로 하면 되겠지?\n\n',
'40:0':'내게 서브칩을\n전송할 수\n있다',
'41:0':'내 장비를\n변경할 수 있다',
'42:0':'데이터 라이브러리를\n확인할 수 있다',
'43:0':'메일을 확인할 수\n있다',
'44:0':'키 아이템을\n확인할 수\n있다',
'45:0':'지금까지의 데이터를\n저장할 수 있다',
'50:5':'」\n일정을 삭제하겠다','50:6':'괜찮겠지?\n\n',
'51:6':'」\n기념일을 삭제하겠다','51:7':'괜찮겠지?\n\n',
'52:3':'」\n기념일을 삭제하겠다','52:4':'괜찮겠지?\n\n'},
'6B525C':{
'0:2':'일입니다\n무엇을 하시겠소!?',
'1:0':'어느 날의 일정을\n입력하시겠소?',
'2:0':'무엇을 등록하시겠소?\n','3:0':'안타깝지만,\n그날은 이미\n지났소...',
'4:0':'더 이상\n등록할 수 없소',
'4:1':'새로 등록하시려면,\n이미 등록된\n일정을 삭제해 주시오',
'5:0':'무엇을 삭제하시겠소?\n','6:0':'어느 날의 일정을\n보시겠소?',
'7:0':'무엇을 등록하시겠소?\n','8:0':'무엇을 삭제하시겠소?\n',
'10:1':'의\n소지품입니다\n',
'20:0':'몇 시부터 시작하시오?','21:0':'어느 종류요?','22:0':'어떤 내용이오?','23:0':'어느 분과의\n약속이오?',
'24:0':'이대로 하면 되겠소?\n\n',
'25:0':',\n같은 시간에\n다른 일정이 있소',
'30:0':'덮어쓰게 됩니다만,\n괜찮겠소?\n',
'31:0':'어떤 기념일이오?\n','32:0':'어디에 등록하시겠소?\n','33:0':'이대로 하면 되겠소?\n\n',
'40:0':'제게 서브칩을\n전송할 수\n있소',
'41:0':'제 장비를\n변경할 수 있소',
'42:0':'데이터 라이브러리를\n확인할 수 있소',
'43:0':'메일을 확인할 수\n있소',
'44:0':'키 아이템을\n확인할 수\n있소',
'45:0':'지금까지의 데이터를\n저장할 수 있소',
'50:5':'」\n일정을 삭제하겠소...','50:6':'괜찮겠소?\n\n',
'51:6':'」\n기념일을 삭제하겠소...','51:7':'괜찮겠소?\n\n',
'52:3':'」\n기념일을 삭제하겠소...','52:4':'괜찮겠소?\n\n'},
'6811F0':{
'0:2':'일입니다\n무엇을 할까요?',
'1:0':'어느 날의 일정을\n입력하시겠습니까?',
'2:0':'무엇을 등록하시겠습니까?\n','3:0':',\n그날은 이미\n지났습니다',
'4:0':'더 이상\n등록할 수 없습니다...',
'4:1':'새로 등록하시려면,\n이미 등록된\n일정을 삭제해 주십시오',
'5:0':'무엇을 삭제하시겠습니까?\n','6:0':'어느 날의 일정을\n보시겠습니까?',
'7:0':'무엇을 등록하시겠습니까?\n','8:0':'무엇을 삭제하시겠습니까?\n',
'10:1':'의\n소지품입니다\n',
'20:0':'몇 시부터 시작합니까?','21:0':'어느 종류입니까?','22:0':'어떤 내용입니까?','23:0':'누구와의 약속입니까?',
'24:0':'이대로 괜찮습니까?\n\n',
'25:0':',\n같은 시간에\n일정이 등록돼 있습니다',
'30:0':'덮어쓰게 됩니다만,\n괜찮습니까?\n',
'31:0':'어떤 기념일입니까?\n','32:0':'어디에 등록할까요?\n','33:0':'이대로 괜찮습니까?\n\n',
'40:0':'제게 서브칩을\n전송할 수\n있습니다',
'41:0':'제 장비를\n변경할 수 있습니다',
'42:0':'데이터 라이브러리를\n확인할 수 있습니다',
'43:0':'메일을 확인할 수\n있습니다',
'44:0':'키 아이템을\n확인할 수\n있습니다',
'45:0':'지금까지의 데이터를\n저장할 수 있습니다',
'50:5':'」\n일정을 삭제합니다','50:6':'괜찮습니까?\n\n',
'51:6':'」\n기념일을 삭제합니다','51:7':'괜찮습니까?\n\n',
'52:3':'」\n기념일을 삭제합니다','52:4':'괜찮습니까?\n\n',
'60:0':'계산 문제집에\n도전하시겠습니까?\n',
'61:0':'얼음 편지를\n읽으시겠습니까?\n','63:0':'......\n지금은 할 수 없는 모양입니다'},
'6A2FBC':{
'0:2':'일이야\n뭘 할까?',
'1:0':'어느 날의 일정을\n입력할 거야?',
'2:0':'뭘 등록할까?\n','3:0':'그날은 이미 지나 버렸는데?',
'4:0':'더 이상 등록할 수 없어',
'4:1':'새로 등록하려면,\n이미 등록된\n일정을 삭제해 줘',
'5:0':'뭘 삭제할 거야?\n','6:0':'어느 날의 일정을 볼까?',
'7:0':'뭘 등록할까?\n','8:0':'뭘 삭제할 거야?\n',
'10:1':'의\n소지품이야\n',
'20:0':'몇 시부터 시작해?','21:0':'어느 종류야?','22:0':'어떤 내용이야?','23:0':'누구와의 약속이야?',
'24:0':'이대로 하면 될까?\n\n',
'25:0':',\n같은 시간에 일정이 있어!',
'30:0':'덮어쓰게 되는데,\n괜찮겠어?\n',
'31:0':'어떤 기념일이야?\n','32:0':'어디에 등록할까?\n','33:0':'이대로 OK일까?\n\n',
'40:0':'나한테 서브칩을\n전송할 수\n있어!',
'41:0':'내 장비를\n변경할 수 있어!',
'42:0':'데이터 라이브러리를\n확인할 수 있어!',
'43:0':'메일을 확인할 수\n있어!',
'44:0':'키 아이템을\n확인할 수\n있어!',
'45:0':'지금까지의 데이터를\n저장할 수 있어!',
'50:5':'」\n일정을 삭제할게','50:6':'괜찮겠어?\n\n',
'51:6':'」\n기념일을 삭제할게','51:7':'괜찮겠어?\n\n',
'52:3':'」\n기념일을 삭제할게','52:4':'괜찮겠어?\n\n',
'60:0':'계산 문제집에\n도전할래?\n','61:0':'얼음 편지를\n읽어 볼래?\n','63:0':'지금은 무리인 모양이네'},
'6C6828':{
'0:2':'일이다\n무엇을 할까?',
'1:0':'어느 날의 일정을\n입력할 거냐?',
'2:0':'무엇을 등록할 거냐?\n','3:0':'그날은 이미 지났다',
'4:0':'더 이상\n등록할 수 없겠군...',
'4:1':'새로 등록하려면,\n이미 등록된\n일정을 삭제해 줘',
'5:0':'무엇을 삭제할 거냐?\n','6:0':'어느 날의 일정을 볼 거냐?',
'7:0':'무엇을 등록할 거냐?\n','8:0':'무엇을 삭제할 거냐?\n',
'10:1':'의\n소지품이다\n',
'20:0':'몇 시부터 시작하나?','21:0':'어느 종류인가?','22:0':'어떤 내용인가?','23:0':'누구와의 약속인가?',
'24:0':'이대로 괜찮나?\n\n',
'25:0':',\n같은 시간에 일정이 있다',
'30:0':'덮어쓰게 된다,\n괜찮겠지?\n',
'31:0':'어떤 기념일인가?\n','32:0':'어디에 등록할 거냐?\n','33:0':'이대로 하면 되겠지?\n\n',
'40:0':'내게 서브칩을\n전송할 수\n있다',
'41:0':'내 장비를\n변경할 수 있다',
'42:0':'데이터 라이브러리를\n확인할 수 있다',
'43:0':'메일을 확인할 수\n있다',
'44:0':'키 아이템을\n확인할 수\n있다',
'45:0':'지금까지의 데이터를\n저장할 수 있다',
'50:5':'」\n일정을 삭제하겠다','50:6':'괜찮겠지?\n\n',
'51:6':'」\n기념일을 삭제하겠다','51:7':'괜찮겠지?\n\n',
'52:3':'」\n기념일을 삭제하겠다','52:4':'괜찮겠지?\n\n',
'60:0':'계산 문제집에\n도전할 건가?\n','62:0':'저격 훈련에\n도전할 거냐?\n','63:0':'지금은 할 수 없는 모양이다...'},
'6C2660':{
'1:1':',\n메일이에요!!','2:1':',\n메일이에요!!','3:1':',\n메일이에요!!',
'4:1':'메일이에요!!','5:1':'메일이에요!!','6:1':'메일이에요!!','7:1':'메일이에요!!',
'20:1':'메일이에요!!','21:1':'메일이에요!!','22:1':'메일이에요!!','23:1':'메일이에요!!','24:1':'메일이에요!!','25:1':'메일이에요!!','26:1':'메일이에요!!'},
'698424':{
'1:0':'퓨퓨~!!','1:1':'난 아쿠아맨이야, 퓨\n잘 부탁해, 퓨!!',
'1:2':'친하게 지내 주지 않으면,\n울어 버릴 거야, 퓨!',
'2:0':'퓨, 퓨우우이!!','2:1':'나를,\n기억하고 있었어, 퓨?',
'2:2':'다행이야, 퓨~!','2:3':'퓨퓨 하며\n시끄럽게 구니까,',
'2:4':'버림받은 줄\n알았어, 퓨~~','2:5':'퓨~이, 퓨~이!'}
}
CONTEXT={a:'Schedule0..8/10/20..33,menu40..45,deletion50..52. Complete6811F0 and every archive literal/control difference inspected; explicit mugshotShow actor. Training only where actual scripts exist.' for a in ACTORS}
CONTEXT['6C2660']='Complete TPL inspected: mail1..7/20..26; quick alert no mugshot. Nickname only1..3; callTournamentReceiveMail only2; flag-clear680/681/623..626 and mail-add9056..9062 intact.'
CONTEXT['698424']='Complete TPL inspected: self-introduction1 explicitly names AquaMan without portrait; return2 quick voice has no portrait or explicit name. Same-source 퓨 candidate preserved without inferring portrait or runtime ownership.'
def authored(archive):
    if archive not in ACTORS:return DRAFT[archive]
    values={**COMMON,**DRAFT[archive]}
    for script in TRAINING.get(archive,()):
        values.update({f'{script}:1':'예  ',f'{script}:2':'아니오'})
    return values
def create(archive):
    digest,count,out=SOURCES[archive];source=f'analysis/full_scope_v1/source_tpl/{archive}.tpl'
    require_hash(ROOT/source,digest);original=(ROOT/source).read_text(encoding='utf-8-sig')
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'))
    plan=json.loads((ROOT/'translations/full_translation_first_plan.json').read_text(encoding='utf8'))
    require_hash(ROOT/plan['source_inventory']['path'],plan['source_inventory']['sha256'])
    catalog=json.loads((ROOT/plan['source_inventory']['path']).read_text(encoding='utf8'))
    ids={u['id'] for u in catalog['units'] if u['archive']==archive and u['status']=='unselected_japanese'}
    values={archive+':'+k:v for k,v in authored(archive).items()}
    selected=[x for x in literals(original) if x.key in ids]
    if len(selected)!=count or set(values)!=ids:raise ValueError('batch scope '+archive)
    units=[]
    for x in selected:
        suffix=':'.join(x.key.split(':')[1:]);t=values[x.key]
        if t.count('\n')!=x.text.count('\n') or t.startswith('\n')!=x.text.startswith('\n') or t.endswith('\n')!=x.text.endswith('\n'):raise ValueError('batch topology '+x.key)
        if re.findall(r'-?\d+|\[[^\]]+\]',t)!=re.findall(r'-?\d+|\[[^\]]+\]',x.text):raise ValueError('batch tokens '+x.key)
        if len(x.text)-len(x.text.rstrip(' '))!=len(t)-len(t.rstrip(' ')):raise ValueError('batch padding '+x.key)
        portrait=ACTORS.get(archive)
        choice=portrait and (suffix in CHOICES or suffix in {*(f'{s}:{i}' for s in TRAINING.get(archive,()) for i in (1,2))})
        units.append(dict(id=x.key,source=x.text,translation=t,state='needs_review',
            speaker='player-choice' if choice else (portrait or ('AquaMan-self-identified' if archive=='698424' and x.key.split(':')[1]=='1' else 'unshown-quick-voice')),
            origin_portrait=portrait,portrait_visibility='shown' if portrait else 'not-shown-in-script',
            context=CONTEXT[archive],variable_context='Date/time/AMPM/frequency/day name/event name/nickname inserts intact. 의 or 님의 possessive invariant; deletion names followed by 일정/기념일 avoids variable particle mismatch. Runtime unverified.'))
    src=ROOT/cfg['source_profile']['filename'];require_hash(src,cfg['source_profile']['sha256'])
    require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==int(archive,16))
    notes=['Batch500-007 exactly500 stable literals: schedule477/mail14/greeting9; not500 unique sentences.',
        'Manually authored per source ID. Complete6811F0/6C2660/698424 and all other archive literals/control differences inspected. No source-string prose replacement, ROM/save writes, human approval or release eligibility.']
    if portrait:
        notes+=['Five57 menus have21 choices/36 prose; three64 menus have25 choices/39 prose. Explicit mugshotShow actors only; no screenshot substitution.',
            'Registration2/7,deletion5/8,past3,capacity4,collision25,overwrite30,anniversary31/32/33 and event50 vs anniversaries51/52 retained.',
            'Buffers/date/time/AMPM/frequency/nickname/event name and width7/8/defaults0/1/BSeparate/clear/flag3611/track467 remain source controls. No kana/newline/choice normalization.',
            'JunkMan stutters match source0/3/4/20/22/31; no synthetic stutter elsewhere. KnightMan archaic respectful and ThunderMan measured register are unapproved wording candidates.',
            'Only ProtoMan3 prints nickname; other seven script3 omit nickname. All script10 preserve nickname possessive; script25 preserve nickname and original line count.',
            'Actual training: ProtoMan/StarMan60 calculation drill61 ice letter; ElecMan60 calculation drill62 sniper; five57 menus have none. 계산 문제집 matches prior Roll candidate; batch006 계산 문제 variation remains terminology review, not silently rewritten.']
    elif archive=='6C2660':
        notes+=['No portrait or named-speaker assignment.14 separate mail alerts; nickname1..3 retained, !! remains unselected original and mail flags/call/timing/sound/box anchors unchanged.']
    else:
        notes+=['Only script1 explicitly self-identifies AquaMan in speech; script2 remains unshown quick voice. 퓨 is a source-conditioned unapproved vocal candidate, not evidence of portrait.',
            'Greeting and return phrases remain separate IDs, including fear of abandonment after noisy 퓨 sounds. No temporary character switching or emulator writes.']
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION',archive=archive,
        source_sha256=cfg['source_profile']['sha256'],source_tpl=dict(path=source,sha256=digest),
        source_archive_sha256=sha(payload_of(src.read_bytes(),row)),consumer='batch500-schedule-menu-mail-greeting',
        context=CONTEXT[archive],voice='Source-conditioned manual draft; explicit menu portraits only; not human approved.',
        review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),
        insertion_state='translation-first draft only; not selected by ROM builder',
        protected_policy='Source IDs/text/TPL/payload, commands, variables,newline/padding and unselected source immutable; no ROM/save writes.',
        batch_id='batch500-007',semantic_review=notes,units=units)
def main():
    if sum(v[1] for v in SOURCES.values())!=500:raise ValueError('500 batch size')
    for a,(_,count,out) in SOURCES.items():
        asset=create(a);p=ROOT/out
        if p.exists():
            if json.loads(p.read_text(encoding='utf8'))!=asset:raise ValueError('preserve batch asset '+out)
        else:p.write_text(json.dumps(asset,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        print(f'Authored {a} {count}; ROM unchanged')
if __name__=='__main__':main()

