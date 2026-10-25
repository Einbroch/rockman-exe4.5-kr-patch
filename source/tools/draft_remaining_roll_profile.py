"""Manual remaining fortune punctuation, reminder and profile drafts; no ROM writes."""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of
SOURCES={
'65FF3C':('440701a8b13a5bfc2c79eada56ca64bf4d69f2b583ed93710ffaf58faa8e9520',6,'translations/fortune_wait_dots_draft_ko.json'),
'660D90':('7b05716e68897b20f166e4075642b49e04df22fcf2726c14fe2c133d16b755de',11,'translations/roll_reminder_remaining_draft_ko.json'),
'661858':('585bb58ff77997f67df38a3d8eae63dac3e7a481236129d50a1189ea9955c66c',102,'translations/quick_profile_remaining_b_draft_ko.json'),
}
DRAFT={
'65FF3C':{'0:4':'.','0:5':'.','0:6':'.','1:3':'.','1:4':'.','1:5':'.'},
'660D90':{
'1:0':' 시작할\n시간이야!','1:1':'서두르지 않으면\n시작해 버려~!!',
'2:0':'\n약속 시간이야!\n벌써 설레네~!',
'5:0':' 일정\n시간이야!',
'21:0':' 시작할\n시간이야!','21:1':'서두르지 않으면\n시작해 버려~!!',
'22:0':'\n약속 시간이야!\n벌써 설레네~!',
'23:0':'있잖아~!\n밥 먹을 시간이야!',
'24:0':'학원에 갈 시간이야\n빨리 준비하지 않으면\n지각하겠어!',
'25:0':' 일정\n시간이야!',
'26:0':'음, 그리고...',
},
'661858':{
'9:0':'배틀을 하면,\n우정이 깊어지는\n것 같지!',
'9:1':'아, 맞다!!',
'9:2':',\n친하게 지내는 친구를\n알려 줘!',
'9:3':'나도 친구가\n되고 싶어!',
'13:0':'PET 안에 있을 땐\n조금, 할 일이 없어\n심심한 느낌이야...',
'13:1':'나 1명이서도\n즐길 수 있는 취미를\n찾아야겠어...',
'13:2':'조금 참고하고 싶어서\n물어보는 건데,',
'13:3':',\n취미가 뭐야?',
'15:0':'토너먼트 우승은\n우리 내비들의\n꿈이지...!',
'15:1':',\n앞으로 어떤 꿈을\n이루고 싶어?',
'15:2':'나, 정말\n궁금해!!',
'17:0':'사랑의 메일이\n오지 않았을까 하고,\n기대했는데',
'17:1':'안 왔더라~',
'17:2':',\n좋아하는 여자아이의\n이름을 알려 줘!',
'17:3':'이름을\n모르면,',
'17:4':'사랑의 메일이 와도\n바로 알아볼 수 없잖아!',
'19:0':'사랑의 메일이\n오지 않았을까 하고,\n기대했는데',
'19:1':'안 왔더라~',
'19:2':'...있잖아~,',
'19:3':',\n좋아하는 남자아이의\n이름을 알려 줘~',
'19:4':'그야, 역시 내비로서\n알아 둬야\n하지 않겠어?',
'19:5':'이름을\n모르면,',
'19:6':'사랑의 메일이 와도\n바로 알아볼 수 없잖아!',
'21:0':'라이브러리를 전부\n채운 사람은,',
'21:1':'정말 열심히 노력하는\n사람인가 봐~\n존경하게 돼...',
'21:2':',\n존경하는 사람은\n누구야?',
'23:0':'이 사람의 메일은\n별로 받고 싶지 않다\n싶은',
'23:1':',\n불편한 사람을 알려 줘!',
'25:0':'난 넷배틀은\n별로 잘하지\n못해...',
'25:1':'어느 쪽이냐면,\n느긋하게 TV를 보는 게\n더 좋은 것 같아!',
'25:2':',\n좋아하는 TV 프로그램은\n이름이 뭐야?',
'31:0':'토너먼트에서\n우승했을 때,',
'31:1':'뭔가 보상을\n주겠다고 하면,\n뭘 받을 거야?',
'32:0':'네가 다니는\n유치원 이름은\n뭐야?',
'33:0':'네가 다니는\n학교 이름은\n뭐야?',
'34:0':'네가 다니는\n회사 이름은\n뭐야?',
'40:0':'의\n형이나 오빠는,',
'41:0':'그 밖에는?\n\n','41:1':'있어  ','41:2':'없어',
'42:0':'그렇구나...',
'43:0':'의\n남동생은,',
'44:0':'그 밖에는?\n\n','44:1':'있어  ','44:2':'없어',
'45:0':'그렇구나...',
'46:0':'의\n누나나 언니는,',
'47:0':'그 밖에는?\n\n','47:1':'있어  ','47:2':'없어',
'48:0':'그렇구나...',
'49:0':'의\n여동생은,',
'50:0':'그 밖에는?\n\n','50:1':'있어  ','50:2':'없어',
'51:0':'그렇구나...',
'52:0':'의\n친구는,',
'53:0':'그 밖에는?\n\n','53:1':'있어  ','53:2':'없어',
'54:0':'그렇구나...',
'55:0':'의\n취미는,',
'56:0':'그 밖에는?\n\n','56:1':'있어  ','56:2':'없어',
'57:0':'그렇구나...',
'58:0':'의\n좋아하는 TV 프로그램은,',
'59:0':'그 밖에는?\n\n','59:1':'있어  ','59:2':'없어',
'60:0':'그렇구나...',
'61:0':'의\n갖고 싶은 것은,',
'62:0':'그 밖에는?\n\n','62:1':'있어  ','62:2':'없어',
'63:0':'그렇구나...',
'80:0':'인터넷이 얼마나\n재밌는지,\n알려 줘!',
'80:1':'그런데...\n형이나 오빠는,\n멋있어?',
'80:2':'농담이야! 후훗!',
'81:0':'남동생과는 싸우기도\n하겠지만,',
'81:1':'인터넷이 얼마나\n재밌는지,\n알려 줘!',
'82:0':'인터넷이 얼마나\n재밌는지,\n알려 줘!',
'82:1':'그렇지만...\n왠지 라이벌로\n생각하게 되네...',
'83:0':'인터넷이 얼마나\n재밌는지, 다정하게\n알려 줘!',
'84:0':'다음에 친구에게\n나를\n소개해 줘!',
'85:0':'나도 그거 정말 좋아해!\n그 아삭아삭한 느낌이\n최고지!',
'85:1':'...어라,\n아니었나?',
'86:0':'그렇구나~, 의외로,\n낭만적이네!',
'87:0':'앞으로 이루고 싶은\n꿈이 있다니,\n멋지다!',
'88:0':'어머~! 정말~?\n와~!!',
'88:1':'왠지 나까지,\n두근거리기 시작했어!',
'89:0':'...누구야?',
'90:0':'뭐, 이렇게\n사람이 많으면,',
'90:1':'그중에는 안 맞는 사람도\n있겠지!',
'90:2':'불편한 사람이\n없는 쪽이,\n더 드문걸',
'91:0':'아, 그 프로그램,\n얼마 전에 봤어!',
'91:1':'그, 털북숭이\n괴물이 날뛰는 거\n맞지?',
'91:2':'...아니었어?',
'92:0':'응, 응, 잘한다고\n생각할 수 있는 게 있다는 건\n멋진 일이야!',
'93:0':'어려워하는 것도,\n노력에 따라\n어떻게든 할 수 있어!',
'94:0':'그렇구나~, 의외로\n유행을 따라가는 편이네...',
'95:0':'귀여운 이름이네!!\n마음에 들었어!',
}}
CONTEXT={
'65FF3C':'Remaining six middle-dot literals in fortune intro0/1; no prose remaining in source catalog for this archive.',
'660D90':'Remaining TV/promise/other quick-box reminders and explicit Roll reminders21..26; other selected entries retained.',
'661858':'Remaining profile questions9..34, existing/additional record flows40..63 and reactions80..95; no mugshot shown.'
}
CHOICES={(s,i) for s in (41,44,47,50,53,56,59,62) for i in (1,2)}
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
    if len(selected)!=count or set(values)!=ids:raise ValueError('remaining scope '+archive)
    units=[]
    for x in selected:
        s,i=map(int,x.key.split(':')[1:]);t=values[x.key]
        if t.count('\n')!=x.text.count('\n') or t.startswith('\n')!=x.text.startswith('\n') or t.endswith('\n')!=x.text.endswith('\n'):raise ValueError('remaining topology '+x.key)
        if re.findall(r'-?\d+|\[[^\]]+\]',t)!=re.findall(r'-?\d+|\[[^\]]+\]',x.text):raise ValueError('remaining tokens '+x.key)
        if len(x.text)-len(x.text.rstrip(' '))!=len(t)-len(t.rstrip(' ')):raise ValueError('remaining padding '+x.key)
        roll=archive=='660D90' and s>=20;choice=archive=='661858' and (s,i) in CHOICES
        speaker='player-choice' if choice else 'Roll' if roll else 'fortune-wait-punctuation' if archive=='65FF3C' else 'unshown-reminder-voice' if archive=='660D90' else 'unshown-profile-voice'
        units.append(dict(id=x.key,source=x.text,translation=t,state='needs_review',speaker=speaker,
            origin_portrait='Roll' if roll else None,portrait_visibility='shown' if roll else 'not-shown-in-script',
            context=CONTEXT[archive],variable_context='Preserve nickname/schedule/string buffers and command ordering. Comma/ownership 의/name + 일정 avoid fixed allomorph; input repertoire/width/caller identity remain unverified.'))
    src=ROOT/cfg['source_profile']['filename'];require_hash(src,cfg['source_profile']['sha256'])
    require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==int(archive,16))
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION',archive=archive,
        source_sha256=cfg['source_profile']['sha256'],source_tpl=dict(path=source,sha256=digest),
        source_archive_sha256=sha(payload_of(src.read_bytes(),row)),consumer='remaining-fortune-reminder-profile',context=CONTEXT[archive],
        voice='Friendly source candidates; explicit Roll only reminder21..26; no inferred named actor from first person or adjacent archive. Not human approved.',
        review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),
        insertion_state='translation-first draft only; not selected by ROM builder',
        protected_policy='Keep prior ROM-selected literals, source commands/control/flags/global/date buffers/newlines/choice padding; waitSkip30 and punctuation segmentation unchanged; no ROM/save writes.',
        semantic_review={
        '65FF3C':['Six source ・ draft as ASCII . for successive ellipsis beats, not six dialogue sentences. Four waitSkip30 calls per intro and separate literal boundaries retained.',
                  'All prior fortune prose/heart branches/global6 values/ratios/heart locations and minigame rewards remain untouched; punctuation appearance/spacing not runtime verified.'],
        '660D90':['Only eleven unselected entries drafted; source3/4/6 quick-box and other selected reminders retained. Explicit Roll21..26 separated from unshown1/2/5.',
                  'Sourceじゅく means 학원; promise anticipation and TV urgency retained. Prefix name + 시작할 or 일정 시간 avoids final-consonant particle; leading newline remains.',
                  'Dispatch0/20, multiple event6/26, flag3585/3658, sound155/wait96 and quick coordinates preserved; actual clock/AMPM/name/event chain/render not tested.'],
        '661858':['102 unselected entries only; already selected family/food/subject prompts unchanged. Actor not inferred as Roll despite neighboring archives and source first person.',
                  'Brother/sister 후보 형이나 오빠/누나나 언니 avoids operator gender assumption; global22 female/male liked-person branches and global23 school/company/kindergarten preserved.',
                  'Romantic mail candidate 사랑의 메일; affection and no-arrival/identity-recognition rationale kept. No sender identity inferred.',
                  'Reaction85 food crunch claim then self-correction and91 TV furry-monster claim then self-correction preserved, not adapted to arbitrary user-entered value.',
                  'Source82 rivalry and94 trendy-interest meanings retained without added jealousy or condemnation; 미ーハー candidate 유행을 따라가는 편 requires wording review.',
                  'Sixteen additional-entry choices keep two spaces/blank lines/global5 record-count/stringBuffer1..3/input flags; actual name-entry/persistence/display and independent wording approval pending.']
        }[archive],units=units)
def main():
    for a,(_,count,out) in SOURCES.items():
        asset=create(a);p=ROOT/out
        if p.exists():
            if json.loads(p.read_text(encoding='utf8'))!=asset:raise ValueError('preserve remaining draft '+out)
        else:p.write_text(json.dumps(asset,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        print(f'Authored {a} {count}; ROM unchanged')
if __name__=='__main__':main()
