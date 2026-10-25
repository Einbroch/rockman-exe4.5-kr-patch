"""Batch500-002: manually authored500 literals, translation-first, no ROM writes."""
import json,re
from build_visibility_poc import ROOT,require_hash,sha
from tpl_literals import literals
from verify_tpi_index import parse_tpi
from compare_archive_payloads import payload_of
from draft_batch500_001 import LABELS
SOURCES={
'6E2E18':('641f9cf3af367513c493c95ce61b44ae9207466641d668deba85951b87574486',51,'translations/batch500_002_equipment_wood_draft_ko.json'),
'6E308C':('ce2e8b6800535e5ad8e4c3d7caa1307159bb8daa7b38895541aac421bf137518',51,'translations/batch500_002_equipment_star_draft_ko.json'),
'6E32FC':('c7ba62fe78c766770db671fa35507e7123c9a2853668fa005207b9361837f4f8',51,'translations/batch500_002_equipment_shadow_draft_ko.json'),
'6E3574':('2d7fba417bc56ef88e3744b4d8629842871708a6618def0cbccfbb78d7251b8e',51,'translations/batch500_002_equipment_knight_draft_ko.json'),
'6E37EC':('b63abeb26937a1a8b3b4b0163b65cb964d427dd41c448e2914b63224f9bfc816',51,'translations/batch500_002_equipment_napalm_draft_ko.json'),
'6E3A64':('817b5462fb08d7ec041745a9ad2f7a971c9d76c4ff47d5337daa57e349a42371',51,'translations/batch500_002_equipment_ice_draft_ko.json'),
'6E3CD8':('707dc89b404b3571cb1647e8e2d3469fe0bf559171ace094b36d5d66fcee4c4b',51,'translations/batch500_002_equipment_elec_draft_ko.json'),
'6E3F4C':('dc1106bd4886e7be7864e686be1636bb0ec7860a70704ab085a76c7e433da67c',51,'translations/batch500_002_equipment_plant_draft_ko.json'),
'6E41C4':('e79c45985cb3ebe1320e59c9a943edde41e098c0328f5ee7d1c74df96cc28ade',51,'translations/batch500_002_equipment_bass_draft_ko.json'),
'68097C':('96d8ec105c61484719469b2d89ef050402c18e2b4d1fc4177a8056d916fd5928',31,'translations/batch500_002_quick_progress_draft_ko.json'),
'68E5E0':('10ea7b0bca57454630d49791f2075cae1744a27f447ac86567d99d720106e6d3',10,'translations/batch500_002_quick_tournament_draft_ko.json'),
}
ACTORS={'6E2E18':'WoodMan','6E308C':'StarMan','6E32FC':'ShadowMan','6E3574':'KnightMan','6E37EC':'NapalmMan','6E3A64':'IceMan','6E3CD8':'ElecMan','6E3F4C':'PlantMan','6E41C4':'Bass'}
# Each dialogue literal is explicitly authored; shared labels were matched manually
# after reading all nine complete equipment scripts, not by prose replacement.
DRAFT={
'6E2E18':{
'60:0':'칩 폴더를\n편집하겠다','61:0':'R 버튼에 배정할\n무기를 골라 줘','62:0':'L 버튼에 배정할\n무기를 골라 줘',
'70:0':'칩 폴더가\n','70:1':'장이 아니다','70:2':'편집을 그만두겠나?\n','70:3':'예  ','70:4':'아니오',
'71:0':'같은 칩은\n3장까지다','72:0':'같은 메가 클래스 칩은\n1장만 넣을 수 있다',
'73:0':'같은 기가 클래스 칩은\n1장만 넣을 수 있다','74:0':'메가 클래스 칩은\n5장만 넣을 수 있다','75:0':'기가 클래스 칩은\n1장만 넣을 수 있다',
},
'6E308C':{
'60:0':'칩 폴더를\n편집할게','61:0':'R 버튼에 배정할\n무기를 골라 줘!','62:0':'L 버튼에 배정할\n무기를 골라 줘!',
'70:0':'칩 폴더가\n','70:1':'장이 아니야!','70:2':'편집을 그만둘래?\n','70:3':'예  ','70:4':'아니오',
'71:0':'같은 칩은\n3장까지야!','72:0':'같은 메가 클래스 칩은\n1장만 넣을 수 있어',
'73:0':'같은 기가 클래스 칩은\n1장만 넣을 수 있어','74:0':'메가 클래스 칩은\n5장만 넣을 수 있어','75:0':'기가 클래스 칩은\n1장만 넣을 수 있어',
},
'6E32FC':{
'60:0':'칩 폴더를\n편집하겠다','61:0':'R 버튼에 배정할\n무기를 고르거라','62:0':'L 버튼에 배정할\n무기를 고르거라',
'70:0':'칩 폴더가\n','70:1':'장이 아니구나','70:2':'편집을 그만두겠느냐?\n','70:3':'예  ','70:4':'아니오',
'71:0':'같은 칩은\n3장까지다...','72:0':'같은 메가 클래스 칩은\n1장만 넣을 수 있다',
'73:0':'같은 기가 클래스 칩은\n1장만 넣을 수 있다','74:0':'메가 클래스 칩은\n5장만 넣을 수 있다','75:0':'기가 클래스 칩은\n1장만 넣을 수 있다',
},
'6E3574':{
'60:0':'칩 폴더를\n편집합니다','61:0':'R 버튼에 배정할\n무기를 골라 주세요','62:0':'L 버튼에 배정할\n무기를 골라 주세요',
'70:0':'칩 폴더가\n','70:1':'장이 아닙니다','70:2':'편집을 그만두시겠습니까?\n','70:3':'예  ','70:4':'아니오',
'71:0':'같은 칩은\n3장까지입니다','72:0':'같은 메가 클래스 칩은\n1장만 넣을 수 있습니다',
'73:0':'같은 기가 클래스 칩은\n1장만 넣을 수 있습니다','74:0':'메가 클래스 칩은\n5장만 넣을 수 있습니다','75:0':'기가 클래스 칩은\n1장만 넣을 수 있습니다',
},
'6E37EC':{
'60:0':'칩 폴더를\n편집하자','61:0':'R 버튼에 배정할\n무기를 골라 줘!','62:0':'L 버튼에 배정할\n무기를 골라 줘!',
'70:0':'칩 폴더가\n','70:1':'장이 아니잖아!','70:2':'편집을 그만둘 거야?\n','70:3':'예  ','70:4':'아니오',
'71:0':'같은 칩은\n3장까지야!','72:0':'같은 메가 클래스 칩은\n1장만 넣을 수 있어',
'73:0':'같은 기가 클래스 칩은\n1장만 넣을 수 있어','74:0':'메가 클래스 칩은\n5장만 넣을 수 있어','75:0':'기가 클래스 칩은\n1장만 넣을 수 있어',
},
'6E3A64':{
'60:0':'칩 폴더를\n편집할 거예요','61:0':'R 버튼에 배정할\n무기를 고르는 거예요!','62:0':'L 버튼에 배정할\n무기를 고르는 거예요!',
'70:0':'칩 폴더가\n','70:1':'장이 아니에요','70:2':'편집을 그만둘 거예요?\n','70:3':'예  ','70:4':'아니오',
'71:0':'같은 칩은\n3장까지예요!','72:0':'같은 메가 클래스 칩은\n1장만 넣을 수 있어요',
'73:0':'같은 기가 클래스 칩은\n1장만 넣을 수 있어요','74:0':'메가 클래스 칩은\n5장만 넣을 수 있어요','75:0':'기가 클래스 칩은\n1장만 넣을 수 있어요',
},
'6E3CD8':{
'60:0':'칩 폴더를\n편집하겠다','61:0':'R 버튼에 배정할\n무기를 골라 줘','62:0':'L 버튼에 배정할\n무기를 골라 줘',
'70:0':'칩 폴더가\n','70:1':'장이 아니다','70:2':'편집을 그만두겠나?\n','70:3':'예  ','70:4':'아니오',
'71:0':'같은 칩은\n3장까지다','72:0':'같은 메가 클래스 칩은\n1장만 넣을 수 있다',
'73:0':'같은 기가 클래스 칩은\n1장만 넣을 수 있다','74:0':'메가 클래스 칩은\n5장만 넣을 수 있다','75:0':'기가 클래스 칩은\n1장만 넣을 수 있다',
},
'6E3F4C':{
'60:0':'칩 폴더를\n편집할게','61:0':'R 버튼에 배정할\n무기를 골라 주겠니?','62:0':'L 버튼에 배정할\n무기를 골라 주겠니?',
'70:0':'칩 폴더가\n','70:1':'장이 아니야','70:2':'편집을 그만둘까?\n','70:3':'예  ','70:4':'아니오',
'71:0':'같은 칩은\n3장까지야','72:0':'같은 메가 클래스 칩은\n1장만 넣을 수 있어',
'73:0':'같은 기가 클래스 칩은\n1장만 넣을 수 있어','74:0':'메가 클래스 칩은\n5장만 넣을 수 있어','75:0':'기가 클래스 칩은\n1장만 넣을 수 있어',
},
'6E41C4':{
'60:0':'칩 폴더를\n편집한다...','61:0':'R 버튼에 배정할\n무기를 골라라...','62:0':'L 버튼에 배정할\n무기를 골라라...',
'70:0':'칩 폴더가\n','70:1':'장이 아니다','70:2':'편집을 그만두겠나?\n','70:3':'예  ','70:4':'아니오',
'71:0':'같은 칩은\n3장까지다...','72:0':'같은 메가 클래스 칩은\n1장만 넣을 수 있다',
'73:0':'같은 기가 클래스 칩은\n1장만 넣을 수 있다','74:0':'메가 클래스 칩은\n5장만 넣을 수 있다','75:0':'기가 클래스 칩은\n1장만 넣을 수 있다',
},
'68097C':{
'10:0':'인터넷을 좀 더\n탐색해 볼까\n...',
'11:0':'견습 라이선스 시험을\n치르러 갈까...',
'12:0':'견습 라이선스\n시험을\n치르러 가자...',
'13:1':'」 칩을\n구하러 가자...',
'14:0':'견습 라이선스를\n받으러 갈까...',
'15:0':'견습 라이선스 시험\n수고했다!',
'15:1':'일단\n플러그아웃할까?',
'16:0':'인터넷3에서\n일어난 사건이\n신경 쓰이는군...',
'17:0':'방금 쓰러뜨린 내비가\n사건의 범인이었던\n모양이군...',
'17:1':'피곤할 테니...\n일단, 플러그아웃\n할까...?',
'18:0':'인터넷5에서\n일어난 사건이\n신경 쓰이는군...',
'19:0':'인터넷7에서\n일어난 사건이\n신경 쓰이는군...',
'20:0':'인터넷9에서\n일어난 사건이\n신경 쓰이는군...',
'21:0':'인터넷10에서\n일어난 사건이\n신경 쓰이는군...',
'22:0':'인터넷12에서\n일어난 사건이\n신경 쓰이는군...',
'23:0':'블랙워크스에게서\n「마이너스 키」를\n되찾자...',
'24:0':'「마이너스 키」는,\n다른 내비 1명이\n가진 모양이군',
'25:0':'「마이너스 키」를\n인터넷9에 있는',
'25:1':'내비에게\n가져다주자',
'26:0':'오피셜\n토너먼트의',
'26:1':'참가 접수 장소로\n가자...',
'27:0':'언더 인터넷으로\n갈까...',
'27:1':'목표 내비를 찾을\n표식은\n관이었지...',
'28:0':'오피셜\n토너먼트에\n참가 신청하러 갈까',
'29:0':'주말에는 오피셜\n토너먼트로군\n우승을 노려 보자...',
'30:0':'오피셜\n토너먼트...\n우승을 노리겠다',
'31:0':'더 깊숙이\n인터넷을\n탐색해 볼까',
'32:0':'오피셜\n토너먼트의 예선을\n치르러 갈까',
'33:0':',\n아직 읽지 않은\n메일이 있었지...',
'34:0':'주말이 지나면\n오피셜\n토너먼트에',
'34:1':'참가 신청하러 가자',
},
'68E5E0':{
'1:0':'...미안하다\n나는 전력을 다해\n싸웠다...',
'1:1':'하지만,\n난 포기하지 않는다',
'1:2':'이 주먹으로 승리를\n거머쥘 때까지는!!',
'2:0':',\n해냈다!!',
'2:1':'우오오오오오오옷!!',
'10:0':',\n참가 신청을 하지 않았다',
'20:0':'드디어 시작이군...\n이 주먹으로 우승을\n거머쥐고 말겠다!',
'21:0':'드디어 시작이군...\n이 주먹으로 우승을\n거머쥐고 말겠다!',
'22:0':'드디어 시작이군...\n이 주먹으로 우승을\n거머쥐고 말겠다!',
'23:0':'드디어 시작이군...\n이 주먹으로 우승을\n거머쥐고 말겠다!',
}}
CONTEXT={a:'Equipment labels0..37, quick prompts60..62 and explicit portrait warnings70..75; full archive read, current unselected entries only.' for a in ACTORS}
CONTEXT.update({'68097C':'Progress dispatcher10..34: license/chip/event/mail/key/weekday/tournament; no portrait in script.',
'68E5E0':'Quick defeat, victory, unregistered warning and fist-victory tournament resolve; no portrait in script.'})

