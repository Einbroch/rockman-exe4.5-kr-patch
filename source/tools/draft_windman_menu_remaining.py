"""Manually authored WindMan menu/schedule draft; no ROM or save writes."""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of
SOURCES={'66B0D4':('38d4704eb3f37ba6ebb2af5dbf17927028ee4c8ff83ad0dc9cadfb0205014a33',57,'translations/windman_menu_remaining_draft_ko.json')}
DRAFT={'66B0D4':{
'0:0':'오늘은 ','0:1':'월','0:2':'일이다\n무엇을 할까...',
'1:0':'어느 날의 일정을\n입력하겠느냐?',
'2:0':'무엇을 등록하겠느냐?\n','2:1':'일정\n','2:2':'기념일',
'3:0':'그날은 이미 지났구나...',
'4:0':'더 이상은\n등록할 수 없구나...',
'4:1':'새로 등록하려면,\n이미 등록한\n일정을 삭제하거라',
'5:0':'무엇을 삭제하겠느냐?\n','5:1':'일정\n','5:2':'기념일',
'6:0':'어느 날의 일정을 보겠느냐?',
'7:0':'무엇을 등록하겠느냐?\n','7:1':'일정\n','7:2':'기념일',
'8:0':'무엇을 삭제하겠느냐?\n','8:1':'일정\n','8:2':'기념일',
'10:0':'이건','10:1':'의\n소지품이다...\n','10:2':'키 아이템 확인',
'20:0':'몇 시부터 시작하느냐?',
'21:0':'어떤 종류냐?','22:0':'어떤 내용이냐?','23:0':'누구와의 약속이냐?',
'24:0':'이대로 하면 되겠느냐?\n\n','24:1':'예  ','24:2':'아니오',
'25:0':',\n같은 시간에 일정이 있구나',
'30:0':'덮어쓰게 되는데,\n괜찮겠느냐?\n','30:1':'예  ','30:2':'아니오',
'31:0':'어떤 기념일이냐?\n','32:0':'어디에 등록하겠느냐?\n',
'33:0':'이대로 하면 되겠느냐?\n\n','33:1':'예  ','33:2':'아니오',
'40:0':'나에게 서브 칩을\n전송할 수\n있다...',
'41:0':'내 장비를\n바꿀 수 있다...',
'42:0':'데이터 라이브러리를\n확인할 수 있다...',
'43:0':'메일을 확인할\n수 있다',
'44:0':'키 아이템을\n확인할 수\n있다...',
'45:0':'지금까지의 데이터를\n저장할 수 있다...',
'50:5':'」\n일정을 삭제하마...','50:6':'괜찮겠느냐?\n\n','50:7':'예  ','50:8':'아니오',
'51:6':'」\n기념일을 삭제하마...','51:7':'괜찮겠느냐?\n\n','51:8':'예  ','51:9':'아니오',
'52:3':'」\n기념일을 삭제하마...','52:4':'괜찮겠느냐?\n\n','52:5':'예  ','52:6':'아니오',
}}
CHOICES={(2,1),(2,2),(5,1),(5,2),(7,1),(7,2),(8,1),(8,2),(10,2),(24,1),(24,2),(30,1),(30,2),(33,1),(33,2),(50,7),(50,8),(51,8),(51,9),(52,5),(52,6)}
CONTEXT={'66B0D4':'Explicit WindMan quick-menu57 Japanese entries: date/menu, schedule/anniversary registration, capacity/conflict/overwrite, item/menu hints and deletion confirmation.'}
NOTES={'66B0D4':[
'All57 unselected Japanese entries drafted, including21 player choices; every script explicitly shows WindMan. Source commands and non-Japanese formatting retained.',
'Past-date refusal, full-capacity remedy, same-time conflict, overwrite warning and final deletion confirmations retain distinct meanings. No destructive action executed.',
'50 uses hour/minute/AMPM/frequency schedule;51 year/month/day/day-name anniversary;52 month/day anniversary. Quoted user event label preserved; category suffix avoids particle allomorph.',
'Nickname ownership uses 의. 이건 prefix replaces sourceこれが without adding forbidden trailing padding; name concatenation appearance still needs runtime review.',
'All defaults/cancel/BSeparate/clear targets and sound467/flag3611/wait1/close/end retained. Two-space choice padding and blank lines unchanged.',
'Source date/month/day and two-digit padding remain. Source quote symbols are structural/non-Japanese literals left unchanged, not unaccounted prose.',
'Voice uses existing WindMan seasonal candidates, not newly approved terminology or voice. Actual input, save, date/time and menu routing/display unverified.',
]}
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
        choice=(s,i) in CHOICES
        speaker='player-choice' if choice else 'WindMan'
        units.append(dict(id=x.key,source=x.text,translation=t,state='needs_review',speaker=speaker,
            origin_portrait='WindMan',portrait_visibility='shown',
            context=CONTEXT[archive],variable_context='Nickname + 의 and quoted event + 일정/기념일 avoids fixed allomorph. Prefix 이건 has no new trailing space: actual concatenation needs review. Date/time/AMPM/frequency/name width and runtime unverified.'))
    src=ROOT/cfg['source_profile']['filename'];require_hash(src,cfg['source_profile']['sha256'])
    require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==int(archive,16))
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION',archive=archive,
        source_sha256=cfg['source_profile']['sha256'],source_tpl=dict(path=source,sha256=digest),
        source_archive_sha256=sha(payload_of(src.read_bytes(),row)),consumer='windman-quick-menu-schedule',context=CONTEXT[archive],
        voice='Calm elder-like source forms motivate 하겠느냐/하거라/하마 candidates, consistent with existing WindMan seasonal candidate. Not human approved.',
        review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),
        insertion_state='translation-first draft only; not selected by ROM builder',
        protected_policy='Keep prior selected literals, commands, flags, buffers, newlines and literal segmentation; no ROM/save writes.',
        semantic_review=NOTES[archive],units=units)
def main():
    for a,(_,count,out) in SOURCES.items():
        asset=create(a);p=ROOT/out
        if p.exists():
            if json.loads(p.read_text(encoding='utf8'))!=asset:raise ValueError('preserve remaining draft '+out)
        else:p.write_text(json.dumps(asset,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        print(f'Authored {a} {count}; ROM unchanged')
if __name__=='__main__':main()
