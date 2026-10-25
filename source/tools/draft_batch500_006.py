"""Batch500-006: manual schedule menus488/tournament12; no ROM/save writes."""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of
SOURCES={
'670568':('8ec6d72cdb194f0bffa4524996d78feb2a36d6cbeec6fe38575aecda6db04fbf',61,'translations/batch500_006_schedule_670568_draft_ko.json'),
'6762A8':('822a6e70353280e87bb1c293255fe995708fa96b5b08006608fb354ef3355779',61,'translations/batch500_006_schedule_6762A8_draft_ko.json'),
'686A60':('1a3da19e23e607982304276c5cdb369d52c472ffdfbf0070cd127558f97de022',61,'translations/batch500_006_schedule_686A60_draft_ko.json'),
'697B70':('b7c6c9a4baa3dee4c94f4496d6b8075b4385cf1cf7e2f41580f79bb4bee28ecf',61,'translations/batch500_006_schedule_697B70_draft_ko.json'),
'6A9970':('1950e0581728babb111900a66427d5f1eec6ece21ad6ec1e99610fb9a0ec40b7',61,'translations/batch500_006_schedule_6A9970_draft_ko.json'),
'6BB2A4':('80947e6113cf090d7aa5193291b6449fdcd7d36c9285ca09d652e3bb63468e19',61,'translations/batch500_006_schedule_6BB2A4_draft_ko.json'),
'6C0E38':('6aedd3a2c149422abc015740278e1dc3255d4cac3322417a0a8268bf5fa05d0d',61,'translations/batch500_006_schedule_6C0E38_draft_ko.json'),
'6CBFC0':('0f179da4118b9f3ff89bd5993767ff1319b9978bd34bef5f840cf046de1d050e',61,'translations/batch500_006_schedule_6CBFC0_draft_ko.json'),
'66C7D8':('9c6d202b93e6b9a655eba65a3a89e62994966c2099f0fa68886e764feda42107',12,'translations/batch500_006_tournament_66C7D8_draft_ko.json'),
}
ACTORS={'670568':'SearchMan','6762A8':'FireMan','686A60':'NumberMan','697B70':'AquaMan','6A9970':'ShadowMan','6BB2A4':'NapalmMan','6C0E38':'IceMan','6CBFC0':'PlantMan'}
TRAINING={'670568':62,'6762A8':62,'686A60':60,'697B70':61,'6A9970':62,'6BB2A4':62,'6C0E38':61,'6CBFC0':60}
# Explicit common fixed-label/choice candidates manually matched to each consumer.
# These are not approved translations or source-string prose replacement rules.
COMMON={
'0:0':'오늘은 ','0:1':'월','10:0':'이것은','10:2':'키 아이템 확인',
'2:1':'일정\n','2:2':'기념일','5:1':'일정\n','5:2':'기념일',
'7:1':'일정\n','7:2':'기념일','8:1':'일정\n','8:2':'기념일',
'24:1':'예  ','24:2':'아니오','30:1':'예  ','30:2':'아니오',
'33:1':'예  ','33:2':'아니오','50:7':'예  ','50:8':'아니오',
'51:8':'예  ','51:9':'아니오','52:5':'예  ','52:6':'아니오'}
CHOICES={'2:1','2:2','5:1','5:2','7:1','7:2','8:1','8:2','10:2','24:1','24:2','30:1','30:2','33:1','33:2','50:7','50:8','51:8','51:9','52:5','52:6'}
DRAFT={
'670568':{
'0:2':'일입니다\n무엇을 할까요?',
'1:0':'어느 날의 일정을\n입력하시겠습니까?',
'2:0':'무엇을 등록하시겠습니까?\n',
'3:0':',\n그날은 이미\n지났습니다',
'4:0':'더 이상\n등록할 수 없습니다...',
'4:1':'새로 등록하시려면,\n이미 등록된\n일정을 삭제해 주십시오',
'5:0':'무엇을 삭제하시겠습니까?\n',
'6:0':'어느 날의 일정을\n보시겠습니까?',
'7:0':'무엇을 등록하시겠습니까?\n','8:0':'무엇을 삭제하시겠습니까?\n',
'10:1':' 님의\n소지품입니다\n',
'20:0':'몇 시부터 시작합니까?','21:0':'어느 종류입니까?','22:0':'어떤 내용입니까?','23:0':'누구와의 약속입니까?',
'24:0':'이대로 괜찮습니까?\n\n',
'25:0':',\n같은 시간에\n일정이 등록돼 있습니다',
'30:0':'덮어쓰게 됩니다만,\n괜찮습니까?\n',
'31:0':'어떤 기념일입니까?\n','32:0':'어디에 등록할까요?\n','33:0':'이대로 괜찮습니까?\n\n',
'40:0':'제게 서브칩을\n전송할 수\n있습니다...',
'41:0':'제 장비를\n변경할 수 있습니다',
'42:0':'데이터 라이브러리를\n확인할 수 있습니다',
'43:0':'메일을 확인할 수\n있습니다',
'44:0':'키 아이템을\n확인할 수\n있습니다',
'45:0':'지금까지의 데이터를\n저장할 수 있습니다',
'50:5':'」\n일정을 삭제합니다','50:6':'괜찮습니까?\n\n',
'51:6':'」\n기념일을 삭제합니다','51:7':'괜찮습니까?\n\n',
'52:3':'」\n기념일을 삭제합니다','52:4':'괜찮습니까?\n\n',
'62:0':'저격 훈련에\n도전하시겠습니까?\n','63:0':'......\n지금은 할 수 없는 모양입니다'},
'6762A8':{
'0:2':'일이야\n뭘 할 거야?',
'1:0':'어느 날의 일정을\n입력할 거야?',
'2:0':'뭘 등록할 거야?\n','3:0':'이봐 이봐,\n그날은 이미 지났다고?',
'4:0':'더 이상 등록할 수 없어',
'4:1':'새로 등록하려면,\n이미 등록된\n일정을 삭제해 줘',
'5:0':'뭘 삭제할 거야?\n','6:0':'어느 날의 일정을 볼 거야?',
'7:0':'뭘 등록할 거야?\n','8:0':'뭘 삭제할 거야?\n',
'10:1':'의\n소지품이야...\n',
'20:0':'몇 시부터 시작해?','21:0':'어느 종류야?','22:0':'어떤 내용이야?','23:0':'누구와의 약속이야?',
'24:0':'이대로 하면 되지?\n\n',
'25:0':',\n같은 시간에\n다른 일정이 있어',
'30:0':'덮어쓰게 되는데,\n괜찮은 거야?\n',
'31:0':'어떤 기념일이야?\n','32:0':'어디에 등록할 거야?\n','33:0':'이대로 하면 되지?\n\n',
'40:0':'나한테 서브칩을\n전송할 수\n있어!',
'41:0':'내 장비를\n변경할 수 있어!',
'42:0':'데이터 라이브러리를\n확인할 수 있어!',
'43:0':'메일을 확인할 수\n있어!',
'44:0':'키 아이템을\n확인할 수\n있어!',
'45:0':'지금까지의 데이터를\n저장할 수 있어!',
'50:5':'」\n일정을 삭제할게','50:6':'괜찮지?\n\n',
'51:6':'」\n기념일을 삭제할게','51:7':'괜찮지?\n\n',
'52:3':'」\n기념일을 삭제할게','52:4':'괜찮지?\n\n',
'62:0':'저격 훈련에\n도전할 거야?\n','63:0':'......\n지금은 무리인 모양이군'},
'686A60':{
'0:2':'일이에요\n자, 뭘 할까요?',
'1:0':'어느 날의 일정을\n입력할까요?',
'2:0':'뭘 등록할까요?\n','3:0':'이런, 그날은 이미\n지나 버렸다고요?',
'4:0':'더 이상\n등록할 수 없어요',
'4:1':'새로 등록하려면,\n이미 등록된\n일정을 삭제해 주세요',
'5:0':'뭘 삭제할까요?\n','6:0':'어느 날의 일정을 볼까요?',
'7:0':'뭘 등록할까요?\n','8:0':'뭘 삭제할까요?\n',
'10:1':'의\n소지품이에요\n',
'20:0':'몇 시부터 시작하나요?','21:0':'어느 종류인가요?','22:0':'어떤 내용인가요?','23:0':'누구와의 약속인가요?',
'24:0':'이대로 괜찮나요?\n\n',
'25:0':',\n같은 시간에\n다른 일정이 있어요',
'30:0':'덮어쓰게 되는데,\n괜찮나요?\n',
'31:0':'어떤 기념일인가요?\n','32:0':'어디에 등록할까요?\n','33:0':'이대로 OK인가요?\n\n',
'40:0':'제게 서브칩을\n전송할 수\n있어요',
'41:0':'제 장비를\n변경할 수 있어요',
'42:0':'데이터 라이브러리를\n확인할 수 있어요',
'43:0':'메일을 확인할 수\n있어요',
'44:0':'키 아이템을\n확인할 수\n있어요',
'45:0':'지금까지의 데이터를\n저장할 수 있어요',
'50:5':'」\n일정을 삭제할게요','50:6':'괜찮나요?\n\n',
'51:6':'」\n기념일을 삭제할게요','51:7':'괜찮나요?\n\n',
'52:3':'」\n기념일을 삭제할게요','52:4':'괜찮나요?\n\n',
'60:0':'계산 문제에\n도전할까요?\n','63:0':'죄송하지만,\n지금은 할 수 없어요...'},
'697B70':{
'0:2':'일이야, 퓨\n뭘 할 거야, 퓨?',
'1:0':'어느 날의 일정을\n입력할 거야, 퓨?',
'2:0':'뭘 등록할 거야, 퓨?\n','3:0':'그날은 이미\n지나 버렸어, 퓨!',
'4:0':'더 이상\n등록할 수 없어, 퓨',
'4:1':'새로 등록하려면,\n이미 등록된\n일정을 삭제해, 퓨',
'5:0':'뭘 삭제할 거야, 퓨?\n',
'6:0':'어느 날의 일정을\n볼 거야, 퓨?',
'7:0':'뭘 등록할 거야, 퓨?\n','8:0':'뭘 삭제할 거야, 퓨?\n',
'10:1':'의\n소지품이야, 퓨!\n',
'20:0':'몇 시부터야, 퓨?','21:0':'어느 종류야, 퓨?','22:0':'어떤 내용이야, 퓨?','23:0':'누구와의 약속이야, 퓨?',
'24:0':'이대로 OK야, 퓨?\n\n',
'25:0':',\n같은 시간에 일정이 있어!',
'30:0':'덮어쓸 거야, 퓨!\n괜찮아, 퓨?\n',
'31:0':'어떤 기념일이야, 퓨?\n','32:0':'어디에 등록할 거야, 퓨?\n','33:0':'이대로 OK야, 퓨?\n\n',
'40:0':'나한테 서브칩을\n전송할 수\n있어, 퓨!',
'41:0':'내 장비를\n변경할 수 있어, 퓨!',
'42:0':'데이터 라이브러리를\n확인할 수 있어, 퓨!',
'43:0':'메일을 확인할 수\n있어, 퓨!',
'44:0':'키 아이템을\n확인할 수\n있어, 퓨!',
'45:0':'지금까지의 데이터를\n저장할 수 있어, 퓨!',
'50:5':'」\n일정을 삭제할 거야, 퓨','50:6':'괜찮아, 퓨?\n\n',
'51:6':'」\n기념일을 삭제할 거야, 퓨','51:7':'괜찮아, 퓨?\n\n',
'52:3':'」\n기념일을 삭제할 거야, 퓨','52:4':'괜찮아, 퓨?\n\n',
'61:0':'얼음 편지를\n읽어 볼 거야, 퓨?\n','63:0':'지금은 할 수 없어, 퓨우'},
'6A9970':{
'0:2':'일이다\n무엇을 하겠느냐...',
'1:0':'어느 날의 일정을\n입력하겠느냐?',
'2:0':'무엇을 등록하겠느냐?\n','3:0':'그날은 이미 지났다...',
'4:0':'더 이상\n등록할 수 없다...',
'4:1':'새로 등록하려면,\n이미 등록된\n일정을 삭제해라',
'5:0':'무엇을 삭제하겠느냐?\n','6:0':'어느 날의 일정을 보겠느냐?',
'7:0':'무엇을 등록하겠느냐?\n','8:0':'무엇을 삭제하겠느냐?\n',
'10:1':'의\n소지품이다\n',
'20:0':'몇 시부터 시작하느냐?','21:0':'어느 종류냐?','22:0':'어떤 내용이냐?','23:0':'누구와의 약속이냐?',
'24:0':'이대로 하면 되겠느냐?\n\n',
'25:0':',\n같은 시간에 일정이 있다',
'30:0':'덮어쓰게 된다만,\n...괜찮겠느냐?\n',
'31:0':'어떤 기념일이냐?\n','32:0':'어디에 등록하겠느냐?\n','33:0':'이대로 하면 되겠느냐?\n\n',
'40:0':'소인에게 서브칩을\n전송할 수\n있다',
'41:0':'소인의 장비를\n변경할 수 있다',
'42:0':'데이터 라이브러리를\n확인할 수 있다',
'43:0':'메일을 확인할 수\n있다',
'44:0':'키 아이템을\n확인할 수\n있다',
'45:0':'지금까지의 데이터를\n기록할 수 있다',
'50:5':'」\n일정을 삭제하겠다...','50:6':'괜찮겠느냐?\n\n',
'51:6':'」\n기념일을 삭제하겠다...','51:7':'괜찮겠느냐?\n\n',
'52:3':'」\n기념일을 삭제하겠다...','52:4':'괜찮겠느냐?\n\n',
'62:0':'저격 훈련에\n도전하겠느냐?\n','63:0':'지금은 할 수 없는 모양이다...'},
'6BB2A4':{
'0:2':'일이다\n뭘 할 거야?',
'1:0':'어느 날의 일정을\n입력할 거야!?',
'2:0':'뭘 등록할 거야!?\n','3:0':'무슨 소리야?\n그날은 이미 지났잖아!?',
'4:0':'더 이상\n등록할 수 없어!',
'4:1':'새로 등록하려면,\n이미 등록된\n일정을 삭제해 줘',
'5:0':'뭘 삭제할 거야!?\n','6:0':'어느 날의 일정을 볼 거야!?',
'7:0':'뭘 등록할 거야!?\n','8:0':'뭘 삭제할 거야!?\n',
'10:1':'의\n소지품이다!\n',
'20:0':'몇 시부터 시작해!?','21:0':'어느 종류야?','22:0':'어떤 내용이야!?','23:0':'누구와의 약속이야!?',
'24:0':'이대로 하면 되지!?\n\n',
'25:0':',\n같은 시간에\n다른 일정이 있는데?',
'30:0':'덮어쓰게 되는데,\n괜찮은 거지!?\n',
'31:0':'어떤 기념일이야!?\n','32:0':'어디에 등록할 거야!?\n','33:0':'이대로 하면 되지!?\n\n',
'40:0':'나한테 서브칩을\n전송할 수\n있어!',
'41:0':'내 장비를\n변경할 수 있어!',
'42:0':'데이터 라이브러리를\n확인할 수 있어!',
'43:0':'메일을 확인할 수\n있어!',
'44:0':'키 아이템을\n확인할 수\n있어!',
'45:0':'지금까지의 데이터를\n저장할 수 있어!',
'50:5':'」\n일정을 삭제할게!','50:6':'괜찮지!?\n\n',
'51:6':'」\n기념일을 삭제할게!','51:7':'괜찮지!?\n\n',
'52:3':'」\n기념일을 삭제할게!','52:4':'괜찮지!?\n\n',
'62:0':'저격 훈련에\n도전할까?\n','63:0':'......\n지금은 무리인 모양이군'},
'6C0E38':{
'0:2':'일이에요\n뭘 할 거예요?',
'1:0':'어느 날의 일정을\n입력할 거예요?',
'2:0':'뭘 등록할 거예요?\n','3:0':'그날은 이미\n지나 버렸어요!',
'4:0':'더 이상\n등록할 수 없어요!',
'4:1':'새로 등록하려면,\n이미 등록된\n일정을 삭제할 거예요',
'5:0':'뭘 삭제할 거예요?\n','6:0':'어느 날의 일정을 볼 거예요?',
'7:0':'뭘 등록할까요?\n','8:0':'뭘 삭제할 거예요?\n',
'10:1':'의\n소지품이에요\n',
'20:0':'몇 시부터인가요?','21:0':'어느 종류인가요?','22:0':'어떤 내용인가요?','23:0':'누구와의 약속인가요?',
'24:0':'이대로 괜찮나요?\n\n',
'25:0':',\n같은 시간에\n다른 일정이 있어요',
'30:0':'덮어쓸 거예요,\n문제없나요?\n',
'31:0':'어떤 기념일인가요?\n','32:0':'어디에 등록할 거예요?\n','33:0':'이대로 괜찮나요?\n\n',
'40:0':'저한테 서브칩을\n전송할 수\n있어요!',
'41:0':'제 장비를\n변경할 수 있어요!',
'42:0':'데이터 라이브러리를\n확인할 수 있어요!',
'43:0':'메일을 확인할 수\n있어요!',
'44:0':'키 아이템을\n확인할 수\n있어요!',
'45:0':'지금까지의 데이터를\n저장할 수 있어요!',
'50:5':'」\n일정을 삭제할 거예요','50:6':'괜찮나요?\n\n',
'51:6':'」\n기념일을 삭제할 거예요','51:7':'괜찮나요?\n\n',
'52:3':'」\n기념일을 삭제할 거예요','52:4':'괜찮나요?\n\n',
'61:0':'얼음 편지를\n읽어 볼 거예요?\n','63:0':'지금은 할 수 없는 것 같아요...'},
'6CBFC0':{
'0:2':'일이야\n무엇을 할까?',
'1:0':'어느 날의 일정을\n입력할 거니?',
'2:0':'무엇을 등록할 거니?\n','3:0':'그날은 이미\n지나 버렸단다',
'4:0':'더 이상 등록할 수 없단다',
'4:1':'새로 등록하려면,\n이미 등록된\n일정을 삭제해 주겠니',
'5:0':'무엇을 삭제할 거니?\n','6:0':'어느 날의 일정을 볼까?',
'7:0':'무엇을 등록할 거니?\n','8:0':'무엇을 삭제할 거니?\n',
'10:1':'의\n소지품이란다\n',
'20:0':'몇 시부터 시작하니?','21:0':'어느 종류니?','22:0':'어떤 내용이니?','23:0':'누구와의 약속이니?',
'24:0':'이대로 괜찮니?\n\n',
'25:0':',\n같은 시간에\n다른 일정이 있네',
'30:0':'덮어쓰게 되는데,\n괜찮겠니?\n',
'31:0':'어떤 기념일이니?\n','32:0':'어디에 등록할까?\n','33:0':'이대로 괜찮은 거니?\n\n',
'40:0':'내게 서브칩을\n전송할 수\n있단다',
'41:0':'내 장비를\n변경할 수 있단다',
'42:0':'데이터 라이브러리를\n확인할 수 있단다',
'43:0':'메일을 확인할 수\n있단다',
'44:0':'키 아이템을\n확인할 수\n있단다',
'45:0':'지금까지의 데이터를\n저장할 수 있단다',
'50:5':'」\n일정을 삭제할게','50:6':'괜찮겠니?\n\n',
'51:6':'」\n기념일을 삭제할게','51:7':'괜찮겠니?\n\n',
'52:3':'」\n기념일을 삭제할게','52:4':'괜찮겠니?\n\n',
'60:0':'계산 문제에\n도전하겠니?\n','63:0':'아쉽지만,\n지금은 무리인 모양이네'},
'66C7D8':{
'1:0':'강력한\n맞바람을\n맞아 버렸군...',
'1:1':'하지만, 언젠가\n바람의 방향도 바뀌겠지',
'2:0':'순풍을 탔군...\n멋진 승리였다',
'10:0':',\n참가 신청을 안 했구나',
'20:0':'가자,','20:1':'\n바람의 방향이 좋다!',
'21:0':'가자,','21:1':'\n바람의 방향이 좋다!',
'22:0':'가자,','22:1':'\n바람의 방향이 좋다!',
'23:0':'가자,','23:1':'\n바람의 방향이 좋다!'}
}
CONTEXT={a:'Schedule0..8/10/20..33,menu40..45,deletion50..52,training60/61/62 and unavailable63. Full670568 and all per-archive literals/control differences inspected; explicit mugshotShow actor.' for a in ACTORS}
CONTEXT['66C7D8']='Complete TPL inspected: defeat1/victory2/unregistered10/cancel and tournament20..23 encouragement; no portrait.'
def authored(archive):
    if archive not in ACTORS:return DRAFT[archive]
    training=TRAINING[archive]
    return {**COMMON,**DRAFT[archive],f'{training}:1':'예  ',f'{training}:2':'아니오'}
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
        choice=portrait and (suffix in CHOICES or suffix in {f'{TRAINING[archive]}:1',f'{TRAINING[archive]}:2'})
        units.append(dict(id=x.key,source=x.text,translation=t,state='needs_review',
            speaker='player-choice' if choice else (portrait or 'unshown-quick-voice'),
            origin_portrait=portrait,portrait_visibility='shown' if portrait else 'not-shown-in-script',
            context=CONTEXT[archive],variable_context='Date/time/AMPM/frequency/day name/event name/nickname inserts intact. 의 or 님의 possessive invariant; deletion names followed by 일정/기념일 avoids variable particle mismatch. Runtime unverified.'))
    src=ROOT/cfg['source_profile']['filename'];require_hash(src,cfg['source_profile']['sha256'])
    require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==int(archive,16))
    notes=['Batch500-006 exactly500 stable literals: schedule menus488/tournament12; not500 unique sentences.',
        'Source-conditioned manually authored candidates; every source literal/control difference inspected. Full670568/66C7D8 read. No prose rule replacement, ROM/save writes, runtime approval or distribution eligibility.']
    if portrait:
        notes+=['Each menu61 has23 player choices/38 prose including date fragments. Explicit mugshotShow governs actor; no NumberMan screenshot substitution.',
            'Registration2/7 vs deletion5/8, dates past3,capacity4,collision25,overwrite30,anniversary31/32/33,deletion50/51/52,subchip40/equipment41/library42/mail43/key44/save45 retained.',
            'Training60 calculation drill/61 ice letter/62 sniper training matched to actual source, including FireMan and NapalmMan sniper prompts; no actor-based correction.',
            'Buffer1 minLength2,padZeros,padLeft,AMPM/frequency/year/month/day/dayname and schedule name; width7/8,defaults0/1,BSeparate true/false,clear false/true,flag3611/track467/wait1 and hide/close/end remain original.',
            '50 event deletion vs51 dated anniversary vs52 annual anniversary wording candidates use explicit type nouns to avoid name-dependent Korean particles. Untranslated separators/quotes/spaces preserved.',
            'AquaMan source25 lacksぴゅ; no 퓨 added there. SearchMan polite,fire direct,number polite casual,Aqua 퓨,Shadow 소인/기록,napalm emphatic,ice soft,plant gentle are unapproved register candidates.']
    else:
        notes+=['Defeat headwind vs future wind change, victory tailwind, unregistered/cancel and four distinct encouragement script IDs retained. Nickname insertion and flag3603 not changed; no named speaker guessed.']
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION',archive=archive,
        source_sha256=cfg['source_profile']['sha256'],source_tpl=dict(path=source,sha256=digest),
        source_archive_sha256=sha(payload_of(src.read_bytes(),row)),consumer='batch500-schedule-menu-tournament',
        context=CONTEXT[archive],voice='Source-conditioned manual draft; explicit menu portraits only; not human approved.',
        review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),
        insertion_state='translation-first draft only; not selected by ROM builder',
        protected_policy='Source IDs/text/TPL/payload, commands, variables,newline/padding and unselected source immutable; no ROM/save writes.',
        batch_id='batch500-006',semantic_review=notes,units=units)
def main():
    if sum(v[1] for v in SOURCES.values())!=500:raise ValueError('500 batch size')
    for a,(_,count,out) in SOURCES.items():
        asset=create(a);p=ROOT/out
        if p.exists():
            if json.loads(p.read_text(encoding='utf8'))!=asset:raise ValueError('preserve batch asset '+out)
        else:p.write_text(json.dumps(asset,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        print(f'Authored {a} {count}; ROM unchanged')
if __name__=='__main__':main()