def create(archive):
    digest,count,out=SOURCES[archive];source=f'analysis/full_scope_v1/source_tpl/{archive}.tpl'
    require_hash(ROOT/source,digest);original=(ROOT/source).read_text(encoding='utf-8-sig')
    cfg=json.loads((ROOT/'project.json').read_text(encoding='utf8'))
    plan=json.loads((ROOT/'translations/full_translation_first_plan.json').read_text(encoding='utf8'))
    require_hash(ROOT/plan['source_inventory']['path'],plan['source_inventory']['sha256'])
    catalog=json.loads((ROOT/plan['source_inventory']['path']).read_text(encoding='utf8'))
    ids={u['id'] for u in catalog['units'] if u['archive']==archive and u['status']=='unselected_japanese'}
    authored={**LABELS,**DRAFT[archive]} if archive in ACTORS else DRAFT[archive]
    values={archive+':'+k:v for k,v in authored.items()}
    selected=[x for x in literals(original) if x.key in ids]
    if len(selected)!=count or set(values)!=ids:raise ValueError('batch scope '+archive)
    units=[]
    for x in selected:
        s,i=map(int,x.key.split(':')[1:]);t=values[x.key]
        if t.count('\n')!=x.text.count('\n') or t.startswith('\n')!=x.text.startswith('\n') or t.endswith('\n')!=x.text.endswith('\n'):raise ValueError('batch topology '+x.key)
        if re.findall(r'-?\d+|\[[^\]]+\]',t)!=re.findall(r'-?\d+|\[[^\]]+\]',x.text):raise ValueError('batch tokens '+x.key)
        if len(x.text)-len(x.text.rstrip(' '))!=len(t)-len(t.rstrip(' ')):raise ValueError('batch padding '+x.key)
        equipment=archive in ACTORS;shown=equipment and s>=70;choice=shown and s==70 and i in (3,4)
        speaker='player-choice' if choice else ACTORS[archive] if shown else 'equipment-label' if equipment and s<60 else 'unshown-equipment-voice' if equipment else 'unshown-quick-voice'
        u=dict(id=x.key,source=x.text,translation=t,state='needs_review',speaker=speaker,
            origin_portrait=ACTORS[archive] if shown else None,portrait_visibility='shown' if shown else 'not-shown-in-script',
            context=CONTEXT[archive],variable_context='Folder required count is buffer1, not hardcoded30; button R/L and abbreviated C/WB/B/D retained. Chip104/name/calendar variables and literal/page boundaries unchanged; runtime/layout unverified.')
        if equipment and s<38:
            u['wording_lineage']='equipment_weapons_ko.json / equipment_labels_ko.json existing candidate; source-label context matched manually; not approval'
        units.append(u)
    src=ROOT/cfg['source_profile']['filename'];require_hash(src,cfg['source_profile']['sha256'])
    require_hash(ROOT/cfg['text_catalog']['path'],cfg['text_catalog']['sha256'])
    row=next(r for r in parse_tpi(ROOT/cfg['text_catalog']['path']) if r['offset']==int(archive,16))
    notes=[
        'Batch500-002 exact500 stable catalog literals in11 fully read archives: equipment459 (342 labels,18 choices,99 prompts/warnings), progress31, tournament10. Not500 unique sentences.',
        'Manual source-conditioned draft candidates; needs_review/non-distribution. No ROM/save writes, human approval or runtime/layout closure.',
    ]
    if archive in ACTORS:
        notes+=['38 shared labels manually matched to same equipment consumer and existing candidates; abbreviations C/WB/B/D not expanded. R/L-only38/39 and printBuffer-only63 untouched.',
            'Folder count remains buffer1; same chip3, same mega/giga1, total mega5/giga1. Source trailing choice padding and newline topology unchanged.',
            'Named portrait only70..75; quick60..62 not attributed solely by adjacency. Wood/Elec direct, Star casual, Shadow archaic, Knight polite, Napalm assertive, Ice childlike polite, Plant gentle, Bass terse are tentative registers, not official voice approval.',
            'Fixed-label cell bounds, dynamic counts and choice geometry require consumer/runtime review; existing equipment font paths do not prove this batch rendered.']
    elif archive=='68097C':
        notes+=['Dispatcher flags/priority, chip104, item11, internet3/5/7/9/10/12, another1Navi and key return internet9 retained.',
            'License congratulations and plug-out request are separate15 pages; entry destination26 spans two pages. Nickname33 followed by unread mail, not inferred sender.',
            'Coffin marks target Navi; weekend0/6 and post-weekend34 retained. Actor unconfirmed; no inferred MetalMan portrait.']
    else:
        notes+=['Preserve apology, full-effort defeat, refusal to give up, fist-victory resolve and shout; no invented blame or calculation formula.',
            'Nickname boundaries, unregistered callCancelMenuTransition and flag3603 for20..23 unchanged. No actor inferred from fist phrasing or adjacent equipment.']
    return dict(schema=1,policy='development-draft; NON-DISTRIBUTION',archive=archive,
        source_sha256=cfg['source_profile']['sha256'],source_tpl=dict(path=source,sha256=digest),
        source_archive_sha256=sha(payload_of(src.read_bytes(),row)),consumer='batch500-equipment-progress-tournament',
        context=CONTEXT[archive],voice='Source-conditioned manual candidates; distinct named portraits only where shown. Not human approved.',
        review=dict(wording='needs_review',layout='needs_runtime_review',release_eligible=False),
        insertion_state='translation-first draft only; not selected by ROM builder',
        protected_policy='All source fields/IDs/TPL/payload, commands, buffers, numerical limits, newlines, padding and current selected entries immutable; no ROM/save writes.',
        batch_id='batch500-002',semantic_review=notes,units=units)

def main():
    if sum(v[1] for v in SOURCES.values())!=500:raise ValueError('500 batch size')
    for a,(_,count,out) in SOURCES.items():
        asset=create(a);p=ROOT/out
        if p.exists():
            if json.loads(p.read_text(encoding='utf8'))!=asset:raise ValueError('preserve batch asset '+out)
        else:p.write_text(json.dumps(asset,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        print(f'Authored {a} {count}; ROM unchanged')
if __name__=='__main__':main()

